# Model Leakage Audit

- Generated: `2026-05-12T03:53:36.206651+00:00`
- Status: **PASS**
- Report-only: `true`
- Writes `model_versions`: `false`
- Checks: 15/15 passed

## Checks

| Category | Check | Status | Detail |
|---|---|---|---|
| feature_point_in_time | _career_stats uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _ufc_fight_count uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _recent_form uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _career_profile uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _weight_class_record_profile uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _round_tendency_profile uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _prior_results_by_opponent uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | _damage_index uses strict prior-event cutoff | pass | query filters prior rows with e.date < target_date |
| feature_point_in_time | build_features derives target context before label | pass | target date and weight class are passed into feature construction before label serialization |
| feature_point_in_time | build_feature_dict threads fight_date through feature helpers | pass | production feature helpers are called from one fight_date-scoped dictionary builder |
| train_test_boundary | train.py uses chronological split | pass | training samples are sorted by event date before holdout split |
| train_test_boundary | walk-forward trains only on earlier events | pass | walk-forward train set excludes same-day and future target events |
| train_test_boundary | walk-forward targets one event at a time | pass | target samples are selected by current event_id only |
| report_only | leakage audit does not write active models | pass | audit source has no model persistence calls |
| database_boundary | loaded walk-forward samples respect event boundaries | pass | checked 777 event boundaries from 8538 labeled samples |

## Policy

This report audits code shape and optional database event boundaries. It does not train a model, save a model file, write `model_versions`, or validate betting edge.
