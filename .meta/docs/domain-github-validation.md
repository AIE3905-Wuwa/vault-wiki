# GitHub state domain validation

The first version saves selected GitHub/gh observations so descriptive queries can reuse local context. It does not make authentication permanent or turn cached permissions into authorization.

## Implemented surface

| Artifact | Responsibility |
| --- | --- |
| `.meta/plugins/domain-github/PLUGIN.yaml` | Domain dependencies, field ownership and projected usage/check contracts |
| `.meta/plugins/domain-github/PLUGIN.md` | Identity, channel, TTL, storage and reconciliation decisions |
| `.meta/plugins/domain-github/scripts/state.py` | Official gh read-only collection, sanitized Markdown snapshots and strictly offline reads |
| `.meta/plugins/domain-github/scripts/check.py` | Local envelope, territory and freshness audit |
| `.meta/command/github-state/SKILL.md` | Agent discovery and operational workflow |
| Generated projections and test-repo mirrors | Kernel-owned deployment artifacts |

## Validation on 2026-10-12

- A real authenticated gh session collected account identity, organization memberships, gh runtime and one explicitly requested repository; the local Markdown round trip preserved the relevant membership and permission facts. Real identities, paths and snapshots are kept only in the ignored sandbox, not this report.
- Offline reading was exercised with gh invocation disabled: fresh pages remained usable and no network call occurred. Expired pages were marked historical.
- Focused local checks covered preservation of human Notes, conflicting numeric identity, wrong active account, failed API collection, an account switch during collection, invalid path components and suppressed raw failure output.
- Kernel validation/convergence, plugin audit and derived-page verification were run. Read-only source queries do not establish permission to push, merge or change repository settings.

## Boundaries

The automated collector is gh-only. Connector snapshots have an agent recording contract with independent channel provenance; no connector cache integration is claimed tested. Issue/PR/CI state, organization-wide crawling, concurrent writers and scheduled refresh are outside v0.1. Each page is atomically replaced after all collection succeeds, but multi-page writes and the derived pipeline are not a filesystem transaction; interruption requires inspection and a retry. No write operation against GitHub was tested or performed.

## Reproduction in a deployment instance

From an instance with the framework and this plugin deployed, run kernel `all`, then:

```text
python .meta/plugins/domain-github/scripts/state.py refresh --host github.com --account LOGIN --repo OWNER/REPO
python .meta/plugins/domain-github/scripts/state.py show --host github.com --account LOGIN --repo OWNER/REPO
python .meta/scripts/wiki_plugin_kernel.py audit domain-github
python .meta/scripts/pipeline.py verify
```

The refresh requires an already-authenticated official gh; use `--gh PATH` if necessary. Show is offline. The human performs any needed login. Do not place personal snapshots in framework history. After a simulated failed refresh, compare snapshot bytes/expiry to the prior version; they must be unchanged. Add a Notes paragraph, refresh successfully and confirm it remains. Repository rules still require only explicit development-file paths in commits.
