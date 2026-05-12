---
# intercept-dr0p
title: 'D2-EH3-B: Implement cached real-axis runner'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:20:32Z
updated_at: 2026-05-12T22:39:00Z
parent: intercept-8423
blocked_by:
    - intercept-j6ip
---

Acceptance criteria:
- [x] Reuse cached base walk-forward model probabilities for variants that differ only by calibration or market blend weight.
- [x] Implement config-driven model hyperparameters, feature subsets/ablations, and calibration transforms.
- [x] Preserve market favorite gate semantics and report-only outputs.
- [x] Add focused unit tests for caching keys, feature subsets, params, calibration, and validation errors.

## Summary of Changes

- Split model scoring from prediction materialization so variants sharing model, params, features, and minimum training sample count reuse cached base walk-forward probabilities.
- Added config-driven XGBoost/logistic model params, feature-group subsets/ablations, and deterministic temperature calibration before market blending.
- Extended variant reports with resolved feature names, model params, calibration settings, and feature counts.

## Verification

- `python -m py_compile services/python/ml/experiment_harness.py`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py -q` => `13 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py services/python/test_market_signal_experiment.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => `23 passed`
