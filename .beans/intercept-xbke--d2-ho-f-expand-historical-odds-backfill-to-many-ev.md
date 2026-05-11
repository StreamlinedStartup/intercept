---
# intercept-xbke
title: 'D2-HO-F: Expand historical odds backfill to many events'
status: todo
type: task
created_at: 2026-05-11T17:12:07Z
updated_at: 2026-05-11T17:12:07Z
parent: intercept-5rw9
blocked_by:
    - intercept-qo0o
---

Acceptance criteria:
- [ ] Expand from the proven one-event path to multiple historical UFC events using the discovered source index or event-list route.
- [ ] Use polite throttling, cache-aware fetches, and source-specific rate limits.
- [ ] Support resumable/idempotent backfill over a bounded date range before full history.
- [ ] Avoid The Odds API historical usage unless the discovery task explicitly justifies cost and rate impact.
- [ ] Preserve raw source metadata and unmatched rows for every imported event.
- [ ] Produce aggregate import metrics: events scanned, fights scanned, odds rows imported, matched rows, unmatched rows, and skipped rows.
- [ ] Do not alter production prediction serving.

Verification:
- Run a bounded multi-event backfill and capture counts in the bean summary.
- Confirm no duplicate rows after a repeat run.
- Confirm scraper/import code does not include copied GPL or third-party scraper code.
