---
# intercept-rmju
title: 'O25-B: Run locked Over 2.5 harness'
status: completed
type: task
priority: normal
created_at: 2026-05-16T05:04:20Z
updated_at: 2026-05-16T05:12:55Z
parent: intercept-dsmc
blocked_by:
    - intercept-30w8
---

Acceptance criteria:
- [x] Run the locked validation harness from the frozen config.
- [x] Publish JSON and Markdown artifacts under data/experiments/harness.
- [x] Record whether Over 2.5 beats market ROI, log-loss, and Brier on the locked holdout.

## Summary of Changes

- Ran `configs/experiments/over-2-5-locked-validation-v1.json` on a last-35-event chronological holdout.
- Published `data/experiments/harness/over-2-5-locked-validation-v1.json` and `.md`.
- The frozen Over 2.5 candidate cleared the configured market gate: +21.9% ROI delta vs market, -0.0363 log-loss delta, -0.0184 Brier delta, 229 selected rows, and 35 scored events.
- Target coverage was market-backed: 316 market rows across 358 labels, or 88.3% coverage.

## Verification

- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=/tmp/interceptor-worktrees/over25-locked-validation/services/python /Users/vulturestudio/intercept/services/python/.venv/bin/python -m ml.experiment_harness --config configs/experiments/over-2-5-locked-validation-v1.json`
