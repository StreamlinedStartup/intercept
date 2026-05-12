---
# intercept-pxkt
title: 'D2-RV-E: Market baseline and blend report'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:23Z
updated_at: 2026-05-12T01:24:02Z
parent: intercept-dmyw
blocked_by:
    - intercept-fxof
    - intercept-aeef
---

Gate validated value status behind market baseline and blend reporting.

Acceptance criteria:
- [x] Compare model, market baseline, and simple blends on matched historical odds.
- [x] Report calibration, ROI, Brier/log loss, and coverage with clear sample sizes.
- [x] Keep value_status at research_only or insufficient_coverage unless validation criteria pass.
- [x] Do not write active model_versions.

## Summary of Changes
- Added a report-only market gate harness at `services/python/ml/market_gate_report.py`.
- Compared the leak-free UFC experience model baseline, the no-vig market favorite, and three model/market blends on matched FightOdds coverage.
- Generated `data/experiments/market-gate-report.json` and `data/experiments/market-gate-report.md`; current status is `insufficient_coverage` with 30 scored fights across 3 events.

## Verification
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.market_gate_report --output data/experiments/market-gate-report.json --markdown data/experiments/market-gate-report.md --stdout summary`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m pytest services/python/test_market_gate_report.py -q`
- `services/python/.venv/bin/python -m compileall -q services/python/ml/market_gate_report.py services/python/test_market_gate_report.py`
