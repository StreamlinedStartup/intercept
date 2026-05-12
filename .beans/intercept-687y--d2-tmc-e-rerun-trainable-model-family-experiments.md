---
# intercept-687y
title: 'D2-TMC-E: Rerun trainable model-family experiments'
status: completed
type: task
priority: high
created_at: 2026-05-12T04:24:02Z
updated_at: 2026-05-12T04:39:53Z
parent: intercept-ftbt
blocked_by:
    - intercept-xsmv
---

Acceptance criteria:
- [x] Rerun blend/calibration and model-family experiment reports on the expanded corpus.
- [x] Report model-eligible events/fights separately from broad market-covered events/fights.
- [x] Compare every candidate to the no-vig market favorite on ROI, log loss, Brier, accuracy, ROC AUC, and calibration.
- [x] Reject candidates with leakage, unstable buckets, or degraded probability metrics.

## Summary of Changes

- Published expanded blend/calibration and model-family reports under `data/experiments/trainable-market-corpus-*`.
- Model-family trainability improved to 40 model-eligible events and 379 model-eligible fights.
- Best full-corpus blend remains `blend_25_model_75_market` at +18.5% ROI, still -1.5pp versus the market favorite.
- Best trainable model-family candidate is `blend_25_xgboost_75_market` at +10.5% ROI, still -8.0pp versus the model-eligible market favorite and rejected on ROI, log loss, and Brier.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_blend_experiments --output data/experiments/trainable-market-corpus-blend-experiments.json --markdown data/experiments/trainable-market-corpus-blend-experiments.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.model_family_experiments --output data/experiments/trainable-market-corpus-model-family-experiments.json --markdown data/experiments/trainable-market-corpus-model-family-experiments.md`
- `jq empty data/experiments/trainable-market-corpus-blend-experiments.json data/experiments/trainable-market-corpus-model-family-experiments.json`
