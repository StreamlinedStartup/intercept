---
# intercept-8gxf
title: 'Phase 2: odds-mma domain plugin'
status: completed
type: epic
priority: high
created_at: 2026-05-09T18:55:13Z
updated_at: 2026-05-09T23:48:15Z
parent: intercept-7c8e
blocked_by:
    - intercept-3fqo
---

domains/odds-mma proxying the-odds-api.com (free 500/mo, 5/min). 1h cache. Daily snapshot to odds_snapshots. Fuzzy-match into events/fighters; unmatched logged.

## Summary of Changes

Phase 2 is complete. It ships the `domains/odds-mma` domain plugin, current MMA odds proxying with 1-hour cache headers, snapshot persistence into `odds_snapshots`, unmatched odds logging into `unmatched_odds`, daily manual snapshot documentation, and the required browser smoke gate evidence.

Verification:

- Phase verification completed in intercept-1fhe.
- Browser smoke gate completed in intercept-qjks.
- Smoke screenshots committed under `data/smoke/phase-2-upcoming.png` and `data/smoke/phase-2-snapshot.png`.
