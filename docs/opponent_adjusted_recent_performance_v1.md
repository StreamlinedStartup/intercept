# Opponent-Adjusted Recent Performance v1

`opponent_adjusted_recent_performance_v1` was evaluated as a report-only, research-only pre-fight signal using existing DB data only.

## Signal

The experiment appends four features to the production feature vector:

- `adj_recent_strike_diff_last_3`
- `adj_recent_grappling_diff_last_3`
- `quality_of_recent_opposition_diff`
- `adj_recent_efficiency_trend_diff`

Each feature uses only fights before the target fight date. For each fighter's last three prior fights, the implementation adjusts recent striking and grappling differentials by the opponent's win rate before that historical bout. Rows without prior opponent-quality context remain `NaN` rather than falling back to zero.

## Result

The signal did not clear the market gate.

| Best variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate |
|---|---:|---:|---:|---|
| `xgb_opponent_adjusted_recent_performance_blend_10` | -3.2% | 0.0085 | 0.0035 | false |

The unblended candidate was slightly better than current XGBoost on ROI but still materially worse than the market favorite:

| Variant | Accuracy | Log loss | Brier | ROI |
|---|---:|---:|---:|---:|
| `market_favorite` | 74.7% | 0.5766 | 0.1952 | 18.5% |
| `xgb_current` | 52.0% | 0.7266 | 0.2641 | -8.9% |
| `xgb_opponent_adjusted_recent_performance` | 53.8% | 0.7267 | 0.2643 | -8.2% |
| `xgb_opponent_adjusted_recent_performance_blend_10` | 73.1% | 0.5851 | 0.1988 | 15.3% |

## Recommendation

Keep this signal `research_only`. Do not promote it, write `model_versions`, or use it for betting/value claims. The next useful slice should add genuinely new pre-fight information or isolate a narrower residual cluster before another full-corpus market-gated run.

Evidence:

- `configs/experiments/opponent-adjusted-recent-performance-v1.json`
- `data/experiments/harness/opponent-adjusted-recent-performance-v1.json`
- `data/experiments/harness/opponent-adjusted-recent-performance-v1.md`
