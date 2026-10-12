# lark: external domain base

## Design summary

- **Why it exists**: external domain base — a domain instance, pointers as the landing strategy. The wiki's proxied objects extend from the local vault out to CLI-reachable external systems. Establishes the 'pointer page': the token is the identity proof, mirroring mapping's path-plus-hash proof; freshness goes to the trust layer, staleness drives the agent to pull fresh, mechanical syncing stays deferred
- **Key rulings**:
  - The base carries no domain knowledge: it establishes only the profile abstraction and territory discipline — one profile per enterprise, living under `wiki/lark/<profile>/`; domain plugins such as docs and im expand in parallel under any profile — the base pattern for in-domain plugin families, see mechanics section 8
  - Pointers land without materialization — options abandoned across four rounds of convergence: vault storage, daemon scheduled syncing, per-profile segmented embedding. The truth stays in lark, locally only projections; the agent is the synchronizer
  - Territory pages take two forms, from 0.2: pointer pages fully regenerable, frontmatter mechanical fields overwritable, precious content distilled into notes; archive pages partitioned — frontmatter mechanical section maintained by reconciliation, body accumulation section append-only, treated like notes. Page form is governed by the domain plugins; the architectural premise for the im domain's archive pages
  - Trust ceiling machine-confirmed, TTL default 7 days, overridable on the identity page; resources gone → mark deprecated, never delete
  - CLI discipline: `--profile` always carried; auth checked live, never written to disk; before entering a new domain, `skills read` comes first

## Structure

- `wiki/lark/<profile>/` — one directory per enterprise; directory name = `lark-cli --profile` name, mechanical correspondence, agent calls must always carry it
- `<profile>/profile.md`, kind: profile — identity page: one sentence, which domains are enabled (a domain hub page being present means enabled), TTL override
- A new profile = create the directory plus the identity page; all active domain plugins cover it automatically. Territory disclosure goes through the index derived chain, progressive disclosure, zero new special pages at the wiki root

## Invariants

- Pointer page `type: lark` plus `lark` block mapping — profile, kind, token, url; token one-to-one with the page, the token is the identity proof; renaming relies on title plus token matching
- Trust ceiling machine-confirmed: `stale_after` = pull date + TTL, default 7 days, overridable on the identity page; check stale before use — when stale, pull fresh with `--profile` to refresh — the agent is the synchronizer
- Resources gone → mark `status: deprecated`, never delete
- Territory pages take two forms, from 0.2: **pointer pages** fully regenerable — frontmatter mechanical fields overwritable, precious content distilled into notes, not kept on pointer pages; **archive pages** partitioned — frontmatter mechanical section maintained by reconciliation, body accumulation section append-only, treated like notes; page form is governed by the domain plugins
- CLI discipline: `--profile` always carried; auth state checked live, never written to disk; before entering a new domain, `lark-cli skills read <domain>` comes first
- Names lowercase ASCII, directories and pages alike

## Changelog

- 0.5 (2026-10-06) inject line compressed to pointer density (issue #12 layer discipline) (family roster duty added) — procedural detail lives in usage / PLUGIN.md / skills- 0.4 2026-10-02: global-domain batch one — attach the mandatory log bridge edge; constitution principle 11, kernel verifies completeness
- 0.3 2026-09-22: domainization — depends adds domain; external-domain-base positioning means pointers land without materialization; territory conventions unchanged; contract in the domain plugin
- 0.2 2026-09-19: establish the two-form partitioning of archive pages — frontmatter mechanical section, body accumulation section append-only; the architectural premise for the im domain's archive pages; pointer page semantics unchanged
- 0.1 2026-09-19: established — four rounds of design convergence: pointer-only, abandoning vault storage; profile-first segmentation; trust lazy refresh replacing the daemon; base and domain plugins split into families with the base owning the abstraction, domain plugins serving in parallel
