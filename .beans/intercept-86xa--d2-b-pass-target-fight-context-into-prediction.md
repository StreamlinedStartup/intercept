---
# intercept-86xa
title: 'D2-B: Pass target fight context into prediction'
status: completed
type: task
priority: high
created_at: 2026-05-11T13:30:50Z
updated_at: 2026-05-11T13:35:31Z
parent: intercept-7c3e
blocked_by:
    - intercept-tk88
---

Acceptance criteria:
- [x] Pass target fight weight_class into ml.predict so prediction-time feature construction matches training.
- [x] Add focused coverage proving the target fight context is forwarded.
- [x] Update this bean with verification evidence before completion.


## Summary of Changes
- Added fight weight_class to prediction participant queries and forwarded it in the ml.predict bridge payload.
- Updated the Python worker and predict_pair to pass target_weight_class into build_feature_row.
- Added focused API and worker tests for weight-class forwarding.

## Verification
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/api test -- src/routes/predict.test.ts
- pnpm --filter @interceptor/api typecheck
- services/python/.venv/bin/python -m pytest services/python/test_worker.py -q
