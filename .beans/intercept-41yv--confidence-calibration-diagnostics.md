---
# intercept-41yv
title: Confidence calibration diagnostics
status: in-progress
type: epic
priority: high
created_at: 2026-05-11T15:41:10Z
updated_at: 2026-05-11T15:41:30Z
parent: intercept-8mw9
---

Add diagnostics that explain whether high-confidence model picks are calibrated, under-confident, or over-confident before tuning confidence upward.

Acceptance criteria:
- [ ] Dedicated epic branch is created from updated fork/main before code or docs changes.
- [ ] Walk-forward reports include average confidence and expected-vs-actual calibration gaps overall and by confidence bucket.
- [ ] Reports identify whether the 70%+ bucket is landing above or below its average stated confidence.
- [ ] Full-corpus backtest summary is regenerated with calibration diagnostics.
- [ ] docs/model_scope.md explains the calibration finding and next tuning implications.
- [ ] Focused verification passes and completed beans are committed.
