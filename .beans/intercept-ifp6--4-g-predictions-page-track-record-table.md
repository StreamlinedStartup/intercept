---
# intercept-ifp6
title: '4-G: /predictions page — track record table'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:30:06Z
parent: intercept-di4c
blocked_by:
    - intercept-lmh6
---

First version of the user-facing track-record page.

- [x] apps/web/src/app/(dashboard)/predictions/page.tsx + predictions-content.tsx
- [x] Header: model version + training date + log_loss + brier + accuracy + n_predictions
- [x] Table: last 50 predictions; columns Date / Fighter / Pick / WinProb / Vegas / Result / ✓✗
- [x] Sidebar nav entry 'Predictions' added (CalendarRange or similar icon)
- [x] Empty state when no predictions yet

## Summary of Changes

- Added `/predictions` with model metadata, aggregate metrics, recent prediction rows, and empty/loading/error states.
- Added the Predictions sidebar entry.
- Captured browser smoke evidence at `data/smoke/phase4-ifp6-predictions-page.png`.

## Verification

- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check --write apps/web/src/app/'(dashboard)'/predictions/page.tsx apps/web/src/app/'(dashboard)'/predictions/predictions-content.tsx apps/web/src/components/layout/nav-main.tsx .beans/intercept-ifp6--4-g-predictions-page-track-record-table.md`
- `curl -sS 'http://localhost:3001/api/predict/history?limit=1'`
- `curl -sS 'http://localhost:3001/api/python/ml.list_models' -X POST -H 'Content-Type: application/json' -d '{"limit":1}'`
- `agent-browser open http://localhost:3000/predictions`
- `agent-browser snapshot`
- `agent-browser screenshot data/smoke/phase4-ifp6-predictions-page.png`
