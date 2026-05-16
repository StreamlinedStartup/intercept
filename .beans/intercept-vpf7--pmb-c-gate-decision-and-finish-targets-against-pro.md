---
# intercept-vpf7
title: 'PMB-C: Gate decision and finish targets against prop market'
status: completed
type: task
priority: high
created_at: 2026-05-16T00:51:38Z
updated_at: 2026-05-16T00:57:09Z
parent: intercept-zh6a
blocked_by:
    - intercept-kwrm
---

Acceptance criteria:
- [x] Wire decision and finish target ROI/gate evaluation to prop market baselines when available.
- [x] Keep unavailable-market status when prop coverage is missing.
- [x] Preserve report-only and writes_model_versions=false policy.
- [x] Add focused harness tests covering decision, finish, and missing-baseline paths.

## Summary of Changes

- Wired decision and finish predictions to target-specific prop market probabilities when `DISTANCE` rows are available.
- Added target-specific market baseline reports so decision/finish variants compare against prop baselines instead of the winner moneyline baseline.
- Preserved explicit `*_market_odds_unavailable` ROI status when prop coverage is missing and added focused tests for decision, finish, and gate behavior.
