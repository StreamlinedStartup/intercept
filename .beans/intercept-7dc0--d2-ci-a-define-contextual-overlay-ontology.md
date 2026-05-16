---
# intercept-7dc0
title: 'D2-CI-A: Define contextual overlay ontology'
status: completed
type: task
priority: normal
created_at: 2026-05-11T13:31:26Z
updated_at: 2026-05-11T19:17:09Z
parent: intercept-vxdl
blocked_by:
    - intercept-qizd
---

Acceptance criteria:
- [x] Define injury, camp, weight-cut, and short-notice labels.
- [x] Design the overlay as auditable risk/research flags, not automatic betting logic.
- [x] Keep model-training integration out of scope until labels and backtests exist.

## Summary of Changes

- Added `docs/contextual_overlay_ontology.md` with normalized injury, camp, weight-cut, and short-notice labels.
- Defined the overlay as sourced, auditable review flags with severity, direction, source, and review status fields.
- Documented that contextual flags stay out of model training, probability adjustment, edge calculation, and betting logic until labels and walk-forward backtests exist.
