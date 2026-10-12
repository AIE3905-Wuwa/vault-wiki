---
name: bb-quiz
owner: bb-quiz
consumes: [bb-quiz, bb-map, bb-track, trust, log]
description: "Question self-testing: read the bb-track cognition profile and courseware knowledge points, generate questions with explanations (question-stem language follows the source, explanation language follows the reader configuration; landed in notes/testing/); after answering, grading flows back into the cognition profile. Triggers on: 出题, 自测, quiz, 生成习题, 考我, quiz me."
---

# bb-quiz: question self-testing

The user specifies a scope (+ optional samples); reading the bb-track cognition profile tells you "which points are rusty and should be tested, which are mastered and can be challenged", and questions with explanations are generated per courseware knowledge points — question-stem language follows the source (samples / known assignments / course materials), explanation language follows the reader (language-page configuration), question type/difficulty align with the samples, knowledge points stay in scope, and explanations backlink the courseware location. Exam papers land in the bb-side material layer (`notes/testing/`, process material, not the profile); after answering, grading flows back into user.md (machine evidence) upon confirmation. Positioning = testing, orthogonal to bb-teach (teaching).

## Scope

Write: cuhksz/bb/<term>/<course>/notes/testing/ (`<name>-questions.md` + `-answers.md` + appended `## Grading`, origin: ai, append-only), log (one post-write line); user.md grading write-back (via the bb-track write contract, after user confirmation)
Read: registry (`.meta/protocol/registry.yaml`, field anchor), courseware (sm-N + terminology), assessments (known assignments), user.md (bb-track cognition profile), notes/ ai notes (best-effort)

## Steps

1. **Parse input**: scope (chapter/unit/sm-N list) + samples (optional) + course location (`<term>/<course>`, omittable for the active term)
2. **Read the full knowledge-point set**: courseware sm-N + `## Terminology` mapping table; take the in-scope subset
3. **Read user cognition**: user.md proficiency/goal layer; when stale use the conservative tier, on cold start treat everything as unanchored
4. **Set question type and difficulty median**: samples → known assignments → user habits (details in the injection region)
5. **[best-effort] Read teaching minutes**: notes/ origin: ai notes — silently skip if absent or empty
6. **Generate questions and write**: `notes/testing/<name>-questions.md` + `-answers.md` (quiz block mapping + origin: ai; the question page contains no answers) + log line + verify
7. **[After answering] grading flows back**: judge question by question → append `## Grading` to the answer page (date + per-question correctness + score) → write back to the user.md evidence stream after user confirmation (machine self-test) → verify

## Prohibitions

- No out-of-scope content (in-scope knowledge points only, unless the user explicitly says otherwise); never write bb/ fetched artifacts; exam papers are append-only, never overwritten; grading never writes user.md without confirmation
- The question page carries no answers/explanations; the answer page carries no full question stems
- Privacy: exam papers and grading content are instance data, never entering the framework repository or test-repo

## Language

Question-stem language follows the source — samples → known assignments → course materials (terminology aligned with the courseware terminology table); explanation and grading language take the annotation key of the language declaration page `wiki/language.md` (a missing page or missing key falls back to the session language); paths and proper nouns keep their original form.

## Parameters

- Scope (chapter/unit/knowledge point; omittable = recent-window knowledge points of the active term)
- Samples (exercises/exam papers, optional)
- Question count (optional; default moderate)

## Injected Section (plugin usage blocks)

> This region is a wiki_plugin_kernel projection: consumes pulls merged with usage_routes source-side routing; disclosure order = owner first, routed blocks in the middle, pulled blocks last (rebuilt by inject / all); handwritten content does not belong here — to change the write-side contract, edit PLUGIN.yaml.

<!-- cmd-inject:start -->
<!-- usage:bb-quiz -->
- Map-first: step 0 = ensure the course is fully mapped (bb-map full); questions and explanations base directly on the mapped sm-N + the `## Terminology` glossary, never on raw source or ad-hoc reading
- Parse input: scope (chapter/unit/sm-N list) + sample (optional); the course is located via the bb directory structure (<term>/<course>, the active term may be omitted)
- Read the full knowledge-point set: courseware sm-N + the `## Terminology` glossary, take the in-scope subset
- Read the user's cognition: user.md proficiency/goal layer/evidence stream; verify stale first (conservative tier before verification), cold start treated as unanchored (discipline in the injection region's bb-track block)
- Fix types and the difficulty median: sample → assessments known assignments → user habits; difficulty = cognitive level 1-5 (remember/understand/apply/analyze/synthesize), median M = the median of the sample's per-question levels (LLM semantic judgment, a soft constraint — the coarse guarantee = unfamiliar leans easy, mastered leans challenging)
- Read teaching minutes (best-effort): notes/ ai notes (origin: ai) — what was recently taught / where the user got stuck — avoiding repetition or emphasizing what was just taught; silently skip when absent or empty
- Select points: in-scope knowledge points covered in the order unfamiliar / unanchored / wrong answers / short-term priorities
- Generate questions: stem language source-aligned (sample → known assignments → course materials), terminology aligned to the courseware glossary, types aligned to the sample, difficulty around M
- Write explanations: reader-aligned language (the language page's annotation key, page or key absent → session language) and the register (audience reading level, default first/second-year undergraduates — intuition before formalism, one concept per step, a concrete example, each term explained at first use, plain prose), each question marked with its knowledge point + sm-N wikilink and citing its source (courseware/textbook) via the mapping's raw_path; grading in the same language and register
- Land: notes/testing/<name>-questions.md + -answers.md (quiz block mapping + origin: ai + generated; the questions page contains no answers); old papers never deleted or overwritten
- Grade (after the user answers): judge per question against the answers page → append `## Grading` on the answers page (date + per-question correctness + score); wrong-answer points and overall performance written back into user.md's evidence stream after user confirmation (source machine self-test) — the significant ones adjust readings per the convergence discipline; the paper itself is material, the profile takes only conclusions
- No out-of-scope: terminology/knowledge points drawn only from in-scope courseware sm-N; out-of-scope questions are discarded and regenerated (unless the user says so; the semantic constraint is self-checked on the generation side)
- Post-write: log line (type other --domain bb) + pipeline.py verify
<!-- /usage:bb-quiz -->

<!-- usage:bb-map -->
- Course information page: create info.md per course (type: bb + bb block mapping term_id/course_id/term_status (active|frozen) + generated/stale_after); the body's `## Basic Information` distills course-policy key points (grading/assessment/faculty/TA/grouping/teaching language/AI policy, itemized `<a id="info-N">` anchors, reading bb/ syllabi and assessment files, missing items marked 'not provided'); 'what happens when' is recorded here, all elements of graded affairs go to assessments pages
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

<!-- usage:bb-track -->
- Map-first: ensure the course is fully mapped (bb-map) before any cognition read/write; the profile anchors directly on the mapped sm-N + evidence, never on raw source or ad-hoc reading
- Profile creation: create user.md on the first significant signal or user instruction (type: bb + generated/updated/stale_after); absence simply means no cognition data — the consumption side degrades gracefully without erroring
- Reading-line anatomy: each line = anchor → status word + recent evidence digest + date; the digest may carry optional facets, open vocabulary — most-recent retrieval outcome (untested/pass/partial/fail or looser words), misconception tag when one is logged (short: what it is confused with, which step broke), confidence marker when self-assessed confidence visibly diverges from evidence (over/under); review counts are derivable from the evidence stream and are not duplicated on the line
- Append evidence: `- MM-DD source (human conversation|machine grades|human note|ai note|human review): assertion → [[backlink]]`; the source vocabulary is open; retrieval-type evidence additionally notes the hint rung — unaided / after hint / partial (the validated signal separating real learning from answer-copying)
- Converge readings (tier-move rules): new evidence arrives → rewrite the reading line (the new value replaces the old, the line keeps a recent evidence digest + date + facets); the evidence stream is untouched; rises to proficient/mastered require retrieval-type evidence — machine self-test pass, independent application, teach-back success; conversation-only evidence caps at familiar unless the human explicitly asserts higher (recorded per its human weight, the divergence facet stays until a retrieval event lands); hint-assisted successes weigh less than unaided ones; a single event never moves a full tier — majority evidence or one human assertion does
- Computed views (consumption-side, never landed): gap = courseware's full knowledge-point set − the anchored set; retention-risk = last-activity age measured against an expanding-interval heuristic (roughly 1/3/7/21-day expansion, reset short on a failed recall) plus assessment proximity read from info; weakness = misconception flags + wrong-answer points + confidence-evidence divergence; views are computed at read time from reading-line dates and the evidence stream — no schedule, no statistic is ever persisted
- Collection attention (teach/quiz channels, all through the confirmation gate): misconception content — not just wrong, but confused-with-what and which step broke; hint rung — how much support a success needed; confidence-evidence divergence — claimed mastery without retrieval backing, or visible underconfidence despite passes; prerequisite gaps — the user asks about X but the missing piece is Y → record Y; avoidance/frustration signals — course-level affect belongs to the goal layer, not per-point facts
- Consumption discipline: before teaching/testing/review-type output, read user.md first; when stale, first verify against recent-window evidence or ask; before verification consume at the conservative tier (states downgraded half a tier); serve the computed views (gap / retention-risk / weakness) alongside the readings — teaching decisions consume the views, never recompute their own statistics
- Notes consumption: read the notes/ overview and stage/origin attributes as signals; never modify, delete, or mark stage on their behalf; ai notes are weak evidence only
- Collection channels (bb-teach / bb-quiz, usage projections hang off the bb-track command injection region): explanation deposits = notes/ ai notes (origin: ai, weak evidence); self-test grading = notes/testing/ papers (machine evidence, source marked machine self-test) — both enter the evidence stream after user confirmation and adjust readings per the convergence discipline
- Post-write pipeline: verify; log line (type profile, --domain bb)
- Cognition-bridge registration (user-profile on-demand bridge): at profile creation, if the profile page is present, maintain one line in its `## Domain Cognition` section: `- bb: wiki/cuhksz/bb/<term>/<course>/user.md` (path form wildcarding multiple courses and profiles); if the profile is absent, skip, never create on its behalf (on-demand bridges tolerate absence)
<!-- /usage:bb-track -->

<!-- usage:trust -->
- When writing a page, write `generated` along the way (block style: `by: agent/<current-model>` / `at: <today>`)
- When a review action happens, append a `verified` event (single line `by: <actor>, at: <date>`), never fabricated to inflate the level
- Reviews are initiated by the user (triggered by human instruction); agents never append verified events on their own
<!-- /usage:trust -->

<!-- usage:log -->
- Writing lines (mechanical, automatic): `python .meta/scripts/pipeline.py log <type> "<one sentence>" [--domain <domain>]` (type value set in the log block of the AGENTS injection region; domain tag = domain-plugin name such as bb/lark/vault, mandatory for in-domain transactions, omitted for framework and native transactions); rolling window and archiving are performed by the script
<!-- /usage:log -->
<!-- cmd-inject:end -->
