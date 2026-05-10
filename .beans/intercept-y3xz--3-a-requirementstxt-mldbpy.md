---
# intercept-y3xz
title: '3-A: requirements.txt + ml/db.py'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-09T23:53:52Z
parent: intercept-at4c
blocked_by:
    - intercept-5cmh
---

Plumbing only. Get Python able to talk to Postgres.

- [x] services/python/requirements.txt adds xgboost, scikit-learn, pandas, numpy, psycopg[binary]
- [x] services/python/.venv setup or update; pip install passes
- [x] services/python/ml/__init__.py
- [x] services/python/ml/db.py with psycopg connection pool reading DATABASE_URL
- [x] Standalone test: python -c 'from ml.db import pool; print(pool.connection().execute("SELECT 1").fetchone())' returns (1,)

## Summary of Changes

- Added Phase 3 Python ML requirements and installed them into `services/python/.venv`.
- Added the `ml` package and `ml.db` Postgres connection-pool adapter reading `DATABASE_URL`.
- Verified the standalone DB smoke command returns `(1,)` against the local interceptor Postgres container.
