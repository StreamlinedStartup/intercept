---
# intercept-vuen
title: 'LSV-A: Add locked validation config'
status: completed
type: task
priority: normal
created_at: 2026-05-16T02:30:39Z
updated_at: 2026-05-16T02:32:20Z
parent: intercept-j1w3
---

Acceptance criteria:
- [x] Add a report-only locked validation config for the market-strength and decision-market indicators.
- [x] Use chronological holdout so the evaluation slice is not the same full-corpus discovery ranking.
- [x] Keep value_status research_only and writes_model_versions false.

## Summary of Changes

- Added `configs/experiments/prop-signal-locked-validation-v1.json`.
- Locked evaluation to the latest 20 chronological events via `corpus.holdout`.
- Added config coverage to `test_experiment_harness.py` and verified the focused test suite.
