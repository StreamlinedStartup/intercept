---
# intercept-brce
title: '3-C: train.py — chronological split + first model'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:02:04Z
updated_at: 2026-05-10T00:17:41Z
parent: intercept-at4c
blocked_by:
    - intercept-pcuc
---

First trainable model. Must beat random.

- [x] services/python/ml/train.py: load all completed fights, build feature matrix, chronological 80/20 split by event.date, fit XGBClassifier with early_stopping_rounds=20
- [x] Compute log_loss, brier_score_loss, accuracy, roc_auc on holdout
- [x] Save model to `data/models/<UTC-iso>.json` (XGBoost native), insert row in model_versions with metrics + path
- [x] CLI test: python -m ml.train prints {model_id, log_loss, accuracy, ...}; log_loss < 0.69 (random) confirms it learned something

## Summary of Changes

- Added `services/python/ml/train.py` with chronological 80/20 loading, XGBClassifier training, holdout metrics, native model save, and `model_versions` insertion.
- Kept the first slice intentionally small: one chronological sample per completed fight using the minimal feature row from `intercept-pcuc`.
- Updated the Python DB pool adapter to rollback read-only transactions before returning connections, which keeps CLI output clean.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.train`
- Result: `model_id=20260510T002020555519Z`, `training_set_size=80`, `log_loss=0.6214818254404825`, `brier_score=0.2150161862373352`, `accuracy=0.6875`, `roc_auc=0.5`
- `SELECT id, training_set_size, log_loss, accuracy, model_path FROM model_versions ORDER BY trained_at DESC LIMIT 1;` returned `data/models/20260510T002020555519Z.json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q` returned `18 passed`
