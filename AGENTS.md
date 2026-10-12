# Project Intro

This repository (directory `agent-obsidian-template`, working name **vault-wiki**) is the build project of the vault-wiki framework and also its first **prototype instance**: since 2026-09-08 the "plugin + command" architecture has landed directly, with spec docs distilled afterwards. **Positioned as a team project** (converted from personal use on 2026-10-02; universalization and matrix testing deferred — fix as used).

- Layout: `.meta/` (prototype core: plugin & command masters, protocol artifacts, mechanical scripts, human docs `docs/`) · `wiki/` (the inner side of the inner/outer divide) + `vault/` / `projects/` / `cuhksz/` (external domain containers, data areas — cuhksz/ school domain: bb/ course workspace + registry/ regulation materialization) · `.agents/skills/` (deployment copies) · `connectors/` (connector masters: deployment-side CLI factual interface + skill usage disclosure — `connectors/*/SKILL.md` lands in `.agents/skills/` via kernel deploy; currently bb-cli / sis-cli / mail-cli / bili-cli) · `test-repo/` (**independent test sandbox**: whitelist-tracked — only the `.meta/` and `.agents/` framework mirrors are committed and re-copied on root-side sync; experimental content inside the sandbox stays local, never in history; the sandbox does not perceive this project)
- Terms: **wiki** = the md world, the inner side of the inner/outer divide (per-domain projections + native notes); **domain** = the adapter contract for an information source outside the wiki (vault is the default domain; lark / project / email / bb / bili are domains too); **vault** = the default domain — the real-asset repository (command side append-only; deletion & editing are the human's freedom)
- Conflict adjudication: the prototype's current state and converged discussion conclusions prevail; spec distillation merges historical versions under `.meta/docs/`
- The personal library (`D:\Obsidian repo\agent-obsidian`) is a read-only reference sample: the original wiki idea has been transformed into this prototype (see log 2026-09-08)

# Core Principles

1. **Prototype first, docs later**: once a design converges in discussion it lands directly as a prototype (`.meta/` plugins & commands) and is validated by real operation; spec docs are distilled afterwards from what actually runs — never drafted in advance.
2. **Skeleton vs instance separation**: anything personal (journal systems, material preferences, address rules…) is recorded as instance configuration, never architecture. Touchstone: what cannot move into a brand-new instance is personal-layer leakage into architecture; likewise, **whatever the agent is assumed to know (unstated conventions, format priors) is knowledge-layer leakage** — in real deployments the agent learns only via the SASU-L order (system prompt → AGENTS.md → Skills → user's words → loop), zero priors.
3. **The architecture does not enumerate**: no enumeration of file formats or note types (a type is a frontmatter field); structure is specified by each plugin; the wiki directory splits into the proxy layer (`wiki/vault/`) and the native area (`wiki/notes/` notes, `wiki/sessions/` sessions).
4. **No tool-private formats**: md + plain files are the foundation; Obsidian, WebUI etc. are replaceable viewers.
5. Actively maintain `log.md` and `README.md`: log holds project status, stages & progress, next steps, past operations — total under 2.5k chars, operations dated (to the day); proactively consolidate when stale or overlong (**consolidation requires prior user consent**); README is the outward charter digest — after structural changes (positioning / layout / plugin & command counts / collaboration rules) land, refresh the affected paragraphs; fix staleness on sight — the authoritative source is always this file. **Team-mode addendum (2026-10-02)**: members **append-only, never edit or consolidate** the log at runtime; over-limit does not block and is not privately consolidated — it flows with the branch and the current user notifies the owner; consolidation rights & consent belong to the owner.
6. This file is directive; total length <250 lines (widened 2026-10-01, originally 150); details go behind pointers; read the important pointers proactively at the start of every session.
7. Project docs and disclosures are written in English (switched 2026-10-06 from Chinese-first; historical Chinese log entries are preserved as-is — the log switches language append-only, see its note); structure files keep ASCII names.
8. **Small proactive commits**: once a design is finalized or a skeleton change lands, the agent commits proactively without waiting for user instruction (anti zero-commit trap); commit message format `module: summary` (e.g. `skeleton: minimal set and directory layout finalized`); one commit does one thing; no proactive push (routine pushes within the entrusted manager's duties excepted — see the delegation clause under "User Requirements"); history-rewriting operations forbidden.
9. **Complete disclosure, validate by use**: skills and specs are written per the SASU-L disclosure paradigm (zero priors — see principle 2 and `.meta/protocol/experiments.md`); framework changes are judged by real-use feedback, fixed as used — no matrix testing (ruled 2026-09-12).
10. **Analysis rounds must not execute**: when the user's request is a brief / discussion / assessment / proposal ("summarize the current state", "any objections", "take a look"), the round delivers analysis only and touches no file; execution waits for an explicit verb (execute / land / do / merge / push…). Preference statements ("names should be sensible", "should be added") are requirement input, not authorization; when an utterance contains both, the request verb prevails; when ambiguous, ask first (ruled 2026-10-01, after a brief-round overstepped into renaming).
11. **Global vs domain plugins**: two classes — global plugins (cross-cutting services & sinks, e.g. trust / log / todo / calendar / notes / user-profile) and domain plugins (domain instance families; whichever depends on domain directly is a domain base, the rest belong via transitivity). Global plugins may declare **bridges** — the manifest `bridge` key marks the attach cardinality (mandatory | on-demand), with integration format & details in the PLUGIN.md bridge section; domain plugins attach bridges via depends, and **mandatory bridges are verified complete by kernel validate** (missing edge on a domain base → error). A bridge holds only "who is here, how to integrate" — no domain-shape knowledge (each plugin owns its own disclosure, SASU-L) (ruled 2026-10-02, derived from the group meeting).

# Commands (user-triggered)

- **init**: read this file's pointers and `log.md`, align across sessions; judge whether the log needs consolidation and pointers need updating.
- **update**: update `log.md` and related docs, then git commit; append a briefing: what was done this round, key decisions & rationale, impact.
- **discuss**: discuss and align professionally and concisely; discussion only — destructive operations forbidden.
- **recover**: end a special state (e.g. discuss) and resume normal work.

# User Requirements (hard constraints)

- The personal library `D:\Obsidian repo\agent-obsidian` is read-only to this project; any backfill requires explicit user instruction.
- Personal private content (user profiles, journals, personal records) must not be written into this repository — the framework is a universal artifact.
- Reference projects (`D:\My Programs\erp - ksbgs`, `D:\My Programs\aijia`) are pattern references only; modify nothing in them.
- **Commit boundary (everyone)**: only development artifacts enter git — `.meta/` (incl. `docs/`), `connectors/`, root-level charters, root data-container empty seeds (`cuhksz/`), test-repo whitelist mirrors (only `.meta/` and `.agents/`, re-copied on root-side sync — ruled by the owner 2026-10-04, fabricated examples stay out too). **Never committed**: real course/grade/submission data, personal privacy, credentials & sessions, sandbox experiment artifacts (everything outside the test-repo whitelist). `test-repo/` is an independent sandbox; its experimental content stays local; **once real experiments happen, none of its out-of-whitelist changes may be committed** — uploading any usage traces is forbidden (mirror updates go through root-side re-copy, never sandbox-side sync).
- **Git discipline (everyone)**: develop on branches; entering master requires the manager — **the manager is exercised by an agent on the owner's delegation (authorized 2026-10-02)**: branch review (red-line scan + kernel validate + projection convergence) → merge & push → remote branch governance (violations deleted on sight and reported to the owner) → PR-page operations (comment/review/close, leaving traces on GitHub — via gh CLI, credentials injected from the GH_TOKEN env var, token taken from `git credential fill`, never echoed or written to disk), with a log entry after each delegated action. One commit does one thing; self-check before merging that the diff contains no non-development content; **opening a gitignore whitelist or force-adding ignored instance data requires the repo owner's explicit authorization, recorded** (rule set after the 2026-10-02 member incident); history rewriting forbidden. **Reserved matters (never delegated; owner-explicit only)**: history rewriting, gitignore exemptions, deleting others' non-violating work, repository settings & member permissions, backup deletion.
- **Commit flow (everyone, standard)**: branch off the latest `master` (name = module-topic or feature/topic) → small commits (`module: summary`) → pre-completion self-check (`python .meta/scripts/wiki_plugin_kernel.py all` passes, diff free of non-development content, log append-only) → push the branch and **opening a PR is recommended** (GitHub merge-request page, the standard review channel, auto-closed with trace on merge; un-PR'd branches are reviewed & merged by the manager all the same) → manager reviews & merges, deletes the merged branch, logs and reports.
- **Collaboration alignment (everyone)**: before touching a plugin/connector, read `log.md` status & next steps; version numbers advance along the changelog — no skipping or pre-reserving; experiments & tests always land in the test-repo sandbox or locally, conclusions via conversation reports or `docs/`.

# Pointers

> Pointers are maintained proactively. Cross-session-critical pointers carry **ATTENTION**; volatile state (progress etc.) lives in `log.md`, never in this file.

- `log.md` — project log: status, stage, next steps, past operations **ATTENTION**
- `.meta/` — prototype core: structural plugins (`plugins/` — the two conceptual roots domain (outer · domain contract) and wiki (inner · origin dichotomy) + domain instance families: vault (default domain; mapping is its mapping law, structure manages its layout), lark (external domain base; pointer/archive dual form; in-domain lark-docs cloud-docs domain / lark-im interpersonal domain), project (self-standing container domain: projects/ workspace + wiki declaration page), email (personal mailbox domain: wiki/email/ account + three assets + unified digest, connector mail-cli), bili (bilibili content domain: wiki/bili/ identity page + digest + emergence-based UP & video archives (video page two sections: overwritable summary + append-only review), query-and-answer, watch-video degradation chain, connector bili-cli — low-risk write whitelist needs the user's explicit verb behind double gates), cuhksz (school domain base: identity page + subsystem family — bb course ops (bb/ workspace + wiki/cuhksz/bb/ territory, term/course dual-side isomorphism; bb-map is its mapping law, bb-track manages the cognition profile), sis student records (wiki/cuhksz/sis/, connector sis-cli), registry academic regulations (materialization + pointer index)) + notes/sessions/link/tag/trust/index/hot/log/user-profile/todo/language/device + calendar the time territory (lark-calendar as source adapter) + cron the deferred-trigger territory (declaration-as-source, executor-as-projection; time | condition triggers × session|script forms) + tmp scratch area — no layering, injection order = dependency topology + alphabetical) plus command masters (`command/`), protocol artifacts (`protocol/`: field registry, action discipline, SASU-L disclosure paradigm) and mechanical scripts (`scripts/`: wiki_plugin_kernel install/compliance/inject/copy + pipeline derived-layer index/tags/hot/log/verify + wikilib the page-parsing backbone); the AGENTS.md injection region is their projection **ATTENTION**
- `wiki/`, `vault/`, `projects/`, `cuhksz/` — data-area skeletons (kept as empty seeds: content belongs to deployment instances, not accumulated in this project — live-repo validation goes through `test-repo/`); `.agents/skills/` — deployment copies of command & connector skills
- `.meta/docs/` — human docs (the authoritative mechanics live in the kernel reference skill; docs do not mirror mechanics): `intro.md` introduction (how we got here — narrative & lineage), `mechanics.md` mechanics (each mechanism one level deeper + a bb-family walkthrough), `usage.md` usage guide (three work loops), `quickstart.md` deployment walkthrough, `research-*.md` research files (user-profile selection, landscape benchmarking)
- `README.md` — project charter
- Design lineage (discussion records, read-only): personal library `wiki/meta/2026-08-25-wiki运行时重构决策.md`, `wiki/sessions/2026-08-25-wiki架构调研与docs-first重构设计.md`
- Reference projects: `D:\My Programs\erp - ksbgs` (source of the AGENTS.md pattern: charter + pointers, log capacity management, command set); `D:\My Programs\aijia` (wiki pointer-style references)

<!-- wiki-inject:start -->

## wiki injection region

> This region holds plugin-injected projections; marker blocks are added/removed as plugins are (un)installed or change injection tier (member-tier plugins exit the region — exposure rides on the family root's roster line, skills, and on-demand manifest reads; the region carries a byte budget); handwritten content does not belong here.

<!-- plugin:domain v0.1 -->
- Domain abstraction (outer): wiki recognizes only the inner/outer distinction; an outer domain = an adapter contract (external territory / landing strategy / identity proof / wiki-side territory / write model / trust model), declared by each domain plugin itself, with in-domain plugins belonging to the domain transitively; landing is essentially a write-model choice (final-state assets → append-only repository, process container → full read/write, truth elsewhere → pointer), and projection density follows translation cost (mirror / pointer / disclosure-only); borrowing vault or pointers is the default posture, self-standing containers are the exception (criteria: write-model or structural-rigidity divergence); a domain must be discoverable within wiki (declaration page or injection line)
<!-- /plugin:domain -->

<!-- plugin:wiki v0.7 -->
- wiki container `wiki/` (the inner side of the inner/outer distinction): origin dichotomy — territory pages in two forms: proxy pages (default, projections of reconcilable external sources, territory paths self-disclosed by each domain's injection line) and in-domain native pages (domain-side archives declared by the domain — the true body lives here, no external source to reconcile, shape owned by the domain plugin; first case bb-track cognition profile user.md); everything outside territories is native pages (writings whose true body lives here; session pages are minutes not mirrors — once the conversation vanishes the page is the true body, writing is birth); index / tags / hot / log are derived pages (mechanical projections); page frontmatter takes a minimal YAML subset (top-level scalars / block lists / one-level block mappings), more complex structures are not parsed
<!-- /plugin:wiki -->

<!-- plugin:device v0.4 -->
- Device profiles: one page per personal device in wiki/notes/ (type: entity suggested); device block mapping minimal keys serial/purchased/warranty_until, rest open; body ## Tool Environment = presence-level connector/runtime/channel registry for cross-device lookup (synced on (un)install, no full inventory); invoice assets via vault + wikilink; attached audit scans warranty_until (30-day window → warning list; todo line only upon confirmation); no real-time monitoring, no team lending
<!-- /plugin:device -->

<!-- plugin:hot v0.10 -->
- Hot cache `wiki/hot.md`: recent-change digest (≤25 entries, <5 days, ≤200 chars per entry); agents read this page first on entering the repository; evict out-of-window entries before writing
<!-- /plugin:hot -->

<!-- plugin:language v0.4 -->
- Writing declaration page wiki/language.md (type: language): language block mapping = key → one-sentence rule (consumer precedents: teaching bb-teach, annotation bb-quiz, register = audience reading level, program default first/second-year undergraduates per AGENTS principle 12) + terms = original → unified translation; body distillation notes append-only; the agent reads it before producing written artifacts; page or key absent → session language (proper nouns/code/paths keep original); default baseline not a mandate — domain source-alignment disciplines take precedence; terms emergence-based (register after recurring hits); direct human edits legitimate
<!-- /plugin:language -->

<!-- plugin:link v0.14 -->
- Link syntax `[[page full name]]` — full name = the relative path within wiki/ minus the trailing .md (e.g. `notes/X`, pdf asset proxy `vault/a.pdf`, md asset proxy `vault/<name>.md`, only one removed); truncated references forbidden, same-name ambiguity resolved by path; fields `related` / `aliases`; broken link = warning (not yet written down), orphan (no inbound links and no references, derived pages don't count as sources) = warning for notes knowledge pages, info for territory-value registration pages (dynamically reads registry type.values, except session)
<!-- /plugin:link -->

<!-- plugin:log v0.15 -->
- Run log `wiki/log.md`: new entries prepended at the top, entries never rewritten; entry = date + type (map/save/query/check/plugin/todo/profile/other) + [domain] (omissible — domainless transactions; log is a mandatory bridge: domain bases must depend on this plugin, constitution principle 11) + one sentence; window ≤100 entries, overflow is mechanically archived to `wiki/archive/<month>/log.md`
<!-- /plugin:log -->

<!-- plugin:notes v0.15 -->
- Native notes `wiki/notes/`: knowledge whose provenance is the wiki itself, subdivided by the type field (open form vocabulary, default values in registry); no-regeneration zone, commands append-only and never modify; session and profile types do not land in this zone (they belong to the sessions / user-profile territories); notes on-demand bridge — domain plugins one-way derive high-value conclusions into this zone on an emergence basis, and must back-link the source page (constitutional principle 11, format owned by this bridge)
<!-- /plugin:notes -->

<!-- plugin:sessions v0.9 -->
- Native sessions `wiki/sessions/`: session backbone pages (type: session, participants required = actor list, default naming YYYY-MM-DD-<topic>); high-value topics promoted to standalone `wiki/notes/` pages with a back-link; no-regeneration zone, commands append-only and never modify
<!-- /plugin:sessions -->

<!-- plugin:tag v0.11 -->
- Page `tags` field: YAML list; primary language follows the default key of the writing-style declaration page `wiki/language.md` (page or key absent → session language); English tags lowercase kebab-case; hierarchy ≤2 (`/` separated), ≤5 per page; open semantic classification, restating type forbidden
<!-- /plugin:tag -->

<!-- plugin:tmp v0.3 -->
- Temporary zone `wiki/tmp/` (the path is the territory; type: tmp optional, landing outside → error): drafts and parsing intermediates, no retention promise, cleanable any time; invisible to the derived layer — excluded from index/tags, never a link source, broken links exempt; promote precious drafts promptly (draft deleted on promotion); intermediates set stale_after as they go — check reports over-age, disposal via confirmation (no automatic deletion); sensitive intermediates best gitignored instance-side
<!-- /plugin:tmp -->

<!-- plugin:trust v0.9 -->
- Trust fields (optional per page): `generated` (who generated it) / `verified` (event list, items single-line by+at) / `stale_after` (expiry moment) / `sources` (sources and signals); level derivation never persisted — no record = unverified, only agent/process = machine-confirmed, contains human = human-reviewed, past stale_after = stale
<!-- /plugin:trust -->

<!-- plugin:calendar v0.4 -->
- Time territory: declaration page wiki/calendar.md (calendar block mapping = source key → declaration; absent = manual-only) + month pages wiki/calendar/YYYY-MM.md — ## Schedule source projection refreshed wholesale + ## Manual Notes append-only; event lines may wikilink, events get no pages; future rolling, past frozen; month stale_after default 2 days; boundary — calendar stores what happens when, todo what is pending; on-demand bridge (domains derive source-keyed lines into the current month)
<!-- /plugin:calendar -->

<!-- plugin:cron v0.4 -->
- Deferred-trigger territory wiki/cron/ (one page per task, the pure directory = the full declaration set): task page type: cron + cron block mapping (trigger: time (crontab 5-field) | condition <kind: file|command|http|process|port|webhook>, condition grammar in PLUGIN.md; action/form session|script/domain/status/last_run/machine) + ## Task + ## Run Notes append-only; declaration-as-source, every executor a replaceable projection — executor names live only in the replay recipes (usage), wiki records intent and traces, probing/delivery semantics stay executor-side; replay lands active pages execution-side upon user confirmation; reconciliation per-form diff against readable executor lists in the check attached audit; intent-change sync both directions; failures report via log only, never blocking others; boundaries — todo one-shot, calendar facts, cron deferred-trigger automation intent; on-demand bridge (domain tasks: page + depends)
<!-- /plugin:cron -->

<!-- plugin:cuhksz v0.3 -->
- CUHK-SZ school domain wiki/cuhksz/ + data zone cuhksz/ (external: the cuhk.edu.cn school-system family — bb course ops · sis student records · registry academic regulations; connectors bb-cli / sis-cli read-only): identity page identity.md (type: cuhksz + sis enrollment block mapping, created when absent); family — bb course ops (members bb-map mapping · bb-track cognition · bb-teach teaching · bb-quiz self-test, connector bb-cli), sis records (connector sis-cli), registry regulations (cuhksz/registry/ materialization + schemes.md index, no connector); official personal PDFs land in-domain (cuhksz/sis/), vault only the containerless fallback; red lines: credentials stay local, enrollment/course/grade data never enters the framework repo; member detail on demand (skills + manifests); trust per subsystem
<!-- /plugin:cuhksz -->

<!-- plugin:index v0.13 -->
- Index overflow-offloading: root wiki/index.md always present (carries format_version), listing all reachable pages full-path; a list over the window (params in pipeline source) splits subtrees into their own index.md by descending page count; wiki/tags.md unchanged; aggregate only, never hand-edited, pure-function rebuild (pipeline.py index); indexes invent no structure — overflow lists in full as-is, the cure is subdirectories
<!-- /plugin:index -->

<!-- plugin:lark v0.5 -->
- External pointer domain wiki/lark/<profile>/ (one directory per enterprise, name = lark-cli --profile, always carried): identity page profile.md per profile (one sentence + TTL override); territory two forms — pointer pages (type: lark + lark block mapping profile/kind/token/url, token one-to-one with the page = identity proof, fully regenerable) and archive pages (mechanical section + append-only accumulation, form owned by domain plugins); subdomains lark-docs cloud docs · lark-im interpersonal · lark-calendar calendar adapter; trust ceiling machine-confirmed, stale_after = pull + TTL (default 7 days, overridable), agent = synchronizer; resources gone → status: deprecated, never deleted; CLI discipline — --profile always, auth live never on disk; member detail on demand (skills + manifests)
<!-- /plugin:lark -->

<!-- plugin:project v0.5 -->
- Project container domain projects/<name>/ (workspaces, full agent read/write — versus vault append-only): body and tracking entirely in-folder, self-description project.md (four sections: goal & context / stages / tasks as lines / decisions append-only); wiki side only the declaration page wiki/projects.md (projects block mapping, bidirectional diff against the directories, drift = warning); searches involving project content go directly to the projects/ subtree; boundary with todo — todo is the agent's working set, project.md tasks the persistent source of truth
<!-- /plugin:project -->

<!-- plugin:todo v0.4 -->
- Temporary memory wiki/todo.md (type: todo): cross-session delegations and reminders; entry = trigger condition (date or context) + one sentence + by/at; read first at session start (before hot; absent → create empty); due or past entries raised proactively; append upon delegation, settle upon completion ([x] + log line, history to log); settled capped at 20; live working set only; on-demand bridge — domain plugins one-way derive action items in
<!-- /plugin:todo -->

<!-- plugin:user-profile v0.6 -->
- User profile wiki/profile.md (type: profile): continuing cognition of the user, static identity + dynamic preference layers, dimensions open; convergence-style updates (new replaces old, trace in body), assertions carry evidence wikilinks, preference layer stale_after; zero own fields, reuses trust; not in the notes territory, no tags; updates via the profile command (dual-track trigger, self-creates on first); read before personalized decisions; cognition bridge — domain cognition pages register one line each in ## Domain Cognition, the profile aggregates pointers only
<!-- /plugin:user-profile -->

<!-- plugin:vault v0.6 -->
- Default domain — real-asset repository `vault/`, wiki-side territory `wiki/vault/`: holds assets of any format, doubling as the landing repository for other domains (the url field is the passthrough interface); append-only on the command side, freedom to delete and modify belongs to the human; layout rules belong to the structure plugin
<!-- /plugin:vault -->

<!-- plugin:bili v0.4 -->
- bilibili content domain wiki/bili/ (connector bili-cli — web-cookie login, command surface and red lines in its skill): identity page bili.md (mid/nickname/TTL + watch list, created when absent); query-and-answer, no default projection — retrieval from fresh pulls, high-value conclusions emerge into notes with backlinks; emergence archives — up/ (repeated hits or explicit request), video/ (explicit request or repeated hits; ai summary overwritable + human review append-only); digest inbox.md (regenerable, short TTL); low-risk write whitelist (watchlater/favorites add-remove, like) each needs the user's explicit verb + CLI --yes double gate — writes outside never offered; derivations out-only (bridges); red lines: cookies stay local, personal watch data never enters the framework repo; trust ceiling machine-confirmed, agent = synchronizer
<!-- /plugin:bili -->

<!-- plugin:email v0.5 -->
- Personal mailbox domain wiki/email/ (one directory per account, the account always named; connector mail-cli): root digest inbox.md (regenerable, short TTL) + global people/ archives (token = email address, one page per person across accounts, relationship append-only) + per-account identity page account.md, thread archives threads/ (Message-ID members + topic conclusions append-only), sources/ subscription governance; no full mapping — retrieval pull-and-discard, archives only on repeated hits (emergence); one-way derivation out-only (bridges); mailbox read-only (PEEK, never marking/moving/deleting), send-type operations always need explicit user request; deprecated never deleted; trust ceiling machine-confirmed, TTL default 1 day (overridable), agent = synchronizer
<!-- /plugin:email -->

<!-- plugin:mapping v0.8 -->
- Proxy layer `wiki/vault/`: 1:1 mirror of root `vault/` (proxy name = original name + .md), pages always carry raw_file / raw_sha256; the path is the origin proof
<!-- /plugin:mapping -->

<!-- plugin:structure v0.3 -->
- vault structure declaration `wiki/structure.md` (type: structure): frontmatter `structure` block mapping = directory → one-line semantics, body records presets (date/format/type/mixed, nestable) and notes; agents read this page before placing assets, placing them by position; page absent = flat tolerance; after the human adjusts vault, sync the declaration, check does a mechanical diff (undeclared top-level directory / declared-but-nonexistent directory → warning)
<!-- /plugin:structure -->

<!-- wiki-inject:end -->
