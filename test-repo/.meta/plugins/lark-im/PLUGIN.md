# lark-im: interpersonal domain

## Design summary

- **Why it exists**: an interpersonal archive layer with lark-cli as its interface — group archives plus person archives. People are anchors of relationships, not roster rows: the wiki stores the **interpersonal landscape** — which groups exist, who one deals with, topic conclusions; it stores no message logs and mirrors no address book
- **Key rulings**:
  - Person archives emergence-based: archived only after a p2p chat, a user naming, or high-frequency interaction — conditions written in the hub policy block; contact resolves, never traverses. The im edition of 'full mapping forbidden'
  - Group archives store key people, not the full roster: the owner always present; the rest are those already archived, wikilinks pointing to person archives
  - Topic records on demand and confirmed: whoever asks, pulls — time window plus threads expanding the reply chains; distilled into a section appended after user confirmation; zero message bodies by default
  - Send, reply, urgent and other write-side operations always require explicit user request
  - Privacy red line: subjective content such as relationship descriptions is instance data, never entering the framework repo or test-repo

## Structure

- `<profile>/im.md`, kind: im — domain hub: frontmatter `im` block mapping = policies, keys such as group-sync, emergence, watch, exclude, values one sentence each; person-archive emergence conditions declared here
- `<profile>/im/chats/<group name>.md`, kind: chat — group archive: frontmatter mechanical section holds the `lark` identity fields, `description` a one-sentence group purpose, `key_members` key people as wikilinks; body accumulation section = topic records, append-only, `## YYYY-MM-DD Topic: X → Result: Y`, written on demand
- `<profile>/im/people/<name>.md`, kind: person — person archive: token = open_id, stable within the app; basics `department` and `position` filled by contact resolution; `chat_id` the p2p chat anchor, one person one archive absorbs the p2p page, absent when no p2p chat; body accumulation section = relationship with me, subjective, append-only converging
- Directory split in two, chats/ and people/; filenames mechanically sanitized — illegal characters, emoji; duplicates get a short token suffix

## Invariants

- Person archives emergence-based: p2p chatted, named by the user (the hub watch list), high-frequency interaction — conditions written in the hub policy block, no archiving of everyone; group participants store no full roster, only key people — the owner always present, the rest those already archived, wikilinks pointing to person archives
- Group archive reconciliation via lark-map: `im +chat-list` full enumeration, token versus page diff, archiving means group-purpose distillation plus key_members starting from the owner, mechanical-section updates, a left group marked `status: deprecated`; people are never enumerated
- Topic records on demand: whoever asks, pulls — time window, contact translating the names, threads expanding the reply chains; distilled into a section **appended after user confirmation**; zero message bodies by default
- Send, reply, urgent and other write-side operations always require explicit user request; lark-map is read-only
- Privacy red line: subjective content such as relationship descriptions is instance data, never entering the framework repo or test-repo; demos use fictional people
- trust lazy-refresh same as the base: TTL default 7 days, overridable on the identity page

## Changelog

- 0.2 (2026-10-06) inject_tier: member — exits the AGENTS.md injection region per the issue #12 layer discipline (exposure: family-root roster line + skill catalog + on-demand manifest reads)

- 0.1 2026-09-19: established — the group/person archive directory split, the emergence regime with policies in the hub, the key-people regime, topics accumulated on demand
