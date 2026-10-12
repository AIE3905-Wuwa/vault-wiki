# Contributing

Dev rules of the vault-wiki framework. The framework repo is a library: no instance data, no run log — the change trail is git history + PRs + issues.

## Roles

- **Three members, all with write access** — develop and experiment
- **Owner holds final say** — repo settings, member permissions and protection rules are owner-only; charter and kernel changes (`.meta/`, `AGENTS`-level contracts) are owner-reviewed
- Everything moves through PRs: **any PR needs 1 approving review to merge** (`enforce_admins` is on — the owner pushes through PRs too; the protection switch itself is the owner's escape hatch for emergency fixes)

## Commit flow

1. Branch off latest master, name it `module/topic` (e.g. `feature/bb-notes`, `kernel/pkg-reconcile`)
2. Small commits, one thing each, message format `模块: 概述`
3. Before opening the PR, self-check: `python .meta/scripts/wiki_plugin_kernel.py all` must pass completely; the diff contains development artifacts only
4. Push the branch, open a PR against master — the standard review channel
5. Kernel/charter PRs: owner reviews. Content/domain PRs: peer review among members
6. After merge the head branch is deleted automatically; every merge is recorded (PR + commit trail)

## Data red lines — never in git

Real course files; grades and submission records; personal privacy; account credentials and sessions; sandbox experiment output. Scan your diff before pushing — if any of the above slipped in, pull it back. Granting an exception for ignored data requires the owner's explicit say-so; nobody edits `.gitignore` to let data through on their own.

`test-repo/` is the sandbox: only the `.meta/` and `.agents/` mirrors are tracked; experiment content stays local and never enters history.

## Version discipline

Read the current state before changing a plugin or connector: versions advance along the changelog — no pre-reserving numbers, no gaps. Conflicts with existing plans get aligned in the group first. Framework-level version is the `.meta/VERSION` anchor + git tag (see [`.meta/docs/packages.md`](.meta/docs/packages.md)); package versions ride their own tags and never lockstep with member plugin versions.

## Packages

Changes to package membership, PKG.yaml, or the plugin layout must keep `kernel validate` green — the roster-vs-closure reconciliation runs as part of it. New domain families land as `domains/<pkg>/` packages (declaration first, code second); see the packages doc for the invariants.

## When something is off

A branch gets rejected: read the reviewer's reason, fix, re-push — the PR updates itself. Disagreeing with a review: comment on the PR or raise it in the group. Unsure whether some data may enter git: ask first, then act.
