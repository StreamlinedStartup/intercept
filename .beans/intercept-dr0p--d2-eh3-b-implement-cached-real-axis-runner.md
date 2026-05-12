---
# intercept-dr0p
title: 'D2-EH3-B: Implement cached real-axis runner'
status: todo
type: task
priority: high
created_at: 2026-05-12T22:20:32Z
updated_at: 2026-05-12T22:20:32Z
parent: intercept-8423
blocked_by:
    - intercept-j6ip
---

Acceptance criteria:\n- [ ] Reuse cached base walk-forward model probabilities for variants that differ only by calibration or market blend weight.\n- [ ] Implement config-driven model hyperparameters, feature subsets/ablations, and calibration transforms.\n- [ ] Preserve market favorite gate semantics and report-only outputs.\n- [ ] Add focused unit tests for caching keys, feature subsets, params, calibration, and validation errors.
