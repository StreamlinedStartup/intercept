# Style Matchup Pressure v1

`style_matchup_pressure_v1` was evaluated as a report-only, research-only pre-fight signal using existing DB career stats only.

## Signal

The experiment appends three style interaction features to the production feature vector:

- `striking_pressure_vs_defense_edge`
- `wrestling_pressure_vs_tdd_edge`
- `submission_pressure_vs_grappling_risk_edge`

Each feature uses only career stats before the target fight date. The signal measures each fighter's offensive pressure against the opponent's defensive vulnerability, then stores fighter A minus fighter B.

## Result

The signal did not clear the market gate.

| Best variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate |
|---|---:|---:|---:|---|
| `xgb_style_matchup_pressure_blend_10` | -3.3% | 0.0090 | 0.0037 | false |

The unblended candidate was roughly flat to current XGBoost on ROI but worse on probability quality, and both remained materially worse than the market favorite:

| Variant | Accuracy | Log loss | Brier | ROI |
|---|---:|---:|---:|---:|
| `market_favorite` | 74.7% | 0.5766 | 0.1952 | 18.5% |
| `xgb_current` | 52.0% | 0.7266 | 0.2641 | -8.9% |
| `xgb_style_matchup_pressure` | 52.5% | 0.7335 | 0.2677 | -8.8% |
| `xgb_style_matchup_pressure_blend_10` | 73.4% | 0.5856 | 0.1990 | 15.2% |

## Recommendation

Keep this signal `research_only`. Do not promote it, write `model_versions`, or use it for betting/value claims. The remaining existing-DB candidates should be treated as calibration or narrow-cluster probes unless they introduce clearly different information than current production features.

Evidence:

- `configs/experiments/style-matchup-pressure-v1.json`
- `data/experiments/harness/style-matchup-pressure-v1.json`
- `data/experiments/harness/style-matchup-pressure-v1.md`
