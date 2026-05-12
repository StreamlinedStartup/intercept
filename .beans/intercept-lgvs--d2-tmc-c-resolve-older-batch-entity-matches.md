---
# intercept-lgvs
title: 'D2-TMC-C: Resolve older batch entity matches'
status: completed
type: task
priority: high
created_at: 2026-05-12T04:23:49Z
updated_at: 2026-05-12T04:33:22Z
parent: intercept-ftbt
blocked_by:
    - intercept-on0t
---

Acceptance criteria:
- [x] Run deterministic matching/rematch tooling for the imported older batch.
- [x] Improve or extend event/fight alias handling only where needed for the older batch.
- [x] Keep unresolved rows reportable with explicit reasons.
- [x] Verify no regression on the existing 37-event corpus.

## Summary of Changes

- Added a deterministic participant-overlap event fallback for same-date UFC events with changed FightOdds headlines.
- Added a `Dontale Mayes` / `Don'Tale Mayes` alias used by normalized participant matching.
- Reran `match:fightodds:all`; all 51 FightOdds events now match, including 14/14 in the older target batch.
- Published `data/experiments/trainable-market-corpus-match-summary.json` and `.md` with review reasons and regression evidence.

## Verification

- `pnpm biome check --write packages/db/src/match-historical-odds.ts packages/db/src/match-historical-odds-core.ts packages/db/src/match-historical-odds.test.ts`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db test`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db match:fightodds:all`
- `jq empty data/experiments/trainable-market-corpus-match-summary.json`
