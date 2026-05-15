---
# intercept-096p
title: 'MOH-E: Run opportunity harness and publish recommendation'
status: completed
type: task
priority: high
created_at: 2026-05-15T16:24:49Z
updated_at: 2026-05-15T17:42:09Z
parent: intercept-77c6
blocked_by:
    - intercept-ivky
    - intercept-xldt
    - intercept-u5rg
---

Acceptance criteria:
- [x] Run the smoke matrix and focused opportunity matrix against the local market corpus.
- [x] Commit compact JSON/Markdown reports with coverage, metrics, ROI, and recommendation.
- [x] Explicitly mark any candidate as promote, iterate, or reject.
- [x] Document remaining data gaps, especially prop odds for decision/finish market validation.

## Summary of Changes
- Ran `market-opportunity-smoke` and `market-opportunity-matrix-v1` against the local matched market corpus.
- Committed compact JSON/Markdown reports under `data/experiments/harness`.
- Published a research-only recommendation: no configured moneyline opportunity candidate clears the market gate.
- Documented that decision and finish targets need historical prop odds before ROI or market-baseline validation is possible.
