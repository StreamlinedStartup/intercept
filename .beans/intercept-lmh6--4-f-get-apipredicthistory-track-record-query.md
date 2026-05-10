---
# intercept-lmh6
title: '4-F: GET /api/predict/history (track-record query)'
status: todo
type: task
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-09T19:14:44Z
parent: intercept-di4c
blocked_by:
    - intercept-oakk
---

Past predictions joined with actual results. Powers the /predictions page.

- [ ] GET /api/predict/history?from=&to=&limit= joins predictions × fight_results × events × fighters
- [ ] Returns rows: {fight_id, event_name, event_date, predicted_winner, predicted_winner_name, win_prob, market_prob, edge_pct, actual_winner_id, actual_winner_name, hit (bool), bet_pl_units (assuming 1u flat-bet on edge>5%)}
- [ ] Returns aggregate header: {n_predictions, n_with_result, accuracy, log_loss, brier, n_bets, roi_units, roi_pct}
- [ ] Curl test once Phase 1 has backfilled enough completed events with predictions
