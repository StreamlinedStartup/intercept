# Market Experiment Harness

- Generated: `2026-05-16T05:12:00.515502+00:00`
- Config: `configs/experiments/over-2-5-locked-validation-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 35
- Model-eligible fights: 358

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | locked_over_2_5_positive_log_c1_conf58 | +21.9% | -0.0363 | -0.0184 | true |  |
| 2 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Target Market Coverage

| Target | Label rows | Market rows | Market coverage | Status |
|---|---:|---:|---:|---|
| over_2_5 | 358 | 316 | 88.3% | market_backed |

## Variants

| Variant | Target | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | winner | market_favorite | none |  | 358 | 70.9% | 0.5790 | 0.1973 | 3.4% |
| locked_over_2_5_positive_log_c1_conf58 | over_2_5 | logistic_regression | production_plus_all_research |  | 229 | 76.0% | 0.5672 | 0.1888 | 33.3% |

## Signal Diagnostics

| Variant | Indicator | Model ROI | Selected market ROI | Market ROI delta | Entries | Read |
|---|---|---:|---:|---:|---:|---|
| locked_over_2_5_positive_log_c1_conf58 | no_positive_market_indicator | 33.3% | 11.4% | +8.0% | 203 | No actionable positive signal in this selected subset. |

## Recommendation

- Status: `candidate_for_locked_evaluation`
- Reason: locked_over_2_5_positive_log_c1_conf58 clears the configured discovery gate; evaluate on a locked future slice before activation.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
