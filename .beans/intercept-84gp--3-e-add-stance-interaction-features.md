---
# intercept-84gp
title: '3-E: Add stance interaction features'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T00:24:43Z
parent: intercept-at4c
blocked_by:
    - intercept-opm3
---

stance_match one-hot ∈ {orthodox_orthodox, orthodox_southpaw, southpaw_orthodox, southpaw_southpaw, switch_involved, unknown}. Asymmetric — keep direction.

- [x] features.py adds stance encoding
- [x] Test: orthodox vs southpaw produces orthodox_southpaw=1 (not southpaw_orthodox)
- [x] Re-train and check log_loss change

## Summary of Changes

- Added six stance one-hot columns to `FEATURE_NAMES`: orthodox/orthodox, orthodox/southpaw, southpaw/orthodox, southpaw/southpaw, switch-involved, and unknown.
- Kept stance direction asymmetric so `orthodox_southpaw` and `southpaw_orthodox` are distinct.
- Added a DB-backed pytest proving orthodox vs southpaw sets only `stance_orthodox_southpaw`.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q` returned `19 passed`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.train`
- Retrain result: `model_id=20260510T002519262039Z`, `log_loss=0.6214818254404825`, unchanged from the prior `intercept-brce` run because the current seed corpus has no real stance coverage yet
