---
# intercept-b6yf
title: 'D2-MRA: Market residual analysis and pre-fight signal discovery'
status: todo
type: epic
priority: high
created_at: 2026-05-12T05:34:24Z
updated_at: 2026-05-12T05:34:24Z
parent: intercept-8mw9
---

Use the trainable 40-event market-covered corpus from D2-TMC to identify where the model loses to the market, isolate pre-fight feature gaps, and choose one or two signal candidates before another model experiment. Keep all outputs research-only; no active model_versions writes or validated activation in this epic.

Acceptance criteria:
- [ ] Freeze D2-TMC artifacts as residual-analysis inputs and baseline current market/model/blend results.
- [ ] Bucket residuals by favorite/underdog, odds range, weight class, event age, feature availability, confidence, and market/model disagreement.
- [ ] Identify high-loss model failure clusters and feature gaps.
- [ ] Define one or two pre-fight-only signal candidates that avoid leakage and post-fight data.
- [ ] Implement only the smallest justified signal candidate as a report-only experiment.
- [ ] Rerun market-gated reports and publish a final JSON/Markdown recommendation.
- [ ] Keep UI/API/docs research-only and do not write active model_versions.
