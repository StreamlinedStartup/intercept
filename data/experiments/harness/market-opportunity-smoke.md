# Market Experiment Harness

- Generated: `2026-05-15T17:40:07.610595+00:00`
- Config: `configs/experiments/market-opportunity-smoke.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 4
- Model-eligible fights: 33

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | winner_abstain_smoke | -63.8% | 0.1107 | 0.0485 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 2 | winner_underdog_edge_smoke | -73.2% | 0.4098 | 0.1884 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 3 | decision_edge_smoke |  |  |  | false | market_baseline_unavailable_for_target |
| 4 | finish_edge_smoke |  |  |  | false | market_baseline_unavailable_for_target |
| 5 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Target | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | winner | market_favorite | none |  | 33 | 78.8% | 0.5155 | 0.1689 | 14.1% |
| winner_underdog_edge_smoke | winner | logistic_regression | production_plus_market_context |  | 9 | 22.2% | 0.9751 | 0.3802 | -48.1% |
| decision_edge_smoke | decision | logistic_regression | production_plus_all_research |  | 7 | 28.6% | 1.4233 | 0.4751 |  |
| finish_edge_smoke | finish | logistic_regression | production_plus_all_research |  | 20 | 45.0% | 1.3931 | 0.4101 |  |
| winner_abstain_smoke | winner | logistic_regression | production_plus_market_context |  | 2 | 0.0% | 0.7100 | 0.2584 | -100.0% |

## Recommendation

- Status: `research_only`
- Reason: winner_abstain_smoke is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.

## Data Gaps

- Decision and finish targets are scored as outcome-probability experiments only; historical decision/finish prop odds are not available in this corpus, so ROI and market-baseline gates are unavailable for those targets.
- Winner opportunity selectors remain market-gated against no-vig moneyline consensus and did not clear the configured gate in this smoke run.
