---
# intercept-cawd
title: 'D2-ME-B: Confidence calibration diagnostics'
status: completed
type: task
priority: normal
created_at: 2026-05-11T15:41:16Z
updated_at: 2026-05-11T15:51:04Z
parent: intercept-41yv
---

Add compact calibration diagnostics so full-corpus walk-forward results show whether confidence buckets are over-performing, under-performing, or calibrated.

Acceptance criteria:
- [x] Run beans list --ready and create the bean graph first.
- [x] Create/switch to a dedicated branch for intercept-41yv before code or docs changes.
- [x] Add average confidence to overall and grouped backtest metrics.
- [x] Add expected-vs-actual calibration gap and absolute calibration error to overall and grouped backtest metrics.
- [x] Regenerate the full-corpus walk-forward report and compact Markdown summary with calibration diagnostics.
- [x] Update docs/model_scope.md with the 70%+ bucket average confidence, actual accuracy, and implications.
- [x] Run focused verification and commit the completed bean.

## Summary of Changes

- Added `avg_confidence`, `calibration_gap`, and `abs_calibration_error` to walk-forward metrics overall, by event/month, by confidence bucket, and by model-edge bucket.
- Expanded `ml.backtest_report` Markdown and JSON summaries to include calibration diagnostics.
- Regenerated `data/backtests/full-corpus-walk-forward.json` and `data/backtests/full-corpus-walk-forward.md`.
- Documented the full-corpus finding in `docs/model_scope.md`: overall calibration is tight, but `70%+` picks average 75.20% confidence and land at 70.03%, a -5.18 percentage-point gap.

## Verification

- `beans list --ready`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --min-train-samples 200 --output data/backtests/full-corpus-walk-forward.json --progress-every 25 --stdout summary`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/full-corpus-walk-forward.json --output data/backtests/full-corpus-walk-forward.md`
- `services/python/.venv/bin/python -m py_compile services/python/ml/backtest.py services/python/ml/backtest_report.py`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/full-corpus-walk-forward.json --format json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --help`
