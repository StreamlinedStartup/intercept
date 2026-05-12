---
# intercept-h336
title: 'D2-MRA-B: Bucket model-vs-market residuals by fight dimensions'
status: todo
type: task
priority: high
created_at: 2026-05-12T05:34:40Z
updated_at: 2026-05-12T05:34:40Z
parent: intercept-b6yf
blocked_by:
    - intercept-nwg3
---

Acceptance criteria:
- [ ] Bucket residuals by favorite/underdog side, odds range, weight class, event date age, feature availability, confidence, and market/model disagreement.
- [ ] Compute per-bucket count, model accuracy, market accuracy, model ROI, market ROI, log loss, Brier, and calibration gap where applicable.
- [ ] Flag unstable buckets and keep them out of promotion recommendations.
- [ ] Publish JSON/Markdown residual bucket reports; no model_versions writes.
