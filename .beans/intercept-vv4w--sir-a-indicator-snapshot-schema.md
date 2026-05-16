---
# intercept-vv4w
title: 'SIR-A: Indicator snapshot schema'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:58:03Z
updated_at: 2026-05-16T13:57:10Z
parent: intercept-qh8w
---

Design and add the materialized snapshot schema for report-only market indicators.

Acceptance criteria:
- [x] Add a table or equivalent persisted shape for indicator snapshots keyed by fight, target, and model version.
- [x] Store model_probability, market_probability, edge_pct, candidate, market_pair_count, value_status, computed_at, and enough source/version metadata to reason about staleness.
- [x] Keep the schema report-only: no automated betting activation fields and no prop prediction writes.
- [x] Include migration/tests or schema verification appropriate to the DB package.

## Summary of Changes

- Added `market_indicator_snapshots` as a report-only materialized indicator table keyed by fight, target, model version, indicator name, and computed timestamp.
- Stored model/market probability, edge, candidate status, market pair count, value status, source metadata, and staleness context without adding betting activation fields or prediction writes.
- Added a focused DB schema test and verified the DB package test/typecheck gates.
