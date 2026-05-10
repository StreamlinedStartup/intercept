---
# intercept-palv
title: '3-G: Add recent form features (rolling windows)'
status: todo
type: task
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-09T19:02:04Z
parent: intercept-at4c
blocked_by:
    - intercept-n40x
---

wins_last_3_diff, wins_last_5_diff, loss_streak, coming_off_loss, days_since_last_fight, long_layoff>365d.

- [ ] features.py adds form features
- [ ] Test: fighter with W,L,W,L,W in last 5 → wins_last_5=3
- [ ] Test: fighter with no prior fights → form features all NaN
- [ ] Re-train
