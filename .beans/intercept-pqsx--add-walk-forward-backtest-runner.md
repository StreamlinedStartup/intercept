---
# intercept-pqsx
title: Add walk-forward backtest runner
status: completed
type: task
priority: normal
created_at: 2026-05-11T00:24:46Z
updated_at: 2026-05-11T00:57:08Z
parent: intercept-r03n
blocked_by:
    - intercept-0vfw
---

Add a Python backtest command that trains only on past fights, predicts the next chronological event, stores metrics by date/confidence/edge bucket, and prevents future-data leakage.



## Summary of Changes

- Added `ml.backtest` as a standalone Python walk-forward runner that trains in memory on fights before each target event and predicts only the next chronological event.
- Reports overall, monthly, confidence-bucket, and model-edge-bucket metrics, plus per-event training sample and prediction counts.
- Writes strict JSON reports under ignored `data/backtests/` and records undefined ROC AUC as `null`.
- Documented smoke and full-run commands in `docs/external_ufcstats_dataset.md`.

## Verification

- `services/python/.venv/bin/python -m py_compile services/python/ml/backtest.py`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --start-date 2024-01-01 --max-events 2 --output data/backtests/smoke-walk-forward.json`
- Smoke report scored 2 events and 23 predictions, with 7,319 and 7,330 prior training samples for the two event folds.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python/test_ml.py -q`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q`
