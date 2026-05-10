---
# intercept-c5rs
title: '4-J: POST /api/predict/train + /admin/predict-train page'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:59:53Z
parent: intercept-di4c
blocked_by:
    - intercept-1ved
---

Admin retrain trigger.

- [x] POST /api/predict/train (header X-Admin-Secret gated, value from env ADMIN_SECRET)
- [x] Calls pythonBridge.call('ml.train'); returns metrics; row inserted in model_versions
- [x] /admin/predict-train page: text input for admin secret (saves to localStorage), 'Train new model' button, polls progress
- [x] On completion: shows new model metrics + top features table
- [x] Admin nav entry hidden behind ?admin=1 query

## Summary of Changes

- Added gated model training job routes under `/api/predict/train`.
- Extended `/admin/predict-train` with admin secret storage, training progress polling, metrics, and top features.
- Added a `?admin=1`-gated sidebar entry and captured browser evidence at `data/smoke/phase4-c5rs-admin-train.png`.

## Verification

- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check --write apps/api/src/routes/predict.ts apps/web/src/app/'(dashboard)'/admin/predict-train/predict-train-content.tsx apps/web/src/components/layout/nav-main.tsx .beans/intercept-c5rs--4-j-post-apipredicttrain-adminpredict-train-page.md`
- `curl -sS -X POST http://localhost:3001/api/predict/train -H 'X-Admin-Secret: codex-smoke'`
- `curl -sS http://localhost:3001/api/predict/train/job/3d4a8eb9-b3e0-495f-b26b-44d3d2278f67 -H 'X-Admin-Secret: codex-smoke'`
- `agent-browser open 'http://localhost:3000/admin/predict-train?admin=1'`
- `agent-browser wait --text 'Training complete'`
- `agent-browser wait --text 'coming_off_loss_b'`
- `agent-browser screenshot data/smoke/phase4-c5rs-admin-train.png`
