# Instance git usage — the minimal contract

> The instance library's git is a snapshot surface for real use — a time machine and an undo button, not a collaboration tool. Usage beyond this minimum is the user's own definition; the framework deliberately does not regulate it. Written 2026-10-13.

## What the framework already records elsewhere

Mechanical facts (install / uninstall / migration / sweep) → the kernel journal; semantic narrative → `wiki/log`; migration state → the migrations ledger. Git adds exactly one thing: **whole-library snapshots**.

## The minimal contract

1. **Positioning**: snapshots of real use — rollback and time travel. Everything beyond (remotes, branches, bundles, whether to rebase) is the user's own; the framework does not regulate it
2. **Snapshot timing**: at transaction close — the agent's duty. A package transaction commits once after validate goes green (mechanical + semantic in one snapshot); a session closes by committing the dirty tree it leaves. No other rhythm is mandated
3. **Message format**: `type: summary` — the same shape as a wiki/log entry (type from the log enumeration: map / save / query / check / plugin / todo / profile / other; optional `[domain]` tag). Git history becomes the mechanical twin of the log
4. **Red lines, exactly three**: credentials and session files never enter git; adding an ignore must sweep already-tracked matches out of tracking; project-domain entities keep their own git — the instance discloses, never hosts
5. **The recovery entrance**: a check-flagged page → `git log -- <page>` (who changed it) → `git checkout -- <page>` (yesterday's truth back)

## One upgrade path, FYI

Pure local (the default) → a `git bundle` file copied elsewhere → a private remote. Before any remote, sweep the sensitive faces (vault/ assets, cuhksz course records — anything you would not hand to a stranger); public remotes are out of the question for an instance.
