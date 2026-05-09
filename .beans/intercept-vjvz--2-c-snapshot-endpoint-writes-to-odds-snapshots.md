---
# intercept-vjvz
title: '2-C: Snapshot endpoint writes to odds_snapshots'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T21:47:51Z
parent: intercept-8gxf
blocked_by:
    - intercept-qsy0
---

Persist a point-in-time row. Bookmaker × fighter × snapshot_at.

- [x] GET /api/odds-mma/snapshot: same fetch as /upcoming, then for each event×bookmaker×outcome → INSERT INTO odds_snapshots
- [x] decimal_odds + american_odds (compute one from the other)
- [x] event_id and fight_id left NULL initially — matched in 2-D
- [x] Returns {snapshot_id, rows_written, requests_remaining}
- [x] Verify: SELECT count(*) FROM odds_snapshots WHERE snapshot_at > now() - interval '1 minute' returns >0

## Summary of Changes

Added `GET /api/odds-mma/snapshot`, which fetches current MMA moneyline odds, creates deterministic placeholder fighter rows for odds API names, and writes one `odds_snapshots` row per fighter/bookmaker/outcome with `event_id` and `fight_id` left null for the follow-up matching task. Decimal odds are persisted directly and American odds are derived from them, with decimal `1` capped to a finite American value so the full snapshot does not fail on floor-priced outcomes.

Verification:
- `pnpm install`
- `pnpm --filter @interceptor/api typecheck`
- `pnpm biome check domains/odds-mma/src/routes.ts domains/odds-mma/package.json pnpm-lock.yaml`
- `curl -i -sS http://localhost:3001/api/odds-mma/snapshot` returned `200` with `rows_written: 321` and `requests_remaining: "495"`.
- `SELECT count(*) FROM odds_snapshots WHERE snapshot_at > now() - interval '1 minute';` returned `321`.
