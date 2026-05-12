---
# intercept-eols
title: 'D2-OARP: Opponent-adjusted recent performance experiment'
status: completed
type: epic
priority: high
created_at: 2026-05-12T22:47:07Z
updated_at: 2026-05-12T22:54:46Z
parent: intercept-8mw9
---

Implement the smallest report-only research experiment for opponent_adjusted_recent_performance_v1 using existing DB data only. Keep all outputs research_only, do not write model_versions, and evaluate through the existing market experiment harness.


## Summary of Changes

- Implemented opponent_adjusted_recent_performance_v1 as a report-only harness feature family using existing DB data only.
- Evaluated the candidate through the market experiment harness on 40 model-eligible events / 379 fights.
- Kept the result research_only because the best candidate did not clear ROI, log-loss, or Brier gates versus market favorite.

## Verification

- PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/features.py services/python/ml/experiment_harness.py
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_ml.py services/python/test_experiment_harness.py -q => 29 passed
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/opponent-adjusted-recent-performance-v1.json --stdout summary

No HTTP/UI smoke gate was required because this epic added research-only Python harness features and static experiment artifacts, not an HTTP endpoint or UI surface.
