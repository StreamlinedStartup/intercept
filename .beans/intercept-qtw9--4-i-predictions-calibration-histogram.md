---
# intercept-qtw9
title: '4-I: /predictions calibration histogram'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:35:08Z
parent: intercept-di4c
blocked_by:
    - intercept-ifp6
---

Bin predictions by predicted probability (0-10%, 10-20%, ..., 90-100%); show actual win rate per bin.

- [x] 10-bucket bar chart (SVG)
- [x] Diagonal reference line for perfect calibration
- [x] Tooltip: bucket count + actual rate

## Summary of Changes

- Added a 10-bucket calibration histogram to `/predictions`.
- Added the perfect-calibration diagonal reference line and SVG bucket tooltips.
- Captured browser smoke evidence at `data/smoke/phase4-qtw9-calibration-histogram.png`.

## Verification

- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check --write apps/web/src/app/'(dashboard)'/predictions/predictions-content.tsx .beans/intercept-qtw9--4-i-predictions-calibration-histogram.md`
- `agent-browser open http://localhost:3000/predictions`
- `agent-browser wait --text Calibration`
- `agent-browser screenshot data/smoke/phase4-qtw9-calibration-histogram.png`
