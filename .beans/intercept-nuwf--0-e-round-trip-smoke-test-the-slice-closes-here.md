---
# intercept-nuwf
title: '0-E: Round-trip smoke test (the slice closes here)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:34:00Z
parent: intercept-3fqo
blocked_by:
    - intercept-ittn
---

Prove the slice works end-to-end: insert one event + one fighter, query them back, type-checked.

- [x] packages/db/src/smoke.ts script: connect, insert UFC 328 event + Khamzat row, SELECT back, console.log results, exit 0
- [x] `pnpm --filter @interceptor/db smoke` runs green
- [x] Document in package README how to run the smoke
- [x] At this point Phase 0 is technically usable — everything after is expansion.

## Smoke output

```
[smoke] event: { id: '9eedac48b497de5a', name: 'UFC 328', date: '2026-05-31', ... }
[smoke] fighter: { id: '767755fd74662dbf', name: 'Khamzat Chimaev', nickname: 'Borz', ... }
[smoke] ok
```

## Summary of Changes

- `packages/db/src/smoke.ts` — inserts UFC 328 (`9eedac48b497de5a`) + Khamzat Chimaev (`767755fd74662dbf`) with `onConflictDoNothing`, reads each back via Drizzle, throws on mismatch, logs `[smoke] ok` on success. Idempotent so it can be re-run.
- `packages/db/package.json` — `smoke` script (`tsx src/smoke.ts`).
- `packages/db/README.md` — documents `docker compose up`, env var, `migrate`, `smoke`, and the host port 5434 rationale.

The vertical slice (Docker → schema → migration → typed client → DB round-trip) is closed. Remaining Phase 0 work is expansion: the other 7 tables, hypertables, and wiring `DATABASE_URL` into the API startup path.
