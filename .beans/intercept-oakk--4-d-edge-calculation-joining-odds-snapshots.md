---
# intercept-oakk
title: '4-D: Edge calculation joining odds_snapshots'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-pct4
---

Compare model probability to market implied probability. Show edge.

- [ ] /api/predict/fight/:id route: also query latest odds_snapshots for this fight_id (join on fighter_id), pick best decimal_odds per fighter
- [ ] Compute market_implied_prob = 1/decimal_odds (or vig-adjusted: prob_a / (prob_a + prob_b))
- [ ] edge_pct = win_prob - market_implied_prob
- [ ] Return {decimal_odds, american_odds, market_prob, edge_pct} alongside the prediction
- [ ] CompareSheet shows an Edge badge: green if model agrees with market AND |edge| > 5%, red if model disagrees with market, neutral otherwise
- [ ] If no odds available yet: omit edge UI silently
