---
# intercept-ftr2
title: '1-F: Compare-sheet integration (corner cells show backfill state)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T21:14:40Z
parent: intercept-1shv
blocked_by:
    - intercept-q4n3
---

Open compare sheet shows state for both fighters. Block 'View prediction' until both are 'current'.

- [x] CompareSheet header cells show backfill state badge per fighter
- [x] Below VS divider, show a Load buttons row when either fighter is none/stale
- [x] (Phase 4 will add the actual prediction button — for now placeholder text 'Predictions ready when both fighters loaded')

## Summary of Changes

Integrated backfill state into the compare sheet: each corner shows loaded/not-loaded/stale status, unloaded or stale fighters get Load/Update actions, and the Phase 4 prediction area is represented by placeholder text.

Verification:
- pnpm --filter @interceptor/web typecheck
- agent-browser opened /upcoming, clicked Compare Fighters, and confirmed the dialog showed Corner A/B backfill states, Load buttons for both fighters, and "Predictions ready when both fighters loaded"
