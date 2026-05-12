---
# intercept-ls80
title: 'D2-EH: Market experiment harness'
status: completed
type: epic
priority: high
created_at: 2026-05-12T06:13:15Z
updated_at: 2026-05-12T06:56:00Z
parent: intercept-8mw9
---

Build a reusable report-only experiment harness for market-scored model and feature variants. The harness should run deterministic chronological experiments from a config matrix, compare candidates against market favorite, keep outputs research-only, and make future experiments faster without writing active model_versions.

## Summary of Changes

- Added a checked-in experiment config contract and example market grid.
- Implemented `ml.experiment_harness` as a report-only chronological runner for market favorite, XGBoost, availability-augmented XGBoost, logistic baseline, and market blends.
- Published initial run artifacts and a recommendation that keeps the work `research_only`; MLflow can be layered on later if tracking UI/search becomes the bottleneck.

## Verification

- `pytest services/python/test_experiment_harness.py services/python/test_market_signal_experiment.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => `16 passed`
- `python -m ml.experiment_harness --config configs/experiments/market-grid.example.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-smoke.json data/experiments/harness/market-grid-summary.json data/experiments/harness/experiment-harness-recommendation.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`

No HTTP/UI smoke gate was required because this epic added a pure Python report-only CLI and committed artifacts, not an HTTP endpoint or UI surface.
