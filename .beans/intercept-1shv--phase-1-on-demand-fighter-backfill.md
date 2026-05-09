---
# intercept-1shv
title: 'Phase 1: On-demand fighter backfill'
status: completed
type: epic
priority: high
created_at: 2026-05-09T18:55:13Z
updated_at: 2026-05-09T22:17:25Z
parent: intercept-7c8e
blocked_by:
    - intercept-3fqo
---

Per-fighter backfill from /upcoming UI. State machine: none|current|stale_count|stale_stats|in_progress|failed. In-process worker (no scheduler). Admin seed buttons.

## Summary of Changes

Phase 1 is complete. It ships the on-demand fighter backfill slice from the
upcoming fight UI through API jobs into Postgres, stale-count detection,
compare-sheet state rendering, and admin seed controls for in-window, PPV
five-year, and all-UFC five-year bootstrap paths.

Verification:

- Phase verification completed in intercept-bgxt.
- Browser smoke gate completed in intercept-5cmh.
- Smoke screenshots committed under `data/smoke/`.
