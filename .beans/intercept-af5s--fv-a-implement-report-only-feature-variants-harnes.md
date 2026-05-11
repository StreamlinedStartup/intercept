---
# intercept-af5s
title: 'FV-A: Implement report-only feature variants harness'
status: completed
type: task
priority: high
created_at: 2026-05-11T16:08:35Z
updated_at: 2026-05-11T16:44:10Z
parent: intercept-ebnb
---

Acceptance criteria:
- [x] Add experiment-only feature variant definitions for baseline, no_weight_class, weight_class_record_v1, no_recent_form, no_damage, no_common_opponents, no_stance, no_physical, and no_career_stats.
- [x] Add point-in-time weight-class prior features for weight_class_record_v1 without changing production prediction behavior.
- [x] Add ml.experiments feature-variants CLI with two-stage screening/finalist runs and compact JSON/Markdown reports.
- [x] Include overall metrics, deltas vs baseline, confidence-bucket metrics, feature lists, ranking, finalist list, and over-confidence flags.
- [x] Cover variant vector alignment, ranking order, and weight-class feature edge cases with pytest.
- [x] Verify py_compile, pytest, tiny smoke, and intended feature-variant run; commit compact report artifacts if reviewable.

## Summary of Changes
- Added variant-aware feature construction and backtesting hooks while keeping production FEATURE_NAMES as the default.
- Added ml.experiments feature-variants with two-stage ranking and compact JSON/Markdown reports.
- Added DB-backed tests for weight-class prior features, variant alignment, and ranking.
- Verified py_compile, pytest, tiny experiment smoke, and the intended full feature-variant report run.
