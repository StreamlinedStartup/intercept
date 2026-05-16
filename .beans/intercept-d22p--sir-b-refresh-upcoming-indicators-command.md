---
# intercept-d22p
title: 'SIR-B: Refresh upcoming indicators command'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:58:09Z
updated_at: 2026-05-16T14:04:46Z
parent: intercept-qh8w
blocked_by:
    - intercept-vv4w
---

Build a repeatable command/job that materializes report-only indicators for upcoming fights.

Acceptance criteria:
- [x] Load upcoming fights from the existing synced/cached fight data path.
- [x] Skip fights without current fighter backfill and record skip reasons.
- [x] Run existing prediction + Over 2.5 indicator logic without retraining.
- [x] Load matched no-vig OVERUNDER_2.5 prop market consensus and compute edge.
- [x] Upsert indicator snapshots idempotently.
- [x] Print a concise summary: scanned, written, skipped, missing props, errors.

## Summary of Changes

- Added `ml.refresh_market_indicators` plus `pnpm --filter @interceptor/db refresh:market-indicators` for repeatable upcoming fight indicator refreshes.
- The command reads synced upcoming fights from Postgres, skips non-current fighter backfill with reasons, runs the frozen Over 2.5 report-only indicator, merges no-vig `OVERUNDER_2.5` consensus, and upserts snapshots.
- Verified focused Python tests and a live local DB refresh: 53 scanned, 47 written, 6 skipped, 47 missing props, 0 errors; a second run held the table at 47 rows.
