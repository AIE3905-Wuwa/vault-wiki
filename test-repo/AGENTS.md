# test-repo — vault-wiki sandbox instance

Kernel-verified seed instance of the vault-wiki framework: core 20 only; domain packages install on demand (see `.meta/docs/packages.md`). Everything here is experiment territory — never real data.

<!-- wiki-inject:start -->

## wiki 注入区

> 本区为插件注入的投影，装卸插件时同步增删对应标记块；手写内容不进此区。

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

<!-- plugin:todo v0.4 -->
- Temporary memory wiki/todo.md (type: todo): cross-session delegations and reminders; entry = trigger condition (date or context) + one sentence + by/at; read first at session start (before hot; absent → create empty); due or past entries raised proactively; append upon delegation, settle upon completion ([x] + log line, history to log); settled capped at 20; live working set only; on-demand bridge — domain plugins one-way derive action items in
<!-- /plugin:todo -->

<!-- plugin:user-profile v0.6 -->
- User profile wiki/profile.md (type: profile): continuing cognition of the user, static identity + dynamic preference layers, dimensions open; convergence-style updates (new replaces old, trace in body), assertions carry evidence wikilinks, preference layer stale_after; zero own fields, reuses trust; not in the notes territory, no tags; updates via the profile command (dual-track trigger, self-creates on first); read before personalized decisions; cognition bridge — domain cognition pages register one line each in ## Domain Cognition, the profile aggregates pointers only
<!-- /plugin:user-profile -->

<!-- plugin:vault v0.6 -->
- Default domain — real-asset repository `vault/`, wiki-side territory `wiki/vault/`: holds assets of any format, doubling as the landing repository for other domains (the url field is the passthrough interface); append-only on the command side, freedom to delete and modify belongs to the human; layout rules belong to the structure plugin
<!-- /plugin:vault -->

<!-- plugin:mapping v0.8 -->
- Proxy layer `wiki/vault/`: 1:1 mirror of root `vault/` (proxy name = original name + .md), pages always carry raw_file / raw_sha256; the path is the origin proof
<!-- /plugin:mapping -->

<!-- plugin:structure v0.3 -->
- vault structure declaration `wiki/structure.md` (type: structure): frontmatter `structure` block mapping = directory → one-line semantics, body records presets (date/format/type/mixed, nestable) and notes; agents read this page before placing assets, placing them by position; page absent = flat tolerance; after the human adjusts vault, sync the declaration, check does a mechanical diff (undeclared top-level directory / declared-but-nonexistent directory → warning)
<!-- /plugin:structure -->

<!-- wiki-inject:end -->
