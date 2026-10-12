# Packages

> Design record of the binding round (issue #20 convergence, 2026-10-12). Mechanism and — more importantly — the reasons behind each decision. Authoritative mechanics live in the kernel (`wiki_plugin_kernel.py`) and in the `PKG.yaml` declarations; this page explains why they are shaped this way.

## Layout: directory == package

`.meta/plugins/` is two-level:

```
.meta/plugins/
├── core/            # 20 framework plugins (the two roots + cross-cutting pieces)
│   ├── wiki/ …
└── domains/         # one directory per package = the install unit
    ├── cuhksz/      #   PKG.yaml + 8 plugin masters
    ├── lark/        #   PKG.yaml + 4 plugin masters
    ├── email/  bili/  project/
```

The **directory boundary == tier boundary == package boundary** — the same structure fact expressed once. Projections stay id-keyed and flat (`.meta/command/`, `.agents/skills/`, registry, the AGENTS injection region): packages regroup masters, not projections, so deploy/inject/registry needed no redesign.

| Unit | Members | Connectors | Depends |
|---|---|---|---|
| framework (core) | 20, incl. the explicit vault/mapping/structure exception — the default domain is constitutional infrastructure, the mapping proxy layer belongs to the wiki body | — | — |
| cuhksz | cuhksz · bb · bb-map · bb-track · bb-teach · bb-quiz · sis · registry | bb-cli, sis-cli | framework |
| lark | lark · lark-docs · lark-im · lark-calendar | lark-cli (external) | framework |
| email | email | mail-cli | framework |
| bili | bili | bili-cli | framework |
| project | project | — | framework |

Why the vault-exception matters: a naive "all domains are packages" split would ship the default domain out of the framework — but every instance boots on vault/mapping/structure before any package exists. Exceptions are declared, not discovered.

## PKG.yaml

```yaml
schema_version: 1
id: cuhksz
version: 0.1            # release ordinal, rides the git tag — NOT tied to member versions
compat: ">= 0.2"        # framework version floor, checked against .meta/VERSION
members: [cuhksz, bb, bb-map, bb-quiz, bb-teach, bb-track, sis, registry]
connectors:             # tri-state:
  - name: bb-cli        #   in-repo: path (code ships with the package)
    path: connectors/bb-cli
  - name: lark-cli      #   external: maintained outside (declaration only)
    external: true
  - name: gh            #   system: a preinstalled binary (capability + version expectation, no code)
    system: true
    expect: ">= 2.0"
depends: [framework]    # v1 flat graph — no package-to-package edges
uninstall:              # declaration, never executable hooks
  retains: [wiki/cuhksz/, cuhksz/]       # data zones never touched by the kernel
  credentials: [~/.bb-cli/, ~/.sis-cli/] # prompted, never auto-deleted
  bridges: [profile#domain-cognition]    # semantic registration points to check
  processes: []                          # long-running executors to stop
```

## Invariants

**Authoring side (D1): `members` == the maximal family closure.** The kernel computes the closure (depends chains reaching the package root) and diffs it against the declaration both ways — drift is a validate error.

*Why declare at all, when the closure is computable?* Because **the depends graph is live and a package is a versioned anchor**. A closure-derived package would silently change contents as the graph evolves — the same tag would ship different things at different times. The declared roster pins contents to the version; reconciliation turns structural drift into a commit-time error instead of an install-time surprise. Redundant, but self-verifying — the third application of the owner×commands dual-declaration pattern.

**Site side (D5): v1 requires full presence** — every member on disk. The subset grammar is fixed now so it never breaks the validator later: `installed ⊆ members`, non-empty, dependency-closed, root mandatory. Prunability classes:

| Class | Example | Rule |
|---|---|---|
| leaf consumers | bb-teach, bb-quiz | freely prunable — nothing depends on them |
| structural members | bb, bb-map, bb-track | prunable only together with their dependents (the closure rule enforces it) |
| family root | cuhksz | never prunable — owns territory, identity page, roster line |
| connectors | bb-cli | prunable when no installed member consumes it |

`--without` is a reserved parameter (v1 reports not-yet-open). Its promise is semantic — zero injection, zero skill surface, zero credentials — not physical: a cached clone of reviewed code is not an exposure surface, so sparse download stays an optimization outside the contract. Family-root roster lines are capability catalogs; **skill presence is the call-time truth** (tolerant degradation, no dynamic reassembly of inject text).

## Versions (D2)

`.meta/VERSION` anchors the framework (`0.2`, git tag `v0.2`); the kernel contract changes (manifest fields, projection rules) are what bump it. Package versions are release ordinals riding their own tags; **member plugins keep their own changelog versions and the two levels never lockstep** — a package is a distribution unit, not a semantic one.

## Kernel surface

| Command | What it does |
|---|---|
| `validate` | full graph + package reconciliation (closure diff, presence, flat graph, compat vs VERSION) |
| `validate --scope <pkg>` | single-package tolerant mode (D3): deps absent outside the package degrade to warnings — the CI shape for package repos post-split, run with a framework checkout alongside |
| `pkg` | package inventory: members, connectors, implicit core remainder |
| `residual <pkg>` | D6 residual scan: greps handwritten AGENTS region + profile/language/calendar/todo/cron anchors for member references (the kernel-managed injection region is skipped — it is cleaned mechanically) |
| `install <pkg>[@tag]` | resolve the [registry](https://github.com/AIE3905-Wuwa/registry) index (members reconciled against PKG.yaml) → trust gate → clone → copy masters/connectors/commands → converge. `install <owner/repo> --yes` installs an unindexed repository (trust: unknown); `--path <dir>` installs a local one (channel C) |
| `uninstall <pkg> --yes` | D6 four-clear (masters/commands/connectors/skills) + convergence + residual scan + retains/credentials reminders — data never touched |
| `list-remote` | index table with installed marks |
| `upgrade` | reconciliation report (local vs index); upgrades run uninstall+install, per-package, never cascaded |

*Why scope mode exists before the split:* after the split the framework repo and each package repo no longer contain the full graph — validate would be blind exactly where it matters most. Absence-tolerance turns "plugin missing" from an error into a listed warning, keeping every repo self-checkable.

## Uninstall contract (D6)

No executable uninstall hooks — that would be a **third execution surface** (after inject text and connectors), running at a privileged moment; the security model declines. Instead the package *declares* its deletion semantics (`uninstall:` above) and the flow is: kernel mechanical four-clear (directory / injection / registry / projections) → residual scan output → agent semantic finish per the declaration (credential reminders, process stops, bridge registration lines) behind a confirmation gate. **Data and credentials are never auto-deleted** — the freedom to delete belongs to the human; retained data zones lapse into the deprecated posture.

## Manifest schema

`schema_version: 1` on PLUGIN.yaml and PKG.yaml. One format migration shared with the upcoming behavior contracts (#34: owns/trigger/emits/never) — versioning the schema once avoids a second format churn when #34 lands.

## Decision ledger

| # | Decision | One-line reason |
|---|---|---|
| D1 | declared roster + closure reconciliation | live graph vs versioned anchor; drift → commit-time error |
| D2 | package version ≠ member versions | distribution unit ≠ semantic unit; lockstep is a trap |
| D3 | scope/tolerant validate in the binding round | the split is only safe if repos can self-check without the full graph |
| D4 | instance-local packages live in `domains/` too | one semantic: package directory == install unit; zero-index private packages |
| D5 | subset grammar fixed now, `--without` opens on demand | validator format never breaks; first real subset user triggers it |
| D6 | declarative uninstall, no hooks | third execution surface declined; deletion knowledge becomes reviewable data |
