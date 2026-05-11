---
# intercept-7rpz
title: Write digestible model_scope doc
status: completed
type: task
priority: normal
created_at: 2026-05-11T00:13:37Z
updated_at: 2026-05-11T00:16:01Z
parent: intercept-lvvl
---

Create docs/model_scope.md explaining the model purpose, input data, current feature groups, how predictions are ranked/interpreted, what contributing_features means, and a plain-English backtesting plan.

## Summary of Changes

- Added `docs/model_scope.md` with a non-statistical explanation of the XGBoost predictor, point-in-time feature construction, current feature groups, model-level feature importance, per-prediction contributions, odds edge, and backtesting options.
- Included the latest local model snapshot and top feature rankings from `model_versions`.

## Verification

- Reviewed `services/python/ml/features.py`, `services/python/ml/train.py`, `services/python/ml/predict.py`, and `apps/api/src/routes/predict.ts` to align the doc with implementation.
- Queried the latest `model_versions` row from local Postgres for current metrics and feature-importance values.
