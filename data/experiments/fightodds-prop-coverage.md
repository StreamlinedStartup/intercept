# FightOdds Prop Coverage

- Generated: `2026-05-16T00:45:39.211Z`
- Report only: `true`
- Writes `model_versions`: `false`
- Source events with prop rows: 1
- Fights matched: 12/14 (85.7%)
- Distance markets: 12
- Prop rows linked: 294/294 (100.0%)
- Current/previous rows: 164/130
- Decision/finish baselines ready: `true`

## Readiness

- Ready for report-only opportunity-harness evaluation of fight_goes_decision and finish_likelihood baselines.
- Not ready for betting recommendations or model promotion; the corpus is still a one-event prop slice.
- Fighter-specific decision, KO/TKO, submission, and inside-distance method markets are present in source data but remain outside this first imported slice.

## Timestamp Limits

- Imported prop rows use line_kind source_current or source_previous only.
- FightOdds exposes oddsPrev but no previous-price timestamp in this query shape.
- oddsOpen, oddsBest, and oddsWorst are preserved in raw_metadata but are not treated as model-ready timestamps.

## Events

| Source event | Date | Fights matched | Distance markets | Prop rows linked |
| --- | --- | ---: | ---: | ---: |
| UFC Fight Night 237: Moreno vs. Royval 2 (5362) | 2024-02-24 | 12/14 | 12 | 294/294 |

## Outcomes

| Side | Is not | Outcome | Rows |
| --- | --- | --- | ---: |
| outcome1 | false | Yes | 61 |
| outcome1 | false | Will The Fight Go The Distance - Yes | 24 |
| outcome1 | false | Goes the Distance - Yes | 23 |
| outcome1 | false | Fight Goes To Decision? - Yes | 20 |
| outcome1 | false | To go the distance - Yes | 19 |
| outcome2 | true | No | 61 |
| outcome2 | true | Will The Fight Go The Distance - No | 24 |
| outcome2 | true | Goes the Distance - No | 23 |
| outcome2 | true | Fight Goes To Decision? - No | 20 |
| outcome2 | true | To go the distance - No | 19 |
