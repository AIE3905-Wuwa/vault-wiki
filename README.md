# OWFA — One Workspace For All (agents)

> **OWFA** is the project; **OWFA Core** is the framework body (formerly `vault-wiki`); **OWFA CLI** is the installer. The public home is moving to **`owfadev/owfa`** — `github.com/owfa` is an unrelated organization. The npm name `owfa` is under application; see [The name](#the-name).

**A team-maintained agent knowledge-base framework**: vault holds real assets, wiki keeps md proxies and native notes, and the agent reads/writes with zero priors per the SASU-L disclosure order. md plus plain files are the foundation; Obsidian and friends are replaceable viewers.

> Status: **alpha** — capability-wise a prototype matured by six weeks of real daily use (born 2026-09-08, validated by two rounds of real operation plus a cold-start disclosure audit, the bb course family live across four courses); distribution-wise v0.3 is the first shape others can install — covered by exactly one fresh-instance acceptance run, zero outside users. Beta gate: behavior contracts (#34) landed · both members running real installs · the legacy-instance conversion walked through · the acceptance script replayable green. `.meta/VERSION` tracks the kernel contract, not product maturity — stage labels live here and in release notes. Universalization and matrix testing remain deferred. Converted from personal use to a team project on 2026-10-02. Docs language switched to English on 2026-10-06 (historical Chinese log entries preserved as-is). 2026-10-12: repo transferred to the GitHub org **AIE3905-Wuwa**; the standardization-and-split improvement phase opened — package binding landed (core 20 + 5 domain packages, see [.meta/docs/packages.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/packages.md)); dev rules now live in [CONTRIBUTING.md](https://github.com/owfadev/owfa/blob/master/CONTRIBUTING.md). 2026-10-13: VERSION 0.3 (tag v0.3) — registry discovery/install, subset installs (--without), upgrade chaining, teardown (x->0) closing the migration algebra, the instance git contract; validated end-to-end by a fresh-instance acceptance run. 2026-10-25: the framework body gets a distribution channel of its own — npm CLI `owfa` (`init` / `upgrade` / `doctor` / `add`), closing the "clone + copy two trees + hand-write AGENTS.md" gap (issues #45/#46); the npm name `owfa` is frozen under the registry's similarity policy and is under application, with `owfadev` as the fallback namespace.

## The name

**OWFA — One Workspace For All (agents).** One workspace — the directory you own, holding `vault/`, `wiki/`, `AGENTS.md` and the framework body — that every agent you use re-enters instead of being re-introduced each session. *All* means all of *your* agents, not all people and not a hosted service; the human stays the owner and the audit anchor. `vault-wiki` retires from the public surface: public copy says **OWFA** (or **OWFA Core**), the GitHub home moves to **`owfadev/owfa`**, and `owfa` is the name the CLI ships under. That last address is not free yet — npm froze `owfa` as too similar to `ow`/`ora`; an application is in progress, and `owfadev` is the fallback package. Full rationale, layers and collision policy: [`.meta/docs/naming.md`](https://github.com/owfadev/owfa/blob/master/.meta/docs/naming.md).

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
| Packages | The index lives in the [registry](https://github.com/owfadev/registry) (Obsidian-model: self-hosted packages, one-line PR is the listing gate). `kernel install`/`list-remote` resolve against it; unindexed repos stay installable with `--yes` (trust: unknown). The org repos `pkg-cuhksz` / `pkg-lark` / `pkg-email` / `pkg-bili` / `pkg-project` / `pkg-github` hold the packages, split with full file lineage |
| `.agents/skills/` | Deployment copies of command & connector skills (framework commands after the split; connector skills arrive with their packages) |
| `bin/` + `templates/` + `package.json` | The npm channel: `owfa` CLI, AGENTS seed, package manifest. `test/` and `scripts/` are development-only and never ship |
| `test-repo/` | Local test sandbox — untracked since 2026-10-13 (owner re-ruling; a fresh clone carries none of it). A scratch deployment for experiments needing an AGENTS.md context; setup and rules in [`.meta/docs/sandbox.md`](https://github.com/owfadev/owfa/blob/master/.meta/docs/sandbox.md). The framework repo itself carries no AGENTS.md — library posture; dev rules live in [CONTRIBUTING.md](https://github.com/owfadev/owfa/blob/master/CONTRIBUTING.md) |
| `.meta/docs/` | Human docs: `intro.md` introduction, `mechanics.md` mechanics, `usage.md` usage guide, `deployment.md` full guide / `quickstart.md` five-minute path, `instance-git.md` the instance-side git minimal contract, `research-*.md` research files — direct links at the end. Authoritative mechanics live in the kernel reference skill; docs do not mirror mechanics |

## Collaboration

This repository is a team project: three members with write access, everything through PRs (1 approving review to merge, `enforce_admins` on); the owner holds final say on repo settings, permissions and charter/kernel changes. Data red lines, commit flow and version discipline are summarized in [CONTRIBUTING.md](https://github.com/owfadev/owfa/blob/master/CONTRIBUTING.md) — the authoritative dev rules; the change trail is git history + PRs + issues (the repo keeps no run log).

## Getting started

Two ways in. **Channel (recommended):** `npx owfa init my-workspace` — Node 16.7+ for the installer, Python 3.9+ for Core; nothing to clone (`npx owfadev init` is the fallback while the npm name is under application). **Manual:** clone this repository and follow the five steps in [quickstart.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/quickstart.md), then `python .meta/scripts/wiki_plugin_kernel.py all`. Full guide, including packages and upgrades: [deployment.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/deployment.md).

Prerequisites: Python 3.9+, pure stdlib, no install needed for the framework itself (connectors carry their own deps); Node 16.7+ only for the npm channel; git recommended (instance snapshots); an agent environment that reads AGENTS.md and skills, e.g. ZCode; Obsidian optional, viewer only.

Open an agent session at the repository root. AGENTS.md is the constitution, containing the plugin injection region; the thirteen commands trigger by natural language: **map / save / profile / query / check / plugin / lark-map / bb-map / asset-read / kernel reference / teach / quiz / track** — map, save, profile, query, check, plugin, lark-map, bb-map, asset-read, wiki_plugin_kernel, bb-teach, bb-quiz, bb-track; masters live in `.meta/command/`. Put a file into `vault/` and say "map" to the agent — that is the first use.

## Deployment

OWFA has three layers: **OWFA CLI** (the installer, never copied into the workspace), **OWFA Core** (`.meta/` + `.agents/skills/`, the thing that is installed), and the **kernel** (a pure-stdlib Python script inside Core — there is no separate kernel install; Python 3.9+ runs it). Domain packages under `.meta/plugins/domains/<pkg>/` are optional.

```bash
npx owfa init my-workspace        # target name; npx owfadev init while the application is pending
cd my-workspace
npx owfa doctor                   # target: python / framework / markers / kernel validate (npx owfadev doctor for the fallback)
npx owfa list                     # registry catalog
npx owfa add cuhksz               # optional package
npx owfa upgrade                  # later: replace the framework trees, preserve instance state
```

While the name is under application, substitute `npx owfadev` for every `npx owfa` command above (or install either package globally; both expose the `owfa` bin).

`init` is additive: existing content is untouched, an existing `AGENTS.md` is preserved and only the injection region is appended. `upgrade` replaces `.meta/` and `.agents/skills/` (instance data is never touched) and keeps the kernel's migration ledger, journal and registry cache.

- Full deployment guide (components, channels, packages, upgrades, troubleshooting): [`.meta/docs/deployment.md`](https://github.com/owfadev/owfa/blob/master/.meta/docs/deployment.md)
- Five-minute path: [`.meta/docs/quickstart.md`](https://github.com/owfadev/owfa/blob/master/.meta/docs/quickstart.md)
- Channel design and release runbook: [`.meta/docs/distribution.md`](https://github.com/owfadev/owfa/blob/master/.meta/docs/distribution.md)

## Doc pointers

- [.meta/docs/deployment.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/deployment.md) — deployment guide: components, channels, first run, packages, upgrades, troubleshooting
- [.meta/docs/naming.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/naming.md) — the name: canonical expansion, what each word commits to, two names two jobs, objections, collision policy
- [.meta/docs/distribution.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/distribution.md) — the npm channel: commands, artifacts, version invariant, release runbook, security posture
- [.meta/docs/packages.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/packages.md) — package mechanism and design rationale: layout, PKG.yaml, invariants, versions, uninstall contract, decision ledger
- [.meta/docs/developer.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/developer.md) — developer guide: where a plugin lands (the three-path table), the dev loop, registration and discovery
- [.meta/docs/agents-example.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/agents-example.md) / [.meta/docs/log-example.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/log-example.md) — instance seeds for AGENTS.md and log.md (the framework repo itself carries neither)
- [.meta/docs/intro.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/intro.md) — introduction: why this framework, narrative & lineage
- [.meta/docs/mechanics.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/mechanics.md) — mechanics: each mechanism one level deeper, with a bb-family walkthrough; read before touching the framework
- [.meta/docs/usage.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/usage.md) — usage guide: the three work loops (library keeping, course learning, collaborative development)
- [.meta/docs/quickstart.md](https://github.com/owfadev/owfa/blob/master/.meta/docs/quickstart.md) — five-minute path: one command or the manual five steps, then first run
- `.meta/protocol/` — field registry, action discipline, disclosure paradigm

## History

2026-08-26 founded as a copy of the personal library's structure; 08-28 repositioned as this project; 09-08 the plugin-plus-command prototype landed directly, validated by real operation then frozen. 09-12 refactor: the conceptual pair wiki & vault established; the original vault plugin renamed mapping; layering abolished; identifiers anglicized. 09-19 the lark family and the calendar time territory established. 09-22 domainization: the domain conceptual root established; vault, lark, project compliant as instances. 09-29 profile became a standalone command; the email domain established; the connector slot established. 10-01 to 10-02 the bb domain suite landed and was validated across four courses; collaboration red lines set; converted to a team project. 10-04 the bb cognition-consumer refactor — bb-teach, bb-quiz, bb-track commands; mechanics docs opened; docs moved to `.meta/docs/`. 10-05 the cuhksz school domain established, bb demoted into the family, sis and registry sub-domains followed. 10-06 the bilibili domain established (query-and-answer + emergence archives, low-risk write whitelist), connector bili-cli first version; the cron time-automation territory established (declaration-as-source, one page per task), lark-calendar/bili/email migrated onto the bridge; bili 0.3 video-archival batch. Docs switched to English. Design-lineage discussions live in the personal library — see AGENTS.md pointers. 10-12 repo transferred to the GitHub org AIE3905-Wuwa; standardization-and-split improvement phase opened: package binding (directory == package, PKG.yaml reconciliation, scope validate, residual scan, VERSION 0.2 anchor + tag v0.2); the convergence record lives in issue #20. 10-13 discovery/download/update shipped (registry INDEX, owner/repo trust gate, silent-reinstall upgrades, --without subsets, VERSION 0.3 + tag v0.3), then teardown (x->0) closed the migration algebra (dormant staging, tri-face warning, residual gate, sweep symmetry); five packages re-released at v0.2; a fresh-instance acceptance run walked the full lifecycle green and fed back the cold-start doc fixes; the sandbox left git tracking (local-only, owner re-ruling); quickstart gained the two postures (clone-as-instance for users, template + instance for developers).

## License

MIT — see [LICENSE](https://github.com/owfadev/owfa/blob/master/LICENSE).

