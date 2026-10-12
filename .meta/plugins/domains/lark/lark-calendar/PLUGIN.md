# lark-calendar: lark calendar source

## Design summary

- **Why it exists**: calendar's first source adapter — projects the Lark calendar reachable via lark-cli into the time territory. Bridge-piece form: semantically depends on the two conceptual plugins calendar and lark, declared explicitly in depends, topology the same as mapping versus vault and wiki; no territory of its own, the entire output = **source syntax and pull discipline**
- **Key rulings**:
  - Writes only the month pages' `## Schedule` section, source key at line end: never touches the journal section, never touches frozen month pages — the write boundary narrows to the section level
  - Source syntax `lark/<profile> <calendar_id|primary>`: the profile must be an active wiki/lark/ directory — the source declaration doubles as the reachability proof
  - Daily refresh cadence = a task page registered via the cron bridge (form: session): registration/replay/reconciliation discipline belongs to the cron plugin, failing sources report to the log without blocking other sources — one link in multi-source confluence fault tolerance (0.2 bridge rewording)

## Structure

- Declaration page source syntax: `calendar` block mapping value = `lark/<profile> <calendar_id|primary>` — the profile must be an active `wiki/lark/` directory, i.e. the cli profile name; multiple calendars declared one source each
- Pull: `lark-cli --profile <name> calendar …` — events instance_view by current and next month windows; `+agenda` for a quick view

## Invariants

- Writes only the month pages' `## Schedule` section, source key at line end; never touches the journal section, never frozen month pages
- `--profile` carried throughout; auth checked live; writes follow the calendar usage sync discipline — verify, log, commit
- No pages or fields of its own — source syntax and pull discipline are the entire output

## Changelog

- 0.3 (2026-10-06) inject_tier: member — exits the AGENTS.md injection region per the issue #12 layer discipline (exposure: family-root roster line + skill catalog + on-demand manifest reads)

- 0.2 2026-10-06: attach the cron bridge — the daily-refresh disclosure reworded to task-page registration (form: session), depends adds cron
- 0.1 2026-09-19: established — the lark calendar source joins calendar, the first source adapter; daily refresh = deployment-side cron-scheduled unattended sessions
