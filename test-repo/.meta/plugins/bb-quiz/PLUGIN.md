# bb-quiz: Self-Test Generation

## Design Summary

- **Why it exists**: bb-track's **testing consumption side** — an examination orthogonal to bb-teach's teaching: self-test generation plus grading flowing back, the machine-evidence entrance of the cognition data loop. teach's artifacts are weak evidence; grading is machine evidence; weights in bb-track. A zero-territory pure-workflow plugin, see mechanics section 8; usage routed source-side onto the bb-track command site
- **Key rulings**:
  - the paper is not a course-native object but process material needed for cognition collection — landed in the bb-side material layer's `notes/testing/` subzone, term/course dual dimensions following the domain; no wiki page, no root container. The 2026-10-04 owner redesign: the exams/ container abolished; bb-exam renamed bb-quiz, drawing the line between informal self-tests and the formal exams governed by bb-map assessments
  - align to the sample rather than invent a style: types and the difficulty median follow the sample; without a sample fall back to known assignments, then to user habits; difficulty = cognitive level 1-5, M a soft constraint — the coarse guarantee: unfamiliar leans easy, mastered leans challenging
  - no out-of-scope: the full set = courseware sm-N intersected with the user scope; out-of-scope questions discarded and regenerated — what is tested is in-scope mastery, not breadth
  - the grading feedback loop: the answers page appends `## Grading`, wrong-answer points written back into user.md after confirmation, machine self-test evidence; the paper itself is material, the profile takes only conclusions
  - teaching minutes best-effort: read teach's ai notes to avoid repetition and to emphasize what was just taught — the two collection channels loosely coupled through the material layer
  - language layering (2026-10-04 neutralization batch): stems **source-aligned** — following the sample/known assignments/course materials, a domain plugin's universal discipline; explanations and grading **reader-aligned** — take the annotation key of the language declaration page `wiki/language.md`, page or key absent → session language. The old 'English questions + Chinese explanations' hard-coding removed — international-student instances work with zero changes; cross-domain reads erect no depends (user-profile precedent)

## Structure

- Zero territory of its own, except the papers subzone: papers land in `cuhksz/bb/<term>/<course>/notes/testing/`; one pair per test — `<name>-questions.md` holds the questions (language follows the source), `<name>-answers.md` holds the explanations (language follows the reader config) plus the `## Grading` append region; ai artifacts append-only; a retest issues a new paper, old papers kept, of review value
- Workflow: parse input; read the full knowledge-point set; read the user's cognition; fix types and the difficulty median; read teaching minutes best-effort; select points; generate questions; write explanations; land; grade, after answering; write back

## Invariants

- Types follow the sample — single choice, multiple choice, fill-in, short answer, calculation, proof, etc., never enumerated; difficulty = cognitive level 1-5: remember, understand, apply, analyze, synthesize; the median M aligns to the sample, fallbacks in order being known assignments, user habits. M is an LLM semantic judgment, a soft constraint of three-layer approximate overlap; the effective guarantee granularity: unfamiliar leans easy, mastered leans challenging
- Stem language source-aligned (sample → known assignments → course materials), terminology aligned to the courseware `## Terminology` glossary; explanation and grading language reader-aligned (the language page's annotation key, absent → session)
- Register (audience reading level): answer explanations and grading are written at the first/second-year undergraduate register — intuition before formalism, one concept per step, a concrete example, each term explained at first use, plain prose, "brief" never "obscure" — taken from the language page's register key (absent → program default, AGENTS principle 12)
- No out-of-scope: the full set = courseware sm-N intersected with the user scope; out-of-scope questions discarded and regenerated, unless the user says so — a semantic constraint, self-checked on the generation side, attached-audit warning level
- Explanations mark the knowledge point with an sm-N wikilink; the position is the birth certificate
- Following bb-track: proficiency drives selection and difficulty distribution; conservative tier before stale verification; cold start, i.e. no profile, everything unanchored, uniform question generation
- **Grading feedback**, established in v0.2: after answering, judge per question; the answers page appends `## Grading` — date, per-question correctness, score; wrong-answer points and overall performance written back into user.md's evidence stream after user confirmation, source machine self-test — machine evidence, the significant ones adjusting readings per the convergence discipline; the paper itself is material, not the profile; the profile takes only conclusions
- Teaching minutes best-effort: read notes/ ai notes, origin: ai, teach's deposits — avoid repetition, emphasize what was just taught; silently skip when absent or empty; teach's default artifact is precisely the notes, so dangling links do not arise
- Write boundary: never write bb/ pulled artifacts; never touch human notes or other ai notes in notes/; the papers subzone append-only; user.md write-back via the bb-track contract, after user confirmation
- Privacy: paper and grading content are instance data, never entering the framework repository or test-repo; notes/testing/ is semantically ignored along with the bb/ data zone

## Changelog

- 0.8 (2026-10-07): audience register + map-first + source citation — explanations and grading default to the first/second-year undergraduate register (overridable via the language page's register key, same batch as language v0.4), step 0 ensures the course is fully mapped (same batch as bb v0.11), and each question/answer cites its source via the mapping's raw_path (same batch as bb-map v0.17) (PR #23, collapsed past master's 0.7 inject_tier entry)
- 0.7 (2026-10-06) inject_tier: member — exits the AGENTS.md injection region per the issue #12 layer discipline (exposure: family-root roster line + skill catalog + on-demand manifest reads)

- 0.6 (2026-10-05) fix: the double-path typo in migration replacement wiki/cuhksz/cuhksz/bb/ → wiki/cuhksz/bb/ (first reported on the instance side; the spec's single layer prevails)

- 0.5 (2026-10-05) cuhksz domain migration: paths rewritten, mechanism unchanged

- 0.4 2026-10-04: language neutralization — the 'English questions + Chinese explanations' hard-coding removed: stems source-aligned (sample/known assignments/materials), explanations reader-aligned (the language page's annotation key, absent → session language); same batch as language v0.2
- 0.3 2026-10-04: established usage_routes: [bb-track] — same as bb-teach, usage routed source-side into the hub command
- 0.2 2026-10-04: redesign, renamed and rebuilt from bb-exam v0.1. The exams/ root container abolished, papers landed in cuhksz/bb/<term>/<course>/notes/testing/, the bb v0.7 material layer, the term dimension restored; renamed quiz — informal self-tests, drawing the line against the formal exams governed by bb-map assessments; the grading feedback established, machine evidence entering user.md after confirmation, the loop completed; out-of-scope and field checks lowered to warning; teaching minutes now read notes/ ai notes, best-effort
- 0.1 2026-10-04, under the bb-exam name: established — testing consumption-side plugin plus command plus exams/ container; five requirements landed: type-and-difficulty alignment, terminology consistency, no out-of-scope, explanation backlinks, following the cognition profile
