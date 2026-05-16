# Model Reliability Final Report

- Generated: `2026-05-12T01:24:57Z`
- Epic: D2-RV Model reliability and market-gated value recovery
- Final `value_status`: `insufficient_coverage`
- Reason: Only 30 matched fights across 3 events were scored; the validation gate requires at least 200 fights across 30 events.
- Writes `model_versions`: `false`

## Completed Evidence

| Area | Artifact | Result |
|---|---|---|
| Safety gate | API/UI/docs wording | Value and ROI surfaces are research-only; `value_status` and `value_status_reason` are returned by prediction responses. |
| Leakage audit | `data/experiments/leakage-audit.md` | Pass, 15 checks, 0 failed. |
| Simple baselines | `data/experiments/simple-baselines.md` | 8 events, 99 samples, 12 market-covered samples, research-only. |
| Historical odds coverage | `data/experiments/historical-odds-coverage.md` | 3 matched events, 30 matched fights, 1,553 linked moneyline rows. |
| Market gate | `data/experiments/market-gate-report.md` | 30 scored fights across 3 events; current status remains `insufficient_coverage`. |

## Market Gate Summary

| Strategy | Count | Accuracy | Log loss | Brier | Sim ROI |
|---|---:|---:|---:|---:|---:|
| model_pick | 30 | 36.7% | 0.7588 | 0.2823 | -16.4% |
| market_favorite | 30 | 76.7% | 0.5166 | 0.1685 | 7.2% |
| blend_50_50 | 30 | 70.0% | 0.6024 | 0.2064 | -3.8% |
| blend_25_model_75_market | 30 | 76.7% | 0.5500 | 0.1827 | 7.2% |
| blend_75_model_25_market | 30 | 46.7% | 0.6712 | 0.2396 | -21.9% |

## Status Decision

The current model and market surfaces must remain research-only in product language. The coverage gate fails before ROI superiority can be considered: 30 scored fights across 3 events is below the 200-fight and 30-event threshold.

## Next Validation Work

- Expand historical odds coverage until at least 30 matched events and 200 scored fights are available.
- Re-run the leakage audit, simple baselines, historical odds coverage report, and market gate report.
- Consider `validated` only if the model or approved blend beats the market-favorite baseline by at least 2 percentage points of simulated flat-stake ROI after coverage passes.
