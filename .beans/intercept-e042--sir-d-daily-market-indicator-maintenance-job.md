---
# intercept-e042
title: 'SIR-D: Daily market indicator maintenance job'
status: todo
type: task
created_at: 2026-05-16T05:58:19Z
updated_at: 2026-05-16T05:58:19Z
parent: intercept-qh8w
blocked_by:
    - intercept-d22p
---

Define and wire the daily operational refresh cadence for upcoming-market indicators.

Acceptance criteria:
- [ ] Daily flow is documented/wired to sync upcoming cards, refresh upcoming fighter backfill, import moneylines/props, canonical-match odds, and run indicator refresh.
- [ ] Job is idempotent and records clear per-step failures without silently masking upstream/API problems.
- [ ] Operator command is explicit and safe to run manually before any scheduler wiring.
- [ ] No retraining or artifact promotion happens in the daily job.
