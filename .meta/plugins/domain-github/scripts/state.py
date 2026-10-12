#!/usr/bin/env python3
"""Allowlisted gh metadata -> Markdown; show is strictly offline. Python stdlib only."""
import argparse
from datetime import datetime, timedelta, timezone
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

NOTES = '\n## Notes\n'
FENCE = re.compile(r'## Snapshot\n\n```json\n(.*?)\n```', re.S)


def component(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value) or value.endswith('.'):
        raise ValueError('Invalid host/account/repository component')
    if value.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(1,10)), *('LPT'+str(i) for i in range(1,10))}:
        raise ValueError('Reserved filesystem component')
    return value.lower()


def repo_name(value):
    pieces = value.split('/')
    if len(pieces) != 2:
        raise ValueError('Repository must be OWNER/REPO')
    return '/'.join(component(p) for p in pieces)


def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('Timestamp must have a timezone')
    return result


def load_page(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n') or NOTES not in text:
        raise ValueError('Malformed existing snapshot; manual reconciliation required')
    header, _ = text[4:].split('\n---\n', 1)
    # Keys emitted by this writer are unique within this narrow envelope.
    fields = dict(re.findall(r'^  (host|account|channel|kind|identity|observed_at|expires_at): (.+)$', header, re.M))
    if len(fields) != 7:
        raise ValueError('Incomplete GitHub snapshot envelope')
    match = FENCE.search(text.split(NOTES, 1)[0])
    if not match:
        raise ValueError('Missing snapshot payload')
    payload = json.loads(match.group(1))
    timestamp(fields['observed_at'])
    if timestamp(fields['expires_at']) <= timestamp(fields['observed_at']):
        raise ValueError('Invalid snapshot freshness interval')
    if not isinstance(payload, dict) or str(payload.get('id')) != fields['identity']:
        raise ValueError('Snapshot payload identity does not match envelope')
    return fields, payload, text.split(NOTES, 1)[1]


def run_gh(executable, args):
    try:
        result = subprocess.run([executable, *args], capture_output=True, text=True,
                                encoding='utf-8', timeout=60, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError('gh unavailable or timed out; cached observations were not refreshed') from exc
    if result.returncode:
        raise ValueError(f'gh failed (exit {result.returncode}); verify network, login and scope; no raw error body retained')
    return result.stdout


def api(executable, host, endpoint, paginate=False):
    args = ['api', '--hostname', host, endpoint]
    if paginate:
        args += ['--paginate', '--slurp']
    data = json.loads(run_gh(executable, args))
    if paginate:
        if not isinstance(data, list) or any(not isinstance(page, list) for page in data):
            raise ValueError('Unexpected paginated API response')
        return [item for page in data for item in page]
    if not isinstance(data, dict):
        raise ValueError('Unexpected API object')
    return data


def numeric_id(value):
    if isinstance(value, bool) or not str(value).isdigit():
        raise ValueError('Missing stable GitHub identity')
    return str(value)


def render(path, host, account, kind, identity, payload, now, hours):
    notes = '\n'
    if path.exists():
        previous, _, notes = load_page(path)
        expected = dict(host=host, account=account, channel='gh', kind=kind, identity=identity)
        if any(previous.get(key) != val for key, val in expected.items()):
            raise ValueError('Snapshot identity changed; reconcile explicitly before replacing it')
    expires = now + timedelta(hours=hours)
    lines = ['---', 'type: source', 'github:']
    fields = dict(host=host, account=account, channel='gh', kind=kind, identity=identity,
                  observed_at=now.isoformat(), expires_at=expires.isoformat())
    lines += [f'  {key}: {val}' for key, val in fields.items()]
    source = payload.get('full_name', account)
    lines += ['sources:', f'  - https://{host}/{source}', 'generated:', '  by: process:github-state', f'  at: {now.date()}',
              f'stale_after: {expires.date()}', '---', f'# GitHub {kind} snapshot', '',
              '## Snapshot', '', '```json', json.dumps(payload, ensure_ascii=True, indent=2), '```']
    return '\n'.join(lines) + '\n' + NOTES + notes


def safe_path(root, relative):
    target = root / relative
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Snapshot path escapes instance root')
    return target


def collect(root, executable, host, account, repos, hours):
    user = api(executable, host, 'user')
    if component(user.get('login', '')) != account:
        raise ValueError('Active gh account differs from --account; no account switch or writes performed')
    uid = numeric_id(user.get('id'))
    members = []
    for item in api(executable, host, 'user/memberships/orgs?per_page=100', paginate=True):
        org = item['organization']
        role, state = item.get('role'), item.get('state')
        if role not in ('admin', 'member') or state not in ('active', 'pending'):
            raise ValueError('Unexpected membership status')
        members.append(dict(organization=component(org['login']), id=numeric_id(org['id']), role=role, state=state))
    version = run_gh(executable, ['--version']).splitlines()[0]
    if not re.fullmatch(r'gh version [0-9][^\r\n]*', version):
        raise ValueError('Unexpected gh version output')
    payload = dict(account=account, id=uid, host=host, channel='gh',
                   membership_scope='authenticated user memberships via gh REST API',
                   memberships=members, runtime=dict(executable=executable, version=version, machine=platform.node()))
    base = Path('wiki/github') / host / account
    records = [(safe_path(root, base/'gh-account.md'), 'account', uid, payload)]
    for name in repos:
        repo = api(executable, host, 'repos/'+name)
        if repo_name(repo.get('full_name', '')) != name:
            raise ValueError('Repository renamed or redirected; reconcile explicitly')
        rid = numeric_id(repo.get('id'))
        perms = repo.get('permissions') or {}
        values = {key: perms.get(key) if isinstance(perms.get(key), bool) else None
                  for key in ('pull', 'push', 'triage', 'maintain', 'admin')}
        parent = repo.get('parent')
        branch = repo.get('default_branch')
        if branch is not None and not isinstance(branch, str):
            raise ValueError('Invalid branch metadata')
        data = dict(id=rid, full_name=name, default_branch=branch,
                    visibility=repo.get('visibility'), archived=repo.get('archived'),
                    fork=repo.get('fork'), parent=repo_name(parent['full_name']) if parent else None,
                    permissions=values)
        records.append((safe_path(root, base/'repos'/(name+'.gh.md')), 'repository', rid, data))
    # Detect a login switch during a multi-request collection before publishing.
    final_user = api(executable, host, 'user')
    if component(final_user.get('login', '')) != account or numeric_id(final_user.get('id')) != uid:
        raise ValueError('Active account changed during refresh; retry under one account')
    now = datetime.now(timezone.utc)
    # Render/validate every old page before touching any, including account-ID checks.
    return [(path, render(path, host, account, kind, ident, data, now, hours))
            for path, kind, ident, data in records]


def publish(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.github-state-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(text)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def pipeline(root, count):
    script = root/'.meta/scripts/pipeline.py'
    for args in (['index'], ['tags'], ['hot', 'other', f'GitHub gh state refreshed ({count} pages).'],
                 ['log', 'other', f'GitHub gh state refreshed ({count} pages).', '--domain', 'domain-github'], ['verify']):
        subprocess.run([sys.executable, '-B', str(script), *args], cwd=root, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['show', 'refresh'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--host', default='github.com')
    parser.add_argument('--account', required=True)
    parser.add_argument('--repo', action='append', default=[])
    parser.add_argument('--gh', default='gh')
    parser.add_argument('--ttl-hours', type=float, default=24)
    args = parser.parse_args(argv)
    try:
        host, account = component(args.host), component(args.account)
        repos = list(dict.fromkeys(repo_name(x) for x in args.repo))
        root = args.root.resolve()
        if args.action == 'show':
            base = Path('wiki/github')/host/account
            paths = [safe_path(root, base/'repos'/(name+'.gh.md')) for name in repos] if repos else [safe_path(root, base/'gh-account.md')]
            for path in paths:
                if not path.exists():
                    print(json.dumps(dict(path=str(path), state='unknown', reason='no cached observation')))
                    continue
                fields, data, _ = load_page(path)
                if fields['host'] != host or fields['account'] != account or fields['channel'] != 'gh':
                    raise ValueError('Cache envelope does not match requested principal/channel')
                if repos and (fields['kind'] != 'repository' or data.get('full_name') not in repos):
                    raise ValueError('Repository payload does not match requested repository')
                if not repos and (fields['kind'] != 'account' or data.get('account') != account):
                    raise ValueError('Account payload does not match requested account')
                fresh = datetime.now(timezone.utc) < timestamp(fields['expires_at'])
                print(json.dumps(dict(path=str(path), state='fresh' if fresh else 'stale', observation=fields, snapshot=data), ensure_ascii=True))
            return 0
        if not math.isfinite(args.ttl_hours) or not 0 < args.ttl_hours <= 168:
            raise ValueError('TTL must be finite and within (0, 168] hours')
        if not (root/'.meta/scripts/pipeline.py').is_file():
            raise ValueError('Instance pipeline not found; deploy the framework before refresh')
        executable = shutil.which(args.gh)
        if not executable:
            raise ValueError('gh executable not found; offline cache remains available')
        for path, text in collect(root, executable, host, account, repos, args.ttl_hours):
            publish(path, text)
        pipeline(root, 1+len(repos))
        print(f'Refreshed {1+len(repos)} gh snapshot(s); authentication was observed only at refresh time.')
        return 0
    except (ValueError, KeyError, TypeError, IndexError, OSError, subprocess.CalledProcessError) as exc:
        # Known errors are deliberately terse; never print API bodies or credentials.
        message = str(exc) if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError) else type(exc).__name__
        print('GitHub state refresh/read did not complete: '+message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
