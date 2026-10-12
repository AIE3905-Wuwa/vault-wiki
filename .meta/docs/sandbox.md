# Using the sandbox

> Reader: team members who need to run experiments against real data. The authoritative source for sandbox governance red lines is the "User requirements" section of AGENTS.md; this document covers operations. Written 2026-10-04.

## What it is

test-repo is a deployment instance living inside the development repository. The framework trees—`.meta/` and `.agents/`—plus the `AGENTS.md` seed enter git as a whitelisted mirror (core-only after the split; packages install on demand), re-copied wholesale when a root-side batch closes; everything else is the sandbox's own data zone, local only and never committed. The inside of the sandbox is unaware of this project: a session opened at the sandbox root reads the sandbox's own AGENTS.md and skills.

## Enabling it

The sandbox is currently initialized: the AGENTS.md shell carries the injection region, and the four empty data directories exist. To redo it from scratch, three steps:

1. Create the `AGENTS.md` shell: one identity paragraph plus a layout description, and insert the injection region marker block—from `<!-- wiki-inject:start -->` to `<!-- wiki-inject:end -->`, keeping the region header and the explanatory lines inside the block
2. Create four empty directories: `vault/`, `wiki/notes/`, `wiki/sessions/`, `wiki/vault/`
3. Run `python .meta/scripts/wiki_plugin_kernel.py all` at the sandbox root—the injection region is filled from the mirror, and all-green validate makes it a usable instance

## Running experiments

Open an agent session at the sandbox root and use commands normally: map, save, query, check, and the course family all work. The data zone grows naturally—wiki derived pages are built on first run, course data lands on the bb side. Artifacts and derivatives are all to be treated as local temporary material.

## Red lines

Three summarized here; the authoritative source is AGENTS.md:

- Experiment content is never committed. All changes outside the whitelist stay out of git—course data, derived pages, session records, all of it
- Mirror updates go only through root-side re-copy. The sandbox side may modify mirror files for framework experiments, but the next re-copy overwrites them; framework-level changes should be made on a root-side branch and go through review-and-merge
- Watch out for one trap: after touching the sandbox mirror, root-side git will see changes to tracked files—those are not your commit material; restore them and do not casually commit them

## Wrap-up and reset

Conclusions go into conversation reports or docs, never into sandbox archives. Whether experiment data stays or goes is up to you; resetting means deleting everything outside the whitelist—`bb/`, `wiki/`, and `__pycache__` inside the mirror—then walking "Enabling it" once more yields a clean sandbox.

## Mirror sync

Re-copy happens when a root-side batch closes. To trigger it yourself: delete the sandbox's two mirror trees, copy the whole trees in from the root side, then run kernel convergence once more. The sandbox carries no `connectors/` sources, so kernel deploy will report the bb-cli copy as an orphan—the warning is expected; keep the copy, it remains usable.

## Sandbox vs. local

The constitution and the usage guide both say "experiments land in the sandbox or locally". The two are the same thing at two scales: test-repo is the shared sandbox inside the repository, shared by team members and synced via the root-side mirror; opening your own local sandbox is just a quickstart deployment—copy two trees, write the shell, create the directories, run convergence—and the target vault is your choice. One selection criterion: use test-repo when you need to stay in sync with the repository mirror; deploy locally for long-term private use or for something close to your real vault.
