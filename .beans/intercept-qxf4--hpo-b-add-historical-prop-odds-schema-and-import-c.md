---
# intercept-qxf4
title: 'HPO-B: Add historical prop odds schema and import contract'
status: completed
type: task
priority: high
created_at: 2026-05-15T23:18:56Z
updated_at: 2026-05-15T23:25:02Z
parent: intercept-1xpw
blocked_by:
    - intercept-6us4
---

Acceptance criteria:
- [x] Add dedicated historical prop odds table or schema extension separate from odds_snapshots.
- [x] Preserve source event/fight/market/outcome identity and raw metadata.
- [x] Keep line_kind semantics source_current/source_previous only unless timestamps are proven.
- [x] Add migration and TypeScript schema coverage.

## Summary of Changes

- Added `historical_prop_odds` to the Drizzle schema as a dedicated historical prop table separate from `odds_snapshots`.
- Added migration `0005_historical_prop_odds` with source event, fight, market, offer, outcome, sportsbook, line, and raw metadata fields.
- Verified the migration creates the table and preserves nullable market timestamp semantics for source-current/source-previous rows.
