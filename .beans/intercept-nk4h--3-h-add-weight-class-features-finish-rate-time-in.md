---
# intercept-nk4h
title: '3-H: Add weight class features + finish rate + time in cage'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T01:23:19Z
parent: intercept-at4c
blocked_by:
    - intercept-palv
---

weight_class_change bool, same_weight_class_count, finish_rate_diff, decision_rate_diff, time_in_cage_a/b.

- [x] features.py adds these
- [x] Test: fighter with 3 LW fights then a WW fight → weight_class_change=true
- [x] Re-train

## Summary of Changes

- Added `weight_class_change`, `same_weight_class_count_diff`, `finish_rate_diff`, `decision_rate_diff`, `time_in_cage_a`, and `time_in_cage_b` to `FEATURE_NAMES`.
- Passed target fight `weight_class` into training feature construction while keeping ad hoc prediction compatible with missing target weight by returning `NaN` weight-class values.
- Added DB-backed pytest coverage for a fighter moving from three lightweight fights into a welterweight target, including finish/decision rate and cage-time assertions.
- Retrain result: `model_id=20260510T012302033681Z`, `log_loss=0.6190711182621691`, slightly worse than prior `0.6167094944392515`; top features included `time_in_cage_b`, `weight_class_change`, `time_in_cage_a`, and `same_weight_class_count_diff`.
