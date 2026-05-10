---
# intercept-jigh
title: '0-G: Convert timeseries tables to TimescaleDB hypertables'
status: completed
type: task
priority: normal
created_at: 2026-05-09T18:55:52Z
updated_at: 2026-05-09T19:36:47Z
parent: intercept-3fqo
blocked_by:
    - intercept-yiny
---

Drizzle migrations don't model create_hypertable(). Add a post-migration step in migrate.ts.

- [x] migrate.ts runs drizzle migrations, then SELECT create_hypertable('fighter_stat_snapshots', by_range('snapshot_at')) for each timeseries table — idempotent (ignore 'already a hypertable')
- [x] Hypertables: fighter_stat_snapshots, odds_snapshots, predictions
- [x] \d <table> in psql shows the hypertable indicator
- [x] Smoke script still passes

## Summary of Changes

- `packages/db/src/migrate.ts` — after `migrate()` runs, iterates over `[(fighter_stat_snapshots, snapshot_at), (odds_snapshots, snapshot_at), (predictions, predicted_at)]` and calls `SELECT create_hypertable(<table>::regclass, by_range(<col>::name), if_not_exists => TRUE, migrate_data => TRUE)`. `if_not_exists` makes it idempotent — second run logs `(N, f)` where `f` = false (no-op) instead of failing.
- Verified `migrate_data => TRUE` because the smoke had already inserted rows during 0-F; without it the conversion would fail on a non-empty table.
- `\dt` style verification: `SELECT hypertable_name, num_chunks FROM timescaledb_information.hypertables` returns the three expected rows.
- Smoke run after conversion still prints `[smoke] ok — all 10 tables round-tripped`.

~~Note: TimescaleDB emits `WARNING: column type "character varying" used for "<id_col>" does not follow best practices` for several FK/PK columns. Logged but not acted on.~~

**Update (same session):** the warnings were addressed in migration `0002_bouncy_bloodaxe.sql`. All 18 ID columns (`varchar(16|32)` → `text`) were converted with idempotent `ALTER COLUMN ... SET DATA TYPE text`. Verified on a wiped + re-migrated DB: zero `character varying` warnings in the postgres logs (only unrelated locale init notices remain). Smoke still round-trips all 10 tables; all 3 hypertables still present.
