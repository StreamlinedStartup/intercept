---
# intercept-82d4
title: 'D2-EH2-C: Publish expanded sweep recommendation'
status: completed
type: task
priority: high
created_at: 2026-05-12T06:36:31Z
updated_at: 2026-05-12T07:01:00Z
parent: intercept-k0yc
blocked_by:
    - intercept-prq8
---

Acceptance criteria:
- [x] Publish concise JSON/Markdown recommendation for the expanded sweep.
- [x] State whether any candidate clears the market gate and whether more variants are justified.
- [x] Record verification commands and model_versions count.
- [x] Close the epic without HTTP/UI smoke gate unless a UI/API surface was added.

## Summary of Changes

- Published `data/experiments/harness/market-grid-expanded-100-recommendation.json` and `data/experiments/harness/market-grid-expanded-100-recommendation.md`.
- Recorded that no candidate cleared the market gate; the best result was a 1% model / 99% market blend that worsened log loss and Brier.
- Documented that more dense blend weights are not justified until the harness supports real new experiment axes.

## Verification

- `jq empty data/experiments/harness/market-grid-expanded-100.json data/experiments/harness/market-grid-expanded-100-recommendation.json`
- `rg -n "xgb_prod_blend_01_model_99_market|research_only|more_blend_weights_justified|model_versions|No HTTP/UI smoke gate" data/experiments/harness/market-grid-expanded-100-recommendation.*`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
