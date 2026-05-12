---
# intercept-prq8
title: 'D2-EH2-B: Run expanded harness sweep'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:36:19Z
updated_at: 2026-05-12T06:52:00Z
parent: intercept-k0yc
blocked_by:
    - intercept-4rxh
---

Acceptance criteria:
- [x] Run the expanded config through ml.experiment_harness on the current market-covered corpus.
- [x] Publish JSON/Markdown expanded sweep artifacts.
- [x] Record top candidates against market favorite and keep value_status research_only unless the predeclared gate passes.
- [x] Verify model_versions count is unchanged by the run.

## Summary of Changes

- Ran the 103-variant expanded sweep with `configs/experiments/market-grid-expanded-100.json`.
- Published `data/experiments/harness/market-grid-expanded-100.json` and `data/experiments/harness/market-grid-expanded-100.md`.
- Recorded that the best configured candidate was `xgb_prod_blend_01_model_99_market`, which did not clear the market gate.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-expanded-100.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-expanded-100.json`
- `jq '{variant_count: (.variants | length), coverage, recommendation, top_ranked: .ranking[0:10], market_baseline}' data/experiments/harness/market-grid-expanded-100.json`
- `rg -n "xgb_prod_blend_01_model_99_market|research_only|market gate|model_versions|Ranking|103" data/experiments/harness/market-grid-expanded-100.md data/experiments/harness/market-grid-expanded-100.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
