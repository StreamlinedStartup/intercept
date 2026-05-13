---
# intercept-jk96
title: Inventory fresh FightOdds import path
status: completed
type: task
priority: high
created_at: 2026-05-13T00:57:17Z
updated_at: 2026-05-13T00:58:40Z
parent: intercept-tco0
---

Acceptance criteria:
- [x] Verify importer, matcher, coverage, and evaluation commands for fresh market data.
- [x] Record date window and source constraints for fresh events.
- [x] Commit bean evidence before data import.



## Summary of Changes

- Verified the existing FightOdds importer supports date-range and explicit event-PK imports.
- Verified the existing matcher, coverage report, and config-driven market harness are the route for fresh validation.
- Added docs/fresh_out_of_sample_market_data.md with the post-holdout window and no-tuning policy.

## Verification

- docker ps confirmed interceptor-postgres is available on localhost:5434.
- Inspected packages/db/src/import-fightodds-event.ts, packages/db/src/report-historical-odds-coverage.ts, and services/python/ml/experiment_harness.py.
- beans check
