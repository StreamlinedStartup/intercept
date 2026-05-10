---
# intercept-azd1
title: '3-I: Damage proxy + SHAP integration'
status: todo
type: task
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-09T19:02:04Z
parent: intercept-at4c
blocked_by:
    - intercept-nk4h
---

damage_index per fighter (sig strikes absorbed last 3 fights, weighted heavier for KO/TKO losses). SHAP for explanations.

- [ ] features.py adds damage_index_a, damage_index_b
- [ ] predict.py adds contributing_features [(name, value, shap)] using xgboost native SHAP
- [ ] Re-train + verify SHAP values returned in ml.predict JSON-RPC response
