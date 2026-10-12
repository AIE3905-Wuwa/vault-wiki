---
name: bb-map
owner: bb-map
consumes: [bb, bb-map, trust, index, hot, log]
description: "Map bb/ fetched artifacts and gradebook snapshots into wiki/cuhksz/bb/<term>/<course>/ canonical four-bucket pages: fetch verification → info/courseware/assessments/attachments placement → reconciliation → post-write pipeline. Triggers on: bb-map, 映射课程, bb 落位, 落位这门课, map bb course."
---

# bb-map: course-domain mapping

Map `cuhksz/bb/` fetched artifacts and gradebook snapshots into `wiki/cuhksz/bb/<term>/<course>/` canonical four-bucket pages — mapping and understanding are decoupled: registration + courseware knowledge-point summaries (coarse-grained distillation) + reconciliation actions (the four-bucket contract and reconciliation fields are in the bb-map block of the injection region). Data fetching goes through the bbcli skill (`connectors/bb-cli/SKILL.md` — session discipline and command quick reference); in-depth teaching is not part of this command (high-value retrospectives go through save into notes, backlinking the territory page).

## Scope

Write: bb-map (info / courseware / assessments / attachments four-bucket pages, mechanical-section overwrite), log, hot, index
Read: registry (`.meta/protocol/registry.yaml`, field and value-set anchor), bb/ fetched artifacts, bbcli (courses / tree / files / dues / assignments / grades / submission), `wiki/cuhksz/bb/inbox.md` (domain configuration)

## Steps

1. **Anchor (one-time read)**: read the registry and `wiki/cuhksz/bb/inbox.md` (`terms` block mapping — active terms and freeze flags); **if the inbox is absent, create it** (register `terms` from a live `bb-cli terms`/`courses` query + first-refresh digest and announcement triage; flow in the bb block of the injection region)
2. Session verification: `bb-cli status` (if not logged in, follow the login discipline in the bbcli skill); locate the target course (directory name = course code, e.g. AIE3005; for a new course, first create the territory directory and identity-page fields)
3. Fetch verification: the `cuhksz/bb/<term>/<course>/` source tree is in place (if missing, place it via the bbcli skill `fetch`, with media filtering on by default — policy in the bb block of the injection region); assessments mechanical-section data is pulled live from `grades` / `submission` snapshots
4. Place bucket by bucket per the injection-region contract: info (identity bb block mapping term_id/course_id/term_status + `## Basic Information` distillation of course-policy key points with `info-N` anchors) → courseware (read sources to identify knowledge points → `## Knowledge Point Summary` (sm-N anchors + one-line gist + chapter hints) + `## Knowledge Point Links` + `## Terminology` + `## Unit Files`) → assessments (summary columns excluded; `## Requirements`/`## References` source-based distillation with `req-N`/`ref-N` anchors + `## Submission`/`## Results` mechanical snapshots; a missing due raises no alert) → attachments (1:1 proxies); mechanical sections are overwritten on reconciliation, accumulation sections are never touched
5. **Present the placement preview** (added / changed / deprecated lists) and wait for user confirmation
6. **Post-write pipeline** (deterministic, mechanical and automatic, no prompting): execute each plugin's write calls in injection-region order (index/tags/hot/log derived-layer rebuilds first), then finish with `python .meta/scripts/pipeline.py verify` (post-write self-verification; on failure, go back and fix); then commit per the commit discipline (`映射: <term>/<course>`, see the vocabulary in `.meta/protocol/actions.md`)
7. Report: course / added·changed·deprecated counts per bucket / stale list (stale items clear after a live bbcli refresh)

## Prohibitions

- Never write any file on the `cuhksz/bb/` source side (fetched artifacts are append-only; deletion and modification are human freedom); never copy full original text
- Accumulation sections (info `## Notes` / assessments `## Review`) are append-only; rebuilds must not touch them
- Never pull the roster; grades go only into the assessments mechanical section (privacy red line: course / grade / submission data is instance data and never enters the framework repository)
- Credential sessions stay on the local machine; write operations such as submitting assignments are not part of this command (always require explicit user instruction and separate design)

## Language

Output language takes the default key of the language declaration page `wiki/language.md` (a missing page or missing key falls back to the session language); proper nouns and paths keep their original form.

## Parameters

- Course (course code / territory directory name, e.g. `AIE3005`; omittable = all courses in the active term)
- Bucket (`info` / `courseware` / `assessments` / `attachments`; omittable = all — for single-bucket reruns)

## Injected Section (plugin usage blocks)

> This region is a wiki_plugin_kernel projection: consumes pulls merged with usage_routes source-side routing; disclosure order = owner first, routed blocks in the middle, pulled blocks last (rebuilt by inject / all); handwritten content does not belong here — to change the write-side contract, edit PLUGIN.yaml.

<!-- cmd-inject:start -->
<!-- usage:bb-map -->
- Course information page: create info.md per course (type: bb + bb block mapping term_id/course_id/term_status (active|frozen) + generated/stale_after); the body's `## Basic Information` distills course-policy key points (grading/assessment/faculty/TA/grouping/teaching language/AI policy, itemized `<a id="info-N">` anchors, reading bb/ syllabi and assessment files, missing items marked 'not provided'); `## Course Conventions` records course-intrinsic conventions (professor's notation, grading habits) that hold for any learner — distinct from bb-track's user.md `## Preferences` (user-specific); 'what happens when' is recorded here, all elements of graded affairs go to assessments pages
- Knowledge-point pages: each bb/ content unit (directory = handouts + attached files as one, or a flat single file; parallel same-kind directories merge into one page) → courseware/<unit-name>.md (type: bb + raw_path pointing at that unit, may be absent for entirely undownloaded units + generated); read sources to identify knowledge points → `## Knowledge Point Summary` itemized `<a id="sm-N">` anchors + one-line gist + source-side section-level hints → `## Knowledge Point Links` cross-links between points → `## Terminology` English-Chinese glossary → `## Unit Files` two-state reconciliation list (present locally / unmaterialized pointer entries — media pointer-based by default, see the bb block; for flat multi-attachment units the list is the correspondence); whole page regenerable, precious content distilled into notes
- Knowledge-point granularity (fine, not coarse): each distinct concept / term = one sm-N anchor, format 'English term — one-line Chinese gist'; never lump multiple concepts into one anchor (e.g. 'axioms + random variables + Bayes' must be three anchors, not one); the sm-N count reflects 'every distinct concept', not 'a few themes'; sm-N is the citation currency of bb-teach / bb-track downstream, so granularity must be fine enough to serve them
- assessments page maintenance: gradebook-column-driven page creation (file name = sanitized original assignment name; summary columns Weighted Total/Total and section-registration columns — registration of sections/attendance that is not a knowledge assessment, e.g. Tutorial Section — excluded, no pages); `## Requirements`/`## References` distilled when sources exist (itemized `<a id="req-N">`/`<a id="ref-N">` anchors, sourceless marked 'no separate requirement file'); the raw block mapping registers requirement/reference/submission files (submissions live in cuhksz/bb/<term>/<course>/submissions/; multiple pages may reference the same file); `## Submission`/`## Results` mechanical regions refreshed from grades/submission snapshots (an absent due reserves an explanation slot and raises no alert; with no submission record use the dedicated wording listing three possibilities); always write a log line (type map) afterwards
- attachments proxies: one page per teacher-released non-handout asset (raw_file/raw_sha256), flat; structural facts like TA/grouping get no attachment pages
- Placement criteria (see the injection line)
- Rebuild discipline: the mechanical region is reconciled and overwritten; the accumulation regions (info notes / assessments review) are append-only, rebuilds must not touch them; attachments proxies are whole-page regenerable
- stale handling: assessments results and info basic information carry stale_after; when stale, refresh via a fresh bbcli pull (the agent is the synchronizer); courseware/attachments are purely local reconciliation, no TTL
- Map-first prerequisite: bb-map is the prerequisite for all course tasks (teaching/quiz/review/Q&A) — run full-course mapping before any of them; the mapping is their single basis (sm-N/info/assessments), never raw source or ad-hoc reading — except the teaching-side unmapped-concept fallback (predict location → read raw → parse → propose mapping the concept back as a new sm-N, emergence-based)
- Source citation: raw_path + sm-N are the citation anchors — derived content (notes/reviews/answers) cites its source (courseware/textbook) through them
- Post-write pipeline (mechanical, automatic): python .meta/scripts/pipeline.py index + tags + hot + log + verify (rebuild the derived layer first, then validate — validation closes at the end, avoiding premature false drift reports from the derived zones)
- Derivation out-only: action items → todo, high-value reviews → notes (backlinks to assessments pages) — the todo/notes bridges
<!-- /usage:bb-map -->

<!-- usage:bb -->
- Map-first: enter the domain by first ensuring the target course is fully mapped via bb-map (info/courseware/assessments/attachments) and reading wiki/cuhksz/bb/inbox.md (digest and domain config in one; created when absent — triggered by the bb-map command anchor or agent initiative); refresh flow = fresh-pull announcements + dues → distill and rewrite the digest (dual-source unsubmitted reminders: assignments without submission ∪ grades with due but no attempt) → sort announcements into derivations → log line (type other); staleness follows the same flow (the agent is the synchronizer)
- Pull and placement: courseware → cuhksz/bb/<term>/<course>/ (source-side directory tree preserved); submissions → cuhksz/bb/<term>/<course>/submissions/; pulled artifacts append-only, never overwritten; changed files with the same name re-pulled via --refresh and landed as new files with a content-hash suffix (old files kept = revision history); the notes zone notes/ is a two-regime coexistence: the machine never writes/deletes/renames human notes (reading and analysis are legitimate — fodder for cognition consumption); ai artifacts (origin: ai — teach explanation notes / quiz papers) are placed through their collection channels, append-only, never overwritten; when fetch placement hits a reserved-name conflict, rename on landing and notify
- New term/new course = create the territory directory + identity page (bb block mapping term_id/course_id); bbcli resolution uses directory names directly (--term term name, course-code substring)
- Materialization layering: documents in full; media (video/audio) pointer-based by default, not landed in bb/ — fetch filter flags (--exclude-mime/--exclude-ext/--max-size) in the bbcli skill; unit-page lists register unmaterialized entries, single-fetch on demand via --match
- Announcement triage: no archiving, no pages (truth lives on BB, pull-fresh on demand); assignment changes → assessments mechanical region, exams/rescheduling → info basic information (+ calendar derivation), policies/faculty/grouping → info basic information, action items → todo, resource releases → trigger fetch then discard, high-value long texts → notes emergence with backlinks
- One-way derivation (out-only): action items → todo; course schedules → calendar; high-value conclusions → notes (backlinks to territory pages) — the todo/calendar/notes bridges, format details belong to the bridges
- Privacy and boundaries: grades pulled on demand and presented only, no default projection; roster never pulled; write actions such as submitting assignments never enter this domain
<!-- /usage:bb -->

<!-- usage:trust -->
- When writing a page, write `generated` along the way (block style: `by: agent/<current-model>` / `at: <today>`)
- When a review action happens, append a `verified` event (single line `by: <actor>, at: <date>`), never fabricated to inflate the level
- Reviews are initiated by the user (triggered by human instruction); agents never append verified events on their own
<!-- /usage:trust -->

<!-- usage:index -->
- Post-write rebuild (mechanical, automatic): `python .meta/scripts/pipeline.py index` (index — overflow-offloading scheme, including deletion of obsolete old indexes after merge-back) and the same script's `tags` (tag reverse index); LLMs never hand-write indexes
<!-- /usage:index -->

<!-- usage:hot -->
- Writing entries (mechanical, automatic): `python .meta/scripts/pipeline.py hot <type> "<wikilink + one-sentence essence>"` (type value set same as log, see the log block of the AGENTS injection region); window eviction and truncation are performed by the script
<!-- /usage:hot -->

<!-- usage:log -->
- Writing lines (mechanical, automatic): `python .meta/scripts/pipeline.py log <type> "<one sentence>" [--domain <domain>]` (type value set in the log block of the AGENTS injection region; domain tag = domain-plugin name such as bb/lark/vault, mandatory for in-domain transactions, omitted for framework and native transactions); rolling window and archiving are performed by the script
<!-- /usage:log -->
<!-- cmd-inject:end -->
