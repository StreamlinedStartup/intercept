---
# intercept-7j7t
title: 'D2-SMP-B: Run style matchup market harness'
status: completed
type: task
priority: high
created_at: 2026-05-12T23:02:17Z
updated_at: 2026-05-12T23:06:28Z
parent: intercept-ovvb
blocked_by:
    - intercept-fn50
---

Evaluate style_matchup_pressure_v1 through the report-only market experiment harness.

Acceptance:
- [x] Adds a checked-in experiment config for style_matchup_pressure_v1.
- [x] Runs ml.experiment_harness against the current market-covered corpus.
- [x] Publishes JSON/Markdown artifacts under data/experiments/harness/.


## Summary of Changes

- Added configs/experiments/style-matchup-pressure-v1.json.
- Ran the report-only market harness on 40 model-eligible events / 379 fights.
- Published JSON and Markdown artifacts for the failed market-gate result.

## Verification

- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/style-matchup-pressure-v1.json --stdout summary
- jq .report_only,.writes_model_versions,.value_status,.recommendation data/experiments/harness/style-matchup-pressure-v1.json => true / false / research_only / research_only recommendation
