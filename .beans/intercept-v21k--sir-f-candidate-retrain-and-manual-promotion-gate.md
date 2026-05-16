---
# intercept-v21k
title: 'SIR-F: Candidate retrain and manual promotion gate'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:58:31Z
updated_at: 2026-05-16T14:18:11Z
parent: intercept-qh8w
blocked_by:
    - intercept-yenm
---

Scope the candidate retraining path and keep production artifact promotion manual and gated.

Acceptance criteria:
- [x] Candidate retrain command can generate experimental artifacts from newly labeled fights.
- [x] Locked validation checks include no-leakage chronology, enough market coverage, calibration, ROI/edge diagnostics, and comparison to market baseline.
- [x] A new frozen artifact is produced only when gates pass and the promotion is explicitly approved.
- [x] Failed/weak candidates remain report-only artifacts with recommendation notes, not production model files.
- [x] Promotion process records model version, source data window, feature set, threshold, calibration, and validation evidence.

## Summary of Changes

- Added `pnpm --filter @interceptor/db candidate:market-indicators` to generate report-only candidate evidence bundles from the post-event evaluator.
- Documented the manual promotion gate, required validation evidence, and rejection behavior in `docs/operations/indicator-promotion-gate.md`.
- Verified candidate artifact generation against the local DB; current output is empty because no refreshed snapshots have settled results yet.
