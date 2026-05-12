---
# intercept-9nqj
title: 'D2-EH-B: Implement configurable experiment runner'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:13:36Z
updated_at: 2026-05-12T06:21:39Z
parent: intercept-ls80
blocked_by:
    - intercept-28c6
---

Acceptance criteria:
- [x] Implement a Python CLI that reads the config and executes chronological market-covered experiments.
- [x] Support at least model families, feature sets/availability transforms, and market blend weights.
- [x] Persist run registry JSON/Markdown artifacts with params, metrics, gates, and rejection reasons.
- [x] Add focused tests for config parsing, feature alignment, and gate behavior; no model_versions writes.

## Summary of Changes

- Added `services/python/ml/experiment_harness.py`, a config-driven report-only experiment runner.
- Supports `market_favorite`, `xgboost`, `logistic_regression`, `production`, `production_plus_availability`, and market blend weights.
- Added `services/python/test_experiment_harness.py` for config validation, feature alignment, gate behavior, recommendations, and Markdown contract.
- Generated the first run registry at `data/experiments/harness/market-grid-smoke.json` and `.md`.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py services/python/test_market_signal_experiment.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => `16 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid.example.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-smoke.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
