---
# intercept-oakk
title: '4-D: Edge calculation joining odds_snapshots'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:14:44Z
updated_at: 2026-05-10T18:22:12Z
parent: intercept-di4c
blocked_by:
    - intercept-pct4
---

Compare model probability to market implied probability. Show edge.

- [x] /api/predict/fight/:id route: also query latest odds_snapshots for this fight_id (join on fighter_id), pick best decimal_odds per fighter
- [x] Compute market_implied_prob = 1/decimal_odds (or vig-adjusted: prob_a / (prob_a + prob_b))
- [x] edge_pct = win_prob - market_implied_prob
- [x] Return {decimal_odds, american_odds, market_prob, edge_pct} alongside the prediction
- [x] CompareSheet shows an Edge badge: green if model agrees with market AND |edge| > 5%, red if model disagrees with market, neutral otherwise
- [x] If no odds available yet: omit edge UI silently

## Summary of Changes

- Added latest-snapshot odds lookup to prediction responses, selecting the best decimal odds per fighter and vig-adjusting market probability.
- Persisted `edge_pct` on prediction rows when odds are available and returned `odds`, `market_prob`, and `edge_pct` in the API response.
- Added an edge badge to the compare sheet model-pick panel while keeping no-odds fights visually unchanged.

Verified:

- Temporary `codex-smoke` odds rows for Allen/Costa produced `edge_pct=0.12626690864562986` and `market_prob=0.55`; screenshot showed `Edge +13%`.
- Removed temporary `codex-smoke` odds rows after verification; remaining count is `0`.
- `curl -sS http://localhost:3001/api/predict/fight/e4aa608124896794` after cleanup omitted odds/edge fields silently.
- `agent-browser screenshot data/smoke/phase4-oakk-edge-badge.png`
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/web typecheck`
- `pnpm biome check apps/api/src/routes/predict.ts apps/web/src/app/'(dashboard)'/upcoming/compare-sheet.tsx`
