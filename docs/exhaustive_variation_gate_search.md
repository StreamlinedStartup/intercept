# Exhaustive Variation Gate Search

The report-only exhaustive variation search found a market-gate-clearing candidate after three loops:

1. `market-grid-exhaustive-v2`: 42,281 model, feature, calibration, and blend variants.
2. `market-grid-selection-v1`: 73,441 selected-fight variants with same-subset market baselines.
3. `market-grid-selection-threshold-v1`: 751 confidence-threshold refinements around the best near miss.

The first two loops did not clear the gate. The threshold refinement produced one gate-clearing candidate.

## Candidate

| Variant | Events | Fights | ROI delta | Log-loss delta | Brier delta | Clears gate |
|---|---:|---:|---:|---:|---:|---|
| `log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63` | 40 | 204 | +2.49% | -0.0011 | -0.0015 | true |

The variant is a report-only logistic regression candidate with:

- Feature set: `production_plus_all_research_market_context`.
- Model params: `C=2.5`.
- Calibration: temperature `2.2`.
- Market blend weight: `0.45`.
- Selection policy: only score fights where candidate confidence is at least `0.63`.

## Policy

This candidate is not production activation proof. Keep it `research_only` and do not write `model_versions`.

The correct next step is a locked evaluation slice. Do not tune on that slice after this candidate is selected.

## Evidence

- `configs/experiments/market-grid-exhaustive-v2.json`
- `configs/experiments/market-grid-selection-threshold-v1.json`
- `data/experiments/harness/market-grid-selection-threshold-v1.json`
- `data/experiments/harness/market-grid-selection-threshold-v1.md`
