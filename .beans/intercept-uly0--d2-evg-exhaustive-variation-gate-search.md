---
# intercept-uly0
title: 'D2-EVG: Exhaustive variation gate search'
status: completed
type: epic
priority: high
created_at: 2026-05-12T23:12:05Z
updated_at: 2026-05-13T00:10:00Z
---

Run a broader report-only exhaustive model variation search through the market harness. Keep all outputs research_only, do not write model_versions, and only recommend a candidate if it clears ROI, log-loss, and Brier gates versus market.

## Summary of Changes

- Added deterministic generators for exhaustive, selection-policy, and threshold-refinement market harness matrices.
- Added report-only market-context feature sets and selected-fight gate baselines.
- Ran 42,281 exhaustive model variants, 73,441 selection variants, and 751 threshold-refinement variants.
- Found one gate-clearing candidate: `log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63`.
- Kept all outputs `research_only` with `writes_model_versions=false`.

## Verification

- `market-grid-exhaustive-v2`: 42,281 variants, 0 clearing candidates.
- `market-grid-selection-v1`: 73,441 variants, near miss failed coverage.
- `market-grid-selection-threshold-v1`: `candidate_for_locked_evaluation`.
- Gate-clearing candidate metrics: 40 events, 204 fights, +2.49% ROI delta, -0.0011 log-loss delta, -0.0015 Brier delta.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py services/python/test_generate_exhaustive_market_matrix.py -q` -> 17 passed.
- HTTP/UI smoke gate not required: pure research/reporting epic with no endpoint or UI surface.
