# Decision Engine v2 Scope

Decision Engine v2 adds auditable fight signals beside the model pick. The goal is not to make the predictor more dramatic. The goal is to show the operator why a matchup deserves review and where the model may be thin.

## Scope

Epic 1 ships two core signals end to end:

- Round tendency: whether each fighter's prior UFC fights tend to resolve early, late, or by decision.
- Common opponents: how both fighters performed against shared prior opponents before the target fight date.

Each signal must exist in three places:

- point-in-time feature construction for training and prediction;
- `decision_signals` in the prediction API output;
- a compact signal tile in the `/upcoming` compare sheet.

## Round Tendency

Round tendency uses only completed fights before the target event date. It can read `fight_round_stats`, `fights`, and `fight_results`.

The first slice should stay small:

- prior average ending round for each fighter;
- prior decision-rate difference;
- prior late-fight exposure difference, derived from completed round stats or known ending round;
- a signal label that describes the tendency without implying certainty.

Suggested labels:

| Label | Meaning |
|---|---|
| `Early finish lean` | Prior fights skew toward finishes before the final scheduled round. |
| `Late/decision lean` | Prior fights skew toward later rounds or decisions. |
| `Mixed history` | No clear directional tendency. |
| `Thin history` | Not enough prior UFC fight data. |

## Common Opponents

Common-opponent metrics compare only opponents both fighters faced before the target fight date. Future rematches, later results, and the target fight itself are excluded.

The first slice should report:

- shared opponent count;
- Fighter A wins against shared opponents;
- Fighter B wins against shared opponents;
- method-adjusted or margin-style details only if they are already available point-in-time without special casing.

Suggested labels:

| Label | Meaning |
|---|---|
| `A stronger vs shared opponents` | Fighter A has the better prior record against shared opponents. |
| `B stronger vs shared opponents` | Fighter B has the better prior record against shared opponents. |
| `Split shared history` | Shared-opponent results do not clearly favor either fighter. |
| `No shared opponents` | There is no safe shared-opponent signal. |

## Leakage Rules

All Decision Engine v2 signals follow the same leakage rules as the model:

- Use only events with `event.date < target_date`.
- Never read the target fight result, target fight stats, or any later fight.
- Prediction-time features must receive the same target-fight context as training features, including `weight_class`.
- If a value cannot be built safely, return `NaN` for model features and a `Thin history` or `No shared opponents` label for UI signals.
- Do not infer missing outcomes or opponent identity from display names when stable IDs are unavailable.

## API Shape

Prediction responses should keep the current model fields and add a separate `decision_signals` object. Signals are explanations and review aids, not betting instructions.

```json
{
  "decision_signals": {
    "round_tendency": {
      "label": "Late/decision lean",
      "summary": "Both fighters have more prior late-fight or decision exposure than early finishes.",
      "advantage": "neutral"
    },
    "common_opponents": {
      "label": "No shared opponents",
      "summary": "No shared prior opponents before this fight date.",
      "advantage": "neutral"
    }
  }
}
```

`advantage` should be one of `fighter_a`, `fighter_b`, or `neutral`.

## UI Copy

The compare sheet should present these as a signal board near the existing probability and value content.

Use short operator-facing copy:

- `Round tendency`
- `Common opponents`
- `Thin history`
- `No shared opponents`
- `Review signal`, not `Bet signal`

Avoid copy that implies certainty:

- Do not say `lock`, `best bet`, `guaranteed`, or `sharp`.
- Do not convert a signal into a wager recommendation.
- Do not call a small model lean a strong prediction.

## Out Of Scope For Epic 1

- Historical odds importer/schema work.
- Injury, camp, weight-cut, or short-notice context ingestion.
- Prop-bet prediction, round prediction, method prediction, or live in-fight logic.
- Model-training use of contextual intelligence before labels and walk-forward backtests exist.

## Contextual Overlay

Epic 3 defines a separate contextual overlay for injury, camp, weight-cut, and short-notice fight context. The ontology is documented in [contextual_overlay_ontology.md](./contextual_overlay_ontology.md).

The overlay is intentionally outside model training for now. It can support operator review, audit trails, and future label collection, but it must not alter model probabilities, edge calculations, stake sizing, or pick selection until labels and walk-forward backtests exist.
