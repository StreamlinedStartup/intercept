---
# intercept-p4ax
title: 'D2-OARP-B: Run market harness experiment'
status: completed
type: task
priority: high
created_at: 2026-05-12T22:47:17Z
updated_at: 2026-05-12T22:53:43Z
parent: intercept-eols
blocked_by:
    - intercept-eols
    - intercept-0uoh
---

Wire the new features into the report-only market experiment harness and run a small locked evaluation.

Acceptance:
- [x] Adds a checked-in experiment config for opponent_adjusted_recent_performance_v1.
- [x] Runs ml.experiment_harness against the current market-covered corpus.
- [x] Publishes JSON/Markdown artifacts under data/experiments/harness/.


## Summary of Changes

- Added configs/experiments/opponent-adjusted-recent-performance-v1.json.
- Ran the report-only market harness on 40 model-eligible events / 379 fights.
- Published JSON and Markdown artifacts for the failed market-gate result.

## Verification

- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/opponent-adjusted-recent-performance-v1.json --stdout summary
- jq .report_only,.writes_model_versions,.value_status,.recommendation data/experiments/harness/opponent-adjusted-recent-performance-v1.json => true / false / research_only / research_only recommendation
