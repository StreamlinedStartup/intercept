---
# intercept-9bfq
title: '2-A: domain scaffold + cache copy'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T21:26:23Z
parent: intercept-8gxf
blocked_by:
    - intercept-o6xw
---

Scaffold the domain plugin shell — no real network calls yet. Reuse the existing scaffolder.

- [x] bash .claude/skills/api-discovery/scripts/scaffold-domain.sh odds-mma the-odds-api.com
- [x] domains/odds-mma/src/cache.ts copied + adapted from domains/ufcstats/src/cache.ts (buckets: oddsList=1h, oddsHistorical=1y)
- [x] domains/odds-mma/src/config.ts: interceptPatterns matching the-odds-api
- [x] Register as workspace dep in apps/api/package.json
- [x] pnpm install + typecheck + biome green

## Summary of Changes

Scaffolded the odds-mma domain plugin, added the odds cache helper, wired the package into the API workspace dependency graph, and registered the domain with a 5/min rate limit for the-odds-api.

Verification:
- bash .claude/skills/api-discovery/scripts/scaffold-domain.sh odds-mma the-odds-api.com
- CI=true pnpm install --no-frozen-lockfile
- pnpm --filter @interceptor/api typecheck
- pnpm biome check domains/odds-mma apps/api/src/register-domains.ts apps/api/package.json
