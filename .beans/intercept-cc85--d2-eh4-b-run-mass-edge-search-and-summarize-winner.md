---
# intercept-cc85
title: 'D2-EH4-B: Run mass edge search and summarize winners'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:31:14Z
updated_at: 2026-05-12T22:48:00Z
parent: intercept-3ymp
blocked_by:
    - intercept-i8il
---

Acceptance criteria:
- [x] Run the generated mass config through ml.experiment_harness on the current market-covered corpus.
- [x] Publish full JSON/Markdown run artifacts plus compact winner summary artifacts.
- [x] Record any gate-clearing candidates or confirm none were found.
- [x] Verify model_versions count remains unchanged.

## Summary of Changes

- Ran the 1,585-variant mass edge search through `ml.experiment_harness`.
- Published full run artifacts plus compact summary artifacts under `data/experiments/harness/`.
- Recorded that 0 candidates cleared the market gate; the best candidate was a 1% model / 99% market blend that worsened log loss and Brier.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-mass-edge-search.json --stdout summary`
- `jq empty data/experiments/harness/market-grid-mass-edge-search.json data/experiments/harness/market-grid-mass-edge-search-summary.json`
- `jq '{variant_count: (.variants | length), gate_clear_count: ([.ranking[] | select(.clears_gate == true)] | length), coverage, recommendation, top_ranked: .ranking[0:20], market_baseline}' data/experiments/harness/market-grid-mass-edge-search.json`
- `PGPASSWORD=interceptor psql -h localhost -p 5434 -U interceptor -d interceptor -Atc "select count(*) from model_versions;"` => `14`
