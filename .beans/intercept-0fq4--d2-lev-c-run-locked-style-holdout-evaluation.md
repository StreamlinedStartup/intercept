---
# intercept-0fq4
title: 'D2-LEV-C: Run locked-style holdout evaluation'
status: completed
type: task
priority: high
created_at: 2026-05-13T00:47:27Z
updated_at: 2026-05-13T01:10:00Z
parent: intercept-5t8l
blocked_by:
    - intercept-mu50
---

Acceptance criteria:

- [x] Runs the frozen candidates on the locked-style holdout config.
- [x] Publishes compact JSON/Markdown artifacts.
- [x] Reports whether each candidate clears ROI, log-loss, Brier, and coverage gates.
- [x] Keeps all outputs research_only and writes_model_versions=false.

## Summary of Changes

- Added `ml.generate_locked_evaluation_config`.
- Generated `configs/experiments/locked-evaluation-v1.json` from the frozen candidate list.
- Ran the three frozen candidates on the last-10-event historical locked-style holdout.
- Published full and compact locked-evaluation artifacts.
- Result: no candidate cleared the locked-style holdout.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_generate_exhaustive_market_matrix.py services/python/test_experiment_harness.py -q` -> 22 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.generate_locked_evaluation_config` -> 4 variants.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/locked-evaluation-v1.json --stdout summary` -> `research_only`.
- `jq -e '.recommendation.status == "research_only" and ([.variants[] | select(.clears_market_gate == true)] | length) == 0 and .report_only == true and .writes_model_versions == false and .value_status == "research_only"' data/experiments/harness/locked-evaluation-v1.json` -> true.
