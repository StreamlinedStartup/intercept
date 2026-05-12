---
# intercept-j6ip
title: 'D2-EH3-A: Extend harness config contract for real axes'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:20:24Z
updated_at: 2026-05-12T22:27:00Z
parent: intercept-8423
---

Acceptance criteria:
- [x] Extend the experiment config schema to support model_params, feature_subset, and calibration fields.
- [x] Add an example real-axes config using hyperparameter, feature ablation, calibration, and blend dimensions.
- [x] Keep all config guardrails report_only, research_only, chronological, and market-gated.
- [x] Validate JSON and config loading in tests.

## Summary of Changes

- Extended `configs/experiments/market-experiment.schema.json` with variant-level `model_params`, `feature_subset`, and `calibration`.
- Added `configs/experiments/market-grid-real-axes-smoke.json` to exercise hyperparameter, feature ablation, calibration, and blend dimensions.
- Added a config-loading test for the new real-axes smoke example while preserving the existing example contract.

## Verification

- `jq empty configs/experiments/market-experiment.schema.json configs/experiments/market-grid-real-axes-smoke.json`
- `jq '.variants | length' configs/experiments/market-grid-real-axes-smoke.json` => `10`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py -q` => `7 passed`
