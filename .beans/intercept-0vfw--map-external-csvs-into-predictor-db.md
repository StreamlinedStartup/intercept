---
# intercept-0vfw
title: Map external CSVs into predictor DB
status: completed
type: task
priority: normal
created_at: 2026-05-11T00:24:42Z
updated_at: 2026-05-11T00:47:44Z
parent: intercept-r03n
blocked_by:
    - intercept-n89z
---

Build an importer that parses the external CSV snapshot and upserts canonical events, fighters, fights, fight_results, fight_round_stats, and fighter_backfill_state rows for training/backtesting.



## Summary of Changes

- Added `pnpm --filter @interceptor/db import:ufcstats <snapshot-dir>` for external UFC Stats CSV snapshots.
- Importer validates snapshot metadata hashes, derives UFC Stats IDs from URLs, parses CSVs, and upserts events, fighters, fights, fight_results, fight_round_stats, and fighter_backfill_state.
- Added explicit ambiguous-row handling for duplicate fighter names and ambiguous fight-stat keys, with skipped-row counts in command output.
- Documented the import command and skipped-row behavior in `docs/external_ufcstats_dataset.md`.

## Verification

- `pnpm --filter @interceptor/db typecheck`
- `pnpm biome check packages/db/src/import-ufcstats-snapshot.ts packages/db/package.json docs/external_ufcstats_dataset.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:ufcstats data/external/ufcstats/codex-verify-n89z-2`
- Import summary: 773 events, 4,491 fighters, 8,686 fights, 17,372 fight_results, 40,874 fight_round_stats, 2,689 fighter_backfill_state rows, 2 skipped ambiguous fight rows, 58 skipped fight-stat rows.
- DB count query confirmed canonical tables populated; local DB includes prior rows, total counts were 785 events, 4,587 fighters, 8,744 fights, 17,488 fight_results, 40,889 fight_round_stats, and 2,691 current backfill states.
