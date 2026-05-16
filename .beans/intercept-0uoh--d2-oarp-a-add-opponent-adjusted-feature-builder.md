---
# intercept-0uoh
title: 'D2-OARP-A: Add opponent-adjusted feature builder'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:47:17Z
updated_at: 2026-05-12T22:51:09Z
parent: intercept-eols
---

Implement opponent_adjusted_recent_performance_v1 feature construction using only existing fight/results/stats DB data available before the target fight.

Acceptance:
- [x] Adds point-in-time opponent-adjusted recent performance fields.
- [x] Leaves production prediction/model_versions writes untouched.
- [x] Covers pure feature behavior with focused pytest tests.


## Summary of Changes

- Added a report-only opponent-adjusted recent-performance feature builder using prior fight and prior opponent context only.
- Extended the market harness feature contract for production_plus_opponent_adjusted_recent_performance without changing production FEATURE_NAMES.
- Added focused DB-backed feature and harness alignment tests.

## Verification

- PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/features.py services/python/ml/experiment_harness.py
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_ml.py services/python/test_experiment_harness.py -q => 29 passed
