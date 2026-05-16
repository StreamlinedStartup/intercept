---
# intercept-z2lz
title: 'D2-MIX-C: Evaluate feature and model-family variants'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:34:15Z
updated_at: 2026-05-12T04:14:52Z
parent: intercept-tgq5
blocked_by:
    - intercept-zx69
---

Acceptance criteria:
- [x] Run report-only feature/model-family variants using the frozen D2-MIX-A contract.
- [x] Include current model baseline, simple market-aware blends, and conservative feature ablations.
- [x] Reject variants that improve ROI through leakage, unstable tiny buckets, or degraded calibration.
- [x] Publish JSON/Markdown experiment results.

## Summary of Changes

- Added a report-only model-family experiment runner that trains each evaluated event only on prior frozen market-covered fights.
- Evaluated current XGBoost, 25/75 and 50/50 XGBoost/market blends, logistic regression, and conservative XGBoost feature ablations.
- Published JSON and Markdown evidence under `data/experiments/market-aware-model-family-experiments.*`.
- Best candidate was `blend_25_xgboost_75_market` at +3.5% ROI on the model-eligible subset, which is -6.3pp versus the market favorite and fails the gate because ROI, stability, log-loss, and Brier checks do not clear.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m pytest services/python/test_model_family_experiments.py services/python/test_market_blend_experiments.py services/python/test_market_gate_report.py -q`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:model-family-experiments`
- `jq empty data/experiments/market-aware-model-family-experiments.json`
