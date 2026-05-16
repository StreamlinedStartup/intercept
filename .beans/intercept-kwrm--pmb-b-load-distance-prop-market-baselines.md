---
# intercept-kwrm
title: 'PMB-B: Load DISTANCE prop market baselines'
status: completed
type: task
priority: high
created_at: 2026-05-16T00:51:34Z
updated_at: 2026-05-16T00:54:27Z
parent: intercept-zh6a
blocked_by:
    - intercept-2sgy
---

Acceptance criteria:
- [x] Add a point-in-time-safe loader for historical_prop_odds DISTANCE consensus probabilities.
- [x] Produce separate market probabilities for decision and finish targets.
- [x] Preserve winner-moneyline behavior for existing winner variants.
- [x] Add focused tests for probability aggregation and target mapping.

## Summary of Changes

- Added a `historical_prop_odds` `DISTANCE` consensus loader that uses source-current rows linked to canonical fights.
- Added no-vig sportsbook-pair aggregation for separate `decision` and `finish` market probabilities.
- Added focused harness tests for paired-outcome requirements, consensus mapping, target probability lookup, and missing-baseline behavior.
