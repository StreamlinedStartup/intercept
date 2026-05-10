---
# intercept-dwtm
title: '0-C: Schema for events + fighters (the smallest pair)'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:32:21Z
parent: intercept-3fqo
blocked_by:
    - intercept-dvmr
---

Define just the two foundational tables in packages/db/src/schema.ts. Skip the other 7 — those come in 0-F.

- [x] events table (id 16-hex pk, name, date, location, completed bool, promotion enum)
- [x] fighters table (id 16-hex pk, name, nickname, dob, height_in, reach_in, stance)
- [x] Generate first migration via drizzle-kit generate

## Summary of Changes

- `packages/db/src/schema.ts` — `promotionEnum` (`ufc|bellator|strikeforce|other`), `events` table (varchar(16) pk, name text, date, location text nullable, completed bool default false, promotion enum default ufc), `fighters` table (varchar(16) pk, name, nickname, dob, height_in real, reach_in real, stance, history_count integer default 0 — added beyond plan because the Phase 1 stale-count detection in the plan reads this off the fighters row).
- `packages/db/src/index.ts` — re-exports schema.
- First migration generated: `packages/db/migrations/0000_perfect_yellow_claw.sql` plus drizzle's `meta/` snapshot. Two tables + one enum, no FKs/indexes (those come with the relational tables in 0-F).
- `pnpm --filter @interceptor/db typecheck` clean.
