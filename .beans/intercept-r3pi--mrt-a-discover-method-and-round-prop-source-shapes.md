---
# intercept-r3pi
title: 'MRT-A: Discover method and round prop source shapes'
status: completed
type: task
priority: normal
created_at: 2026-05-16T02:46:25Z
updated_at: 2026-05-16T02:52:19Z
parent: intercept-v41p
---

Acceptance criteria:
- [x] Inspect imported FightOdds prop rows for method, KO/TKO, submission, decision, and round/total labels.
- [x] Identify which source offer types and market families can support each requested target.
- [x] Publish a concise source-shape note for implementation.

## Summary of Changes

- Published `data/experiments/harness/method-round-prop-source-shapes.md`.
- Confirmed `DISTANCE` supports decision and finish, fight-level method odds support KO/TKO and submission distributions, and `OVERUNDER_*` supports round totals.
- Marked fighter-specific method and exact-round props as out of this slice because the source shape is sparse/single-sided.
