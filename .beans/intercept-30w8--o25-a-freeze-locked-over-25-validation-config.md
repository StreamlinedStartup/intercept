---
# intercept-30w8
title: 'O25-A: Freeze locked Over 2.5 validation config'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:04:20Z
updated_at: 2026-05-16T05:06:08Z
parent: intercept-dsmc
---

Acceptance criteria:
- [x] Add a report-only locked validation config for the exact over_2_5_positive_log_c1_conf58 candidate.
- [x] Use a chronological holdout and prohibit threshold tuning in the config description.
- [x] Add focused config/test coverage so the candidate target, threshold, and write policy are locked.

## Summary of Changes

- Added `configs/experiments/over-2-5-locked-validation-v1.json` with the exact frozen `over_2_5_positive_log_c1_conf58` candidate.
- Locked the validation to a last-35-event chronological holdout with `frozen_candidates_only`, `report_only=true`, and `writes_model_versions=false`.
- Extended harness config tests to assert the Over 2.5 target, `positive_target_edge` policy, `0.58` threshold, holdout, and no-write policy.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=/tmp/interceptor-worktrees/over25-locked-validation/services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest /tmp/interceptor-worktrees/over25-locked-validation/services/python/test_experiment_harness.py -q`
