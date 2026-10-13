# Quickstart

> Reader: anyone who wants to install the framework into their own directory—an Obsidian vault or any folder works—or the agent doing it for you. About ten minutes end to end; every step has been rehearsed and verified against a clean directory. First verified 2026-09-13; updated 2026-10-04 to 28 plugins, 13 commands; 2026-10-06 counts refreshed to 35 plugins; 2026-10-12 package layout — core 20 + 5 domain packages (see [packages.md](packages.md)); 2026-10-13 kernel install/upgrade/migrate replace the copy-loop model for packages.

## What you get

- `vault/` holds real assets in any format; `wiki/` carries proxy pages and native notes. Markdown plus plain files as the foundation; Obsidian is just an optional viewer
- An agent that tends the vault for you: say "map" when placing assets; "save" to store insights; "query" to ask for knowledge; "teach", "quiz", or "cognition profile" for course learning. Index, tags, hot cache, and log are maintained automatically
- Additive deployment: not one byte of the target vault's existing content is touched

## Prerequisites

| Item | Requirement |
|---|---|
| Python | 3.x, pure standard library, zero dependencies |
| agent | A coding assistant that can read AGENTS.md and `.agents/skills/`, e.g. ZCode |
| Obsidian | Optional, viewer only |

## Five deployment steps

**① Get the framework**: `git clone https://github.com/AIE3905-Wuwa/vault-wiki.git`, or download the ZIP and unzip it (the old personal-repo address redirects).

**② Copy two trees** to the target vault root: `.meta/` and `.agents/skills/`. Plugin masters, command masters and copies, protocol artifacts, and mechanical scripts all live there. The clone ships **core 20 only** — no domain packages. Packages are added per need from the registry: `python3 .meta/scripts/wiki_plugin_kernel.py install <pkg> --yes` (see [packages.md](packages.md)); offline alternative — copy a package's `domains/<pkg>/` directory in and rerun `all`.

**③ Write the target vault's AGENTS.md**: draft the shell yourself—one identity paragraph plus a layout description; copy the injection region marker block verbatim from [agents-example.md](agents-example.md), not a single character changed—from `<!-- wiki-inject:start -->` to `<!-- wiki-inject:end -->`—it is the sole source of the structural contract. If the target vault already has an AGENTS.md, paste in only the injection region block.

**④ Create four empty directories**: `vault/`, `wiki/notes/`, `wiki/sessions/`, `wiki/vault/`. Derived pages need no hand-creation—index, tags, hot, and log are built by the pipeline on first run; the root index's `format_version` is also rendered by the pipeline.

**⑤ Converge the projections**, run at the target vault root:

```
python .meta/scripts/wiki_plugin_kernel.py all
```

Expected: core 20 (plus whichever packages you have installed) pass validate, package rosters reconcile; injection region unchanged; command copies in sync. Any error means the copy is incomplete—fix it and rerun.

## First-run verification

1. Put any file into `vault/`, e.g. `memo.txt`
2. Open an agent session at the target vault root and say "**map**"
3. The agent should produce the `wiki/vault/memo.txt.md` proxy page, with SHA-256; the post-write pipeline builds `wiki/index.md`, each directory's `index.md`, `tags.md`, `hot.md`, `log.md`; the attached-audit report follows
4. Then say "**check**"—all green means the deployment succeeded

## One-word daily commands

| You say | The agent does |
|---|---|
| map | register vault assets as proxy pages |
| save | distill conversation insights into native notes |
| query | answer synthetically from hot cache, index, and grep, with wikilink citations |
| check | vault health audit |
| plugin | (un)install structural plugins |
| profile | maintain a continuous cognition profile of you |
| cognition profile / teach & answer / quiz self-test | the bb domain course-learning family; connect the course domain first, see below |
| kernel reference | wiki_plugin_kernel usage and mechanics overview |

Command details are as disclosed in each SKILL.md under `.agents/skills/`—thirteen in all, listed in README; for how workflows chain together see `.meta/docs/usage.md`.

## Optional domain plugins

The core deployment includes only vault and general wiki capabilities; external domains are enabled as needed. `kernel list-remote` shows the catalog; `kernel install <pkg> --yes` lands a package — plugins, commands, and in-repo connectors in one step (the bb course domain brings bb-cli, connecting to Blackboard with credentials stored only locally; lark declares the external lark-cli for Feishu; email brings mail-cli for a personal mailbox). On first use, each connector's skill ships its own disclosure.

## Upgrade and uninstall

- **Upgrade**: framework — re-copy `.meta/` and `.agents/skills/` over the old ones, rerun `all` (a kernel self-update command is designed but not yet shipped; the copy is manual until then); packages — `kernel upgrade` compares against the registry and applies per package (silent reinstall, never cascaded). A new version may stage **semantic migrations** — the kernel warns on three faces and walks you through; see [packages.md](packages.md). Data zones are unaffected
- **Uninstall**: package-level — `kernel uninstall <pkg> --yes` (four-clear; a declared teardown stages the semantic-deletion warning with a residual gate; data zones stay, lapsing into the deprecated posture); the whole framework — delete the two trees plus the AGENTS.md injection region block. The data zones are yours—dispose of them as you see fit

## FAQ

- **Target vault already has content?** The framework is append-only and changes nothing; existing content stays as is. New assets go into `vault/` via map; whether to proxy old content is your decision, made incrementally
- **Can I copy the whole `.agents/` tree?** Yes—this repository's `.agents/` contains only `skills/`
- **Cross-platform?** Pure standard library, no hardcoded paths; tested on Windows Git Bash; macOS and Linux need nothing extra
