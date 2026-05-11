---
# intercept-lvvl
title: Model scope documentation
status: completed
type: epic
priority: normal
created_at: 2026-05-11T00:13:34Z
updated_at: 2026-05-11T00:16:59Z
---

Document how the UFC predictor model works, which features it uses, how predictions and feature rankings should be interpreted, and how backtesting should be approached for non-statistical readers.

## Summary of Changes

- Created `docs/model_scope.md` as the human-readable model scope reference.
- Covered the model objective, XGBoost training approach, point-in-time leakage controls, feature groups, feature rankings, odds edge, current model metrics, and backtesting plan.

## Verification

- Child task `intercept-7rpz` completed and committed.
- `pnpm biome check docs/model_scope.md .beans/intercept-7rpz--write-digestible-model-scope-doc.md .beans/intercept-lvvl--model-scope-documentation.md` reported these markdown files are ignored by Biome.
