# FightOdds Prop Shape Discovery

Date: 2026-05-15
Source: FightOdds GraphQL (`https://api.fightodds.io/gql`)
Scope: discovery only; no production tables or imports were written.

## Probe

Matched source event:

- `eventOfferTable(pk: 5362)`
- Event slug: `ufc-fight-night-237-moreno-vs-royval-2`
- Fight slug: `brandon-moreno-vs-brandon-royval-51622`
- Fight source pk: `51622`
- Fight result: Brandon Moreno def. Brandon Royval by split decision, round 5, `5:00`
- Source fight had `propCount: 76`

GraphQL surfaces used:

- `eventOfferTable(pk)` returns event-level fight offers and the fight slug needed for prop discovery.
- `fightPropOfferTable(slug)` returns fight-level prop markets and sportsbook offers.
- `FightPropOfferTableNode` fields: `id`, `fight`, `propOffers`.
- `PropOfferNode` fields: `offerType`, `propName1`, `propName2`, `bestOdds1`, `bestOdds2`, `offers`.
- `OfferTypeNode` fields used: `offerTypeId`, `category`, `subCategory`, `description`, `value`, `notDescription`.
- `OfferTableOfferNode` fields used: `id`, `sportsbook`, `outcome1`, `outcome2`.
- `OutcomeNode` fields used: `id`, `name`, `fighter`, `odds`, `oddsPrev`, `oddsOpen`, `oddsBest`, `oddsWorst`, `isNot`.

## Market Availability

The source has enough prop coverage for the opportunity harness targets.

| Target | Source evidence | Import posture |
| --- | --- | --- |
| Fight goes to decision | `offerTypeId: DISTANCE`, `description: Fight goes the distance`, `notDescription: Fight ends inside distance`; two outcomes per sportsbook | Primary import candidate. `outcome1` is decision/distance yes; `outcome2` is inside-distance/no. |
| Finish likelihood | Same `DISTANCE` market, `outcome2` no/distance-not outcome; fight also exposes `fightItdOdds` summary | Primary import candidate via two-way `DISTANCE`; use summary field only as fallback/reporting, not as sportsbook-level baseline. |
| Fighter wins by decision | Fight summary exposes `fighter1DecOdds` and `fighter2DecOdds`; prop feed includes method/round decision types such as `R_5_DEC` | Import later only after confirming a clean non-round fighter-by-decision market across multiple fights. Do not infer from `R_5_DEC`. |
| Fighter wins inside distance | Fight summary exposes `fighter1ItdOdds` and `fighter2ItdOdds`; `KO_SUB` exists as fighter wins by KO/TKO or submission | Import later as a fighter finish family; `KO_SUB` is one-sided in the observed feed. |
| KO/TKO | Fight summary exposes `fighter1KoOdds` and `fighter2KoOdds`; prop feed includes round-specific KO/TKO ids such as `KO_1`, `KO_2`, etc. | Present, but round-specific markets should be out of the first import slice. |
| Submission | Fight summary exposes `fighter1SubOdds` and `fighter2SubOdds`; prop feed includes round-specific `SUB_1` through `SUB_5` ids | Present, but round-specific markets should be out of the first import slice. |

Observed market ids that should be excluded from the first prop import:

- `STRAIGHT`: duplicate moneyline-like market already handled by historical moneyline import.
- `DRAW`: one-sided long-tail market, not part of the initial decision/finish harness baseline.
- `OVERUNDER_*`: round totals, useful later but not equivalent to decision.
- `R_*`, `KO_*`, `SUB_*`: round-specific methods, not the first harness target.
- `STRAIGHT_NS`: scorecards no-action fighter straight market, useful later but not a fight-level finish baseline.

## Field Contract

Use these identifiers in the future import slice:

- Source event id: `eventOfferTable.pk` as text, with event slug and source URL for operator traceability.
- Source fight id: `fightPropOfferTable.fight.pk` as text, plus fight slug.
- Source prop market id: deterministic key from `fight.pk`, `offerType.offerTypeId`, `propName1`, and `propName2`; the observed `PropOfferNode` payload did not expose a stable scalar id in the queried shape.
- Sportsbook id: `offers.edges[].node.sportsbook.slug`; keep `shortName` as display metadata.
- Outcome id: `outcome.id` when present; otherwise deterministic key from source prop id, sportsbook slug, and side.
- Outcome side: `outcome1` and `outcome2`; preserve `isNot` because no/under/not-distance outcomes mark complement semantics.
- Odds fields:
  - `odds` is the source current price at scrape/import time.
  - `oddsPrev` is the previous source price, but the API does not expose its timestamp in this shape.
  - `oddsOpen` exists and can be stored separately later, but it must not be treated as close/current.
  - `oddsBest` and `oddsWorst` are source range summaries, not sportsbook-current prices.

## Recommendation

The first production slice should import only the two-way `DISTANCE` market into a new historical prop odds table. That directly supports `fight_goes_decision` and `finish_likelihood` without deriving complements from result text or round totals. Fighter-specific method markets should follow after a second discovery pass over multiple events confirms a clean non-round `DEC`, `ITD`, `KO`, and `SUB` offer family instead of relying on summary fields or round-specific props.
