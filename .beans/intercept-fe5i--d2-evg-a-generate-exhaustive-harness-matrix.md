---
# intercept-fe5i
title: 'D2-EVG-A: Generate exhaustive harness matrix'
status: completed
type: task
priority: high
created_at: 2026-05-12T23:12:15Z
updated_at: 2026-05-12T23:28:00Z
parent: intercept-uly0
---

Acceptance criteria:

- [x] Generates every configured model/feature/calibration/blend variation from a single reproducible script.
- [x] Includes current supported production, availability, opponent-adjusted recent performance, and style matchup feature sets.
- [x] Keeps config report_only/research_only/no model_versions writes.
- [x] Adds tests or deterministic validation for variant count and uniqueness.

## Summary of Changes

- Added `ml.generate_exhaustive_market_matrix` to generate the v2 market-gate search config deterministically.
- Added market-context and combined research feature sets to the report-only harness.
- Generated `configs/experiments/market-grid-exhaustive-v2.json` with 42,281 variants across model families, feature sets, hyperparameters, calibration settings, and market blends.
- Extended harness schema and tests for the new feature sets and generator.

## Verification

- `PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/experiment_harness.py services/python/ml/generate_exhaustive_market_matrix.py`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py services/python/test_generate_exhaustive_market_matrix.py -q` -> 15 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.generate_exhaustive_market_matrix` -> 42,281 variants.
- Harness `_load_config(Path("configs/experiments/market-grid-exhaustive-v2.json"))` accepted the generated research-only config.
