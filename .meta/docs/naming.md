# The name

> **OWFA — One Workspace For All (agents).** One canonical expansion, one scope, one address.
> Technical name of the code: `vault-wiki`. Distribution name of the product: `owfa`.

This page exists because a name is a contract with the people who type it. It records what the words commit to, which objections are already answered by the scope, and where the name lives mechanically.

## The line

Use the expansion exactly as written. Do not expand it as *One Wiki For All* or *One Web For All* in any public text — the first is a different (smaller) claim, the second belongs to an unrelated GitHub organization. When the acronym has to stand alone, pair it with the parenthetical once per document, then use `OWFA`.

- 中文：**一个工作区，装下你所有的 agent。**
- 一句话：OWFA gives every agent you use one workspace to re-enter — your assets, your wiki, your instructions — instead of re-introducing yourself every session.
- Agent-facing: "This is an OWFA workspace: `vault/` holds real assets, `wiki/` holds the md world, `.meta/` + `.agents/skills/` are the framework body. Read AGENTS.md, then work from the indexes."

## What each word commits to

**One** — one directory, one place a new session re-enters. Not one app that swallows every tool, and not one vendor account. The unit is a workspace the human owns and every agent reads.

**Workspace** — the outer object: `vault/` + `wiki/` + `AGENTS.md` + the framework body. The wiki is the *inner* markdown world; the workspace is what the user actually owns, moves, backs up, and points agents at. Naming the workspace rather than the wiki is deliberate: the contribution is the re-entry surface, not markdown as a format.

**For all (agents)** — all *your* agents: across harnesses (ZCode, Claude Code, Cursor, dsh…), across sessions, across time. It does **not** mean all people, all data, or a hosted service. The parenthetical is part of the name, not a footnote — it is what keeps the claim true. Humans stay the owner and the audit anchor; agents are the ones that re-enter with zero priors.

The name answers the project's actual starting pain: an agent that must be re-introduced every session. "One workspace for all agents" is that pain inverted.

## Two names, two jobs

| Name | Job | Where it appears |
|---|---|---|
| `vault-wiki` | technical name — what the code is, what the repo and docs call the framework | repository, registry, package repos, kernel docs, existing links |
| `owfa` | distribution name — what a user types and what a registry resolves | npm package, CLI, README first line, install command, templates |

This split is ordinary and load-bearing, not a compromise: descriptive names explain, short handles travel. A name that exists only in slides is a slogan; a name that resolves in a package manager is an address. **OWFA is the address** — `npx owfa init`.

Renaming the repository or the package family is *not* required for the name to be real. If the team later wants a full rename, the distribution identity already exists and the move is mechanical; until then, `vault-wiki` remains accurate as the technical name and no links break.

## The collision, stated once

- The GitHub organization `owfa` is held by an unrelated, dormant organization ("One Web For All"). We do not claim it, link it, or wait for it. It is not needed for install, docs, or identity.
- The npm package `owfa` was free when checked on 2026-10-25. It becomes the namespace the project holds at first publish; until then it is only a plan. Publishing is the claim — every week the naming debate stays open is a week the address can be taken by someone else.
- The repository stays at `AIE3905-Wuwa/vault-wiki`; the registry and `pkg-*` repos are unchanged.
- A dormant GitHub org is not a brand. Ownership is expressed where the name has to resolve: the package manager and the command line.

## What OWFA is not

- Not a SaaS or hosted product; every workspace is local and the framework has no telemetry.
- Not "for all people" and not a claim of access to all data; the scope is *your* workspace and *your* agents.
- Not the GitHub org named `owfa`, and not affiliated with "One Web For All".
- Not a replacement for `vault-wiki` as the technical name.

## Objections, answered

1. **"It overclaims — it sounds like a universal product."**
   The scope is bounded twice: *your* workspace, *your* agents. The docs never say all data or all people. A slogan fails when it cannot be falsified; this one has a mechanical test — install it and see whether a fresh agent re-enters without being re-introduced.

2. **"'Workspace' is vague; the thing is a wiki."**
   The wiki is the medium; the workspace is the owned unit of re-entry. The product's value is that a new session knows where to look, not that files end in `.md`.

3. **"The GitHub org is taken, so the name is not ours."**
   Names are held where they resolve. The org is not a distribution channel for this project; npm is. We hold `owfa` where `npx` reads it, and the repo name stays honest about the code.

4. **"Then we would have to rename the repo and all packages."**
   No. Two names, two jobs (above). This is the `ripgrep`/`rg` pattern: descriptive project, short command.

5. **"It is still just a slogan."**
   It is now the package and the command — `npx owfa init`, `npx owfa upgrade`. That is the difference between a position paper and a channel.

## Where the name is enforced

- `package.json` — `"name": "owfa"`, `"bin": { "owfa": "bin/owfa.js" }`
- `README.md` — first line and the *Name* section
- `templates/AGENTS.template.md` — the identity paragraph a new instance starts from
- `.meta/docs/distribution.md` — the channel's version invariant and release runbook
- `scripts/verify-release.js` — the release gate (package version rides `.meta/VERSION`, tag matches)

The framework's internal identifiers stay `vault-wiki`; nothing in the kernel, plugin IDs, or registry depends on the brand.
