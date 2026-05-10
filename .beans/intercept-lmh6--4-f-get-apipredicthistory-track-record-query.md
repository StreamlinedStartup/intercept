---
# intercept-lmh6
title: '4-F: GET /api/predict/history (track-record query)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:25:41Z
parent: intercept-di4c
blocked_by:
    - intercept-oakk
---

Past predictions joined with actual results. Powers the /predictions page.

- [x] GET /api/predict/history?from=&to=&limit= joins predictions × fight_results × events × fighters
- [x] Returns rows: {fight_id, event_name, event_date, predicted_winner, predicted_winner_name, win_prob, market_prob, edge_pct, actual_winner_id, actual_winner_name, hit (bool), bet_pl_units (assuming 1u flat-bet on edge>5%)}
- [x] Returns aggregate header: {n_predictions, n_with_result, accuracy, log_loss, brier, n_bets, roi_units, roi_pct}
- [x] Curl test once Phase 1 has backfilled enough completed events with predictions

## Summary of Changes

- Added `GET /api/predict/history?from=&to=&limit=` with prediction/result/fighter/event joins.
- Returned per-prediction track-record rows with hit status, market probability, edge, and flat-bet P/L.
- Added aggregate metrics: prediction counts, completed-result count, accuracy, log loss, Brier score, bet count, ROI units, and ROI percent.

Verified:

- `curl -sS 'http://localhost:3001/api/predict/history?limit=5'` returned `n_predictions=5`, `n_with_result=1`, `accuracy=1`, `log_loss=0.4780358009429998`, `brier=0.1444`, plus a completed UFC 328 row for Khamzat Chimaev with `hit=true`.
- `pnpm --filter @interceptor/api typecheck`
- `pnpm biome check --write apps/api/src/routes/predict.ts .beans/intercept-lmh6--4-f-get-apipredicthistory-track-record-query.md`
