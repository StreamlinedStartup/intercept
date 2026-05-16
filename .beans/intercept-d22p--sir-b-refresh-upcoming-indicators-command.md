---
# intercept-d22p
title: 'SIR-B: Refresh upcoming indicators command'
status: todo
type: task
created_at: 2026-05-16T05:58:09Z
updated_at: 2026-05-16T05:58:09Z
parent: intercept-qh8w
blocked_by:
    - intercept-vv4w
---

Build a repeatable command/job that materializes report-only indicators for upcoming fights.

Acceptance criteria:
- [ ] Load upcoming fights from the existing synced/cached fight data path.
- [ ] Skip fights without current fighter backfill and record skip reasons.
- [ ] Run existing prediction + Over 2.5 indicator logic without retraining.
- [ ] Load matched no-vig OVERUNDER_2.5 prop market consensus and compute edge.
- [ ] Upsert indicator snapshots idempotently.
- [ ] Print a concise summary: scanned, written, skipped, missing props, errors.
