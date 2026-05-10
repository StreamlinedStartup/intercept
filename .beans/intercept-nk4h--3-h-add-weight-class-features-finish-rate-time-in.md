---
# intercept-nk4h
title: '3-H: Add weight class features + finish rate + time in cage'
status: todo
type: task
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-09T19:02:04Z
parent: intercept-at4c
blocked_by:
    - intercept-palv
---

weight_class_change bool, same_weight_class_count, finish_rate_diff, decision_rate_diff, time_in_cage_a/b.

- [ ] features.py adds these
- [ ] Test: fighter with 3 LW fights then a WW fight → weight_class_change=true
- [ ] Re-train
