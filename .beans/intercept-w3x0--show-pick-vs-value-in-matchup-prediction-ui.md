---
# intercept-w3x0
title: Show pick vs value in matchup prediction UI
status: completed
type: task
priority: normal
created_at: 2026-05-11T02:05:11Z
updated_at: 2026-05-11T02:15:40Z
---

Update the upcoming fight compare sheet to distinguish the model's straight-up pick from the market value side using model-vs-market edge.

## Summary of Changes
- Split the matchup prediction panel into separate Model Pick and Value Pick tiles.
- Compute value pick from per-fighter model probability minus normalized market probability when matched odds are present.
- Added clear unavailable copy when two matched moneylines are not available.

## Verification
- pnpm biome check --write 'apps/web/src/app/(dashboard)/upcoming/compare-sheet.tsx'
- pnpm --filter @interceptor/web typecheck
- agent-browser opened /upcoming, opened Allen vs Costa compare sheet, and captured /private/tmp/intercept-pick-value-compare-sheet.png showing Model Pick and Value Pick tiles.
