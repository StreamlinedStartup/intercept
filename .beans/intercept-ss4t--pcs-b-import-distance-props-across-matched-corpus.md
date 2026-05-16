---
# intercept-ss4t
title: 'PCS-B: Import DISTANCE props across matched corpus'
status: completed
type: task
priority: high
created_at: 2026-05-16T01:13:29Z
updated_at: 2026-05-16T02:10:19Z
parent: intercept-fmpi
blocked_by:
    - intercept-oiry
---

Acceptance criteria:
- [x] Run the FightOdds importer with --include-props across the selected historical event cohort.
- [x] Capture import counts and skipped-market reasons.
- [x] Verify idempotent prop rows and linked canonical fights.
- [x] Do not change moneyline import semantics.

## Summary of Changes

- Optimized the FightOdds prop query to fetch the first prop page, which includes `DISTANCE`, instead of downloading every ignored round/method market.
- Ran the prop importer through 31 matched events before stopping the long batch for analysis.
- Verified 31 prop events, 398 distance markets, 15,215 unique prop rows, 8,338 source-current rows, and 6,877 source-previous rows.
