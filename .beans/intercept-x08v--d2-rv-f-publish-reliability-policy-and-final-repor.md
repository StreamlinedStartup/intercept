---
# intercept-x08v
title: 'D2-RV-F: Publish reliability policy and final report'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:27Z
updated_at: 2026-05-12T01:25:55Z
parent: intercept-dmyw
blocked_by:
    - intercept-pxkt
---

Publish the reliability policy and final report after the market baseline gate.

Acceptance criteria:
- [x] Document when value_status may become validated.
- [x] Publish final report artifacts and policy summary.
- [x] Keep UI/API wording aligned with the current validated or research-only state.
- [x] Do not write active model_versions.

## Summary of Changes
- Added `docs/model_reliability_policy.md` with the current `insufficient_coverage` status and validation criteria.
- Published `data/experiments/model-reliability-final-report.json` and `.md` as the D2-RV final report artifacts.
- Linked the policy from model scope and prediction interpretation docs so research-only UI/API wording has a durable source of truth.

## Verification
- `jq empty data/experiments/model-reliability-final-report.json`
- `rg -n "Value pick|value pick|betting edge|automatic bet|auto-bet|validated" docs/model_reliability_policy.md docs/model_scope.md docs/prediction_interpretation.md data/experiments/model-reliability-final-report.md apps/web/src/app/'(dashboard)'/upcoming/compare-sheet.tsx apps/web/src/app/'(dashboard)'/predictions/predictions-content.tsx apps/api/src/routes/predict.ts`
