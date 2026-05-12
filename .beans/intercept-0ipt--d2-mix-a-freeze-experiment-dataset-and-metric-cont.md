---
# intercept-0ipt
title: 'D2-MIX-A: Freeze experiment dataset and metric contract'
status: completed
type: task
priority: high
created_at: 2026-05-12T03:34:01Z
updated_at: 2026-05-12T03:59:31Z
parent: intercept-tgq5
blocked_by:
    - intercept-136k
---

Acceptance criteria:
- [x] Freeze the D2-MCU coverage-passing, research-only evidence bundle.
- [x] Define the exact train/test chronology, scored-fight inclusion rules, and market baseline metric contract.
- [x] Publish a report-only experiment manifest.
- [x] Confirm no active model_versions writes.

## Summary of Changes

- Published the D2-MIX experiment manifest as JSON and Markdown.
- Froze the D2-MCU coverage-passing research bundle as the input for downstream model experiments.
- Defined chronology, inclusion/exclusion, market-baseline, metric, and simulated ROI contracts.
- Confirmed `model_versions` remains at 14 rows and this task writes no active model state.

## Verification

- `jq empty data/experiments/market-aware-model-experiment-manifest.json`
- `jq '{report_only,writes_model_versions, activation_allowed, baseline: .metric_contract.primary_baseline, min_roi: .metric_contract.roi_policy.minimum_candidate_roi, scored_events: .dataset_contract.scored_market_covered_events, scored_fights: .dataset_contract.scored_market_covered_fights}' data/experiments/market-aware-model-experiment-manifest.json`
- `psql 'postgres://interceptor:interceptor@localhost:5434/interceptor' -F $'\\t' -A -c "select count(*) as model_versions from model_versions;"`
