---
# intercept-exy7
title: 'MOH-A: Extend harness config for opportunity targets'
status: completed
type: task
priority: high
created_at: 2026-05-15T16:24:31Z
updated_at: 2026-05-15T16:26:17Z
parent: intercept-77c6
---

Acceptance criteria:
- [x] Add a target dimension to the market experiment schema and runtime validation.
- [x] Support winner, decision, and finish targets without production model writes.
- [x] Keep report_only/value_status/writes_model_versions guards intact.
- [x] Add focused tests for target validation and defaults.

## Summary of Changes
- Added variant-level `target` support for `winner`, `decision`, and `finish` with `winner` as the backward-compatible default.
- Added schema support, runtime validation, report metadata, and cache-key separation for target-aware variants.
- Added focused harness tests for target defaults, accepted targets, invalid targets, market baseline constraints, and cache separation.
