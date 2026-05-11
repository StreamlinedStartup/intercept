---
# intercept-n5nk
title: Retrain predictor on external UFC stats corpus
status: completed
type: task
priority: normal
created_at: 2026-05-11T01:11:27Z
updated_at: 2026-05-11T01:14:00Z
---

Retrain the Python ML model after importing the external UFC Stats CSV corpus, verify the new model_versions row, and record the operational evidence.



## Summary of Changes

- Retrained the Python XGBoost predictor after importing the external UFC Stats corpus.
- New latest model: `20260511T011334074447Z` at `data/models/20260511T011334074447Z.json`.
- Training set increased from 80 samples to 8,538 samples.
- Model artifact remains ignored under `data/models/`; the durable runtime pointer is the local `model_versions` row.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.train`
- Train output: 8,538 samples, 6,830 train rows, 1,708 holdout rows, accuracy 0.6042154566744731, log_loss 0.6583929196070333, Brier 0.233173668384552, ROC AUC 0.6484823395011892.
- Verified latest `model_versions` row points to `data/models/20260511T011334074447Z.json`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q`
