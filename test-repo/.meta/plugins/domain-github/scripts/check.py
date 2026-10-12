"""Read-only audit; no network, file mutations or credential discovery."""
from datetime import datetime, timezone


def check(ctx):
    issues = []
    for rel, fm, body in ctx.pages:
        block = fm.get('github')
        if block is None:
            if rel.startswith('github/'):
                issues.append(dict(level='warning', message=f'{rel}: GitHub envelope missing'))
            continue
        if not isinstance(block, dict) or not rel.startswith('github/'):
            issues.append(dict(level='error', message=f'{rel}: invalid GitHub territory/envelope'))
            continue
        host, account, channel, kind = (block.get(k, '') for k in ('host', 'account', 'channel', 'kind'))
        prefix = f'github/{host}/{account}/'
        valid = rel == prefix+f'{channel}-account.md' if kind == 'account' else (
            kind == 'repository' and rel.startswith(prefix+'repos/') and rel.endswith(f'.{channel}.md') and
            len(rel[len(prefix+'repos/'):].split('/')) == 2)
        if not valid or channel not in ('gh', 'connector') or not str(block.get('identity', '')).isdigit():
            issues.append(dict(level='error', message=f'{rel}: path/channel/identity mismatch'))
        try:
            observed, expires = [datetime.fromisoformat(str(block[k]).replace('Z', '+00:00')) for k in ('observed_at', 'expires_at')]
            if observed.tzinfo is None or expires.tzinfo is None or expires <= observed:
                raise ValueError('invalid freshness interval')
            if datetime.now(timezone.utc) >= expires:
                issues.append(dict(level='info', message=f'{rel}: historical GitHub observation; refresh before current-state claims'))
        except (KeyError, TypeError, ValueError):
            issues.append(dict(level='error', message=f'{rel}: invalid observation/expiry timestamps'))
        if '## Snapshot\n' not in body or '\n## Notes\n' not in body:
            issues.append(dict(level='warning', message=f'{rel}: snapshot/notes section missing'))
    return issues
