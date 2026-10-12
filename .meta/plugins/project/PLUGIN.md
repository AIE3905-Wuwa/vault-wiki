# project: project containers

## Design summary

- **Why it exists**: a self-standing container domain, a domain instance — **the exemplar of a rigid write-model fork**: a process container needs full read/write; landing it inside vault's append-only discipline would paralyze it. Empirical proof of the domain two-discipline test, see mechanics section 8. A project = a mid-to-long-term undertaking with a goal, stages and completion criteria; the body is the real workspace `projects/<project name>/`. This very repo is a living instance of this form
- **Key rulings**:
  - The wiki discloses, it does not host: the declaration page tells the agent which projects exist; searches involving project content go directly to the `projects/` subtree — zero-translation projection density for an md-native territory
  - Project self-sufficiency: entering the directory yields the full context; the conventional self-description project.md has four sections — goal & context, stages, task lines, decisions append-only. Task lines are not pages, line-level lightweight, light before heavy
  - Declaration versus reality bidirectional diff, the structure precedent's second consumer: drift → warning, disposal belongs to the human
  - Dual boundary: with todo — todo is the agent's working set of delegated tasks, project.md tasks are the persistent decomposition source of truth; with vault — vault stores assets hence append-only, projects store workspaces hence full authority; work that needs to modify existing files goes into projects

## Structure

- `projects/<project name>/` — project workspace; free structure, code, documents and materials all welcome; conventionally carries the self-description `project.md`
- `project.md`, the workspace self-description, not a wiki page: frontmatter kept minimal — title, stage, due optional; stage vocabulary open: planning, in-progress, paused, completed. The body's four sections keep line-level lightweight: goal & context; stages — numbered plus checkboxes plus target dates; tasks `- [ ] one sentence (due YYYY-MM-DD)`, lines not pages; decisions `- date decided X because Y`, append-only
- `wiki/projects.md`, type: project — declaration page: frontmatter `projects` block mapping = project name to one sentence, machine-readable; the body holds cross-cutting remarks

## Invariants

- The wiki discloses, it does not host: project content never enters the wiki, searches involving project content go directly to the `projects/` subtree; the declaration page is the sole wiki-side product
- Declaration versus reality bidirectional diff, the structure precedent: a declared project with no directory → warning; an undeclared directory → warning; disposal belongs to the human
- The todo boundary unchanged: todo is the agent's working set of delegated tasks, `project.md` tasks are the persistent decomposition source of truth
- Completion criteria met → self-description `stage: completed`; the workspace is not deleted, the declaration page may annotate
- The vault boundary: vault stores assets, command side append-only; projects store workspaces, full read/write — work that needs to modify existing files goes into projects, storage and outputs go into vault

## Changelog

- 0.5 (2026-10-06) inject line compressed to pointer density (issue #12 layer discipline) (family roster duty added) — procedural detail lives in usage / PLUGIN.md / skills- 0.4 2026-10-02: global-domain batch one — attach the mandatory trust and log bridge edges; constitution principle 11, kernel verifies completeness
- 0.3 2026-09-22: domainization — depends adds domain, a self-standing container domain; wiki-side declaration-only disclosure = zero-translation projection density for an md-native territory; contract in the domain plugin
- 0.2 2026-09-19: the body leaves the wiki — projects land in the root container `projects/<name>/`, workspaces with full agent read/write; the four-section self-description travels with the project as `project.md`; the wiki side converges to the declaration page plus bidirectional diff, the structure precedent's second consumer; 0.1's `wiki/projects/` territory retired
- 0.1 2026-09-19: established — one project one page four-section regime, open stage vocabulary, the todo boundary, task-line lightweight i.e. the light-before-heavy ruling
