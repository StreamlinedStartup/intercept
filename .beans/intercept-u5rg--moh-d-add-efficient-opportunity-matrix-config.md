---
# intercept-u5rg
title: 'MOH-D: Add efficient opportunity matrix config'
status: completed
type: task
priority: high
created_at: 2026-05-15T16:24:41Z
updated_at: 2026-05-15T16:32:19Z
parent: intercept-77c6
blocked_by:
    - intercept-exy7
---

Acceptance criteria:
- [x] Add checked-in configs for a small smoke matrix and a focused opportunity matrix.
- [x] Reuse cached base predictions across blend, calibration, threshold, and strategy variants.
- [x] Keep outputs under data/experiments/harness and report-only.
- [x] Add config validation tests for opportunity matrices.

## Summary of Changes
- Added `market-opportunity-smoke.json` for fast cross-target harness checks.
- Added `market-opportunity-matrix-v1.json` for focused moneyline residual, decision, finish, and abstain opportunity searches.
- Kept all outputs under `data/experiments/harness` with `report_only=true` and `writes_model_versions=false`.
- Added config-loading tests for both opportunity matrices.
