---
# intercept-g4oo
title: '4-E: GET /api/predict/event/:id (batch)'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-1ved
---

Predict every fight on a card in one call. Avoids 13 round-trips from the dashboard.

- [ ] GET /api/predict/event/:id loops fight rows for that event, returns array of predictions
- [ ] Update event-fight-card to use batch endpoint instead of per-row
- [ ] Same predictions row write per fight
