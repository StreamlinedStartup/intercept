---
# intercept-pcuc
title: '3-B: features.py — minimal feature set with leakage test (THE SLICE)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T00:15:38Z
parent: intercept-at4c
blocked_by:
    - intercept-y3xz
---

Build the smallest feature set that works end-to-end, with the leakage test in place. Expand later.

Features included in this iteration ONLY:
  - slpm_diff, str_acc_diff, sapm_diff, str_def_diff, td_avg_diff, td_acc_diff, td_def_diff, sub_avg_diff
  - height_diff, reach_diff, age_diff

- [x] services/python/ml/features.py: build_features(fight_id) returns numpy array + label
- [x] All aggregations use event.date < target_fight.date (strict < — no leakage)
- [x] Missing data → NaN (XGBoost handles it)
- [x] services/python/test_ml.py::test_no_leakage — synthesizes a fighter with two fights; computes features as-of fight 1; asserts feature does NOT include data from fight 2
- [x] pytest passes

## Summary of Changes

- Added `services/python/ml/features.py` with the minimal Phase 3 feature row and `FEATURE_NAMES`.
- Aggregated career-to-date stats through `fight_results` joined to target event dates using strict `event.date < target_fight.date`.
- Added `services/python/test_ml.py::test_no_leakage`, which proves a later fight changes later features but stays absent from an earlier target fight.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q`
