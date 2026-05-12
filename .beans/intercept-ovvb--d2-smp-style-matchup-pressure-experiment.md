---
# intercept-ovvb
title: 'D2-SMP: Style matchup pressure experiment'
status: completed
type: epic
priority: high
created_at: 2026-05-12T23:02:07Z
updated_at: 2026-05-12T23:16:00Z
parent: intercept-8mw9
---

Implement the smallest report-only research experiment for style_matchup_pressure_v1 using existing DB data only. Keep all outputs research_only, do not write model_versions, and evaluate through the existing market experiment harness.

## Summary of Changes

- Added point-in-time style matchup pressure features for striking pressure versus defense, wrestling pressure versus takedown defense, and submission pressure versus grappling risk.
- Registered the report-only harness feature set `production_plus_style_matchup_pressure`.
- Ran `style_matchup_pressure_v1` through the market experiment harness and published JSON/Markdown artifacts.
- Recommendation: keep the signal research-only. It did not clear the market gate, and no `model_versions` writes were performed.

## Verification

- `PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m py_compile services/python/ml/features.py services/python/ml/experiment_harness.py`.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_ml.py services/python/test_experiment_harness.py -q` -> 30 passed.
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/style-matchup-pressure-v1.json --stdout summary`.
- `jq -e '.report_only == true and .writes_model_versions == false and .value_status == "research_only" and .recommendation.status == "research_only"' data/experiments/harness/style-matchup-pressure-v1.json` -> true.
- HTTP/UI smoke gate not required: this was a pure research/reporting epic with no endpoint or UI surface.
