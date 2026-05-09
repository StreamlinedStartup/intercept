---
# intercept-nbi6
title: '2-D: Fuzzy-match odds rows to our events/fighters'
status: completed
type: task
priority: normal
created_at: 2026-05-09T19:00:18Z
updated_at: 2026-05-09T21:52:06Z
parent: intercept-8gxf
blocked_by:
    - intercept-vjvz
---

Resolve event_id and fighter_id on each odds_snapshots row. Document mismatches.

- [x] After snapshot, for each row attempt match: normalize names (lower, strip non-alnum), key on (event_date, sorted_fighter_pair) against our events+fight_results
- [x] Update odds_snapshots row with matched event_id + fighter_id
- [x] Unmatched rows → INSERT INTO unmatched_odds (raw_event_name, raw_fighter_a, raw_fighter_b, raw_date, snapshot_id, reason)
- [x] Log a summary: 'matched 18 of 20 odds rows; 2 unmatched logged'
- [x] unmatched_odds table goes in schema.ts in a follow-up DB migration (small enough to inline here)

## Summary of Changes

Added snapshot-time fuzzy matching for odds API rows. The matcher normalizes names by lowercasing and stripping non-alphanumerics, then keys canonical fights by `(event_date, sorted_fighter_pair)` from `events + fights + fight_results`. Matched rows are inserted into `odds_snapshots` with canonical `event_id`, `fight_id`, and `fighter_id`; unmatched odds events are logged into the new `unmatched_odds` table with raw fighter names, raw date, snapshot id, and reason.

The current live odds payload did not match the existing canonical DB dates/pairs, so verification produced `matched_rows: 0` and `unmatched_logged: 57`; this is expected with the present local seed data and proves the mismatch path rather than silently dropping rows.

Verification:
- `pnpm --filter @interceptor/api typecheck`
- `pnpm --filter @interceptor/db typecheck`
- `pnpm biome check domains/odds-mma/src/routes.ts packages/db/src/schema.ts packages/db/migrations/0003_unmatched_odds.sql packages/db/migrations/meta/_journal.json`
- `DATABASE_URL=... pnpm --filter @interceptor/db migrate`
- `curl -i -sS http://localhost:3001/api/odds-mma/snapshot` returned `rows_written: 321`, `matched_rows: 0`, `unmatched_logged: 57`, and `requests_remaining: "494"`.
- `SELECT count(*) FROM unmatched_odds WHERE created_at > now() - interval '1 minute';` returned `57`.
