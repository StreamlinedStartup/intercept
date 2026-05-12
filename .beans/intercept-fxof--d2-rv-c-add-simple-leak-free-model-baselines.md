---
# intercept-fxof
title: 'D2-RV-C: Add simple leak-free model baselines'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:19Z
updated_at: 2026-05-12T01:04:38Z
parent: intercept-dmyw
blocked_by:
    - intercept-tjvc
---

Add report-only simple baselines for model reliability comparison.

Acceptance criteria:
- [ ] Include simple leak-free baselines such as market favorite where available and non-odds statistical baselines.
- [ ] Use chronological walk-forward evaluation.
- [x] Report log loss, Brier, accuracy, ROC AUC, and ROI only as simulated research metrics.
- [ ] Do not write active model_versions.



## Summary of Changes
- Added `ml.baselines`, a report-only evaluator for UFC experience, recent-form, younger-fighter, and market-favorite baselines.
- Evaluated baselines in chronological event order using point-in-time feature rows and historical market odds where matched.
- Generated `data/experiments/simple-baselines.json` and `data/experiments/simple-baselines.md` with log loss, Brier, accuracy, ROC AUC, and simulated research ROI.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.baselines --start-date 2024-02-01 --max-events 8 --output data/experiments/simple-baselines.json --markdown data/experiments/simple-baselines.md --stdout summary`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m pytest services/python/test_baselines.py -q`
- `services/python/.venv/bin/python -m compileall -q services/python/ml/baselines.py services/python/test_baselines.py`
