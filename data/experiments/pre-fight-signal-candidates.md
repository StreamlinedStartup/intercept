# Pre-Fight Signal Candidates

- Generated: `2026-05-12T22:45:00Z`
- Value status: `research_only`
- Writes `model_versions`: `false`

## Decision

The next smallest justified experiment is `opponent_adjusted_recent_performance_v1`.

Current model families, feature variants, calibration, and mass-search sweeps did not beat market. The next candidates must add genuinely new pre-fight information or better opponent/context normalization, not more variants of the same feature families.

## Pre-Fight Rules

- Use only data timestamped before the scheduled fight date.
- Do not use fight result, post-fight totals, post-fight odds, or future opponent records.
- Missing source context stays `NaN`; do not silently fill unknowns with zero.
- Promotion requires the same market gate: ROI at least +2pp over market favorite with log loss and Brier not worse on a locked future slice.

## Existing-Data Candidates

| Priority | Signal | Readiness | Why |
|---:|---|---|---|
| 1 | `opponent_adjusted_recent_performance_v1` | ready existing DB | Current stats and recent form do not normalize recent performance by opponent quality. |
| 2 | `style_matchup_pressure_v1` | ready existing DB | Current features are mostly differentials; matchup interactions may capture strength-versus-weakness effects. |
| 3 | `low_information_uncertainty_v1` | ready existing DB | Availability helped ROI versus current XGBoost but failed probability quality; a targeted uncertainty signal may help calibration. |
| 4 | `weight_class_context_v2` | ready existing DB | Weight-class movement likely needs directional interactions rather than simple differentials. |

### Recommended First Signal

`opponent_adjusted_recent_performance_v1`

Feature semantics:

| Feature | Meaning |
|---|---|
| `adj_recent_strike_diff_last_3` | Recent significant-strike differential adjusted by opponent quality at the time each prior fight occurred. |
| `adj_recent_grappling_diff_last_3` | Recent takedown/control/submission pressure differential adjusted for opponent defensive quality. |
| `quality_of_recent_opposition_diff` | Difference in recent opponent quality faced before the target fight. |
| `adj_recent_efficiency_trend_diff` | Slope of opponent-adjusted performance across the last three fights, fighter A minus fighter B. |

Minimum validation:

- Improve log loss and Brier versus current XGBoost.
- Reduce the market gap in at least one residual cluster.
- Stay report-only unless it clears the locked market gate.

## New-Data Candidates

| Priority | Signal | Readiness | Why |
|---:|---|---|---|
| 1 | `line_movement_microstructure_v1` | requires odds time series | The strongest failure mode is market-prior gap; line movement may expose pre-fight information arrival. |
| 2 | `fight_week_context_v1` | requires external event context | Late fight-week information such as short notice, weigh-in misses, or rebookings is absent from UFCStats history. |

## Rejected Or Diagnostic Only

| Signal | Reason |
|---|---|
| `feature_availability_flags_v1` | Already tested; improved ROI versus current XGBoost but worsened log loss/Brier and remained far below market. |
| `market_disagreement_context` | Residual evidence shows a market-prior gap, not an internal fighter-stat signal. |
| `more_blend_weights` | Mass search showed best candidates are effectively 1% model / 99% market blends and still worsen probability quality. |
