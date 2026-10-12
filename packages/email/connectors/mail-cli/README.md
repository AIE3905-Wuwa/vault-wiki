# mail-cli

Connector for the wiki email domain (multi-provider: Microsoft Graph / Gmail API / IMAP), OAuth2 device flow or authorization-code login. Contract: `.meta/plugins/email/`.

## Discipline

- Read side is read-only: fetching never implicitly marks messages as read (Graph GET / IMAP `BODY.PEEK`), never moves, archives, or deletes
- Credentials stay on the local machine in `~/.config/mail-cli/` (0600), never enter any repo; the GCP OAuth client likewise stays local only, in `gcp.json`
- Send policy gate (see below): send-type operations are governed at the connector layer by a manually configured policy

## Usage

`--account` is the plugin-contract account (= `wiki/email/<account>/` directory name = profile name).

```
mail-cli auth start  --account <name> [--provider graph|gmail] [--send]  # device flow (graph) / loopback (gmail); graph by default requests only the Mail.Read read-only scope (the read-only consent surface usually needs no admin approval), --send includes write/send
mail-cli auth setup  --account <name> --user <address> --auth-code <code> [--imap-host H] [--smtp-host H]  # imap (e.g. 163)
mail-cli auth status --account <name>
mail-cli profiles                                 # account list (digest-page traversal entry)
mail-cli folders --account <name> [--all]           # folders/labels (imap auto-decodes Chinese UTF-7 folder names)
mail-cli fetch --account <name> [--folder F] [--since D | --days 7] [--from A]
                [--unread] [--headers] [--limit 30] [--next <url>]
mail-cli read --account <name> --id <id> [--text]   # single message body; --text extracts plain text
mail-cli search --account <name> --query <q> [--limit 10]
mail-cli attach ls  --account <name> --id <id>
mail-cli attach get --account <name> --id <id> --att <aid> [--name filename] --dest <dir>
mail-cli draft create --account <name> --to A[,B] [--cc] [--subject S] [--body T | --body-file F]
                       [--html] [--attach path]... [--reply-to <msg-id>]   # replies auto-carry thread headers
mail-cli draft list/show/delete --account <name> --id <draft-id> (list takes no --id)
mail-cli send --account <name> --id <draft-id> [--yes]
```

Output is always single-line JSON. graph/gmail tokens auto-renew on expiry.

## Send policy (manually configured; the connector only reads it)

`~/.config/mail-cli/policy.json`, hand-edited by a human, **absent = deny everything**:

```json
{"<account>": {"send": "deny|confirm|auto", "auto_allow": ["whitelisted addresses"]}}
```

- `deny`: send is always refused (drafts can still be created)
- `confirm`: TTY enter-to-confirm; non-TTY requires `--yes` (= the user has already explicitly agreed in conversation; the agent only executes the consent already given)
- `auto`: pass through directly; with `auto_allow` set, only whitelisted recipients pass, everything else falls back to confirm

## Provider routes and measured pitfalls

| provider | auth | route | known pitfalls |
|---|---|---|---|
| graph (Microsoft/school) | device flow | Graph API v1.0 | `internetMessageHeaders` can only be `$select`ed, not `$expand`ed; school tenants may need admin approval for write permissions |
| gmail | loopback (ssh -L tunnel to receive the callback) | Gmail API v1 | **device flow does not grant Gmail scopes** (invalid_scope, even for TV clients); requires a desktop client + a temporary local HTTP service |
| imap (163 etc.) | authorization code (auth setup) | IMAP4_SSL + SMTP_SSL, standard library | **163 requires sending IMAP ID to self-identify, otherwise select reports Unsafe Login**; Chinese folder names are modified UTF-7 (already decoded); Chinese search terms fall back to client-side filtering (imaplib parameters are ascii-only) |

## Dependencies

None (Python 3 standard library). graph borrows the public Microsoft Graph PowerShell client; gmail needs your own GCP OAuth client (`gcp.json`).

## Changelog

- 0.4 2026-10-05: graph least privilege — default scope narrowed to `Mail.Read offline_access` (reading mail no longer triggers the write/send consent surface and the admin approval that follows), `auth start --send` explicitly requests the broad scope; token records the granted scope (refresh preserves the surface), draft create/delete and send are rejected early under read-only credentials (token_read_only)
- 0.3 2026-10-05: multi-provider (graph/gmail/imap); send policy gate policy.json (deny/confirm/auto + whitelist); full draft suite and send (graph createReply / gmail threadId / imap In-Reply-To thread headers); 163 IMAP ID and UTF-7 folder decoding; gmail loopback auth flow
- 0.2 2026-10-05: multi-account command surface — `--account` aligned with the plugin contract (was `--profile`); added profiles / folders / attach ls·get; fetch gained `--folder/--since/--from/--unread/--headers` and pagination; read gained `--text` plain-text extraction and message-id/references; errors became JSON output
- 0.1 2026-10-05: initial setup — auth / fetch / read / search, single-line JSON, auto-renewal
