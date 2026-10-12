# cuhksz: CUHK-SZ School Domain

## Design Summary

- **Why it exists**: a student's complete picture at one school = enrollment identity (sis) + course operations (bb) + institutional rules (registry); the three share one identity source (the student ID) and one unified authentication (STS ADFS — bb-cli/sis-cli verified to share it in practice). The domain's mission is 'the complete adaptation of one class of external sources', and a school is exactly that class — bb and sis are subsystems inside the domain, not parallel domains, aligned with the lark precedent (enterprise base + docs/im/calendar subdomain family). This plugin is the domain base: it only establishes the answers to the six contract questions and the identity proof, holding no content
- **Key rulings**:
  - 2026-10-05 owner ruling: bb demoted from an independent domain **to an in-domain plugin family** — migration cost is lowest at the single-term data point; umbrella-domain attachment (a domain hanging off a domain) was rejected as semantically fractured
  - the bb family's five plugins **keep their original names without a prefix** (bb, bb-map...) — a full-chain rename (manifest/command/skill/changelog) yields nothing; 'structure is specified by each plugin', the naming convention is not mandatory
  - the domain root holds only the identity page and subsystem navigation; digests belong to each subdomain (bb inbox / sis inbox) — avoiding double-layer maintenance
  - personal official PDFs (certificate of enrollment / unofficial transcript) land in `cuhksz/sis/` as in-domain materialization (2026-10-05 owner ruling revision): when a domain has its own self-standing container, materialization lands inside the domain; vault is only the fallback for containerless domains — the old vault route was inertia from the device precedent (no container), inapplicable once cuhksz has a container; not into registry (an institutional-document zone)
- **Rejected alternatives**: the cuhksz-vs-sis naming dispute — the domain takes cuhksz (school domain; sources go beyond SIS); bb umbrella-domain attachment — a domain hanging off a domain is semantically odd; prefixing and renaming the bb family — a rename explosion

## Structure

- Data zone `cuhksz/` (root container): `bb/` (course operations workspace, governed by the bb domain plugin) + `sis/` (official personal document materialization zone, governed by the sis domain plugin — receives only school-issued enrollment documents, not general data) + `registry/` (academic regulations materialization zone, governed by the registry domain plugin)
- Territory `wiki/cuhksz/`: `identity.md` (domain declaration page) + `bb/` + `sis/` + `registry/` (each governed by its domain plugin)
- Identity proof: the `sis` block mapping of identity.md (student_id/college/school/major/admitted/status) is one-to-one with the connector identity; data source is the sis-cli transcript

## Invariants

- Six contract questions: external territory is the cuhk.edu.cn school-system family; landing = two-sided directories (data zone + territory); identity proof = the identity.md sis block mapping; territory is wiki/cuhksz/; write model belongs to each subsystem (bb process container / sis read-only querying / registry append-only materialization); trust model belongs to each subsystem, identity page machine-confirmed
- Intra-domain cross-references are bridge-exempt: subsystem plugins reading and writing each other (sis grades → bb-track evidence stream) is direct intra-domain reference, not through a principle-11 bridge; cross-domain derivation (todo/calendar/notes/cognition bridge) still goes through bridges
- Domain discoverability: identity.md is the declaration page (type: cuhksz)
- Privacy red line: enrollment identity data is instance data and never enters the framework repository; identity.md is created in the instance library

## Changelog

- 0.3 (2026-10-06) inject line compressed to pointer density (issue #12 layer discipline) (family roster duty added) — procedural detail lives in usage / PLUGIN.md / skills- 0.2 (2026-10-05) personal official documents materialized in-domain instead (cuhksz/sis/, owner ruling): the landing criterion fixed as 'when a domain has its own self-standing container, materialization lands in-domain; vault is the fallback for containerless domains'
- 0.1 (2026-10-05) established: domain base; the bb family's five plugins attached and migrated in (wiki/bb/ → wiki/cuhksz/bb/, bb/ → cuhksz/bb/); sis/registry subdomains first established
