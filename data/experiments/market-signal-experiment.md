# Market Signal Experiment

- Generated: `2026-05-12T05:58:15.841465+00:00`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Signal: `pre_fight_feature_availability_flags`
- Model-eligible events: 40
- Model-eligible fights: 379

## Strategy Comparison

| Strategy | Count | Accuracy | Log loss | Brier | ROI |
|---|---:|---:|---:|---:|---:|
| market_favorite | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| xgboost_current | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% |
| xgboost_feature_availability | 379 | 53.8% | 0.7291 | 0.2653 | -5.5% |

## Deltas

- Candidate ROI delta vs market: -23.9%
- Candidate log-loss delta vs market: 0.1525
- Candidate Brier delta vs market: 0.0701
- Candidate ROI delta vs current model: +3.5%
- Candidate log-loss delta vs current model: 0.0025
- Candidate Brier delta vs current model: 0.0011

## Target Cluster Checks

| Cluster | Count | Candidate acc | Market acc | Candidate ROI | Market ROI | ROI delta |
|---|---:|---:|---:|---:|---:|---:|
| feature_availability:sparse | 64 | 53.1% | 81.2% | -11.4% | 24.5% | -35.9% |
| confidence:model_70_plus | 51 | 49.0% | 80.4% | -27.7% | 20.4% | -48.1% |
| odds_range:heavy_favorite_75_plus | 64 | 64.1% | 87.5% | -14.0% | 11.0% | -25.0% |

## Recommendation

- Status: `do_not_promote`
- Reason: Candidate remains behind the market favorite and does not improve both log loss and Brier versus the current model (ROI delta vs market -23.9%).

## Policy

This experiment is report-only and does not write active model_versions or activate betting/value claims.
