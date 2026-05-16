---
# intercept-qh8w
title: Scheduled market indicator refresh and promotion pipeline
status: todo
type: epic
priority: high
created_at: 2026-05-16T05:57:58Z
updated_at: 2026-05-16T05:57:58Z
parent: intercept-8mw9
---

Build the report-only operating pipeline for market indicators. Scope: materialize upcoming fight indicators, refresh them on a repeatable cadence, track post-event outcomes, and keep retrained artifacts behind explicit validation and promotion gates. No automated betting activation.

Acceptance criteria:
- [ ] Materialized indicator snapshot design exists for report-only prop signals.
- [ ] Upcoming indicator refresh command/job is scoped.
- [ ] UI snapshot-read behavior is scoped.
- [ ] Daily maintenance cadence is scoped.
- [ ] Weekly post-event evaluation cadence is scoped.
- [ ] Retrain/promote gate is scoped with manual promotion only.
- [ ] Smoke and operator verification closeout is scoped.
