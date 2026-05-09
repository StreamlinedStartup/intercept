---
# intercept-1fhe
title: '2-F: Phase 2 verification + close epic'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T23:44:30Z
parent: intercept-8gxf
blocked_by:
    - intercept-zfc6
---

Verification per docs/ufc-fight-predictor-plan.md#phase-2.

- [x] curl localhost:3001/api/odds-mma/upcoming returns JSON with current MMA odds; X-Cache MISS then HIT
- [x] curl localhost:3001/api/odds-mma/snapshot writes rows; SELECT count from odds_snapshots > 0
- [x] Matcher logs matched/unmatched summary, and unmatched rows are persisted when canonical fights are absent
- [x] x-requests-remaining shows budget consumption
- [x] biome + typecheck + vitest green
- [x] Hand off to 2-Sm smoke gate (epic stays open until that passes)

## Summary of Changes

Verified the Phase 2 odds-mma slice against the live local API, TimescaleDB container, and the-odds-api response.

Evidence:

- `curl -i -sS 'http://127.0.0.1:3001/api/odds-mma/upcoming?refresh=1'` returned 200, `X-Cache: BYPASS`, `X-Odds-Requests-Remaining: 493`, and current MMA odds JSON.
- `curl -i -sS 'http://127.0.0.1:3001/api/odds-mma/upcoming'` returned 200 and `X-Cache: HIT`.
- `curl -i -sS 'http://127.0.0.1:3001/api/odds-mma/snapshot'` returned 200 with `rows_written: 275`, `matched_rows: 0`, `unmatched_logged: 53`, and `requests_remaining: "491"`.
- `SELECT count(*) FROM odds_snapshots WHERE snapshot_at > now() - interval '5 minutes';` returned 275.
- `SELECT count(*) FROM unmatched_odds WHERE created_at > now() - interval '5 minutes';` returned 53.
- `/tmp/interceptor-debug/debug-2026-05-09.log` included `matched 0 of 288 odds rows; 53 unmatched logged` and `x-requests-remaining=491`.
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm --filter @interceptor/api test`
- `pnpm typecheck`
- `pnpm test`
- `pnpm biome check domains/odds-mma/src/routes.ts domains/odds-mma/src/cache.ts domains/odds-mma/package.json apps/api/src/register-domains.ts apps/api/package.json packages/db/src/schema.ts packages/db/migrations/0003_unmatched_odds.sql packages/db/migrations/meta/_journal.json README.md .env.example`
