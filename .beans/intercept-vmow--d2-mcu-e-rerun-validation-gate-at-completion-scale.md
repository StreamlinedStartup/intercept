---
# intercept-vmow
title: 'D2-MCU-E: Rerun validation gate at completion scale'
status: todo
type: task
priority: high
created_at: 2026-05-12T03:33:43Z
updated_at: 2026-05-12T03:33:43Z
parent: intercept-p6uo
blocked_by:
    - intercept-p6v3
---

Acceptance criteria:
- [ ] Rerun leakage audit with DB checks.
- [ ] Rerun simple baselines and historical odds coverage.
- [ ] Rerun market gate and record scored fights, scored events, model ROI, market-favorite ROI, and blend ROI.
- [ ] Keep value_status insufficient_coverage unless both coverage thresholds pass; keep validated inactive unless all activation requirements truly pass.
- [ ] Confirm report tooling does not write active model_versions.
