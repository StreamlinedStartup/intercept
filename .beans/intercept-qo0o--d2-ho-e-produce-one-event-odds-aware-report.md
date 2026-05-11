---
# intercept-qo0o
title: 'D2-HO-E: Produce one-event odds-aware report'
status: todo
type: task
created_at: 2026-05-11T17:12:00Z
updated_at: 2026-05-11T17:12:00Z
parent: intercept-5rw9
blocked_by:
    - intercept-gopa
---

Acceptance criteria:
- [ ] Join walk-forward model predictions for UFC Fight Night 237 / Moreno vs Royval 2 to matched historical moneyline odds.
- [ ] Convert American odds to implied probability.
- [ ] Remove vig when both sides of a bout are available.
- [ ] Compute edge as model probability minus no-vig market probability.
- [ ] Simulate flat-stake ROI for model-edge selections and market-favorite baseline.
- [ ] Include confidence buckets, edge buckets, and calibration versus market for the event where sample size allows.
- [ ] Label odds timestamp semantics honestly, including whether lines represent close/current rather than true point-in-time snapshots.
- [ ] Keep accuracy, log loss, Brier score, and ROC AUC as secondary context only.

Verification:
- Produce a tiny event report under data/experiments/ or data/backtests/ with JSON plus Markdown when useful.
- Unit tests cover implied probability, no-vig normalization, edge, and flat-stake payout math.
- Report command is repeatable from the imported one-event data.
