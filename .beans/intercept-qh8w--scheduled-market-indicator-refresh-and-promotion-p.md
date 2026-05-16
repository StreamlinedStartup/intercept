---
# intercept-qh8w
title: Scheduled market indicator refresh and promotion pipeline
status: completed
type: epic
priority: high
created_at: 2026-05-16T05:57:58Z
updated_at: 2026-05-16T05:57:58Z
parent: intercept-8mw9
---

Build the report-only operating pipeline for market indicators. Scope: materialize upcoming fight indicators, refresh them on a repeatable cadence, track post-event outcomes, and keep retrained artifacts behind explicit validation and promotion gates. No automated betting activation.

Acceptance criteria:
- [x] Materialized indicator snapshot design exists for report-only prop signals.
- [x] Upcoming indicator refresh command/job is scoped.
- [x] UI snapshot-read behavior is scoped.
- [x] Daily maintenance cadence is scoped.
- [x] Weekly post-event evaluation cadence is scoped.
- [x] Retrain/promote gate is scoped with manual promotion only.
- [x] Smoke and operator verification closeout is scoped.

## Summary of Changes

- Added report-only `market_indicator_snapshots`, upcoming refresh, daily maintenance, weekly evaluation, and manual promotion gate surfaces.
- Switched Over 2.5 product responses to snapshot-backed indicators with explicit missing/stale states.
- Verified focused tests, typechecks, dry-run operator command, live DB refresh/evaluation commands, and agent-browser `/upcoming` smoke evidence.
