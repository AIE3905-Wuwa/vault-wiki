# domain-github

## Design summary

Agents repeatedly rediscover the GitHub login, organization slug, default branch, repository permissions and gh installation. This domain keeps small, channel-qualified observations in Markdown so a later session can answer those questions locally. GitHub remains the authority; the agent is the synchronizer. Runtime authentication and authorization are never durable guarantees.

The six domain questions:

| Contract | Decision |
| --- | --- |
| External territory | GitHub host APIs, the official gh executable, and a separately authorized GitHub connector |
| Landing strategy | Selected metadata snapshots with source identifiers; no clone, issue archive or external container |
| Identity proof | Host + observing account numeric id; repository numeric id plus full name; channel is part of the key |
| Wiki territory | `wiki/github/<host>/<account>/` |
| Write model | Machine snapshot replaced after successful collection; human Notes preserved verbatim |
| Trust | Machine observation only, explicit UTC observation/expiry, failure preserves history |

## Structure

`gh-account.md` contains identity, organization membership observations and local gh environment. `repos/<owner>/<repo>.gh.md` contains one explicitly requested repository. The account name in every path is the observing principal, not the repository owner. Account and repository IDs guard against username/name reuse. A numeric-ID change is a reconciliation request, not a silent overwrite.

Pages use the existing `source` type to avoid widening the protocol's closed type vocabulary. The `github` field owns identity and freshness. `stale_after` follows the shared date-only contract; `github.expires_at` is authoritative for exact freshness. Ordinary index/tag/log projections remain owned by existing plugins.

The helper writes this minimal shape (placeholders illustrate structure, never imply a real observation):

````text
---
type: source
github:
  host: github.com
  account: LOGIN
  channel: gh
  kind: account
  identity: NUMERIC_ID
  observed_at: UTC_TIMESTAMP
  expires_at: UTC_TIMESTAMP
generated:
  by: process:github-state
  at: YYYY-MM-DD
stale_after: YYYY-MM-DD
---
# GitHub account snapshot

## Snapshot

```json
{ "account": "LOGIN", "id": "NUMERIC_ID" }
```

## Notes

Human-owned notes, preserved exactly on refresh.
````

The Snapshot object is an allowlist, not an API-response dump. Account fields: account, id, host, channel, membership_scope, memberships (organization/id/role/state), runtime (executable/version/machine). Repository fields: id, full_name, default_branch, visibility, archived, fork, parent, permissions (nullable booleans). The collector never reads `gh auth status` output or credential stores. An unsuccessful gh invocation exposes only its exit code, not stderr, which might contain private data.

## Connector observations

An agent may create `connector-account.md` or `repos/<owner>/<repo>.connector.md` using the same frontmatter and Snapshot/Notes boundaries, with `github.channel: connector`. Record only tool-confirmed identity and selected facts; add `observation_scope` in the payload (which connector and which listing was queried). If no numeric identity can be verified, do not create an identity-bearing snapshot yet. Empty installation/organization lists mean no entries were returned within that connector's scope, not that the user has no organizations. Missing permissions stay null. Do not copy credentials, email addresses, arbitrary API bodies or gh runtime into a connector page. Apply the shared write pipeline after an agent-recorded refresh. This v0.1 collector implements gh only; connector recording is a disclosed agent workflow, not a simulated API integration.

## Invariants

- Default TTL is 24 hours. Expiry means historical, not false. Failed refresh leaves observations and Notes intact; no false timestamp renewal.
- A fresh snapshot can answer a descriptive question without network. A request for current status overrides TTL. Cached permissions cannot authorize writes; branch protections and rulesets are not represented by push permission.
- Memberships are collected only for the authenticated user via the membership API. A permission error is not an empty organization list. Repositories are explicit inputs; the collector does not scan every repository in an organization.
- Host/account/owner/name components are validated before filesystem writes; existing malformed pages and conflicting identities are refused. Source text is untrusted data. No issue text or remote instruction is executed.
- Switching accounts/hosts does not overwrite another principal's cache. A machine identifier qualifies runtime observations; a cache copied to another machine is not evidence that gh exists there.
- Refreshing one repo does not renew another repo's expiry. Collection is completed before publication; each page replacement is atomic, but this is not a multi-page filesystem transaction. A write/pipeline failure must be reported as an incomplete refresh, not success.
- Live and test snapshots are instance data, never framework commits. Do not widen gitignore exemptions. No unattended polling, remote mutation or automatic credential persistence.

## Changelog

- 0.1 2026-10-12: establish cache-first GitHub domain, gh collector/offline reader, connector recording contract and local audit.
