---
# intercept-j675
title: Evaluate frozen candidates on fresh corpus
status: todo
type: task
priority: high
created_at: 2026-05-13T00:57:17Z
updated_at: 2026-05-13T00:57:40Z
parent: intercept-tco0
blocked_by:
    - intercept-keji
---

Acceptance criteria:
- [ ] Evaluate only frozen candidates; do not tune candidate parameters on fresh data.
- [ ] Compare each candidate against market favorite on ROI, log loss, and Brier.
- [ ] Emit research-only JSON/Markdown evidence with writes_model_versions=false.
- [ ] State whether any candidate clears the market gate.
