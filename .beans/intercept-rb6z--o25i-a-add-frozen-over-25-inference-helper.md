---
# intercept-rb6z
title: 'O25I-A: Add frozen Over 2.5 inference helper'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:21:03Z
updated_at: 2026-05-16T05:23:51Z
parent: intercept-ptdd
---

Acceptance criteria:
- [x] Add a Python helper/worker method that returns the frozen Over 2.5 model probability for one fight.
- [x] Use the locked candidate parameters: over_2_5, logistic regression C=1.0, temperature=1.6, threshold=0.58, production_plus_all_research.
- [x] Return report-only metadata and tests without writing model_versions or predictions.

## Summary of Changes

- Added `ml.prop_indicators.over_2_5_indicator` with the frozen locked-validation candidate parameters.
- Added worker method `ml.prop_indicator.over_2_5` for API use.
- Added focused tests for worker forwarding, frozen threshold behavior, report-only metadata, and insufficient-training handling.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=/tmp/interceptor-worktrees/promote-over25-report-indicator/services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest /tmp/interceptor-worktrees/promote-over25-report-indicator/services/python/test_prop_indicators.py /tmp/interceptor-worktrees/promote-over25-report-indicator/services/python/test_worker.py -q`
