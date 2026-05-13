---
# intercept-5iu2
title: 'D2-ECW-B: Search for additional expanded-corpus winners'
status: completed
type: task
priority: high
created_at: 2026-05-13T00:21:34Z
updated_at: 2026-05-13T00:41:00Z
parent: intercept-gzb7
blocked_by:
    - intercept-3eph
---

Acceptance criteria:

- [x] Generates additional selected-fight threshold/refinement variants.
- [x] Runs them through ml.experiment_harness.
- [x] Identifies all variants that clear the configured market gate.
- [x] Publishes compact evidence artifacts.

## Summary of Changes

- Added `ml.generate_additional_winner_search`.
- Generated `configs/experiments/additional-winner-search-v1.json` with 7,777 variants.
- Ran the additional selected-fight search at `min_train_samples=20`.
- Found 150 market-gate-clearing variants.
- Published compact JSON/Markdown evidence summaries.

## Verification

- `PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/generate_additional_winner_search.py`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_generate_exhaustive_market_matrix.py -q` -> 5 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.generate_additional_winner_search` -> 7,777 variants.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/additional-winner-search-v1.json --stdout summary` -> `candidate_for_locked_evaluation`.
- `jq '[.variants[] | select(.clears_market_gate == true)] | length' data/experiments/harness/additional-winner-search-v1.json` -> 150.
