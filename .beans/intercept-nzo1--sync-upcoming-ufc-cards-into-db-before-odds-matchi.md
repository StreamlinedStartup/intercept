---
# intercept-nzo1
title: Sync upcoming UFC cards into DB before odds matching
status: todo
type: task
priority: normal
created_at: 2026-05-09T21:58:17Z
updated_at: 2026-05-09T21:58:23Z
parent: intercept-8gxf
blocked_by:
    - intercept-qjks
---

Seed canonical upcoming event/fight/fighter rows from ufcstats upcoming events before relying on high odds match rates.

Acceptance:
- [ ] Fetch /api/ufcstats/events/upcoming and each /api/ufcstats/event/:id.
- [ ] Upsert upcoming events, fights, fighters, and pending fight rows sufficient for odds matching.
- [ ] Re-run /api/odds-mma/snapshot and verify match rate is meaningful against live upcoming cards.
- [ ] Document any remaining unmatched odds rows with reasons.
