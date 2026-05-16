---
# intercept-qhy2
title: 'SIR-C: UI reads indicator snapshots first'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:58:14Z
updated_at: 2026-05-16T14:12:19Z
parent: intercept-qh8w
blocked_by:
    - intercept-d22p
---

Switch upcoming UI and compare-sheet behavior to prefer materialized indicator snapshots.

Acceptance criteria:
- [x] Prediction responses expose snapshot-backed Over 2.5 indicator data when available.
- [x] /upcoming fight cards and compare sheet preserve the existing badge/tile presentation.
- [x] Show a clear stale/missing state when the snapshot is unavailable or outdated.
- [x] Avoid request-time retraining or hidden fallback behavior in normal product paths.
- [x] Add focused API/UI tests for snapshot-backed rendering states.

## Summary of Changes

- Prediction endpoints now load Over 2.5 from `market_indicator_snapshots` and return explicit `missing_snapshot` or `stale_snapshot` states instead of request-time indicator fallback.
- The upcoming fight chip and compare-sheet tile preserve the existing candidate presentation while showing missing/stale snapshot states.
- Added focused API and web tests for snapshot-backed current/stale/missing rendering states.
