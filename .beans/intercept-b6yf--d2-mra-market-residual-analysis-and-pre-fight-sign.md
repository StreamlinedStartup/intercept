---
# intercept-b6yf
title: 'D2-MRA: Market residual analysis and pre-fight signal discovery'
status: completed
type: epic
priority: high
created_at: 2026-05-12T05:34:24Z
updated_at: 2026-05-12T06:04:54Z
parent: intercept-8mw9
---

Use the trainable 40-event market-covered corpus from D2-TMC to identify where the model loses to the market, isolate pre-fight feature gaps, and choose one or two signal candidates before another model experiment. Keep all outputs research-only; no active model_versions writes or validated activation in this epic.

Acceptance criteria:
- [x] Freeze D2-TMC artifacts as residual-analysis inputs and baseline current market/model/blend results.
- [x] Bucket residuals by favorite/underdog, odds range, weight class, event age, feature availability, confidence, and market/model disagreement.
- [x] Identify high-loss model failure clusters and feature gaps.
- [x] Define one or two pre-fight-only signal candidates that avoid leakage and post-fight data.
- [x] Implement only the smallest justified signal candidate as a report-only experiment.
- [x] Rerun market-gated reports and publish a final JSON/Markdown recommendation.
- [x] Keep UI/API/docs research-only and do not write active model_versions.

## Summary of Changes

- Completed D2-MRA tasks A-F with one commit per task.
- Published residual baseline, bucket, cluster, signal-candidate, signal-experiment, and final recommendation artifacts under `data/experiments/`.
- Final recommendation remains `research_only` / `do_not_promote`: feature availability improved ROI versus current XGBoost but worsened log loss/Brier and stayed -23.9pp ROI versus market favorite.

## Verification

- `jq empty data/experiments/market-residual-final-*.json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_market_residual_analysis.py services/python/test_market_residual_clusters.py services/python/test_market_signal_experiment.py services/python/test_market_gate_report.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => `21 passed`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
- Pure report/backend epic; no HTTP/UI smoke gate required.
