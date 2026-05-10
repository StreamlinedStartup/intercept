---
# intercept-palv
title: '3-G: Add recent form features (rolling windows)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T01:20:31Z
parent: intercept-at4c
blocked_by:
    - intercept-n40x
---

wins_last_3_diff, wins_last_5_diff, loss_streak, coming_off_loss, days_since_last_fight, long_layoff>365d.

- [x] features.py adds form features
- [x] Test: fighter with W,L,W,L,W in last 5 → wins_last_5=3
- [x] Test: fighter with no prior fights → form features all NaN
- [x] Re-train

## Summary of Changes

- Added rolling form features: `wins_last_3_diff`, `wins_last_5_diff`, loss streak, coming-off-loss, days-since-last-fight, and long-layoff flags.
- Computed form only from prior completed win/loss results where `event.date < target_fight.date`; fighters with no prior form return `NaN` form values.
- Added DB-backed pytest coverage for a W,L,W,L,W last-five history and no-prior-fights missing form.
- Retrain result: `model_id=20260510T012006941302Z`, `log_loss=0.6167094944392515`, worse than prior `0.5968872791151922`; top features were form-heavy (`loss_streak_b`, `days_since_last_fight_b`, `coming_off_loss_b`).
