---
# intercept-sq6u
title: 'D2-SMP-C: Publish recommendation and close epic'
status: completed
type: task
priority: high
created_at: 2026-05-12T23:02:17Z
updated_at: 2026-05-12T23:16:00Z
parent: intercept-ovvb
blocked_by:
    - intercept-7j7t
---

Summarize the style matchup result and close the research-only epic.

Acceptance:
- [x] Documents whether the signal cleared probability and ROI gates.
- [x] Confirms report_only/research_only/no model_versions writes.
- [x] Updates the epic summary and verification.
- [x] Notes that no HTTP/UI smoke gate is required.

## Summary of Changes

- Published `docs/style_matchup_pressure_v1.md` with the report-only result and recommendation.
- Updated `docs/pre_fight_signal_catalog.md` to mark `style_matchup_pressure_v1` evaluated and market-gate rejected.
- Confirmed the best variant, `xgb_style_matchup_pressure_blend_10`, remains research-only: ROI delta -3.3%, log-loss delta +0.0090, Brier delta +0.0037 versus market.
- No HTTP/UI smoke gate is required because this epic only changes Python research features, experiment configs, and docs.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m pytest services/python/test_ml.py services/python/test_experiment_harness.py -q` -> 30 passed.
- `jq -e '.report_only == true and .writes_model_versions == false and .value_status == "research_only" and .recommendation.status == "research_only"' data/experiments/harness/style-matchup-pressure-v1.json` -> true.
- `rg -n "research_only|model_versions|did not clear|style_matchup_pressure_v1" docs/style_matchup_pressure_v1.md docs/pre_fight_signal_catalog.md data/experiments/harness/style-matchup-pressure-v1.md`.
