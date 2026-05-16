---
# intercept-ely2
title: 'PCS-C: Report expanded prop coverage readiness'
status: completed
type: task
priority: high
created_at: 2026-05-16T01:13:34Z
updated_at: 2026-05-16T02:12:13Z
parent: intercept-fmpi
blocked_by:
    - intercept-ss4t
---

Acceptance criteria:
- [x] Run the FightOdds prop coverage report after corpus import.
- [x] Publish updated JSON/Markdown artifacts.
- [x] State whether decision/finish baselines have enough coverage for market-opportunity analysis.
- [x] Preserve timestamp and research-only limitations.

## Summary of Changes

- Regenerated the FightOdds prop coverage JSON and Markdown artifacts after the expanded DISTANCE import.
- Coverage now spans 31 source events, 398 distance markets, and 15,215 prop rows, with 12,379 rows linked to canonical fights.
- Marked decision/finish prop baselines as research-useful but not production-ready because canonical prop-row linking is 81.4%, not complete.
