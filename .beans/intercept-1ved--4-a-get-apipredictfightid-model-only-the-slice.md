---
# intercept-1ved
title: '4-A: GET /api/predict/fight/:id (model only, THE SLICE)'
status: todo
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:15:43Z
parent: intercept-di4c
blocked_by:
    - intercept-elww
---

Smallest predict route: takes a fight_id, calls Python ml.predict, returns the model's pick. No odds yet.

- [ ] apps/api/src/routes/predict.ts with GET /api/predict/fight/:id
- [ ] Route loads (event.date, fighter_a_id, fighter_b_id) from DB, calls pythonBridge.call('ml.predict', {fighter_a_id, fighter_b_id, fight_date})
- [ ] Returns {predicted_winner_id, win_prob, model_version}
- [ ] Persist row to predictions table on every call
- [ ] curl test: returns valid prediction for any fight_id where both fighters have backfill_state='current'
