# Prop Market Baseline Contract

Date: 2026-05-16
Status: report-only planning artifact for `intercept-2sgy`

## Goal

Connect imported FightOdds `DISTANCE` prop odds to the market opportunity harness so `decision` and `finish` targets can be evaluated against a real market baseline instead of returning `*_market_odds_unavailable`.

This does not activate betting recommendations, validated status, production prediction writes, or `model_versions` writes.

## Source Rows

Use `historical_prop_odds` rows where:

- `source_offer_type_id = 'DISTANCE'`
- `market_family = 'fight_distance'`
- `line_kind = 'source_current'` for primary scoring
- `historical_odds_fights.canonical_fight_id` links the source fight to the model sample `fight_id`

Keep `source_previous` rows out of primary scoring until timestamp semantics improve. They can be reported as coverage only.

## Target Mapping

The `DISTANCE` market is a two-outcome prop:

- Decision target:
  - target: `decision`
  - label `1`: fight goes the distance
  - source side: `outcome1`, `is_not = false`
- Finish target:
  - target: `finish`
  - label `1`: fight ends inside distance
  - source side: `outcome2`, `is_not = true`

Both targets use the same paired sportsbook market. Do not infer either target from round totals, result text, method-specific props, `oddsOpen`, `oddsBest`, or `oddsWorst`.

## Consensus Probability

For each canonical fight and line kind:

1. Pair rows by `source_market_id`, `sportsbook_slug`, and `line_kind`.
2. Require both `outcome1` and `outcome2` rows for that sportsbook pair.
3. Use stored `implied_probability` values to remove vig:
   - `decision_probability = outcome1_implied / (outcome1_implied + outcome2_implied)`
   - `finish_probability = outcome2_implied / (outcome1_implied + outcome2_implied)`
4. Average no-vig probabilities across sportsbook pairs for a fight-level consensus.
5. Track pair count; a target market baseline is unavailable when pair count is zero.

## Harness Integration

Decision and finish model predictions should carry:

- `market_probability`: market probability for label `1`
- `market_predicted_label`: `1` when `market_probability >= 0.5`, else `0`
- `picked_market_probability`: market probability of the model-selected label
- `picked_model_market_edge`: model probability of the selected label minus market probability of that selected label

Target ROI for decision/finish should use the selected side's consensus no-vig decimal price:

- if predicted label is `1`, use target probability `p`
- if predicted label is `0`, use `1 - p`
- no-vig decimal odds are `1 / selected_market_probability`
- flat 1u win returns `decimal - 1`; loss returns `-1`

Market baseline comparison should be target-specific. A decision variant compares against a `decision_market_baseline`; a finish variant compares against a `finish_market_baseline`; winner variants continue using the existing `market_favorite` baseline.

## Limits

- One-event prop coverage is enough to prove the harness path, not enough to validate betting value.
- The first report must remain `report_only`, `value_status = research_only`, and `writes_model_versions = false`.
- A missing prop baseline must remain explicit as `decision_market_odds_unavailable` or `finish_market_odds_unavailable`; do not silently fall back to winner moneyline markets.
