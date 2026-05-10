---
# intercept-c5rs
title: '4-J: POST /api/predict/train + /admin/predict-train page'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-1ved
---

Admin retrain trigger.

- [ ] POST /api/predict/train (header X-Admin-Secret gated, value from env ADMIN_SECRET)
- [ ] Calls pythonBridge.call('ml.train'); returns metrics; row inserted in model_versions
- [ ] /admin/predict-train page: text input for admin secret (saves to localStorage), 'Train new model' button, polls progress
- [ ] On completion: shows new model metrics + top features table
- [ ] Admin nav entry hidden behind ?admin=1 query
