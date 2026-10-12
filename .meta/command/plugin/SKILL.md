---
name: plugin
owner: framework
description: "Package & plugin lifecycle management: plan (disclosure wizard), install (three channels + --without subsets), uninstall, list-remote, upgrade, pkg, residual. Mechanical steps all go through .meta/scripts/wiki_plugin_kernel.py; the agent runs the consent conversation and the one-shot commands. Triggers on: plugin, 插件, 装插件, 卸插件, 装包, install package, uninstall package."
---

# plugin: package lifecycle

The framework's self-management command, package era (issue #20). Every mechanical step goes through the kernel script; the agent's job is **consent and choice** — never writing `.meta/` by hand.

## Scope

Write: only via the kernel script (package masters in/out, connectors/, command masters, injection region, registry, skill copies — six sites)
Read: INDEX via the kernel, PKG.yaml, manifests

## Discovery → download: the consent wizard (human path)

When a user asks to install a package and has NOT already specified what to include:

1. `python .meta/scripts/wiki_plugin_kernel.py plan <pkg>` — one-shot disclosure plan: trust line, package disclosure (network/privacy/credentials, package-authored), baseline (the family root, always installed), optional members with one-line summaries and what each selection pulls in, connectors
2. Relay the plan **in the user's language** (render at the agent layer per wiki/language.md — canonical texts are English; the agent translates when relaying, never edits the source)
3. Walk the steps: trust + disclosure → user acknowledges; optional members → user picks (each pick auto-pulls its dependency closure — show the resolved final set, users cannot compose an illegal subset); connectors → confirm (they ride the package)
4. Execute: `python .meta/scripts/wiki_plugin_kernel.py install <pkg> --without <unwanted> [--yes]`
5. Report the convergence output (validate/inject/registry/deploy) in one breath

## One-shot path (agent / pre-authorized)

If consent already exists (user named exactly what they want, or pre-authorized), skip the conversation:

```
python .meta/scripts/wiki_plugin_kernel.py plan <pkg> --json        # machine-readable plan (optional)
python .meta/scripts/wiki_plugin_kernel.py install <pkg> [--without a,b] [--yes]
```

Kernel commands never prompt — every invocation completes in one shot.

## Command surface

| Command | What it does |
|---|---|
| `plan <pkg> [--json] [--without a,b]` | disclosure plan (+ subset preview); clone discarded, nothing installed |
| `install <pkg>[@tag]` | registry path: trust gate → clone → verify (id/compat/members ↔ index) → place masters/connectors/commands → converge |
| `install <owner/repo> --yes` | unindexed direct install (trust: unknown — the registry PR is how a package earns reviewed trust) |
| `install <pkg> --path <dir>` | local package (developer loop, channel C) |
| `install ... --without a,b` | D5 subset: named leaves + their dependents pruned; root never prunable; result is dependency-closed by construction |
| `uninstall <pkg> --yes` | D6 four-clear + convergence + residual scan + retains/credentials reminders; data zones and credentials never touched |
| `list-remote` | registry index with members and trust marks |
| `upgrade` | reconciliation report; upgrades run uninstall+install per package, never cascaded |
| `pkg` / `ls` / `residual <pkg>` | local inventory / plugin list / anchor-surface reference scan |

## Boundaries

- **Consent is the agent's duty**: no install without user acknowledgment of the disclosure (unless pre-authorized); `--yes` gates exist precisely so consent is explicit
- **Trust is earned in the registry**: unindexed = installable but flagged unknown; the one-line registry PR is the review gate (inject text and connectors are the security faces)
- The script touches only its six mechanical sites; data zones (`wiki/`, `vault/`, `cuhksz/`, `projects/`), credentials (`~/*-cli`), and the AGENTS.md handwritten region are never touched
- Errors from the script always block; warnings are reported only
- Uninstall leaves data in place (deprecated posture); physical deletion belongs to the human
