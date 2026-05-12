---
# intercept-jnqm
title: 'D2-MRA-F: Rerun market-gated reports and publish recommendation'
status: completed
type: task
priority: high
created_at: 2026-05-12T05:36:14Z
updated_at: 2026-05-12T06:04:00Z
parent: intercept-b6yf
blocked_by:
    - intercept-fypt
---

Acceptance criteria:
- [x] Rerun leakage audit, residual bucket report, market gate, blend, and model-family reports after the signal experiment.
- [x] Publish final JSON/Markdown recommendation with candidate result, ROI delta versus market favorite, probability-quality metrics, blockers, and next step.
- [x] Keep value_status research_only unless the gate truly passes.
- [x] Do not write active model_versions or activate validated status in this epic.

## Summary of Changes

- Reran final leakage audit, residual bucket, market gate, blend, and model-family reports under `data/experiments/market-residual-final-*`.
- Published `data/experiments/market-residual-final-recommendation.json` and `.md`.
- Recommendation remains `research_only` / `do_not_promote`: feature availability improved ROI versus current XGBoost but worsened log loss/Brier and remains -23.9pp ROI versus market favorite.

## Verification

- `PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.leakage_audit --output data/experiments/market-residual-final-leakage-audit.json --markdown data/experiments/market-residual-final-leakage-audit.md --stdout summary` => `14/14 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_gate_report --output data/experiments/market-residual-final-market-gate-report.json --markdown data/experiments/market-residual-final-market-gate-report.md --stdout summary`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_blend_experiments --output data/experiments/market-residual-final-blend-experiments.json --markdown data/experiments/market-residual-final-blend-experiments.md --stdout summary`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_residual_analysis --output data/experiments/market-residual-final-buckets.json --markdown data/experiments/market-residual-final-buckets.md --stdout summary`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.model_family_experiments --output data/experiments/market-residual-final-model-family-experiments.json --markdown data/experiments/market-residual-final-model-family-experiments.md --stdout summary`
- `jq empty data/experiments/market-residual-final-*.json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_market_residual_analysis.py services/python/test_market_residual_clusters.py services/python/test_market_signal_experiment.py services/python/test_market_gate_report.py services/python/test_market_blend_experiments.py services/python/test_model_family_experiments.py -q` => `21 passed`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
