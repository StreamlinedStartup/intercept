---
# intercept-1ved
title: '4-A: GET /api/predict/fight/:id (model only, THE SLICE)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T17:56:33Z
parent: intercept-di4c
blocked_by:
    - intercept-elww
---

Smallest predict route: takes a fight_id, calls Python ml.predict, returns the model's pick. No odds yet.

- [x] apps/api/src/routes/predict.ts with GET /api/predict/fight/:id
- [x] Route loads (event.date, fighter_a_id, fighter_b_id) from DB, calls pythonBridge.call('ml.predict', {fighter_a_id, fighter_b_id, fight_date})
- [x] Returns {predicted_winner_id, win_prob, model_version}
- [x] Persist row to predictions table on every call
- [x] curl test: returns valid prediction for any fight_id where both fighters have backfill_state='current'

## Summary of Changes

- Added GET `/api/predict/fight/:id`, loading fight date and both fighters from Postgres, requiring both backfill states to be `current`, calling `ml.predict`, and returning model output plus contributing features.
- Persisted each route call into `predictions` with `edge_pct = null` for the model-only Phase 4 slice.
- Updated API Python bridge startup to prefer `PYTHON_PATH` or the local `services/python/.venv/bin/python`, so the API route can load the Phase 3 ML dependencies in local dev.

Verified:

- `curl -sS http://localhost:3001/api/predict/fight/47b37ff5458e7ee6` returned `predicted_winner_id=476fe566d2df676e`, `win_prob=0.6542974710464478`, `model_version=20260510T012856362940Z`, and `contributing_features`.
- Latest `predictions` row for fight `47b37ff5458e7ee6` has `model_version=20260510T012856362940Z`, `predicted_winner_id=476fe566d2df676e`, and `win_prob=0.6542975`.
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/shared test -- --runInBand`
- `pnpm biome check apps/api/src/bridge.ts apps/api/src/index.ts apps/api/src/routes/predict.ts .beans/intercept-1ved--4-a-get-apipredictfightid-model-only-the-slice.md`
