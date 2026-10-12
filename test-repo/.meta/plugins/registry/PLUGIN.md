# registry: Academic Regulations Subdomain

## Design Summary

- **Why it exists**: curriculum schemes, GE/PE/national-condition requirements and other institutional documents decide 'what must be taken, what counts as adequate' — the institutional framework of a degree. The source is the Registry's official site (registry.cuhk.edu.cn), no API, no connector; manual download with materialization + pointer navigation is currently the only route
- **Position in the family**: a subsystem inside the cuhksz domain, peer of bb/sis; one of the dual sources of institutional cross-checking (the institutional source) — the dynamic source being the sis-cli Degree Progress Report (DPR)
- **Key rulings**:
  - **pointers first, materialization on demand** (projection density follows translation cost): fully materializing 40+ majors × multiple cohort batches of PDFs is not worth it — the index page gives full pointers (URLs); only the user's relevant schemes are materialized into the zone
  - institutional documents separated from personal assets: official public PDFs (curriculum schemes) live in cuhksz/registry/; personal official documents (enrollment certificates/transcripts) go through vault — the dividing line is 'public institution vs personal certificate'
  - trust uses human-reviewed + version anchors (document/Senate numbers) instead of TTL: institutional change is caught by the cross-check cadence (semester start + document days), not by expiry
  - PDF domain discipline: hosted at registry.cuhk.edu.cn (the same path on www.cuhk.edu.cn returns 403) — both indexing and downloading use the registry domain
- **Rejected alternatives**: full materialization — with zero translation cost, pointers suffice; crawling the official site automatically — no stable API, manual cross-checking is enough

## Structure

- Materialization zone `cuhksz/registry/`: official-site PDFs flat under original names, append-only; version batches advance (the 2025-26 and 2026-27 editions coexist)
- Territory `wiki/cuhksz/registry/`: the schemes.md index page (college → major → scheme page URLs; page-creation sources /page/20 and the /page/22 family, covering double majors/joint programmes/minors) + proxy pages (registry block mapping + distillation + cross-check records)

## Invariants

- Official-site structure (field-verified 2026-10-05): main portal /page/19 (master table of academic programmes, 5 batches by admission year) + /page/20 (major list) + /page/21 (GE) + /page/22 (handbook index); each major has its own /page/{id} (containing per-year PDF download areas); PDFs under the sites/default/files/ path
- Append-only, never overwritten: new version batches advance, old versions kept (still applicable to past cohorts)
- Cross-check cadence: semester start + Senate document days; pages carry no dates, spot-check by PDF Last-Modified
- trust human-reviewed + the edition version anchor; no stale_after
- Dual-source cross-checking: this zone's institutional provisions (authoritative) + the DPR's dynamic computation (real-time) — conclusions enter notes after confirmation, with backlinks

## Changelog

- 0.2 (2026-10-06) inject_tier: member — exits the AGENTS.md injection region per the issue #12 layer discipline (exposure: family-root roster line + skill catalog + on-demand manifest reads)

- 0.1 (2026-10-05) established: first established with the cuhksz domain; the university-wide 9-college + double-major/joint/minor pointer list completed by field verification on the official site (42 major pages verified one by one)
