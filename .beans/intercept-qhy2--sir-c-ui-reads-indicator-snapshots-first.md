---
# intercept-qhy2
title: 'SIR-C: UI reads indicator snapshots first'
status: todo
type: task
created_at: 2026-05-16T05:58:14Z
updated_at: 2026-05-16T05:58:14Z
parent: intercept-qh8w
blocked_by:
    - intercept-d22p
---

Switch upcoming UI and compare-sheet behavior to prefer materialized indicator snapshots.

Acceptance criteria:
- [ ] Prediction responses expose snapshot-backed Over 2.5 indicator data when available.
- [ ] /upcoming fight cards and compare sheet preserve the existing badge/tile presentation.
- [ ] Show a clear stale/missing state when the snapshot is unavailable or outdated.
- [ ] Avoid request-time retraining or hidden fallback behavior in normal product paths.
- [ ] Add focused API/UI tests for snapshot-backed rendering states.
