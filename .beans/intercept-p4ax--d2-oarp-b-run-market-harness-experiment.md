---
# intercept-p4ax
title: 'D2-OARP-B: Run market harness experiment'
status: todo
type: task
priority: high
created_at: 2026-05-12T22:47:17Z
updated_at: 2026-05-12T22:47:27Z
parent: intercept-eols
blocked_by:
    - intercept-eols
    - intercept-0uoh
---

Wire the new features into the report-only market experiment harness and run a small locked evaluation.

Acceptance:
- [ ] Adds a checked-in experiment config for opponent_adjusted_recent_performance_v1.
- [ ] Runs ml.experiment_harness against the current market-covered corpus.
- [ ] Publishes JSON/Markdown artifacts under data/experiments/harness/.
