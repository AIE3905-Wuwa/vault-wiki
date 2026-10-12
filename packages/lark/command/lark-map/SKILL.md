---
name: lark-map
owner: lark
consumes: [lark, lark-docs, lark-im, trust, index, hot, log]
description: "Map Lark-side resources into wiki/lark/ pointer pages: read profiles and domain declarations → enumerate per domain via lark-cli → diff token sets → create/modify/mark deprecated → post-write pipeline. Triggers on: lark-map, 拉取飞书, 同步飞书, lark map."
---

# lark-map: external pointer mapping

Map the Lark resources reachable by lark-cli into `wiki/lark/` territory pages — mapping and understanding are decoupled: pure registration and reconciliation actions (the pointer-page contract and the archive-page zone system are in the lark block of the injection region). Content polishing and distillation are not this command's business (go through save into notes / archive accumulation sections).

## Scope

Write: lark (pointer pages, archive-page mechanical sections, and domain hubs), log, hot, index
Read: registry (`.meta/protocol/registry.yaml`, field and value-set anchor), lark domain-plugin hub pages (docs.md / im.md etc.), lark-cli (enumeration and metadata)

## Steps

1. **Anchor (one-time read)**: read the registry and the `wiki/lark/` directory set (= the profile list) and each `profile.md` (TTL overrides)
2. For each profile × active domain (a domain whose hub page is present is active), run the domain reconciliation:
   - docs domain: read the `docs.md` areas of interest (`docs` block mapping) → enumerate via `lark-cli --profile <name>` (knowledge-space node tree / drive file tree) → resolve the object set of the areas of interest → diff against the `docs/` pointer-page token set → create pages for additions, modify pages for changes (frontmatter mechanical-field overwrite), mark disappearances `status: deprecated`; if the structure digest is stale, re-distill and reset stale_after
   - im domain: read the `im.md` policy (`im` block mapping) → enumerate all chats via `im +chat-list` → diff against the `im/chats/` group-archive token set → create (group-purpose description distillation + key_members starting from the owner) / modify the mechanical section / mark departures `status: deprecated`; **people are never enumerated** (emergence-based, see the lark-im block of the injection region); key_members appends wikilinks for already-archived members
3. **Present the reconciliation preview** (added / changed / deprecated lists) and wait for user confirmation
4. **Post-write pipeline** (deterministic, mechanical and automatic, no prompting): `python .meta/scripts/pipeline.py verify` (post-write self-verification; on failure, go back and fix); then commit per the commit discipline (`映射: <profile>/<domain>`, see the vocabulary in `.meta/protocol/actions.md`)
5. Report: profile / domain / added / changed / deprecated counts

## Prohibitions

- Full mapping is forbidden in the docs domain — enumeration serves only the structure digest and area-of-interest resolution (the lark-docs block of the injection region is authoritative)
- Archive-page body accumulation sections (topic records, relationships) are append-only; this command never writes accumulation sections (on-demand distillation is a separate action and requires user confirmation)
- Write-surface operations such as sending / replying / urgent-marking are not part of this command (always require explicit user instruction)
- CLI calls always carry `--profile`; auth status is queried live and never written to disk
- Never touch notes / sessions or `wiki/vault/` (mapping territory); snapshot excerpts are on demand, full-text copying forbidden

## Language

Output language takes the default key of the language declaration page `wiki/language.md` (a missing page or missing key falls back to the session language); proper nouns and paths keep their original form.

## Parameters

- Profile name (omittable = all); domain name (omittable = all active domains)

## Injected Section (plugin usage blocks)

> This region is a wiki_plugin_kernel projection: consumes pulls merged with usage_routes source-side routing; disclosure order = owner first, routed blocks in the middle, pulled blocks last (rebuilt by inject / all); handwritten content does not belong here — to change the write-side contract, edit PLUGIN.yaml.

<!-- cmd-inject:start -->
<!-- usage:lark -->
- Pointer page registration fields: `type: lark` + `lark` block mapping (profile = containing directory name, kind = object type, token, url) + generated / stale_after
- On a stale pointer page: pull fresh with `--profile` via lark-cli, overwriting the frontmatter mechanical fields (updated / stale_after); snapshot-type body content is appended, never overwritten
- Creating a new profile: create a directory under `wiki/lark/` (name = cli profile name) + `profile.md` (kind: profile, one sentence + optional TTL override); domain plugins automatically cover that directory
- Domain plugin contract: depends lark, iterate all profile directories serving in parallel, constrain only their own kind vocabulary and in-domain page format, never touch the profile abstraction
<!-- /usage:lark -->

<!-- usage:lark-docs -->
- Adding/changing an area of interest: edit the `docs` block mapping of `docs.md` (one-sentence scope: knowledge space name / drive directory / specific object), lark-map or the agent enumerates per area and lands pointer pages; the area of interest is the directory segment of pointer pages
- Structure digest: the wiki-space list + top-level drive tree distilled onto one screen (agent product), stale_after reset on each pull; no pursuit of real-time parity with the lark side
- Pointer page body starts from a one-line summary; snapshot section `## Snapshot YYYY-MM-DD` appends selected excerpts, full-text copying forbidden
- kind vocabulary follows lark obj_type: docx / wiki / sheet / base / file / … (open; look new words up in the registry first)
<!-- /usage:lark-docs -->

<!-- usage:lark-im -->
- Building group archives (lark-map reconciliation): `im +chat-list` full enumeration → token↔page diff → create (group-purpose description distillation + key_members starting from the owner) / update the mechanical section / a left group marked deprecated
- Building person archives (emergence, hand-created when a hub condition hits): contact resolution fills department / position; p2p present → fill the chat_id anchor; the relationship section starts blank
- Topic records (on demand): `chat-messages-list` pulls a time window → contact translates the names, threads expand the reply chains → distilled into a `## YYYY-MM-DD Topic: X → Result: Y` section → appended after user confirmation (accumulation section append-only)
- Relationship updates: append a line per new observation (date + one sentence + evidence wikilink), old assertions never deleted or edited, convergence relies on human adjudication
<!-- /usage:lark-im -->

<!-- usage:trust -->
- When writing a page, write `generated` along the way (block style: `by: agent/<current-model>` / `at: <today>`)
- When a review action happens, append a `verified` event (single line `by: <actor>, at: <date>`), never fabricated to inflate the level
- Reviews are initiated by the user (triggered by human instruction); agents never append verified events on their own
<!-- /usage:trust -->

<!-- usage:index -->
- Post-write rebuild (mechanical, automatic): `python .meta/scripts/pipeline.py index` (index — overflow-offloading scheme, including deletion of obsolete old indexes after merge-back) and the same script's `tags` (tag reverse index); LLMs never hand-write indexes
<!-- /usage:index -->

<!-- usage:hot -->
- Writing entries (mechanical, automatic): `python .meta/scripts/pipeline.py hot <type> "<wikilink + one-sentence essence>"` (type value set same as log, see the log block of the AGENTS injection region); window eviction and truncation are performed by the script
<!-- /usage:hot -->

<!-- usage:log -->
- Writing lines (mechanical, automatic): `python .meta/scripts/pipeline.py log <type> "<one sentence>" [--domain <domain>]` (type value set in the log block of the AGENTS injection region; domain tag = domain-plugin name such as bb/lark/vault, mandatory for in-domain transactions, omitted for framework and native transactions); rolling window and archiving are performed by the script
<!-- /usage:log -->
<!-- cmd-inject:end -->
