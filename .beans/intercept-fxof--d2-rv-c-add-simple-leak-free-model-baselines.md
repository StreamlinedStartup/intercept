---
# intercept-fxof
title: 'D2-RV-C: Add simple leak-free model baselines'
status: todo
type: task
priority: high
created_at: 2026-05-12T00:21:19Z
updated_at: 2026-05-12T00:21:19Z
parent: intercept-dmyw
blocked_by:
    - intercept-tjvc
---

Add report-only simple baselines for model reliability comparison.

Acceptance criteria:
- [ ] Include simple leak-free baselines such as market favorite where available and non-odds statistical baselines.
- [ ] Use chronological walk-forward evaluation.
- [ ] Report log loss, Brier, accuracy, ROC AUC, and ROI only as simulated research metrics.
- [ ] Do not write active model_versions.
