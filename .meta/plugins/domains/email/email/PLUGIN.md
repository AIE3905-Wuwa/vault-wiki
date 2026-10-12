# email: personal mailbox domain

## Design summary

- **Why it exists**: hooking one or more personal mailboxes into the wiki as external sources. The design axis is **velocity-gap filtering between the stream and slow assets**: the inbox is a high-frequency stream, the wiki a low-velocity accumulation layer; this domain is the filter — from the stream it keeps only three slow assets, people, sources and threads, plus one regenerable present-tense digest; everything else is pull-and-discard
- **Key rulings**:
  - The full-mapping ban is this domain's lifeline, not a stylistic preference: the one-page-per-mail temptation is permanent, so restraint is written up front. Retrieval is pull-and-discard; only repeated hits earn an archive, emergence-based, conditions on the account identity page
  - Pointer model: the truth is in the mailbox, a live source; the wiki side holds projections only. Old sent mails are near-immutable, cold sources — snapshot sections may hold full text by value, distillation remains the default posture
  - Person archive token = email address, **global scope** — versus lark open_id's tenant scope; the token's scope decides the page's home; one page per person across accounts
  - The read-only discipline does not vary with trust assumptions: pulls PEEK without implicitly marking read, no moving, no archiving, no deleting — the mailbox is ground the human tills by hand daily; send-type operations always require explicit user request
  - Declaration first, ruled 2026-09-29 at establishment: the contract lives in manifest usage, calendar form, no command no adapter; connector experiments follow

## Structure

- `wiki/email/inbox.md` — unified inbox digest: cross-account distillation, lines tagged with the account, quotas on the identity pages; whole page regenerable, short TTL default 1 day; a single account naturally degrades to a single group
- `wiki/email/people/` — person archives: token = email address, **global scope** — against lark open_id's tenant scope, the token's scope decides the page's home; one page per person across accounts; aliases collect multiple addresses of the same person; register differences — work via account A, personal ties via account B — recorded in the body; body = relationship with me, append-only converging, plus key-thread wikilinks
- `wiki/email/<account>/` — one directory per account; directory name = connector profile name, credentials isolated:
  - `account.md` identity page: address, protocol, pull window, TTL override, emergence conditions, areas-of-interest declaration, alias claiming — instance configuration lives here
  - `threads/` thread archives: mechanical section i.e. the `email` block mapping members = Message-ID list plus last pull date; accumulation section `## date topic→result` append-only, `## Snapshot YYYY-MM-DD` full text by value; default naming `YYYY-MM-DD-<topic>`
  - `sources/` source archives: the governance unit for subscriptions and notifications — types newsletter, bills, notifications, verification-code sources; cadence; latest delivery; reading signals; handling policy
- Single-item pointer pages get no preset directory: created on demand only when some mail is to be wikilinked as evidence from other pages in the vault, token = Message-ID

## Invariants

- Full mapping forbidden: enumeration serves only the digest and area-of-interest resolution; retrieval is pull-and-discard, only repeated hits earn an archive — emergence-based, conditions on the account identity page
- Read-only discipline: pulls PEEK without implicitly marking read, no moving, no archiving, no deleting — the mailbox is ground the human tills by hand daily, the source's original state belongs to the human; such is the write model, unvarying with trust assumptions
- Send red line: drafting allowed; sending, forwarding, moving, deleting always require explicit user request
- One-way derivation out-only: action items go to todo; invitations go to calendar; attachments go to vault — once materialized, origin follows the landing, via the map proxy; high value goes to notes, backlinking the thread archive. The todo, calendar, notes bridges; format authority in each global plugin's usage, projected to the point of consumption; this domain's territory keeps only the three assets plus the digest
- Contract six questions: external territory = the online mailbox, connector-reachable; landing = pointers primarily plus attachments via vault; identity proof = Message-ID one-to-one with the page, thread archives as a members list; territory = `wiki/email/`; write model = source side read-only plus sending by explicit request; trust = TTL lazy refresh, the agent is the synchronizer, ceiling machine-confirmed
- Resources gone — a mail deleted, an account closed — mark status: deprecated, never delete
- Privacy red line: instance data never enters the framework repo or test-repo — constitution-level, an audience question, unvarying with trust assumptions; in-instance privacy boundaries belong to a future privacy plugin

## Changelog

- 0.5 (2026-10-06) inject line compressed to pointer density (issue #12 layer discipline) (family roster duty added) — procedural detail lives in usage / PLUGIN.md / skills- 0.4 2026-10-06: attach the cron bridge — the optional daily-refresh disclosure reworded to task-page registration (form: session), depends adds cron
- 0.3 2026-10-02: global-domain batch two — derivation sentences gain bridge pointers
- 0.2 2026-10-02: global-domain batch one — attach the mandatory log bridge edge; constitution principle 11, kernel verifies completeness
- 0.1 2026-09-29: established — declaration first, the user ruled establish first verify later; no command no adapter, calendar form, the contract lives in manifest usage; connector experiments follow — server-side search capability and thread-header integrity will write back mechanical-section field shapes, e.g. fallback-clustering soft fields
