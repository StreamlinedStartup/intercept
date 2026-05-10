---
# intercept-opm3
title: '3-D: predict.py + JSON-RPC handlers in worker.py'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T00:21:36Z
parent: intercept-at4c
blocked_by:
    - intercept-brce
---

Wire prediction into the IPC bridge so Node can call it.

- [x] ml/predict.py: load latest active model, predict_pair(fighter_a_id, fighter_b_id, fight_date) returns {predicted_winner_id, win_prob}
- [x] worker.py extended: ml.train, ml.predict, ml.list_models JSON-RPC handlers
- [x] Existing PythonBridge in packages/shared/src/python-bridge can call them — write a vitest that spawns the bridge, calls ml.list_models, gets a list back
- [x] At this point the Phase 3 slice is closed: end-to-end Python ML callable from Node.

## Summary of Changes

- Added `services/python/ml/predict.py` with latest-model loading, `predict_pair()`, and `list_models()`.
- Extended `services/python/worker.py` with lazy JSON-RPC handlers for `ml.train`, `ml.predict`, and `ml.list_models`.
- Fixed PythonBridge `PYTHONPATH` to point at `services/python`, then added a bridge Vitest that calls `ml.list_models` through the real worker.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q` returned `18 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/shared test -- --runInBand` returned `2 passed`, `20 passed`
- `predict_pair('767755fd74662dbf', '8a8b8c8d8e8f9091', '2026-05-31')` returned `predicted_winner_id='767755fd74662dbf'`, `win_prob=0.6743682026863098`, `model_version='20260510T002020555519Z'`
