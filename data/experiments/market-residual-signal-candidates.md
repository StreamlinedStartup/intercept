# Market Residual Signal Candidates

- Generated: `2026-05-12T05:55:00Z`
- Epic: `intercept-b6yf`
- Task: `intercept-tktt`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Input report: `data/experiments/market-residual-clusters.json`

## Decision

Build exactly one smallest justified report-only experiment in Task E: `pre_fight_feature_availability_flags`.

Do not force a market-disagreement feature in this epic. The largest loss clusters there are market-prior gaps already covered by prior blend/model-family reports, not evidence of a missing internal pre-fight signal.

## Recommended Signal

`pre_fight_feature_availability_flags`

| Evidence cluster | Fights | Events | ROI delta vs market | High-conf wrong | Feature gap |
|---|---:|---:|---:|---:|---|
| `feature_availability:sparse` | 64 | 30 | -35.9pp | 23.4% | missing rate 50.3% vs corpus 9.5%; recent-form availability 0.0% vs 83.1% |
| `confidence:model_70_plus` | 53 | 25 | -35.8pp | 52.8% | missing rate 16.2% vs corpus 9.5%; recent-form availability 69.8% vs 83.1% |
| `odds_range:heavy_favorite_75_plus` | 64 | 32 | -20.8pp | 12.5% | missing rate 14.7% vs corpus 9.5%; recent-form availability 71.9% vs 83.1% |

### Feature Semantics

| Feature | Type | Meaning |
|---|---|---|
| `feature_missing_count` | numeric | Count of NaN values in the existing point-in-time feature vector before model training. |
| `feature_missing_rate` | numeric | Share of NaN values in the existing point-in-time feature vector before model training. |
| `has_recent_form_context` | binary | 1 when `wins_last_3_diff` and `wins_last_5_diff` are both present before the fight, else 0. |
| `has_weight_context` | binary | 1 when `weight_class_change` and `same_weight_class_count_diff` are both present before the fight, else 0. |

### Leakage Review

Status: `pre_fight_only`

The indicators are derived only from whether existing point-in-time inputs are present before the target fight. They do not inspect fight result, post-fight stats, or future events.

### Expected Direction

Missingness should reduce overconfident model picks or let the report-only model learn that sparse/recent-form-missing rows are less reliable than fully observed rows.

### Minimum Task E Validation

- Rerun the same market residual bucket report on the augmented feature set.
- Compare `model_70_plus`, `feature_availability:sparse`, and `heavy_favorite_75_plus` buckets against the Task C baseline.
- Require no degradation in overall log loss/Brier and at least one actionable cluster moving toward market performance before recommending broader model-family work.

## No-Build Candidate

`market_disagreement_context`

| Evidence cluster | Fights | Events | ROI delta vs market | Classification |
|---|---:|---:|---:|---|
| `favorite_underdog_side:model_on_market_underdog` | 146 | 39 | -71.1pp | market-prior gap |
| `market_model_disagreement:disagree_delta_20pp_plus` | 95 | 37 | -66.9pp | market-prior gap |

Market probabilities are pre-fight/current-at-import, but D2-MIX already tested market blends and market-aware model-family candidates. Rebuilding this signal would mostly teach the model to defer to market favorites when model and market disagree, so keep it diagnostic and do not spend Task E on it.

## Task E Recommendation

Implement `pre_fight_feature_availability_flags` as a report-only feature experiment. Do not write active `model_versions`.
