---
# intercept-g6vf
title: '1-G: Admin seed: in-window cards (smallest)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T21:19:29Z
parent: intercept-1shv
blocked_by:
    - intercept-vsbt
---

First admin seed button. Backfills fighters appearing on cards within next 30 days.

- [x] POST /api/predict/backfill/seed?scope=in-window
- [x] Worker: GET /api/ufcstats/events/upcoming, filter date<=now+30d, for each event GET /event/:id, collect unique fighter ids, queue each through the same per-fighter backfill flow
- [x] /admin/predict-train page (skeleton): single button 'Seed: in-window' → POST → shows progress count
- [x] Test: <5 minutes for current week + next week's cards

## Summary of Changes

Added the in-window seed endpoint and a minimal /admin/predict-train page. The endpoint collects fighters from UFC cards in the next 30 days, returns queued counts immediately, and runs the existing per-fighter backfill flow sequentially in the background.

Verification:
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- POST /api/predict/backfill/seed?scope=in-window returned event_count=3, fighter_count=76, queued_count=76
- agent-browser clicked "Seed: in-window" on /admin/predict-train and saw Events=3, Fighters=76, Queued=76
