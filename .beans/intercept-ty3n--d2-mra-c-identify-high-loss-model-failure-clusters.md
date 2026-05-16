---
# intercept-ty3n
title: 'D2-MRA-C: Identify high-loss model failure clusters and feature gaps'
status: completed
type: task
priority: high
created_at: 2026-05-12T05:34:53Z
updated_at: 2026-05-12T05:52:36Z
parent: intercept-b6yf
blocked_by:
    - intercept-h336
---

Acceptance criteria:
- [x] Identify clusters where the model is confidently wrong or trails market badly.
- [x] Compare feature availability and missingness inside failure clusters versus the scored corpus.
- [x] Distinguish actionable pre-fight feature gaps from market-only/noise explanations.
- [x] Publish JSON/Markdown cluster report; no model_versions writes.

## Summary of Changes

- Added `services/python/ml/market_residual_clusters.py` to classify high-loss residual buckets from the Task B residual row source.
- Published `data/experiments/market-residual-clusters.json` and `.md` with 25 high-loss clusters and feature-availability comparisons against the scored corpus.
- Classified clusters as actionable pre-fight feature gaps, market-prior gaps, calibration/noise, or unstable/noise for Task D input.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_market_residual_clusters.py services/python/test_market_residual_analysis.py -q` => `8 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.market_residual_clusters --output data/experiments/market-residual-clusters.json --markdown data/experiments/market-residual-clusters.md --stdout summary`
- `jq empty data/experiments/market-residual-clusters.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
