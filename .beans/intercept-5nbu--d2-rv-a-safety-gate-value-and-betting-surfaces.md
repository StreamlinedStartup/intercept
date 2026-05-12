---
# intercept-5nbu
title: 'D2-RV-A: Safety-gate value and betting surfaces'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:02Z
updated_at: 2026-05-12T00:26:46Z
parent: intercept-dmyw
---

Remove validated betting/value implications from the live product surfaces while preserving numeric prediction and odds fields for research.

Acceptance criteria:
- [x] /upcoming compare sheet uses Market comparison / research edge language instead of Value pick.
- [x] /predictions ROI and edge filters clearly say simulated/research-only.
- [x] Prediction responses keep edge_pct, market_prob, and odds fields available.
- [x] Prediction responses include value_status and value_status_reason without breaking callers.
- [x] Docs no longer imply a validated betting edge.
- [x] Focused verification passes.



## Summary of Changes
- Added non-breaking `value_status` and `value_status_reason` fields to prediction and history responses while preserving existing odds, `market_prob`, and `edge_pct` fields.
- Updated `/upcoming` compare sheet and `/predictions` copy to present market edge and ROI as simulated research-only outputs.
- Updated predictor docs and roadmap language so current surfaces do not imply a validated betting edge.

## Verification
- `pnpm biome check --write apps/api/src/routes/predict.ts apps/api/src/routes/predict.test.ts apps/web/src/app/'(dashboard)'/upcoming/compare-sheet.tsx apps/web/src/app/'(dashboard)'/predictions/predictions-content.tsx`
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/web typecheck`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- predict.test.ts`
