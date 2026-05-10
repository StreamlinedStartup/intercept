---
# intercept-g0wt
title: '4-K: Phase 4 verification + ship'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-g4oo
    - intercept-33qk
    - intercept-qtw9
    - intercept-c5rs
---

Verification per docs/ufc-fight-predictor-plan.md#phase-4.

- [ ] curl /api/predict/event/9eedac48b497de5a returns N predictions for UFC 328
- [ ] /upcoming shows pick chips on every fight row
- [ ] CompareSheet shows win-prob bars + edge badge when odds present
- [ ] /predictions table populated, ROI chart renders, calibration plot renders
- [ ] /admin/predict-train trains a new model end-to-end and shows updated metrics
- [ ] Zero console errors on each page (Patchright check)
- [ ] biome + typecheck + vitest + pytest green
- [ ] ./scripts/ci-local.sh passes
- [ ] Mark E4 completed; mark milestone intercept-7c8e completed
