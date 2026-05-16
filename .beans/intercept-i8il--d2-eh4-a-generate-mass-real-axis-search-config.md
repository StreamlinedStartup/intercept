---
# intercept-i8il
title: 'D2-EH4-A: Generate mass real-axis search config'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:31:07Z
updated_at: 2026-05-12T22:37:00Z
parent: intercept-3ymp
---

Acceptance criteria:
- [x] Add a reproducible generator for a large curated real-axis experiment config.
- [x] Cover XGBoost hyperparameters, logistic regularization, feature subsets/ablations, temperature calibration, and limited market blends.
- [x] Avoid invalid variants and preserve research_only/report_only/model-gated settings.
- [x] Validate generated JSON and variant/base-key counts before running.

## Summary of Changes

- Added `scripts/experiments/generate-mass-edge-grid.mjs`.
- Generated `configs/experiments/market-grid-mass-edge-search.json` with 1,585 variants over 66 cached base keys.
- Covered XGBoost params, logistic `C`, feature subsets/ablations, temperature calibration, and a small market blend ladder.

## Verification

- `node scripts/experiments/generate-mass-edge-grid.mjs`
- `jq '.variants | length' configs/experiments/market-grid-mass-edge-search.json` => `1585`
- `jq empty configs/experiments/market-grid-mass-edge-search.json`
- Python `_load_config` and `_base_prediction_key` assertions => `{"variant_count": 1585, "base_key_count": 66}`
