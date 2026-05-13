---
# intercept-kraf
title: 'D2-LEV-A: Define locked evaluation candidates and protocol'
status: completed
type: task
priority: high
created_at: 2026-05-13T00:47:12Z
updated_at: 2026-05-13T00:55:00Z
parent: intercept-5t8l
---

Acceptance criteria:

- [x] Freezes the exact candidate list before evaluation.
- [x] Defines the historical locked-style holdout window and explains its limits.
- [x] Keeps protocol report_only/research_only/no model_versions writes.
- [x] Documents that no tuning is allowed after results are inspected.

## Summary of Changes

- Added `configs/experiments/locked-evaluation-candidates-v1.json` with three frozen candidates.
- Added `docs/locked_evaluation_protocol.md`.
- Defined the holdout as the last 10 chronological market-covered events.
- Documented that this is historical locked-style validation, not true future validation.

## Verification

- `jq -e '.report_only == true and .writes_model_versions == false and .value_status == "research_only" and (.candidates|length)==3 and .holdout_policy.type == "last_n_events" and .holdout_policy.event_count == 10' configs/experiments/locked-evaluation-candidates-v1.json` -> true.
- `rg -n "Do not tune|research_only|last 10|not true future validation" docs/locked_evaluation_protocol.md`.
