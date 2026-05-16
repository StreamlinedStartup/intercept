---
# intercept-vv4w
title: 'SIR-A: Indicator snapshot schema'
status: todo
type: task
created_at: 2026-05-16T05:58:03Z
updated_at: 2026-05-16T05:58:03Z
parent: intercept-qh8w
---

Design and add the materialized snapshot schema for report-only market indicators.

Acceptance criteria:
- [ ] Add a table or equivalent persisted shape for indicator snapshots keyed by fight, target, and model version.
- [ ] Store model_probability, market_probability, edge_pct, candidate, market_pair_count, value_status, computed_at, and enough source/version metadata to reason about staleness.
- [ ] Keep the schema report-only: no automated betting activation fields and no prop prediction writes.
- [ ] Include migration/tests or schema verification appropriate to the DB package.
