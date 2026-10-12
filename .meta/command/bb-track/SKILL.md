---
name: bb-track
owner: bb-track
consumes: [bb-track, trust, log]
description: "Cognition profile: read/create/update the learning state in wiki/cuhksz/bb/<term>/<course>/user.md (cognition readings + evidence stream + goal layer), gap/retention-risk/weakness views computed on the spot; the collection channels (bb-teach explaining / bb-quiz self-testing) mount their usage here. Triggers on: 认知档案, 学习状态, 我学得怎么样, user.md, bb-track."
---

# bb-track: cognition profile

The bb domain's cognition hub — each course's user.md is the single profile of "the user's cognitive state on each knowledge point of that course" (convergent readings overwritten in place + append-only evidence stream + goal layer); profile creation is lazy, the term is the boundary. This command manages the profile's read / create / update and gap analysis; the usage projections of the two collection channels (bb-teach explaining and Q&A, bb-quiz question self-testing) are mounted in this command's injection region — teaching and testing artifacts land in the bb-side material layer (notes/), and cognition conclusions are written back into this profile after confirmation.

## Scope

Write: wiki/cuhksz/bb/<term>/<course>/user.md (reading convergence + evidence append, after user confirmation), log (one post-write line)
Read: registry (`.meta/protocol/registry.yaml`, field anchor), courseware (full knowledge-point set for on-the-spot gap computation), assessments (retrospective/grade signals), notes/ (human note attributes + ai notes as weak evidence + testing/ exam grading), profile (domain-cognition registration, when present)

## Steps

1. **Locate and read the profile**: locate the course `<term>/<course>`, read the user.md cognition readings (anchor → status word + optional facets: retrieval outcome / misconception tag / confidence divergence), evidence stream, goal layer — details in the bb-track block of the injection region
2. **Computed views**: gap (courseware full set − anchored set), retention-risk (last-activity age vs expanding-interval heuristic + assessment proximity from info), weakness (misconception flags + wrong-answer points + confidence-evidence divergence) — all computed on the spot, never landed
3. **Create or update**: profile creation is lazy; evidence append (retrieval-type evidence carries the hint rung) and reading convergence (tier-move rules — upper tiers need retrieval-type evidence) follow the bb-track block discipline of the injection region, all after user confirmation
4. **Post-write**: verify plus a log line

## Prohibitions

- Evidence-stream entries are never rewritten or deleted; every reading must have traceable evidence; note stage belongs to the human and is never marked on their behalf
- Computed views (gap / retention-risk / weakness) are never persisted — no schedule, no statistic lands in user.md; review counts are never duplicated onto reading lines (derivable from the stream)
- Never write bb/ fetched artifacts or notes/ (the material layer belongs to the collection channels); never write user.md without confirmation
- Privacy: cognition content is instance data, never entering the framework repository or test-repo

## Language

Output language takes the default key of the language declaration page `wiki/language.md` (a missing page or missing key falls back to the session language); knowledge-point anchors and proper nouns keep their original form.

## Parameters

- Course (omittable = all courses in the active term, or a specified course)
- Action (read profile / views overview / create profile / update readings; omittable = read profile + gap/retention-risk/weakness overview)

## Injected Section (plugin usage blocks)

> This region is a wiki_plugin_kernel projection: consumes pulls merged with usage_routes source-side routing; disclosure order = owner first, routed blocks in the middle, pulled blocks last (rebuilt by inject / all); handwritten content does not belong here — to change the write-side contract, edit PLUGIN.yaml.

<!-- cmd-inject:start -->
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

<!-- usage:bb-teach -->
- Map-first: step 0 = ensure the course is fully mapped (bb-map full); the explanation bases directly on the mapped sm-N anchors + terminology, never on raw source or ad-hoc reading — except the unmapped-concept fallback (predict location → read raw → parse), which never invents content
- Locate: question → extract keywords → layered query retrieval (hot → index → grep → read pages) → narrow via bb-map courseware sm-N anchors and the `## Terminology` glossary — course-agnostic, no course hint needed; list all matches across pages and points; when a concept matches multiple courses, list all candidates with course tags and pick the most likely by context, or ask the user if genuinely ambiguous; when no sm-N hits, run the unmapped-concept fallback
- Unmapped-concept fallback: when the question's concept has no mapped sm-N anchor, predict its likely location from the wiki (course structure — courseware unit titles, `## Terminology`, concept lists, index, info weekly plan); read the relevant raw source via the predicted unit's `raw_path` (extract + parse the original PDF/PPTX, never invent); explain from the parsed source, marking it 'not yet mapped'; then propose mapping the newly-found concept back as a new sm-N (emergence-based, so future questions locate directly)
- Read state: read user.md cognition readings (anchor → status word + facets) + evidence stream + goal layer; verify stale, take the computed views (gap / retention-risk / weakness) — discipline in the injection region's bb-track block
- Division of labor: bb-teach produces only the fine-grained explanation; the coarse summary is bb-map's courseware page (sm-N + gist + terminology + knowledge-point links) — never re-produced, only backlinked
- Retrieval-first gate (testing effect): on familiar-and-above points, open with one recall probe before explaining — pass → step up one tier and touch lightly; fail or stumble → step down and explain targeted (diagnose the broken step, never re-teach wholesale); unanchored/unfamiliar points skip the gate and teach first — testing the unlearned is low-yield
- Mode matrix (proficiency × difficulty): unanchored/hardcore → worked example with annotated steps + prerequisite-chain completion + analogy + numeric example; unfamiliar just-taught → completion problems (partially worked) — fading; familiar → how-to-use + pitfalls, entered through the retrieval-first gate; proficient → why + pitfalls + cross-point links + open questions, worked examples dropped (expertise reversal — examples become noise at high proficiency); mastered → ask-back / challenge questions / guided self-check, no lecturing — when the reading lacks retrieval evidence the ask-back doubles as the calibration probe, a failed probe proposing an overconfidence/misconception note via bb-track, never a unilateral demotion
- Hardcore concept list (difficulty calibration): the mode matrix's 'unanchored hardcore' cell covers concepts like convolution / self-attention / exponential family / graphical models / Bayes / entropy / law of large numbers / central limit theorem — these get the full worked-example structure, 'rather longer than under-explained'; simple definitions (complement/union/basic) stay lean with no padding
- Refutation structure (misconception-flagged points): acknowledge the intuitive model as reasonable → show a case where it visibly fails (counterexample/edge case) → give the correct conception → contrast the two side-by-side; never a mere restatement of the right answer — the coexisting misconception survives restatement; re-test later (consolidation/quiz handoff)
- Hint ladder (problem-type asks): five rungs — (1) what have you tried? (2) name which concept applies, nothing more (3) state the first step without computing (4) structural hint — steps with blanks (5) one fully worked similar example, then the user retries their own; escalate one rung per explicit stuck signal, reset after correct steps; the direct answer is never the escalation — pleading for the answer reaches only the ladder top; graded-assignment final answers are declined, every refusal bundling an alternative path (concept review / similar worked example)
- Turn discipline: one question per turn; the user tries twice before any reveal; low tiers → shorter turns, finer steps (dense exposition only at high tiers); vary the rhythm — explain → probe → apply → explain-back
- Explain-back elicitation: at the close of fresh teaching invite one own-words explanation of why the mechanism works (never a bare 'understood?'); diagnose gaps from the paraphrase; teach-back is the terminal mastery check before any mastered-tier proposal
- Scaffold contingency (in-session, never landed): support up one rung/tier per failure; fade one after two consecutive successes; never jump from full support to none in one move
- Feedback discipline: task/process-level and specific — point at the step that broke and the fix path, never the person; specific praise of what was correct ('you noticed X applies'), never generic; disagreement stated plainly, never unconditional agreement (anti-sycophancy); checks and corrections anchored to the courseware source — uncertain → flagged uncertain, a correct answer never marked wrong without evidence
- Explanation language: reader-aligned — take the teaching key of the language declaration page `wiki/language.md` (page or key absent → session language); cross-domain reads erect no depends, the framework presumes no specific language
- Register (audience reading level): the writing register defaults to first/second-year undergraduates — intuition and motivation before formalism, one concept per step, a concrete example for each abstraction, every term explained at first use (never presumed known), plain short-sentence prose instead of dense bullet-lists, and 'brief' never meaning 'obscure' (a short answer still states the intuition); the register is orthogonal to the mode matrix (the matrix adjusts depth, the register keeps it readable at every tier); take the language page's register key, key absent → the program default
- Terminology threshold: terms allowed to appear = the user's anchored set (not 'appeared earlier in this course'); anything beyond is explained on the spot, never presumed known; global terms not in the anchored set fall back to the language page's terms table, the anchored set wins on conflict
- Formula-with-parameter annotations: when explaining a theorem / algorithm, give the formula and annotate each parameter's meaning (even if the courseware omits it); each symbol is explained as 'what it computes'
- Course-level explanation principles: each course may keep `wiki/cuhksz/bb/<term>/<course>/explanation-principles.md` recording course-specific explanation requirements (created when absent at the first explanation); priority AGENTS.md > course-level > these global rules
- Goal and wrong-answer injection: hits on time-scoped short-term priorities get one depth tier up, marked 'recent focus', expired ones downgraded; hits on assessments-review wrong-answer points or weakness-view misconception flags get their pitfalls one tier up, called out, and taught through the refutation structure
- Output: an inline bold-label skeleton (直觉 intuition / 是什么 what / 为什么 why / 怎么用 how-to-use / 类比 analogy / 易错点 pitfalls / 前置 prerequisites) scaled by the mode matrix — delivered progressively across turns at low tiers (progressive disclosure rather than one dense drop), each knowledge-point title carrying its English original (`中文名（English term）`), each item backlinking courseware sm-N and citing its raw source (courseware/textbook) via the mapping's raw_path; a closing 知识点联系 section lists cross-point links + a closing 术语对照 section (English → Chinese, the unit's important terms, sourced from the courseware page's `## Terminology`)
- Consolidation hook: at explanation end, one line, opt-in — retention-risk points from the computed view get an offer of a quick recap probe now or a bb-quiz mini handoff (scope = today's points + flagged misconceptions); never nagging, silence accepted
- Three-tier feedback loop: single-turn feedback (got it / follow-up / wrong answer) only adjusts the current turn's delivery per the scaffold contingency, never landed; significant Q&A (structured deposit value or user-explicit 'note it down') lands as notes/ ai notes — one per question (question + explanation skeleton + pitfalls + anchor backlinks), origin: ai / form: text, named <date>-<topic>.md, append-only never overwritten; only significant signals (stable across sessions / proactive correct application / machine verification) may propose converging user.md — tier-rise proposals following bb-track's evidence rules (upper tiers need retrieval-type evidence) and carrying the hint-rung signal; write-back delegated to the bb-track write contract, after user confirmation; a single 'got it' writes nothing, a single 'did not get it' does not mark unfamiliar
- Profile posture: verify user.md stale first (conservative tier before verification); absence (cold start) → explain everything thoroughly at the unanchored tier — never refuse to explain for lack of a profile
- log discipline: explanation conversations write no log (no behavioral signals collected); after a significant Q&A lands in notes/, write one line (other --domain bb); cognition convergence goes through the bb-track post-write pipeline (log profile --domain bb + verify)
<!-- /usage:bb-teach -->

<!-- usage:trust -->
- When writing a page, write `generated` along the way (block style: `by: agent/<current-model>` / `at: <today>`)
- When a review action happens, append a `verified` event (single line `by: <actor>, at: <date>`), never fabricated to inflate the level
- Reviews are initiated by the user (triggered by human instruction); agents never append verified events on their own
<!-- /usage:trust -->

<!-- usage:log -->
- Writing lines (mechanical, automatic): `python .meta/scripts/pipeline.py log <type> "<one sentence>" [--domain <domain>]` (type value set in the log block of the AGENTS injection region; domain tag = domain-plugin name such as bb/lark/vault, mandatory for in-domain transactions, omitted for framework and native transactions); rolling window and archiving are performed by the script
<!-- /usage:log -->
<!-- cmd-inject:end -->
