---
# intercept-33qk
title: '4-H: /predictions ROI cumulative chart'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:32:32Z
parent: intercept-di4c
blocked_by:
    - intercept-ifp6
---

Visualize betting performance over time.

- [x] Cumulative units chart along event.date (SVG line chart, no chart lib needed for v1 — keep KISS)
- [x] Filter: 'all' / 'edge>5%' / 'edge>10%'
- [x] Annotation: 'breakeven' horizontal line

## Summary of Changes

- Added a cumulative ROI SVG chart to `/predictions`.
- Added all, edge >5%, and edge >10% filters.
- Captured browser smoke evidence at `data/smoke/phase4-33qk-roi-chart.png`.

## Verification

- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check --write apps/web/src/app/'(dashboard)'/predictions/predictions-content.tsx .beans/intercept-33qk--4-h-predictions-roi-cumulative-chart.md`
- `agent-browser open http://localhost:3000/predictions`
- `agent-browser wait --text 'Cumulative ROI'`
- `agent-browser click @e4`
- `agent-browser wait --text 'No resolved bets for this filter'`
- `agent-browser screenshot data/smoke/phase4-33qk-roi-chart.png`
