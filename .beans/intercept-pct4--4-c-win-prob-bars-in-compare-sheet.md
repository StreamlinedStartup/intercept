---
# intercept-pct4
title: '4-C: Win-prob bars in compare-sheet'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:14:51Z
parent: intercept-di4c
blocked_by:
    - intercept-a5wm
---

Show model probabilities prominently in the compare sheet UI.

- [x] CompareSheet: add a third parallel fetch to /api/predict/fight/:id
- [x] In each corner cell, add a horizontal bar showing that fighter's win probability
- [x] Below the stats grid, add a 'Model Pick' row with the predicted winner highlighted
- [x] Loading state with skeleton bars

## Summary of Changes

- Passed resolved fight IDs from `/upcoming` fight rows into the compare sheet.
- Added a prediction fetch to `CompareSheet` and rendered fighter-specific win-probability bars in both corner cells.
- Added a `Model Pick` panel with the predicted winner, probability, and model version, with skeleton loading states.

Verified:

- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check --write apps/web/src/app/'(dashboard)'/upcoming/compare-sheet.tsx apps/web/src/app/'(dashboard)'/upcoming/event-fight-card.tsx apps/web/src/app/'(dashboard)'/upcoming/upcoming-content.tsx .beans/intercept-pct4--4-c-win-prob-bars-in-compare-sheet.md`
- `agent-browser snapshot` after opening the current main-event compare sheet showed `68%` for Arnold Allen, `32%` for Melquizael Costa, and `MODEL PICK Arnold Allen · 68%`.
- `agent-browser screenshot data/smoke/phase4-pct4-compare-prob-bars.png`
