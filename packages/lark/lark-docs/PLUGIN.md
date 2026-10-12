# lark-docs: cloud-docs domain

## Design summary

- **Why it exists**: a domain plugin serving the profile abstraction — access to and mapping of Lark cloud docs, i.e. the knowledge base and the drive. Areas-of-interest regime: cloud docs are massive and the user cares only about parts; mapping takes the area of interest as its only entry
- **Key rulings**:
  - Full mapping explicitly forbidden: enumeration serves exactly two things — the hub page's 'structure digest' and area-of-interest resolution; pointer pages land only for objects inside areas of interest
  - The three-piece set: hub, areas of interest, per-area mapping. The `docs.md` hub collects area-of-interest to scope, is instance configuration, human-editable agent-readable; the structure digest is a distillation not a mirror, governed by stale_after; flat tolerance inside area-of-interest subtrees
  - Snapshot sections append selected excerpts, full-text copying forbidden — distillation is the default posture
  - kind vocabulary open, following lark obj_type: docx, wiki, sheet, base, file, etc.

## Structure

- `<profile>/docs.md`, kind: docs — domain hub: frontmatter `docs` block mapping = area of interest to one-sentence scope, instance configuration, human-editable agent-readable; body 'drive structure digest' distilled by the agent — knowledge-space list, top-level directories, one sentence each, with stale_after, not a mirror
- `<profile>/docs/<area-of-interest>/…` — pointer page subtree; one level of areas of interest, flat tolerance below
- kind vocabulary open, following lark obj_type: docx, wiki, sheet, base, file, etc.

## Invariants

- Full mapping forbidden; the area of interest is the only entry to mapping
- The structure digest is a distillation product, expiry via stale_after, no pursuit of real-time parity with the lark side
- Pointer page body starts from a one-line summary; snapshot section `## Snapshot YYYY-MM-DD` appends selected excerpts, full-text copying forbidden
- TTL default 7 days, overridable in profile.md

## Changelog

- 0.2 (2026-10-06) inject_tier: member — exits the AGENTS.md injection region per the issue #12 layer discipline (exposure: family-root roster line + skill catalog + on-demand manifest reads)

- 0.1 2026-09-19: established — the docs.md three-piece set: structure digest, areas of interest, per-area mapping
