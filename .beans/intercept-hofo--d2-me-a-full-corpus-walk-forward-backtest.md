---
# intercept-hofo
title: 'D2-ME-A: Full-corpus walk-forward backtest'
status: completed
type: task
priority: normal
created_at: 2026-05-11T14:29:06Z
updated_at: 2026-05-11T14:52:51Z
parent: intercept-stba
---

Run and report a full-corpus walk-forward model evaluation over the imported UFC Stats CSV-backed database. This is separate from intercept-zivm, which remains historical odds source discovery.

Acceptance criteria:
- [x] Run beans list --ready and create the bean graph first.
- [x] Create/switch to a dedicated branch for intercept-stba before code or docs changes.
- [x] Run a full eligible historical UFC walk-forward backtest from the imported CSV-backed DB, removing or raising --max-events 20.
- [x] Choose and document start date and min_train_samples policy.
- [x] Produce a summarized backtest report suitable for commit; do not blindly commit huge raw artifacts if they are too large.
- [x] Update docs/model_scope.md with full-corpus metrics, confidence buckets, and caveats.
- [x] If runtime or artifact size is a problem, improve the backtest/report tooling narrowly so it can emit a compact summary JSON/Markdown.
- [x] Run focused verification and commit the completed bean.

## Summary of Changes

- Created `intercept-stba` for the small Decision Engine v2 full-corpus model evaluation epic and completed this task on `epic/intercept-stba-full-corpus-model-evaluation`.
- Added backtest progress output, compact stdout control, and report-writer support for Markdown summaries with confidence and model-edge buckets.
- Ran the full imported CSV-backed UFC walk-forward backtest with no `--max-events` cap: 753 events, 8,332 predictions, 59.35% accuracy, 0.669 log loss, 0.238 Brier score, and 0.627 ROC AUC.
- Documented the no-explicit-start-date policy, `min_train_samples=200` floor, confidence buckets, and odds/ROI caveat in `docs/model_scope.md`.

## Verification

- `beans list --ready`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --min-train-samples 200 --output data/backtests/full-corpus-walk-forward.json --progress-every 25`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/full-corpus-walk-forward.json --output data/backtests/full-corpus-walk-forward.md`
- `services/python/.venv/bin/python -m py_compile services/python/ml/backtest.py services/python/ml/backtest_report.py`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/full-corpus-walk-forward.json --format json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --help`
