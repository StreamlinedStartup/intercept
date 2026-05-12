---
# intercept-8423
title: 'D2-EH3: Real experiment axes'
status: completed
type: epic
priority: high
created_at: 2026-05-12T22:20:17Z
updated_at: 2026-05-12T22:55:00Z
parent: intercept-8mw9
---

Extend the market experiment harness beyond blend-weight sweeps by adding cached base walk-forward predictions and config-driven real experiment axes: model hyperparameters, feature subsets/ablations, and calibration transforms. Keep outputs report-only and research_only.

## Summary of Changes

- Extended the harness config contract with `model_params`, `feature_subset`, and `calibration`.
- Implemented cached base walk-forward probabilities so variants sharing model, params, features, and min-train count can reuse scoring across calibration and market blends.
- Added config-driven XGBoost/logistic params, feature group subsets/ablations, deterministic temperature calibration, and a real-axis smoke sweep.

## Verification

- `jq empty configs/experiments/market-experiment.schema.json configs/experiments/market-grid-real-axes-smoke.json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py services/python/test_market_signal_experiment.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => `23 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-real-axes-smoke.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-real-axes-smoke.json data/experiments/harness/market-grid-real-axes-smoke-recommendation.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`

No HTTP/UI smoke gate was required because this epic added CLI/config/artifact work only, not an HTTP endpoint or UI surface.
