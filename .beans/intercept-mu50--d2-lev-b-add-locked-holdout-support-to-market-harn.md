---
# intercept-mu50
title: 'D2-LEV-B: Add locked holdout support to market harness'
status: completed
type: task
priority: high
created_at: 2026-05-13T00:47:19Z
updated_at: 2026-05-13T01:02:00Z
parent: intercept-5t8l
blocked_by:
    - intercept-kraf
---

Acceptance criteria:

- [x] Supports evaluating only a chronological holdout event window.
- [x] Keeps training strictly before each target event.
- [x] Preserves same-selected-fight market baselines.
- [x] Adds focused tests for holdout filtering and validation.

## Summary of Changes

- Added `corpus.holdout` support to the market experiment harness.
- Implemented `last_n_events` filtering after eligibility and before scoring.
- Added holdout coverage summaries to harness reports.
- Extended schema and tests for holdout validation.

## Verification

- `PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/experiment_harness.py`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_experiment_harness.py -q` -> 16 passed.
