---
# intercept-q4n3
title: '1-E: Stale-count detection in event-fight-card'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:59:30Z
updated_at: 2026-05-09T20:48:56Z
parent: intercept-1shv
blocked_by:
    - intercept-vsbt
---

When a backfilled fighter has new fights, badge turns yellow with 'Update — N new fights' button.

- [x] When event-fight-card fetches backfill state, if state='current' compare history_count_at_backfill against the fresh historyCount from /api/ufcstats/fighter/:id (already cached, so free)
- [x] If currentCount > stored, server returns state='stale_count' with the diff
- [x] UI shows yellow badge + Update button
- [x] Click triggers a delta-only backfill (refactor 1-A: only fetch fights newer than last_known_fight_id)
- [x] Test: manually decrement history_count_at_backfill in DB → badge yellow → click → green again with correct count

## Summary of Changes

Added stale-count detection to the backfill state endpoint, delta-only update behavior for already-backfilled fighters, and Update button labeling in the upcoming fight card UI.

Verification:
- pnpm --filter @interceptor/api typecheck
- pnpm --filter @interceptor/web typecheck
- Manually set history_count_at_backfill=9 for fighter 767755fd74662dbf
- GET /api/predict/backfill/state/767755fd74662dbf returned status=stale_count and new_fight_count=1
- agent-browser snapshot on /upcoming showed button "Update — 1 new fight"
- Clicking the Update button ran a job with progress "Backfill already current"; final state returned status=current and history_count_at_backfill=10
