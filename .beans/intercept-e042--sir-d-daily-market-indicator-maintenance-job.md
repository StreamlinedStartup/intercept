---
# intercept-e042
title: 'SIR-D: Daily market indicator maintenance job'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:58:19Z
updated_at: 2026-05-16T14:07:36Z
parent: intercept-qh8w
blocked_by:
    - intercept-d22p
---

Define and wire the daily operational refresh cadence for upcoming-market indicators.

Acceptance criteria:
- [x] Daily flow is documented/wired to sync upcoming cards, refresh upcoming fighter backfill, import moneylines/props, canonical-match odds, and run indicator refresh.
- [x] Job is idempotent and records clear per-step failures without silently masking upstream/API problems.
- [x] Operator command is explicit and safe to run manually before any scheduler wiring.
- [x] No retraining or artifact promotion happens in the daily job.

## Summary of Changes

- Added `pnpm ops:market-indicators:daily` as an explicit daily maintenance runner for upcoming-card sync, in-window backfill refresh, moneyline snapshot, optional FightOdds prop import/match, and indicator refresh.
- Documented the operator flow and cron example in `docs/operations/market-indicator-maintenance.md`.
- Kept the job report-only: no retraining, no `model_versions` writes, no artifact promotion, and per-step failure/skipped status in the JSON summary.
