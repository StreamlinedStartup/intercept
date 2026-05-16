---
# intercept-sqia
title: 'O25I-C: Surface Over 2.5 indicator in upcoming UI'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:21:03Z
updated_at: 2026-05-16T05:28:02Z
parent: intercept-ptdd
blocked_by:
    - intercept-50hg
---

Acceptance criteria:
- [x] Show the Over 2.5 indicator in fight cards when the candidate fires.
- [x] Show model probability, market probability, edge, and report-only status in compare sheet.
- [x] Keep unavailable/insufficient-market states compact and non-disruptive.

## Summary of Changes

- Added compact `O2.5` fight-card badges when the report-only candidate fires.
- Added an Over 2.5 compare-sheet signal tile with model probability, market probability, edge, and status.
- Kept missing prop market and insufficient training states as compact non-blocking statuses.

## Verification

- `pnpm --filter @interceptor/web typecheck`
- `pnpm --filter @interceptor/web test -- --runInBand`
