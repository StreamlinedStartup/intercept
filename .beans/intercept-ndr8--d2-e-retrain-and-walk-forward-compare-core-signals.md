---
# intercept-ndr8
title: 'D2-E: Retrain and walk-forward compare core signals'
status: completed
type: task
priority: high
created_at: 2026-05-11T13:31:02Z
updated_at: 2026-05-11T14:05:05Z
parent: intercept-7c3e
blocked_by:
    - intercept-c483
---

Acceptance criteria:
- [x] Retrain with the core signal features.
- [x] Run walk-forward backtest comparison.
- [x] Update docs with observed metric deltas; metric lift is reported, not required for merge.
- [x] Update this bean with verification evidence before completion.


## Summary of Changes
- Retrained the expanded Decision Engine v2 feature set into local model 20260511T134646095031Z.
- Ran a 20-event walk-forward backtest from 2024-01-01 and wrote local artifact data/backtests/decision-engine-v2-core-signals.json.
- Updated docs/model_scope.md with current model metrics, previous-model deltas, and walk-forward results.

## Verification
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.train
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --start-date 2024-01-01 --max-events 20 --min-train-samples 200 --output data/backtests/decision-engine-v2-core-signals.json
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -c "from ml.predict import list_models; import json; print(json.dumps(list_models(5), default=str, indent=2))"
- rg -n "20260511T134646095031Z|Decision Engine v2 Core Signals|Walk-Forward Backtest|avg_ending_round_diff|common_opponent_count" docs/model_scope.md data/backtests/decision-engine-v2-core-signals.json
