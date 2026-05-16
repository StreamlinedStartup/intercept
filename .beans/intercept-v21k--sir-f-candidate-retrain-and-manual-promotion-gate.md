---
# intercept-v21k
title: 'SIR-F: Candidate retrain and manual promotion gate'
status: todo
type: task
created_at: 2026-05-16T05:58:31Z
updated_at: 2026-05-16T05:58:31Z
parent: intercept-qh8w
blocked_by:
    - intercept-yenm
---

Scope the candidate retraining path and keep production artifact promotion manual and gated.

Acceptance criteria:
- [ ] Candidate retrain command can generate experimental artifacts from newly labeled fights.
- [ ] Locked validation checks include no-leakage chronology, enough market coverage, calibration, ROI/edge diagnostics, and comparison to market baseline.
- [ ] A new frozen artifact is produced only when gates pass and the promotion is explicitly approved.
- [ ] Failed/weak candidates remain report-only artifacts with recommendation notes, not production model files.
- [ ] Promotion process records model version, source data window, feature set, threshold, calibration, and validation evidence.
