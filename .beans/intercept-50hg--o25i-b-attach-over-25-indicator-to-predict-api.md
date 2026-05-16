---
# intercept-50hg
title: 'O25I-B: Attach Over 2.5 indicator to predict API'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:21:03Z
updated_at: 2026-05-16T05:26:34Z
parent: intercept-ptdd
blocked_by:
    - intercept-rb6z
---

Acceptance criteria:
- [x] Extend prediction responses with an optional Over 2.5 report-only indicator.
- [x] Load no-vig OVERUNDER_2.5 market probability when available.
- [x] Preserve prediction persistence behavior for winner predictions only; do not write prop indicator rows.

## Summary of Changes

- Extended `GET /api/predict/fight/:id` and `GET /api/predict/event/:id` prediction payloads with `over_2_5_indicator`.
- Added no-vig `OVERUNDER_2.5` market consensus from `historical_prop_odds`.
- Kept `predictions` table persistence limited to winner predictions; prop indicators are response-only.
- Added API tests for no-vig market consensus and report-only indicator merging.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- --runInBand apps/api/src/routes/predict.test.ts`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api typecheck`
