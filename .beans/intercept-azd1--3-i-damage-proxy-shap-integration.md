---
# intercept-azd1
title: '3-I: Damage proxy + SHAP integration'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T01:27:50Z
parent: intercept-at4c
blocked_by:
    - intercept-nk4h
---

damage_index per fighter (sig strikes absorbed last 3 fights, weighted heavier for KO/TKO losses). SHAP for explanations.

- [x] features.py adds damage_index_a, damage_index_b
- [x] predict.py adds contributing_features [(name, value, shap)] using xgboost native SHAP
- [x] Re-train + verify SHAP values returned in ml.predict JSON-RPC response

## Summary of Changes

- Added `damage_index_a` and `damage_index_b`, computed from significant strikes absorbed in the last three prior fights with KO/TKO losses weighted 2x.
- Added native XGBoost contribution output to `ml.predict` as `contributing_features: [{name, value, shap}]`, sorted by absolute contribution and JSON-safe for missing values.
- Extended DB-backed pytest coverage to prove damage weighting in the existing weight-class fixture.
- Retrain result: `model_id=20260510T012526889566Z`, `log_loss=0.6213893292960028`, slightly worse than prior `0.6190711182621691`; JSON-RPC `ml.predict` returned SHAP values for model `20260510T012526889566Z`.
