---
# intercept-fypt
title: 'D2-MRA-E: Implement smallest justified signal experiment'
status: completed
type: task
priority: high
created_at: 2026-05-12T05:35:07Z
updated_at: 2026-05-12T05:58:43Z
parent: intercept-b6yf
blocked_by:
    - intercept-tktt
---

Acceptance criteria:
- [x] Implement only the smallest justified pre-fight signal candidate from Task D.
- [x] Keep the implementation report-only until market-gated validation passes.
- [x] Add focused tests for leakage boundaries and feature-vector alignment.
- [x] Publish experiment output comparing candidate versus market favorite; no active model_versions writes.

## Summary of Changes

- Added `services/python/ml/market_signal_experiment.py` for the report-only `pre_fight_feature_availability_flags` experiment.
- Added four pre-fight availability features: missing count, missing rate, recent-form availability, and weight-context availability.
- Published `data/experiments/market-signal-experiment.json` and `.md`; result is `do_not_promote` because the candidate remains behind market favorite and worsens log loss/Brier versus current XGBoost.
- Added focused tests for feature-vector alignment, leakage boundary semantics, recommendation behavior, and Markdown policy output.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_market_signal_experiment.py services/python/test_market_residual_analysis.py -q` => `8 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_signal_experiment --output data/experiments/market-signal-experiment.json --markdown data/experiments/market-signal-experiment.md --stdout summary`
- `jq empty data/experiments/market-signal-experiment.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
