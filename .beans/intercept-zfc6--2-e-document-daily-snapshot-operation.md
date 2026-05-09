---
# intercept-zfc6
title: '2-E: Document daily snapshot operation'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T21:54:03Z
parent: intercept-8gxf
blocked_by:
    - intercept-nbi6
---

No scheduler infra in v1 — just a documented manual cron.

- [x] README.md adds 'Odds snapshots' section: `curl localhost:3001/api/odds-mma/snapshot` daily
- [x] If user wants automation later: cron / systemd timer / GitHub Action are all viable; not built v1
- [x] Document budget math in README: ~30/mo daily snapshots leaves 470 for dashboard/dev

## Summary of Changes

Added an `Odds snapshots` README section documenting the manual daily `curl localhost:3001/api/odds-mma/snapshot` operation, the `ODDS_API_KEY` requirement, the snapshot/unmatched logging behavior, and the 500-request monthly budget math. It explicitly leaves cron, systemd timers, and GitHub Actions as later automation options rather than building scheduler infrastructure in v1.

Verification:
- `git diff --check README.md .beans/intercept-zfc6--2-e-document-daily-snapshot-operation.md`
