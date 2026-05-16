---
# intercept-zx69
title: 'D2-MIX-B: Evaluate calibration and market-blend variants'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:34:08Z
updated_at: 2026-05-12T04:05:08Z
parent: intercept-tgq5
blocked_by:
    - intercept-0ipt
---

Acceptance criteria:
- [x] Evaluate probability calibration and model/market blend families with walk-forward discipline.
- [x] Compare every candidate to the no-vig market favorite on log loss, Brier, accuracy, ROC AUC, and simulated research ROI.
- [x] Report whether any candidate clears +2pp ROI over market favorite without leakage.
- [x] Keep outputs report-only; do not activate validated.

## Summary of Changes

- Added a report-only market-blend experiment runner that evaluates the no-vig market favorite, raw model pick, model/market blend grid, and simple shrinkage calibration variants.
- Wrote JSON and Markdown evidence under `data/experiments/market-aware-blend-experiments.*` with per-candidate log loss, Brier score, accuracy, ROC AUC, and simulated flat-stake ROI.
- Best candidate was `blend_25_model_75_market` at +15.9% ROI, which is -0.3pp versus the market favorite baseline and does not clear the +2pp activation gate.
- Outputs remain `research_only` and explicitly record `writes_model_versions: false`.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m pytest services/python/test_market_blend_experiments.py services/python/test_market_gate_report.py -q`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:market-blend-experiments`
- `jq empty data/experiments/market-aware-blend-experiments.json`
