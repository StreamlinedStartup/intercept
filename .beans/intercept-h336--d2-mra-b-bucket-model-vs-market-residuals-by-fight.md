---
# intercept-h336
title: 'D2-MRA-B: Bucket model-vs-market residuals by fight dimensions'
status: completed
type: task
priority: high
created_at: 2026-05-12T05:34:40Z
updated_at: 2026-05-12T05:48:51Z
parent: intercept-b6yf
blocked_by:
    - intercept-nwg3
---

Acceptance criteria:
- [x] Bucket residuals by favorite/underdog side, odds range, weight class, event date age, feature availability, confidence, and market/model disagreement.
- [x] Compute per-bucket count, model accuracy, market accuracy, model ROI, market ROI, log loss, Brier, and calibration gap where applicable.
- [x] Flag unstable buckets and keep them out of promotion recommendations.
- [x] Publish JSON/Markdown residual bucket reports; no model_versions writes.

## Summary of Changes

- Added `services/python/ml/market_residual_analysis.py` to build report-only `xgboost_current` vs no-vig market residual buckets from the frozen matched market corpus.
- Published `data/experiments/market-residual-buckets.json` and `.md` with seven dimensions, per-bucket metrics, ROI deltas, and unstable-bucket flags.
- Added focused tests for bucket metrics, unstable policy, helper labels, and Markdown policy text.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_market_residual_analysis.py -q` => `4 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_residual_analysis --output data/experiments/market-residual-buckets.json --markdown data/experiments/market-residual-buckets.md --stdout summary`
- `jq empty data/experiments/market-residual-buckets.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
