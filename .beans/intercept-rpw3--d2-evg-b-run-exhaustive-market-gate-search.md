---
# intercept-rpw3
title: 'D2-EVG-B: Run exhaustive market gate search'
status: completed
type: task
priority: high
created_at: 2026-05-12T23:12:19Z
updated_at: 2026-05-13T00:03:00Z
parent: intercept-uly0
blocked_by:
    - intercept-fe5i
---

Acceptance criteria:

- [x] Runs the exhaustive matrix through ml.experiment_harness.
- [x] Publishes JSON and Markdown artifacts.
- [x] Identifies whether any variant clears ROI, log-loss, and Brier gates.
- [x] Records top-ranked variants and rejection reasons.

## Summary of Changes

- Ran `market-grid-exhaustive-v2`: 42,281 variants, no gate-clearing candidate.
- Added selected-fight gate baselines and selection policies for report-only model variants.
- Ran `market-grid-selection-v1`: 73,441 variants, no gate-clearing candidate, but found confidence-threshold near misses.
- Ran `market-grid-selection-threshold-v1`: 751 variants and found one gate-clearing candidate.
- Gate-clearing candidate: `log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63`.

## Gate-Clearing Metrics

- Events scored: 40.
- Fights scored: 204.
- ROI delta vs selected-fight market baseline: +2.49%.
- Log-loss delta vs selected-fight market baseline: -0.0011.
- Brier delta vs selected-fight market baseline: -0.0015.
- `clears_market_gate`: true.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-exhaustive-v2.json --stdout summary` -> 0 clearing variants.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-selection-v1.json --stdout summary` -> near miss failed coverage.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/market-grid-selection-threshold-v1.json --stdout summary` -> `candidate_for_locked_evaluation`.
- `jq -e '.recommendation.status == "candidate_for_locked_evaluation" and ([.variants[] | select(.clears_market_gate == true)] | length) >= 1 and .report_only == true and .writes_model_versions == false and .value_status == "research_only"' data/experiments/harness/market-grid-selection-threshold-v1.json` -> true.
