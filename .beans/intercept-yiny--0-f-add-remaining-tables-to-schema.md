---
# intercept-yiny
title: '0-F: Add remaining tables to schema'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:34:57Z
parent: intercept-3fqo
blocked_by:
    - intercept-nuwf
---

Expand schema.ts with the other 7 tables. Generate + apply a second migration.

- [x] fights, fight_results, fight_round_stats
- [x] fighter_backfill_state (status enum: none/current/stale_count/stale_stats/in_progress/failed)
- [x] fighter_stat_snapshots (regular table for now; hypertable in 0-G)
- [x] odds_snapshots (regular for now)
- [x] predictions (regular for now)
- [x] model_versions
- [x] drizzle-kit generate + migrate runs clean
- [x] Smoke script extended to insert one row of each, query back

## Summary of Changes

- `packages/db/src/schema.ts` — added 8 tables and 2 enums:
  - `backfillStatusEnum` (none/current/stale_count/stale_stats/in_progress/failed)
  - `outcomeEnum` (win/loss/draw/nc)
  - `fighter_backfill_state` (PK fighter_id → fighters)
  - `fighter_stat_snapshots` (composite PK fighter_id+snapshot_at; will become a hypertable in 0-G)
  - `fights` (PK id, FK event_id)
  - `fight_results` (composite PK fight_id+fighter_id, FKs to fights/fighters)
  - `fight_round_stats` (composite PK fight_id+fighter_id+round)
  - `odds_snapshots` (composite PK fighter_id+snapshot_at+bookmaker — supports the same fighter at multiple bookmakers and through time; will become a hypertable in 0-G)
  - `model_versions` (PK string id)
  - `predictions` (composite PK fight_id+model_version+predicted_at; will become a hypertable in 0-G)
- New migration `migrations/0001_open_dragon_man.sql` generated and applied. `\dt` shows 10 tables.
- `packages/db/src/smoke.ts` — extended to insert and round-trip read all 10 tables, exits with `[smoke] ok — all 10 tables round-tripped`.
- Drizzle prints deprecation warnings on the callback-form `extraConfig` for composite PKs (TS6387). Deferred — non-blocking, would touch every composite-PK table; can migrate to the array form when drizzle-orm is upgraded.
