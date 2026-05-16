---
# intercept-2sgy
title: 'PMB-A: Map prop baseline contract into harness'
status: completed
type: task
priority: high
created_at: 2026-05-16T00:51:30Z
updated_at: 2026-05-16T00:52:37Z
parent: intercept-zh6a
---

Acceptance criteria:
- [x] Inspect existing market opportunity harness target and ROI flow.
- [x] Define how historical_prop_odds DISTANCE rows map to decision and finish target market probabilities.
- [x] Document no-vig aggregation and timestamp limitations.
- [x] Commit a compact planning artifact before code changes.

## Summary of Changes

- Inspected `services/python/ml/experiment_harness.py` and confirmed decision/finish targets currently return market-baseline-unavailable ROI.
- Defined the `historical_prop_odds` `DISTANCE` mapping for decision and finish target market probabilities.
- Published `data/experiments/harness/prop-market-baseline-contract.md` with no-vig aggregation, target ROI, and timestamp limits.
