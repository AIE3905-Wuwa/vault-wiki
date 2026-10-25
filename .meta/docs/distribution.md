# Distribution

> How the framework itself reaches a machine, and how it is upgraded. Packages have had a channel (registry + `kernel install`) since v0.3; the framework body had none — install was *clone, copy two trees, hand-write AGENTS.md*. This page records the npm channel that closes that gap.

## Why npm

The framework is pure-stdlib Python with no runtime dependencies. npm is not a runtime choice here; it is a **delivery vehicle** chosen because it already exists on the machines that run agents:

- one command, no clone: `npx owfa init my-workspace`
- a versioned, immutable, checksummed artifact (the npm tarball) instead of a moving branch
- Windows does not need Python's script directory on `PATH` (the failure that motivated #46)
- `npx` keeps a cache, so re-running is cheap; upgrades fetch a new tarball by version
- no `postinstall` scripts: `npm install` executes nothing from this package

Python remains the only runtime dependency of the framework. Node is needed to *install*, not to *use*.

The name is part of the channel: **OWFA — One Workspace For All (agents)**. The package is `owfa`, the command is `owfa`, and the repository keeps its technical name `vault-wiki`. See [naming.md](naming.md) for the rationale and the collision policy.

## What ships

The npm tarball is the framework body, byte-for-byte what the git channel copies:

| Path | Contents | In tarball |
|---|---|---|
| `.meta/` | kernel, plugins, commands, protocol, docs | yes |
| `.agents/skills/` | command/connector skill copies | yes |
| `templates/AGENTS.template.md` | the instance shell with the injection markers | yes |
| `bin/owfa.js` | CLI (zero dependencies) | yes |
| `README.md`, `LICENSE` | — | yes |
| `test/`, `scripts/`, `CONTRIBUTING.md`, `.github/` | development-only | no |

Local state never ships: `__pycache__`, `*.pyc`, `.meta/kernel-journal.log`, `.meta/migrations/pending.json`, `.meta/registry-cache.yaml`, `test-repo/`. The release gate (`scripts/verify-release.js`) refuses to publish if any of them would be packed.

## Commands

```
owfa init [dir] [--name NAME] [--packages a,b] [--force]
owfa upgrade [dir] [--check] [--backup] [--force]
owfa doctor [dir]
owfa add <pkg> [--yes] [--without a,b]
owfa version
```

**init** — additive deployment, the five quickstart steps mechanized:

1. copies `.meta/` and `.agents/skills/` from the tarball
2. creates `vault/`, `wiki/notes/`, `wiki/sessions/`, `wiki/vault/`
3. writes `AGENTS.md` from the template when absent; when one exists, **appends only the injection region** (handwritten content before it is preserved byte-for-byte); refuses if the markers are half-present
4. runs `python .meta/scripts/wiki_plugin_kernel.py all` (validate, inject, registry, skills)
5. optionally installs packages from the registry (`--packages cuhksz,lark`)

A package may declare a **first-run semantic migration** (root packages such as `project` do). Installing it stages the migration, and the CLI stops there with the exact `kernel migrate` command — clearing it is an agent act (create the identity/declaration page), not something a mechanical installer may fake. `init --packages` therefore exits non-zero in that state: the workspace is installed but not converged.

`--force` re-copies the framework trees over an existing instance, preserving the kernel state listed below. Instance data (`vault/`, `wiki/`) is never touched by any `init` or `upgrade`. If `.agents/skills/` already exists, framework skill copies with the same names are updated in place; unrelated skills are left alone.

**upgrade** — tree replacement plus convergence:

- compares the instance's `.meta/VERSION` with the tarball's; refuses downgrades unless `--force`
- preserves instance-local kernel state: `.meta/migrations/pending.json`, `.meta/kernel-journal.log`, `.meta/registry-cache.yaml`
- **replaces** local edits under `.meta/` and `.agents/skills/` — instance hotfixes belong in the instance's git history, which is the rollback path (the `--backup` flag also drops a copy under `.owfa/backup/<version>-<timestamp>/`)
- reruns `all`; a pending semantic migration blocks convergence and is reported with the exact `kernel migrate` command
- `--check` is a read-only report

**doctor** — prints Node/Python/framework versions, checks the AGENTS injection markers, runs `kernel validate`. It never writes.

**add** — thin wrapper over `kernel install` plus convergence. Registry trust rules still apply; `--yes` is forwarded.

## Version invariant

The npm version rides the framework anchor: `.meta/VERSION` `0.3` → package `0.3.x`. The release gate refuses a package whose `major.minor` diverges, and refuses a `v*` tag that does not match the package version exactly. `.meta/VERSION` still tracks the kernel contract, not product maturity (stage labels live in the README); npm patch releases may fix packaging without touching the contract.

Install identification is therefore trivial: `.meta/VERSION` says which framework a workspace is on; `owfa version` says which channel the CLI is on.

## Release runbook

One-time:

1. Create the npm account that will own `owfa` (the unscoped name is what makes the command `npx owfa`; the name was free on 2026-10-25).
2. Add `NPM_TOKEN` as a repository secret (automation token with publish rights), or run `npm login` locally for a manual first release.

Every release:

```bash
# 1. the framework contract and the package version move together
$EDITOR .meta/VERSION          # e.g. 0.3 -> 0.4
$EDITOR package.json           # "version": "0.4.0"
git commit -am "release: framework 0.4.0"
git tag v0.4.0 && git push --follow-tags
```

The tag triggers `.github/workflows/publish.yml`, which re-runs the release gate, publishes with `--provenance`, and fails closed on any mismatch. For a manual release: `npm publish --access public --provenance`.

Before tagging, run locally:

```bash
node scripts/verify-release.js
node test/smoke.js
npm pack --dry-run
```

## Security posture

- **Zero dependencies** — nothing to audit but this package.
- **No consumer lifecycle scripts** — `prepublishOnly` runs for the publisher only; installing or running `owfa` never executes package scripts.
- **Provenance** — CI publishes with npm provenance, binding the tarball to this repository and commit.
- **Additive by default** — `init` only appends to `AGENTS.md`; all destructive replacement is explicit (`upgrade`, `--force`) and reversible through instance git.
- **No telemetry** — the CLI talks to npm only when npm itself does; `init`/`upgrade` do not phone home. Package installs from the registry are the kernel's existing GitHub-based channel, unchanged.

## Scope and non-goals (v1)

- Domain packages stay on the registry/`kernel install` channel. `owfa add` is a convenience wrapper, not a second package format.
- No self-update of the CLI from inside the CLI; `npx owfa@latest` is the update path.
- No platform installers (Homebrew, apt, pipx). The npm tarball is the single artifact; a PyPI mirror can be added later without changing the payload.
- Offline install: `npm pack` on a connected machine, copy the `.tgz`, `npm install -g ./owfa-x.y.z.tgz`, then `owfa init`.
- The git channel remains fully supported: clone-as-instance and developer template workflows are unchanged.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `Python 3.9+ not found` | install Python 3, or set `OWFA_PYTHON=/path/to/python3`; the installer itself is Node-only |
| `already contains .meta/` | the directory is already an instance — use `owfa upgrade`; `--force` re-copies the trees |
| `npx` runs an old version | `npx owfa@latest …`; npm caches by version range |
| upgrade blocked by pending migrations | run `python .meta/scripts/wiki_plugin_kernel.py migrate <pkg>` and follow the printed page before upgrading again |
| Windows: `python` opens the Store | install Python 3 and ensure `py -3` or `python3` works; `OWFA_PYTHON` overrides detection |
