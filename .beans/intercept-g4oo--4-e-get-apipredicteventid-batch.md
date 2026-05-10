---
# intercept-g4oo
title: '4-E: GET /api/predict/event/:id (batch)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:11:26Z
parent: intercept-di4c
blocked_by:
    - intercept-1ved
---

Predict every fight on a card in one call. Avoids 13 round-trips from the dashboard.

- [x] GET /api/predict/event/:id loops fight rows for that event, returns array of predictions
- [x] Update event-fight-card to use batch endpoint instead of per-row
- [x] Same predictions row write per fight

## Summary of Changes

- Added `GET /api/predict/event/:id` to batch eligible fight predictions for one event and report skipped fights that are not ready.
- Reused the single-fight prediction persistence path so every predicted fight still writes a `predictions` row.
- Updated `/upcoming` fight cards to fetch one event-level prediction batch instead of one request per ready fight row.

Verified:

- `curl -sS http://localhost:3001/api/predict/event/73abb7a5c57fb443` returned 4 predictions and skipped non-current fights for `UFC Fight Night: Allen vs. Costa`.
- Local DB query confirmed `predictions` rows exist for event `73abb7a5c57fb443` (`prediction_count=18` after repeated verification calls).
- `agent-browser snapshot` on `http://localhost:3000/upcoming` showed the batch-fed chips: `68% Arnold Allen`, `65% Daniel Santos`, `65% Malcolm Wellmaker`, `65% Modestas Bukauskas`, and `Backfill required` on non-current rows.
- `agent-browser screenshot data/smoke/phase4-g4oo-batch-predictions.png`
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check --write apps/api/src/routes/predict.ts apps/web/src/app/'(dashboard)'/upcoming/event-fight-card.tsx .beans/intercept-g4oo--4-e-get-apipredicteventid-batch.md`
