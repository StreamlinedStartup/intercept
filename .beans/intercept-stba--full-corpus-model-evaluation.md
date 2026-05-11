---
# intercept-stba
title: Full-corpus model evaluation
status: in-progress
type: epic
priority: high
created_at: 2026-05-11T14:28:59Z
updated_at: 2026-05-11T14:29:22Z
parent: intercept-8mw9
---

Evaluate the Decision Engine v2 model over the full imported UFC Stats CSV corpus using walk-forward backtesting, then document compact metrics and caveats without committing oversized raw artifacts.

Acceptance criteria:
- [ ] Dedicated epic branch is created from updated fork/main before code or docs changes.
- [ ] Full eligible historical UFC walk-forward backtest runs from the imported CSV-backed DB without the D2-E 20-event cap.
- [ ] Start date and min_train_samples policy are chosen and documented.
- [ ] Compact summary report is produced for commit; oversized raw artifacts are not committed.
- [ ] docs/model_scope.md records full-corpus metrics, confidence buckets, and caveats.
- [ ] Focused verification passes and completed beans are committed.
