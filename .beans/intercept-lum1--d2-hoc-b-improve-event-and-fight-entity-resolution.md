---
# intercept-lum1
title: 'D2-HOC-B: Improve event and fight entity-resolution heuristics'
status: todo
type: task
priority: high
created_at: 2026-05-12T02:27:33Z
updated_at: 2026-05-12T02:27:33Z
parent: intercept-vgy0
blocked_by:
    - intercept-kex7
---

Acceptance criteria:
- [ ] Improve matching with normalized names, event date, promotion, weight class, bout participants, and cancelled-bout handling.
- [ ] Verify no regression on the current 3-event historical odds corpus.
- [ ] Keep unresolved rows reportable instead of silently dropping them.
