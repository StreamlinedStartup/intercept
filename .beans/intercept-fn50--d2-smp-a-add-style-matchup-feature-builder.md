---
# intercept-fn50
title: 'D2-SMP-A: Add style matchup feature builder'
status: completed
type: task
priority: high
created_at: 2026-05-12T23:02:17Z
updated_at: 2026-05-12T23:04:57Z
parent: intercept-ovvb
---

Implement style_matchup_pressure_v1 feature construction using only existing pre-fight DB stats.

Acceptance:
- [x] Adds report-only style matchup pressure fields.
- [x] Leaves production prediction/model_versions writes untouched.
- [x] Covers feature behavior with focused pytest tests.


## Summary of Changes

- Added a report-only style matchup pressure feature builder from existing point-in-time career stats.
- Extended the market harness feature contract for production_plus_style_matchup_pressure without changing production FEATURE_NAMES.
- Added focused DB-backed feature and harness alignment tests.

## Verification

- PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/features.py services/python/ml/experiment_harness.py
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_ml.py services/python/test_experiment_harness.py -q => 30 passed
