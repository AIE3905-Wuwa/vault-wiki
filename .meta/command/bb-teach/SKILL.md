---
name: bb-teach
owner: bb-teach
consumes: [bb-teach, bb-track]
description: "A question instantly becomes a fine-grained explanation (细粒度讲解): locate courseware knowledge points → read the bb-track cognition profile → explain with two-dimensional scaling by proficiency × difficulty + difficulty-graded length + the professional-term threshold + formula annotations. Triggers on: 讲解, 答疑, 我不懂, 为什么, 这个知识点, 帮我理一理, explain, bb-teach."
---

# bb-teach: question-driven explaining

When the user asks, first read the bb-track cognition profile to know "whether this user is actually rusty or proficient on the relevant knowledge points", then explain with two-dimensional scaling by "user proficiency × concept difficulty" — skim or ask back on what is known, explain thoroughly what is unknown, and proactively align with the user's short-term goals and past wrong answers. This command produces only the fine-grained explanation (细粒度讲解); the coarse summary (粗粒度摘要) is bb-map's courseware page, backlinked not re-produced. Locating, state reading, and write-back are all delegated to existing plugins; this command holds only three unique responsibilities: "teaching decisions + output format + feedback-loop proposal".

## Scope

Write: notes/ ai notes (for significant Q&A, origin: ai, one question per note, append-only), log (one line when a note lands); user.md cognition convergence (via the bb-track write contract, after user confirmation)
Read: registry (`.meta/protocol/registry.yaml`, field anchor), query retrieval (hot/index/tags/grep), courseware / assessments (bb-map pages, sm-N/req-N anchors), user.md (bb-track cognition profile)

## Steps

1. **Locate knowledge points**: question → extract keywords → query layered retrieval (hot→index→grep→read pages) → narrow down via courseware `sm-N` anchors and the `## Terminology` mapping table; hits may span multiple sm-N / multiple courses — list them all
2. **Read user cognition**: read the user.md cognition readings (anchor→status word) + evidence stream + goal layer; if `stale_after` has expired, first verify against recent-window evidence or ask (never misjudge from stale state); gap = courseware full set − anchored set, computed on the spot; wrong-answer point-level conclusions come from assessments reviews
3. **Explain the fine-grained explanation**: output per the scaling rules in the bb-teach block of the injection region — two-dimensional scaling (proficiency × difficulty) + difficulty-graded length + terminology threshold (two guards) + formula-with-parameter annotations + course-level 讲解原则 + wrong-answer/goal injection + anchor backlinks + a closing 知识点联系 section
4. **[Optional] Three-layer feedback loop**: single-turn feedback only adjusts that turn's explanation and is never written to disk; significant Q&A (structured capture value, or the user explicitly says "note this down") lands as an ai note in `cuhksz/bb/<term>/<course>/notes/` (one question per note: question + explanation skeleton + pitfalls + anchor backlinks; origin: ai, `<date>-<topic>.md`, append-only) + a log line (other --domain bb); only significant signals (stable across sessions / spontaneous application / machine verified) propose converging user.md — after confirmation, go through the bb-track write contract + pipeline

## Prohibitions

- Never write `cuhksz/bb/` fetched artifacts; never modify courseware / assessments pure proxy pages; never touch human notes in notes/ (read-only: origin/form/stage as signals); ai notes are append-only, never overwritten
- A single-turn "got it" never writes user.md; user.md is never written without user confirmation; explanation conversations write no log
- Privacy: cognition / explanation content is instance data, never entering the framework repository or test-repo

## Language

Explanation language is reader-aligned — take the teaching key of the language declaration page `wiki/language.md` (a missing page or missing key falls back to the session language); proper nouns and paths keep their original form.

## Parameters

- Question (natural language, may contain course code / knowledge-point name / terminology; omittable = the agent locates relevant courses in the active term)

## Injected Section (plugin usage blocks)

> This region is a wiki_plugin_kernel projection: consumes pulls merged with usage_routes source-side routing; disclosure order = owner first, routed blocks in the middle, pulled blocks last (rebuilt by inject / all); handwritten content does not belong here — to change the write-side contract, edit PLUGIN.yaml.

<!-- cmd-inject:start -->
<!-- usage:bb-teach -->
- Map-first: step 0 = ensure the course is fully mapped (bb-map full); the explanation bases directly on the mapped sm-N anchors + terminology, never on raw source or ad-hoc reading — except the unmapped-concept fallback (predict location → read raw → parse), which never invents content
- Locate: question → extract keywords → layered query retrieval (hot → index → grep → read pages) → narrow via bb-map courseware sm-N anchors and the `## Terminology` glossary — course-agnostic, no course hint needed; list all matches across pages and points; when a concept matches multiple courses, list all candidates with course tags and pick the most likely by context, or ask the user if genuinely ambiguous; when no sm-N hits, run the unmapped-concept fallback
- Unmapped-concept fallback: when the question's concept has no mapped sm-N anchor, predict its likely location from the wiki (course structure — courseware unit titles, `## Terminology`, concept lists, index, info weekly plan); read the relevant raw source via the predicted unit's `raw_path` (extract + parse the original PDF/PPTX, never invent); explain from the parsed source, marking it 'not yet mapped'; then propose mapping the newly-found concept back as a new sm-N (emergence-based, so future questions locate directly)
- Read state: read user.md cognition readings (anchor → status word) + evidence stream + goal layer; verify stale, compute gaps on the fly (courseware full set − anchored set), point-level conclusions from wrong answers — discipline in the injection region's bb-track block
- Division of labor: bb-teach produces only the fine-grained explanation (细粒度讲解); the coarse summary (粗粒度摘要) is bb-map's courseware page (sm-N + gist + terminology + knowledge-point links) — never re-produced, only backlinked
- Two-dimensional scaling (proficiency × difficulty): unanchored/unfamiliar → explain thoroughly; familiar → focus on how to use + pitfalls; proficient → why + pitfalls + cross-point links + open questions; mastered → ask back / challenge questions / guided self-check (no lecturing)
- Difficulty-graded length: simple concepts (complement/union/basic definitions) keep to 1–2 paragraphs, no padding; abstract/hardcore concepts (matrix dimension/convolution/self-attention/exponential family/graphical models/Bayes/entropy/law of large numbers/central limit theorem) expand to 5–10 paragraphs with the full structure — rather longer than under-explained
- Explanation language: reader-aligned — take the teaching key of the language declaration page `wiki/language.md` (page or key absent → session language); cross-domain reads erect no depends, the framework presumes no specific language
- Register (audience reading level): the writing register defaults to first/second-year undergraduates — intuition and motivation before formalism, one concept per step, a concrete example for each abstraction, every term explained at first use (never presumed known), plain short-sentence prose instead of dense bullet-lists, and 'brief' never meaning 'obscure' (a short answer still states the intuition); the register is orthogonal to the two-dimensional scaling (scaling adjusts depth, the register keeps it readable at every tier); take the language page's register key, key absent → the program default
- Terminology threshold (two guards): (1) anchored-set guard — terms allowed to appear = the user's anchored set; global terms not in the anchored set fall back to the language page's terms table, the anchored set wins on conflict; (2) prerequisite guard — prose avoids terms beyond the reader's prerequisite, allowed only when already appeared earlier in this course / covered by high-school + calculus / must be introduced — then explain it on the spot, never presume known; anything else avoided
- Formula-with-parameter annotations: when explaining a theorem / algorithm, give the formula and annotate each parameter's meaning (even if the courseware omits it); each symbol is explained as 'what it computes'
- Course-level 讲解原则: each course may keep `wiki/cuhksz/bb/<term>/<course>/讲解原则.md` recording course-specific explanation requirements (created when absent at the first explanation); priority AGENTS.md > course-level > these global rules
- Goal and wrong-answer injection: hits on time-scoped short-term priorities get one depth tier up, marked 'recent focus', expired ones downgraded; hits on assessments-review wrong-answer points get their pitfalls one tier up and called out
- Output: an inline bold-label skeleton (直觉 intuition / 是什么 what / 为什么 why / 怎么用 how-to-use / 类比 analogy / 易错点 pitfalls / 前置 prerequisites) scaled by the matrix, each knowledge-point title carrying its English original (`中文名（English term）`), each item backlinking courseware sm-N and citing its raw source via the mapping's raw_path; a closing 知识点联系 section lists cross-point links + a closing 术语对照 section (English → Chinese, the unit's important terms, sourced from the courseware page's `## Terminology`)
- Three-tier feedback loop: single-turn feedback (got it / follow-up / wrong answer) only adjusts the current turn's delivery, never landed; significant Q&A (structured deposit value or user-explicit 'note it down') lands as notes/ ai notes — one per question (question + explanation skeleton + pitfalls + anchor backlinks), origin: ai / form: text, named <date>-<topic>.md, append-only never overwritten; only significant signals (stable across sessions / proactive correct application / machine verification) may propose converging user.md — propose = proactively ask at key points (see Agent-triggered confirmation), write-back delegated to the bb-track write contract, after explicit user adoption; a single 'got it' writes nothing, a single 'did not get it' does not mark unfamiliar
- Agent-triggered confirmation (proactive, at key points): at teaching key points — a hardcore concept fully explained, a demonstrated mastery or confusion, a structured-deposit-worthy Q&A — the agent proactively asks the user whether to record the current content into the cognition profile (user.md) and in what form (ai note / evidence-stream assertion / reading status); the agent may offer a specific suggestion (which point, which status word, which form); it writes ONLY after the user explicitly adopts — passive silence and a single 'got it' are never adoption
- Profile posture: verify user.md stale first (conservative tier before verification); absence (cold start) → explain everything thoroughly at the unanchored tier — never refuse to explain for lack of a profile
- log discipline: explanation conversations write no log (no behavioral signals collected); after a significant Q&A lands in notes/, write one line (other --domain bb); cognition convergence goes through the bb-track post-write pipeline (log profile --domain bb + verify)
<!-- /usage:bb-teach -->

<!-- usage:bb-track -->
- Map-first: ensure the course is fully mapped (bb-map) before any cognition read/write; the profile anchors directly on the mapped sm-N + evidence, never on raw source or ad-hoc reading
- Profile creation: create user.md on the first significant signal or user instruction (type: bb + generated/updated/stale_after); absence simply means no cognition data — the consumption side degrades gracefully without erroring
- Append evidence: `- MM-DD source (human conversation|machine grades|human note|ai note|human review): assertion → [[backlink]]`; the source vocabulary is open
- Converge readings: new evidence arrives → rewrite the reading line (the new value replaces the old, the line keeps a recent evidence digest and date); the evidence stream is untouched
- Consumption discipline: before teaching/testing/review-type output, read user.md first; when stale, first verify against recent-window evidence or ask; before verification consume at the conservative tier (states downgraded half a tier); gap analysis = courseware's full knowledge-point set − the anchored set, computed on the fly
- Notes consumption: read the notes/ overview and stage/origin attributes as signals; never modify, delete, or mark stage on their behalf; ai notes are weak evidence only
- Collection channels (bb-teach / bb-quiz, usage projections hang off the bb-track command injection region): explanation deposits = notes/ ai notes (origin: ai, weak evidence); self-test grading = notes/testing/ papers (machine evidence, source marked machine self-test) — both enter the evidence stream after agent-triggered confirmation (the agent proactively asks at teaching key points whether/what-form to record, not passively waiting) and adjust readings per the convergence discipline
- Post-write pipeline: verify; log line (type profile, --domain bb)
- Cognition-bridge registration (user-profile on-demand bridge): at profile creation, if the profile page is present, maintain one line in its `## Domain Cognition` section: `- bb: wiki/cuhksz/bb/<term>/<course>/user.md` (path form wildcarding multiple courses and profiles); if the profile is absent, skip, never create on its behalf (on-demand bridges tolerate absence)
<!-- /usage:bb-track -->
<!-- cmd-inject:end -->
