---
# intercept-j39k
title: '4-Sm: Smoke gate (agent-browser)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:24:40Z
updated_at: 2026-05-10T23:21:26Z
parent: intercept-di4c
blocked_by:
    - intercept-g0wt
---

Final epic gate. Epic E4 (intercept-di4c) does NOT close until this passes. This is also the v1 ship gate.

Prerequisites: full pipeline working. Both fighters on UFC 328 main event backfilled (Phase 1 done). A model trained (Phase 3 done). Odds snapshot taken (Phase 2 done).

- [x] `agent-browser open http://localhost:3000/upcoming`
- [x] `agent-browser screenshot data/smoke/phase-4-upcoming-chips.png` shows prediction chips on every fight row whose fighters are loaded
- [x] Click main event 'Compare Fighters'; `agent-browser screenshot data/smoke/phase-4-compare.png` shows win-probability bars in both corner cells AND an Edge badge if odds present
- [x] `agent-browser open http://localhost:3000/predictions`
- [x] `agent-browser screenshot data/smoke/phase-4-predictions.png` shows track-record table, ROI chart, calibration histogram
- [x] `agent-browser snapshot` confirms ROI + calibration sections render (a11y tree)
- [x] `agent-browser open http://localhost:3000/admin/predict-train?admin=1`
- [x] Click 'Train new model'; verify progress text appears (don't wait for completion); `agent-browser screenshot data/smoke/phase-4-train.png`
- [x] All four screenshots show zero broken layouts, zero error banners, zero overlap, no missing data placeholders
- [x] `agent-browser eval 'window.__errors || []'` empty across all pages
- [x] Mobile check: `agent-browser open http://localhost:3000/upcoming` with viewport 375x812; `agent-browser screenshot data/smoke/phase-4-mobile.png` shows working chips on mobile
- [x] `agent-browser close --all`
- [x] Commit screenshots
- [x] Mark epic E4 (intercept-di4c) completed
- [x] Mark milestone (intercept-7c8e) completed

## Summary of Changes

- Completed the final Phase 4 agent-browser smoke gate.
- Captured desktop, compare-sheet, predictions, admin-train, and mobile screenshots under `data/smoke/`.
- Confirmed browser console output had no runtime errors and `window.__errors || []` was empty.

## Verification

- `agent-browser screenshot data/smoke/phase-4-upcoming-chips.png`
- `agent-browser screenshot data/smoke/phase-4-compare.png`
- `agent-browser screenshot data/smoke/phase-4-predictions.png`
- `agent-browser screenshot data/smoke/phase-4-train.png`
- `agent-browser screenshot data/smoke/phase-4-mobile.png`
- `agent-browser eval 'window.__errors || []'` => `[]`
- `agent-browser close --all`
