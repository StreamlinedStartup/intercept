---
# intercept-3ymp
title: 'D2-EH4: Mass edge search harness'
status: completed
type: epic
priority: high
created_at: 2026-05-12T22:31:00Z
updated_at: 2026-05-12T23:00:00Z
parent: intercept-8mw9
---

Build an en-masse experiment generator and run a large report-only market-gated sweep across real experiment axes. The goal is to search for candidate edge faster while keeping outputs research_only until a predeclared market gate and locked evaluation pass.

## Summary of Changes

- Added a reproducible mass edge grid generator.
- Generated and ran a 1,585-variant search across 66 cached base keys covering XGBoost params, logistic regularization, feature subsets/ablations, temperature calibration, and limited market blends.
- Published full run artifacts plus compact summary/recommendation artifacts; no candidate cleared the market gate.

## Verification

- `node scripts/experiments/generate-mass-edge-grid.mjs`
- `jq '.variants | length' configs/experiments/market-grid-mass-edge-search.json` => `1585`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-mass-edge-search.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-mass-edge-search.json data/experiments/harness/market-grid-mass-edge-search-summary.json data/experiments/harness/market-grid-mass-edge-search-recommendation.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`

No HTTP/UI smoke gate was required because this epic added CLI/config/artifact work only, not an HTTP endpoint or UI surface.
