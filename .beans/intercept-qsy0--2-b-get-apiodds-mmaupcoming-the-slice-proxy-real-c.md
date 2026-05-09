---
# intercept-qsy0
title: '2-B: GET /api/odds-mma/upcoming (THE SLICE — proxy real call)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T21:37:36Z
parent: intercept-8gxf
blocked_by:
    - intercept-9bfq
---

Make one round-trip to the-odds-api and return the JSON. Read API key from env.

- [x] Add ODDS_API_KEY to .env.example
- [x] domains/odds-mma/src/routes.ts with GET /upcoming
- [x] Route calls https://api.the-odds-api.com/v4/sports/mma_mixed_martial_arts/odds?regions=us&markets=h2h&apiKey=ODDS_API_KEY via rateLimitedFetch
- [x] Cache 1h via the cache.ts pattern (X-Cache: HIT/MISS/BYPASS, Cache-Control header)
- [x] Register rate limit in apps/api/src/register-domains.ts: api.the-odds-api.com {maxPerMinute:5, retryOn429:1}
- [x] curl test returns JSON with current MMA odds; second curl is HIT
- [x] Log x-requests-remaining response header so we can track budget

## Summary of Changes

Added `GET /api/odds-mma/upcoming` as a direct `rateLimitedFetch` route to the-odds-api MMA odds endpoint, reading `ODDS_API_KEY` from env, caching successful responses for 1 hour, and returning `X-Cache` plus `Cache-Control` headers. Added the env key to `.env.example`, set the API rate limit to 5/min with one 429 retry, and logged the upstream `x-requests-remaining` header via `DEBUG`.

Verification:
- `pnpm --filter @interceptor/api typecheck`
- `pnpm biome check domains/odds-mma/src/routes.ts apps/api/src/register-domains.ts .env.example`
- `curl -i -sS 'http://localhost:3001/api/odds-mma/upcoming?refresh=1'` returned `200`, `X-Cache: BYPASS`, and current MMA odds JSON.
- `curl -i -sS http://localhost:3001/api/odds-mma/upcoming` returned `200` and `X-Cache: HIT`.
- API logs showed `x-requests-remaining=498`.
