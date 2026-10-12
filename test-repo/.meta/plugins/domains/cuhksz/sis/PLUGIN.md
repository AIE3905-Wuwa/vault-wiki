# sis: Student Records Subdomain

## Design Summary

- **Why it exists**: student-record information (grades/history/registration/exams/identity) is a student's institutional facts; the source is SIS (PeopleSoft CS), query-and-answer, fully regenerable. With bb (course operations) it belongs to the same school domain and completes the picture: bb runs the process, sis holds the institutional facts
- **Position in the family**: a subsystem inside the cuhksz domain, peer of the bb family; identity data feeds back into the domain-root identity.md; grades, as machine evidence, are directly referenced in-domain by bb-track (no cross-domain bridge — the first payoff of unification)
- **Key rulings**:
  - **query-and-answer, no default projection** (2026-10-05): with the SIS connector present and term interaction working, the wiki side keeps only the digest page — no pre-created enumeration pages like grades.md; detail pages are emergence-based (aligned with 'the architecture does not enumerate')
  - schedule-source gap filled: the 'schedule source and post-class triggers' left missing by the log are supplied here — sis schedule → calendar derivation
  - official-document split rule (2026-10-05 revision): school-issued official personal PDFs (transcripts/certificates/course descriptions) land in `cuhksz/sis/` as in-domain materialization — when a domain has its own self-standing container, materialization lands in-domain; official transcript requests are write operations, never entering the domain
- **Rejected alternatives**: per-term grade archive pages — the data is fully regenerable (the connector re-pulls anytime), archiving only adds maintenance; borrowing vault for materialization — ruled in 0.1, revised in 0.2 (in-domain landing when the domain has a container, owner ruling)

## Structure

- Materialization zone `cuhksz/sis/`: official personal PDFs, append-only (unlike the bb courseware workspace — this zone receives only school-issued enrollment documents)
- Territory `wiki/cuhksz/sis/`: inbox.md digest page (recent window: schedule overview/registration windows/holds/grade snapshot; rows tagged with term; whole page regenerable with short TTL, created when absent) + docs/ proxy pages (raw_file/raw_sha256 pointing into the materialization zone)
- The connector sis-cli (connectors/sis-cli/): ADFS OAuth2 same-source + PeopleSoft PIA adaptation (PS_DEVICEFEATURES shell-breaking, direct psc+PTCNAV component hits, term radio POST), fully read-only

## Invariants

- Read-only red line: write operations — course add/drop/swap, submissions, official requests — never enter the domain (real enrollment consequences); the only POST is the Continue of term selection for querying
- Trust ceiling machine-confirmed; stale_after = pull date + TTL (default 1 day for the digest; date granularity); the agent is the synchronizer
- One-way derivation (out-only): registration windows nearing → todo; schedule/exam arrangements → calendar; term grades → bb-track evidence stream (intra-domain direct reference, after user confirmation); high-value conclusions → notes with backlinks
- Privacy red line: grade and enrollment data are instance data, never entering the framework repository; CLI output stays in the terminal and the conversation
- Credential discipline: stored locally at ~/.sis-cli/, never in the repository

## Changelog

- 0.3 (2026-10-06) inject_tier: member — exits the AGENTS.md injection region per the issue #12 layer discipline (exposure: family-root roster line + skill catalog + on-demand manifest reads)

- 0.2 (2026-10-05) official personal documents switched to in-domain materialization (cuhksz/sis/ + the territory's docs/ proxy pages, owner-ruling revision — the old vault route was inertia from the device containerless precedent)
- 0.1 (2026-10-05) established: first established with the cuhksz domain; the sis-cli v0.2 connector present beforehand
