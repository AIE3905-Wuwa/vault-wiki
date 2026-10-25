# Quickstart

> The five-minute path. Full guide — components, channels, packages, upgrades, troubleshooting: [deployment.md](deployment.md). The channel's design and release record: [distribution.md](distribution.md).
> Status: npm `owfa` is under application (frozen on similarity grounds); until the registry serves it, the git channel works today. The fallback package `owfadev` carries the same CLI once published.

## 1. Prerequisites

- **Python 3.9+** — the framework and kernel are pure stdlib; no pip, no venv.
- **Node 16.7+** — only for the npm channel (the CLI is Node).
- **An agent** that reads `AGENTS.md` and `.agents/skills/` (ZCode, Claude Code, Cursor, dsh…).
- **git** recommended — instance snapshots and the upgrade rollback path.

## 2. One command (npm channel)

```bash
npx owfa init my-workspace          # target name, once granted
# while the name is pending:
npx owfadev init my-workspace       # fallback package, same CLI
cd my-workspace
npx owfa doctor                     # target: python / framework / markers / kernel validate
npx owfadev doctor                  # fallback: same check
```

`init` copies `.meta/` + `.agents/skills/`, creates `vault/` and the three wiki directories, writes or appends `AGENTS.md`, and runs the kernel. Existing content is untouched. Optional packages: `npx owfa init my-workspace --packages cuhksz,lark`.

Already have a workspace? `init` refuses if `.meta/` exists; use `npx owfa upgrade` (or `--force` to re-copy the framework trees).

## 3. Manual five steps (git or offline)

1. **Get the framework**: `git clone https://github.com/owfadev/vault-wiki.git my-workspace` — a clone is a valid instance. (Before the org rename, clone `https://github.com/AIE3905-Wuwa/vault-wiki.git`; the old URL redirects afterwards.) To embed into an existing vault, clone the template elsewhere and copy `.meta/` + `.agents/skills/` into the target root.
2. **Write `AGENTS.md`**: one identity paragraph, one layout paragraph, and the injection markers verbatim from [agents-example.md](agents-example.md). Existing `AGENTS.md`? Paste in only the marker block.
3. **Create four directories**: `vault/`, `wiki/notes/`, `wiki/sessions/`, `wiki/vault/`.
4. **Converge**:
   ```bash
   python .meta/scripts/wiki_plugin_kernel.py all
   ```
5. **Verify**: drop a file into `vault/`, open an agent at the root, say "map", then "check".

There is no separate kernel install: the kernel is `.meta/scripts/wiki_plugin_kernel.py` inside the tree; Python 3.9+ runs it. On Windows use `py -3` or set `OWFA_PYTHON`.

## 4. Next

```bash
owfa list                  # registry catalog: packages, versions, installed marks
owfa add cuhksz            # install a domain package (stops at a semantic migration if one is staged)
owfa pkg                   # what is installed here
owfa upgrade               # later: replace the framework trees, preserve instance state
```

These assume a global install (`npm i -g owfa` or `npm i -g owfadev`); without one, use `npx owfa …` / `npx owfadev …`.

- Package lifecycle, trust levels, offline installs, uninstall: [deployment.md](deployment.md#7-packages--finding-and-installing).
- Daily use: [usage.md](usage.md); mechanics: [mechanics.md](mechanics.md).
- Developing the framework itself: [CONTRIBUTING.md](../../CONTRIBUTING.md).
