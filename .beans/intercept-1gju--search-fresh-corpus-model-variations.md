---
# intercept-1gju
title: Search fresh corpus model variations
status: completed
type: task
priority: high
created_at: 2026-05-13T01:10:47Z
updated_at: 2026-05-13T01:13:41Z
parent: intercept-tco0
blocked_by:
    - intercept-j675
---

Acceptance criteria:
- [x] Generate a report-only search config over fresh post-holdout market events.
- [x] Run the variation search through the market harness.
- [x] Count clearing candidates and record the best winner or failure.
- [x] Keep value_status=research_only and writes_model_versions=false.



## Summary of Changes

- Added a fresh selected-fight winner-search generator and generated a 7,777-variant config.
- Ran the full fresh-corpus variation search through the report-only market harness.
- Documented that no fresh-search variant cleared the market gate.

## Verification

- generate_fresh_winner_search emitted configs/experiments/fresh-winner-search-v1.json with 7,777 variants.
- ml.experiment_harness --config configs/experiments/fresh-winner-search-v1.json completed on 30 fresh events / 304 model-eligible fights.
- Node summary over data/experiments/harness/fresh-winner-search-v1.json found 0 clearing variants.
- Best variant: log_marketctx_c5p0_temp1p6_blend60_min_confidence0p65, ROI delta +1.481pp, log-loss delta +0.0107, Brier delta +0.0039.
