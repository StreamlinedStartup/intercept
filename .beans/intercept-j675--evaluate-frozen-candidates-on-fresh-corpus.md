---
# intercept-j675
title: Evaluate frozen candidates on fresh corpus
status: completed
type: task
priority: high
created_at: 2026-05-13T00:57:17Z
updated_at: 2026-05-13T01:10:20Z
parent: intercept-tco0
blocked_by:
    - intercept-keji
---

Acceptance criteria:
- [x] Evaluate only frozen candidates; do not tune candidate parameters on fresh data.
- [x] Compare each candidate against market favorite on ROI, log loss, and Brier.
- [x] Emit research-only JSON/Markdown evidence with writes_model_versions=false.
- [x] State whether any candidate clears the market gate.



## Summary of Changes

- Added an after_date holdout policy to isolate the imported fresh market slice.
- Added a frozen-candidate fresh locked-evaluation config.
- Ran the frozen candidates on the 30-event post-holdout market slice and documented the failed gate.

## Verification

- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/pytest services/python/test_experiment_harness.py
- DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/fresh-market-locked-evaluation-v1.json --stdout summary
- Result: 0 frozen candidates cleared the market gate; best candidate still had ROI delta +0.0%, log-loss delta +0.0129, Brier delta +0.0045.
