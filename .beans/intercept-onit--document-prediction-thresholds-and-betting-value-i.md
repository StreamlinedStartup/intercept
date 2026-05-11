---
# intercept-onit
title: Document prediction thresholds and betting value interpretation
status: completed
type: task
priority: normal
created_at: 2026-05-11T01:18:24Z
updated_at: 2026-05-11T01:19:27Z
---

Add operator documentation explaining model probability, confidence, implied odds, edge, EV, threshold bands, and how to interpret cases where the value side differs from the straight-up pick.



## Summary of Changes

- Added `docs/prediction_interpretation.md` explaining model win probability, confidence, market implied probability, model-vs-market edge, expected value, threshold bands, and calibration.
- Included the Strickland-Chimaev-style example where the model pick and value side differ.
- Documented operator rules to prevent overreading one fight or using edge bands as automatic betting instructions.

## Verification

- Read `docs/prediction_interpretation.md` for formula correctness and operator clarity.
- `pnpm biome check docs/prediction_interpretation.md` attempted; Biome ignores Markdown docs in this repo, so no files were processed.
