# Contextual Overlay Ontology

The contextual overlay captures fight-week and camp-context risk that the model does not currently know. It is an operator review layer, not a model feature set and not betting logic.

The first version tracks four contexts:

- injury
- camp
- weight cut
- short notice

Each context is recorded as an auditable flag with source attribution. A flag can inform review copy, filtering, and future labeling, but it must not change model probability, edge, stake sizing, or pick selection until labels and walk-forward backtests prove value.

## Shared Shape

Every contextual flag should use the same core shape:

| Field | Meaning |
|---|---|
| `context` | One of `injury`, `camp`, `weight_cut`, or `short_notice`. |
| `label` | The normalized label for the observed context. |
| `severity` | `low`, `medium`, `high`, or `unknown`. |
| `direction` | `negative`, `positive`, `mixed`, or `unknown` from the flagged fighter's perspective. |
| `fighter_id` | Canonical fighter ID when matched. |
| `fight_id` | Canonical fight ID when matched. |
| `event_id` | Canonical event ID when matched. |
| `observed_at` | Timestamp when the source was captured or reviewed. |
| `source_url` | URL or internal artifact proving where the flag came from. |
| `source_type` | `official`, `interview`, `news`, `social`, `commission`, or `manual_review`. |
| `source_excerpt` | Short human-readable evidence excerpt. |
| `review_status` | `unreviewed`, `confirmed`, `rejected`, or `superseded`. |
| `notes` | Optional reviewer note for ambiguous cases. |

`severity`, `direction`, and `review_status` are deliberately separate. For example, a confirmed camp change can have unknown direction if the new camp quality cannot be defended from evidence.

## Injury Labels

Injury labels capture known or reported physical availability risk.

| Label | Use When | Default Direction |
|---|---|---|
| `active_injury_reported` | A current injury is reported before the fight and the fighter still competes. | `negative` |
| `recent_medical_issue` | Illness, infection, surgery recovery, or other medical issue is reported near camp or fight week. | `negative` |
| `postponed_due_to_injury` | This matchup or a recent scheduled bout was postponed because this fighter withdrew injured. | `negative` |
| `returning_from_injury_layoff` | The fighter is returning after an injury-linked layoff rather than only a generic long layoff. | `negative` |
| `injury_denied_or_cleared` | Prior injury concern is explicitly denied or cleared by a credible source. | `mixed` |
| `injury_context_unclear` | Injury discussion exists but cannot be mapped to a stronger label. | `unknown` |

Do not infer actual injuries from damage proxies, betting movement, or long layoffs alone. Those are separate model or market observations unless a source ties them to an injury.

## Camp Labels

Camp labels capture training environment and preparation changes.

| Label | Use When | Default Direction |
|---|---|---|
| `camp_change` | Fighter changed primary gym, head coach, or core training location for this fight. | `unknown` |
| `camp_disruption` | Source reports travel, visa, illness, personal, gym, or scheduling disruption during camp. | `negative` |
| `specialized_camp` | Source reports a targeted camp addition that directly maps to opponent style or preparation. | `positive` |
| `shortened_camp` | Fighter reports or credible source confirms a shortened camp, separate from formal short-notice status. | `negative` |
| `stable_camp_reported` | Source explicitly reports normal/stable camp after public uncertainty. | `positive` |
| `camp_context_unclear` | Camp context exists but cannot be mapped to a stronger label. | `unknown` |

Camp quality is hard to label. Avoid ranking gyms, coaches, or partners unless the evidence is explicit and reviewable.

## Weight-Cut Labels

Weight-cut labels capture making-weight and fight-week body-composition risk.

| Label | Use When | Default Direction |
|---|---|---|
| `missed_weight_recent` | Fighter missed contracted weight in a recent relevant bout. | `negative` |
| `missed_weight_current` | Fighter misses contracted weight for the current fight. | `negative` |
| `heavy_cut_reported` | Fighter or credible source reports an unusually difficult cut. | `negative` |
| `weight_class_change` | Fighter moves to a materially different division for the current fight. | `mixed` |
| `catchweight_context` | Bout is catchweight or changed weight terms in a way relevant to preparation. | `mixed` |
| `weight_cut_context_unclear` | Weight-cut discussion exists but cannot be mapped to a stronger label. | `unknown` |

The existing model can already use target `weight_class` and historical division movement. This overlay is for sourced fight-week context, not duplicating structured features.

## Short-Notice Labels

Short-notice labels capture preparation asymmetry caused by late booking or opponent change.

| Label | Use When | Default Direction |
|---|---|---|
| `short_notice_fighter` | Fighter accepts the bout on short notice. | `negative` |
| `replacement_opponent` | Fighter faces a late replacement opponent. | `mixed` |
| `opponent_changed_late` | Opponent changes late enough to affect preparation but the fighter is not necessarily the replacement. | `mixed` |
| `late_location_or_weight_change` | Fight terms changed late in a way that affects preparation. | `mixed` |
| `full_camp_against_short_notice_opponent` | Fighter had a normal camp and faces a short-notice opponent. | `positive` |
| `short_notice_context_unclear` | Short-notice discussion exists but cannot be mapped to a stronger label. | `unknown` |

Short notice should be labeled relative to the affected fighter. The same fight can have a negative flag for one fighter and a positive or mixed flag for the other.

## Review Rules

- Keep every flag tied to a source or explicit manual review artifact.
- Prefer `unknown` over invented severity or direction.
- Preserve rejected flags for audit history instead of deleting them.
- Treat public reporting as mutable; later official weigh-in, bout-cancellation, or commission facts can supersede earlier reports.
- Never use contextual flags as model-training features, probability adjustments, wager recommendations, or auto-betting triggers until a labeled historical set and walk-forward backtest exist.

## First Slice Output

The first product slice should expose this data as a separate `contextual_overlay` object beside model output and decision signals:

```json
{
  "contextual_overlay": {
    "flags": [
      {
        "context": "short_notice",
        "label": "short_notice_fighter",
        "severity": "medium",
        "direction": "negative",
        "review_status": "confirmed"
      }
    ],
    "summary": "One confirmed short-notice preparation flag requires review.",
    "risk_level": "review"
  }
}
```

`risk_level` should be `none`, `watch`, or `review`. It is a review priority, not a betting recommendation.
