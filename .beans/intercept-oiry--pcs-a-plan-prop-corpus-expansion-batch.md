---
# intercept-oiry
title: 'PCS-A: Plan prop corpus expansion batch'
status: completed
type: task
priority: high
created_at: 2026-05-16T01:13:22Z
updated_at: 2026-05-16T01:14:29Z
parent: intercept-fmpi
---

Acceptance criteria:
- [x] Identify the existing matched FightOdds event cohort to use for prop import.
- [x] Define a safe import command and batch size/delay policy.
- [x] Record expected coverage and report-only constraints.
- [x] Commit a compact planning artifact before running the large import.

## Summary of Changes

- Identified the existing 81-event matched FightOdds corpus in Postgres.
- Confirmed current prop coverage is only one event with 12 distance markets and 294 prop rows.
- Published `data/experiments/harness/prop-corpus-expansion-plan.md` with the import command, delay policy, and report-only constraints.
