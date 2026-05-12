---
# intercept-k0yc
title: 'D2-EH2: Expanded market experiment sweep'
status: completed
type: epic
priority: high
created_at: 2026-05-12T06:35:51Z
updated_at: 2026-05-12T07:08:00Z
parent: intercept-8mw9
---

Run a larger report-only harness sweep across curated market-scored variants. Keep all outputs research_only, compare every candidate against market favorite, and publish the expanded run artifacts without writing model_versions.

## Summary of Changes

- Added a reproducible generator and 103-variant expanded market sweep config.
- Ran the expanded harness against the current market-covered corpus and committed JSON/Markdown artifacts.
- Published a recommendation: no candidate cleared the market gate; more blend weights are not justified until the harness supports real new axes such as cached base predictions, hyperparameters, feature subsets, calibration, or new pre-fight signals.

## Verification

- `node scripts/experiments/generate-expanded-market-grid.mjs`
- `jq '.variants | length' configs/experiments/market-grid-expanded-100.json` => `103`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-expanded-100.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-expanded-100.json data/experiments/harness/market-grid-expanded-100-recommendation.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`

No HTTP/UI smoke gate was required because this epic added CLI/config/artifact work only, not an HTTP endpoint or UI surface.
