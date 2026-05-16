---
# intercept-ivky
title: 'MOH-B: Add target-specific labels and metrics'
status: completed
type: task
priority: high
created_at: 2026-05-15T16:24:41Z
updated_at: 2026-05-15T16:28:55Z
parent: intercept-77c6
blocked_by:
    - intercept-exy7
---

Acceptance criteria:
- [x] Build point-in-time labels for decision and finish targets from completed fight outcomes.
- [x] Keep winner metrics compatible with existing market-favorite baseline.
- [x] Emit target-aware probability metrics, calibration, and coverage counts.
- [x] Add tests for decision/finish label extraction and target-aware metrics.

## Summary of Changes
- Added decision and finish target labels from completed fight method outcomes.
- Kept winner variants on the existing market-favorite probability and ROI path.
- Added target-aware prediction rows and probability metrics for non-winner targets while marking prop-market ROI unavailable until prop odds exist.
- Added focused tests for target labels, non-winner prediction rows, and non-winner market-blend rejection.
