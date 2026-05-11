---
# intercept-qo0o
title: 'D2-HO-E: Produce one-event odds-aware report'
status: completed
type: task
created_at: 2026-05-11T17:12:00Z
updated_at: 2026-05-11T18:31:00Z
parent: intercept-5rw9
blocked_by:
    - intercept-gopa
---

Acceptance criteria:
- [x] Join walk-forward model predictions for UFC Fight Night 237 / Moreno vs Royval 2 to matched historical moneyline odds.
- [x] Convert American odds to implied probability.
- [x] Remove vig when both sides of a bout are available.
- [x] Compute edge as model probability minus no-vig market probability.
- [x] Simulate flat-stake ROI for model-edge selections and market-favorite baseline.
- [x] Include confidence buckets, edge buckets, and calibration versus market for the event where sample size allows.
- [x] Label odds timestamp semantics honestly, including whether lines represent close/current rather than true point-in-time snapshots.
- [x] Keep accuracy, log loss, Brier score, and ROC AUC as secondary context only.

Verification:
- Produce a tiny event report under data/experiments/ or data/backtests/ with JSON plus Markdown when useful.
- Unit tests cover implied probability, no-vig normalization, edge, and flat-stake payout math.
- Report command is repeatable from the imported one-event data.

## Summary of Changes

- Added `services/python/ml/odds_aware_report.py`, which regenerates one-event walk-forward predictions for UFC Fight Night: Moreno vs. Royval 2, joins them to matched FightOdds `source_current` moneylines, no-vig normalizes paired sportsbook offers, computes model edge, and simulates flat-stake ROI.
- Added `data/experiments/odds-aware-one-event.json` and `data/experiments/odds-aware-one-event.md` evidence. The report scored 12 fights, 310 current moneyline rows, and 155 complete offer pairs; model-edge selections were 0-6 for -100.0% ROI and market favorites were 10-12 for +31.4% ROI.
- Wired `pnpm --filter @interceptor/db report:odds-aware:event` as the repeatable operator command and added odds math unit coverage.

Verification:
- `services/python/.venv/bin/python -m pytest services/python/test_odds_aware_report.py -q`
- `pnpm --filter @interceptor/db typecheck`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db report:odds-aware:event`
- `pnpm --filter @interceptor/db test`
