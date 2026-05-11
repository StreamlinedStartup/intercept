---
# intercept-u1vf
title: Expose backtest outputs for model tuning
status: completed
type: task
priority: normal
created_at: 2026-05-11T00:24:51Z
updated_at: 2026-05-11T00:59:18Z
parent: intercept-r03n
blocked_by:
    - intercept-pqsx
---

Persist and document backtest reports so model tweaks can be compared by accuracy, log loss, Brier score, calibration, and ROI/edge buckets before promotion.



## Summary of Changes

- Added `ml.backtest_report` to summarize saved walk-forward report JSON files as Markdown or strict JSON.
- Exposed overall accuracy, log loss, Brier score, ROC AUC, confidence buckets, and model-edge buckets for model-tuning comparisons.
- Documented report summary commands, ignored report storage, and the current ROI boundary until pre-event odds snapshots are available.

## Verification

- `services/python/.venv/bin/python -m py_compile services/python/ml/backtest_report.py`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/smoke-walk-forward.json`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/smoke-walk-forward.json --format json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q`
