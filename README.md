# vault-wiki

**A team-maintained agent knowledge-base framework**: vault holds real assets, wiki keeps md proxies and native notes, and the agent reads/writes with zero priors per the SASU-L disclosure order. md plus plain files are the foundation; Obsidian and friends are replaceable viewers.

> Status: prototype frozen — built 2026-09-08 to 09-12, validated by two rounds of real operation and a cold-start disclosure audit; current stage is daily use, fix as used. Converted from personal use to a team project on 2026-10-02; see `log.md` for the timeline. Universalization and matrix testing remain deferred. Docs language switched to English on 2026-10-06 (historical Chinese log entries preserved as-is). 2026-10-12: repo transferred to the GitHub org **AIE3905-Wuwa**; the standardization-and-split improvement phase opened — package binding landed (core 20 + 5 domain packages, see [.meta/docs/packages.md](.meta/docs/packages.md)); dev rules now live in [CONTRIBUTING.md](CONTRIBUTING.md).

## What it does

Let an AI coding agent run a "personal wiki" for you:

- Drop assets into `vault/`, any format — md, txt, csv, pdf, images. The **map** command registers each as an md proxy page under `wiki/vault/`, with SHA-256, metadata and links
- Insights and decisions from conversations are distilled by the **save** command into native notes under `wiki/notes/`; session backbone pages go to `wiki/sessions/`
- The **query** command reads the hot cache and indexes first, then answers with wikilink-cited results
- Index, tags, hot cache and the run log are all maintained automatically by the derived layer; the **check** command audits library health; the **plugin** command installs/uninstalls structural plugins
- External sources attach as domains: lark and email land as pointers or archive pages; calendar manages the timeline; project manages project containers; bb pulls courseware, assignments and grades via bb-cli; bilibili answers on demand via bili-cli (search/details/favorites/UP tracking; video summaries and reviews archived on explicit request; low-risk write whitelist behind explicit user verbs). Translation happens outside domains; inside the wiki everything interlinks
- The **profile** command maintains a living cognition file about the user: assertions carry evidence, preferences expire; read it before any personalization
- The **teach** command explains per the cognition profile — skim or quiz the known, unpack the unknown; significant Q&A settles into ai notes
- The **quiz** command generates practice from a scope plus optional samples; grading flows back into the cognition profile
- The **track** command reads/writes per-course user.md learning state; teach and quiz usage mounts here

## Core concepts

| Concept | Definition |
|---|---|
| wiki | the md world, the inner side of the inner/outer divide: per-domain projections + native notes + derived layer |
| domain | the adapter contract for an information source outside the wiki. vault is the default domain; lark, project, email, bb, bili are domains too |
| vault | the default domain — the real-asset repository; command side append-only, deletion & editing belong to the human |
| SASU-L | the disclosure paradigm: the agent learns only via system prompt, AGENTS.md, Skills, user's words, loop |

## Layout

| Directory | Contents |
|------|------|
| `.meta/` | Prototype core, two-level plugin layout: `plugins/core/` (20 framework plugins — the two conceptual roots domain and wiki, cross-cutting pieces, and the explicit vault/mapping/structure constitutional exception) + `plugins/domains/<pkg>/` (one package per directory: `PKG.yaml` + family masters — cuhksz 8, lark 4, email, bili, project). Directory boundary == tier boundary == package boundary; `PKG.yaml` declares the roster and the kernel reconciles it against the family closure; `.meta/VERSION` anchors the framework version (package `compat` floors checked against it). Injection order = dependency topology + alphabetical; the AGENTS injection region is tiered — member-tier domain pieces exit it (family roster + skills + on-demand manifest reads carry exposure) under a kernel byte budget; global plugins may declare bridges, and mandatory bridges are kernel-verified. Also 13 command masters, protocol artifacts — registry, actions, experiments — and the mechanical scripts wiki_plugin_kernel, pipeline, wikilib, pure stdlib with zero deps |
| `connectors/` | Connector masters: deployment-side CLI factual interface + skill usage disclosure. `connectors/*/SKILL.md` lands in `.agents/skills/` via kernel deploy; currently bb-cli, sis-cli, mail-cli, bili-cli. Connectors ride with their packages in `PKG.yaml` — physical relocation into the per-package repos happens at the split round |
| Packages | The index lives in the [registry](https://github.com/AIE3905-Wuwa/registry) (Obsidian-model: self-hosted packages, one-line PR is the listing gate). `kernel install`/`list-remote` resolve against it; unindexed repos stay installable with `--yes` (trust: unknown). The org repos `pkg-cuhksz` / `pkg-lark` / `pkg-email` / `pkg-bili` / `pkg-project` / `pkg-github` hold the packages, split with full file lineage |
| `.agents/skills/` | Deployment copies of command & connector skills (framework commands after the split; connector skills arrive with their packages) |
| `test-repo/` | Independent test sandbox. Whitelist-tracked: the `.meta/` and `.agents/` framework mirrors plus the `AGENTS.md` seed (core-only instance — packages install on demand); experimental content stays local, never in history; the sandbox does not perceive this project. The framework repo itself carries no AGENTS.md — library posture; dev rules live in [CONTRIBUTING.md](CONTRIBUTING.md) |
| `.meta/docs/` | Human docs: `intro.md` introduction, `mechanics.md` mechanics, `usage.md` usage guide, `quickstart.md` deployment walkthrough, `research-*.md` research files — direct links at the end. Authoritative mechanics live in the kernel reference skill; docs do not mirror mechanics |

## Collaboration

This repository is a team project: three members with write access, everything through PRs (1 approving review to merge, `enforce_admins` on); the owner holds final say on repo settings, permissions and charter/kernel changes. Data red lines, commit flow and version discipline are summarized in [CONTRIBUTING.md](CONTRIBUTING.md) — the authoritative dev rules; the change trail is git history + PRs + issues (the repo keeps no run log).

## Getting started

Prerequisites: Python 3, pure stdlib, no install needed for the framework itself (connectors carry their own deps); git; an agent environment that reads AGENTS.md and skills, e.g. ZCode; Obsidian optional, viewer only.

Open an agent session at the repository root. AGENTS.md is the constitution, containing the plugin injection region; the thirteen commands trigger by natural language: **map / save / profile / query / check / plugin / lark-map / bb-map / asset-read / kernel reference / teach / quiz / track** — map, save, profile, query, check, plugin, lark-map, bb-map, asset-read, wiki_plugin_kernel, bb-teach, bb-quiz, bb-track; masters live in `.meta/command/`. Put a file into `vault/` and say "map" to the agent — that is the first use.

## Deployment

The framework proper is three things: `.meta/`, `.agents/skills/`, and the AGENTS.md injection region. Deployment is an additive copy: copy the two trees, write the AGENTS shell, create empty directories, converge with the kernel; existing content in the target repo stays untouched. Derived pages self-build on first run — no hand-crafting. Step-by-step walkthrough in [.meta/docs/quickstart.md](.meta/docs/quickstart.md), rehearsed against a clean directory.

## Doc pointers

- [.meta/docs/packages.md](.meta/docs/packages.md) — package mechanism and design rationale: layout, PKG.yaml, invariants, versions, uninstall contract, decision ledger
- [.meta/docs/developer.md](.meta/docs/developer.md) — developer guide: where a plugin lands (the three-path table), the dev loop, registration and discovery
- [.meta/docs/agents-example.md](.meta/docs/agents-example.md) / [.meta/docs/log-example.md](.meta/docs/log-example.md) — instance seeds for AGENTS.md and log.md (the framework repo itself carries neither)
- [.meta/docs/intro.md](.meta/docs/intro.md) — introduction: why this framework, narrative & lineage
- [.meta/docs/mechanics.md](.meta/docs/mechanics.md) — mechanics: each mechanism one level deeper, with a bb-family walkthrough; read before touching the framework
- [.meta/docs/usage.md](.meta/docs/usage.md) — usage guide: the three work loops (library keeping, course learning, collaborative development)
- [.meta/docs/quickstart.md](.meta/docs/quickstart.md) — quick start: five deployment steps and first-run verification
- `.meta/protocol/` — field registry, action discipline, disclosure paradigm

## History

2026-08-26 founded as a copy of the personal library's structure; 08-28 repositioned as this project; 09-08 the plugin-plus-command prototype landed directly, validated by real operation then frozen. 09-12 refactor: the conceptual pair wiki & vault established; the original vault plugin renamed mapping; layering abolished; identifiers anglicized. 09-19 the lark family and the calendar time territory established. 09-22 domainization: the domain conceptual root established; vault, lark, project compliant as instances. 09-29 profile became a standalone command; the email domain established; the connector slot established. 10-01 to 10-02 the bb domain suite landed and was validated across four courses; collaboration red lines set; converted to a team project. 10-04 the bb cognition-consumer refactor — bb-teach, bb-quiz, bb-track commands; mechanics docs opened; docs moved to `.meta/docs/`. 10-05 the cuhksz school domain established, bb demoted into the family, sis and registry sub-domains followed. 10-06 the bilibili domain established (query-and-answer + emergence archives, low-risk write whitelist), connector bili-cli first version; the cron time-automation territory established (declaration-as-source, one page per task), lark-calendar/bili/email migrated onto the bridge; bili 0.3 video-archival batch. Docs switched to English. Design-lineage discussions live in the personal library — see AGENTS.md pointers. 10-12 repo transferred to the GitHub org AIE3905-Wuwa; standardization-and-split improvement phase opened: package binding (directory == package, PKG.yaml reconciliation, scope validate, residual scan, VERSION 0.2 anchor + tag v0.2); the convergence record lives in issue #20.
