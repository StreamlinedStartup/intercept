# Method and Round Prop Source Shapes

- Source: FightOdds `fightPropOfferTable`
- Discovery fight: `brandon-moreno-vs-brandon-royval-51622`
- Status: `research_only`

## Supported From Existing Imports

| Target | Source shape | Notes |
|---|---|---|
| goes to decision | `DISTANCE` paired market | Already imported as `historical_prop_odds` with `market_family='fight_distance'`; outcome1 is decision/goes-distance, outcome2 is finish/inside-distance. |
| finish likelihood | `DISTANCE` paired market | Complement of goes-to-decision market. |
| KO/TKO | `propFight.fighter1KoOdds`, `propFight.fighter2KoOdds` in imported prop row metadata | FightOdds exposes fight-level best method odds. Use no-vig normalization across KO/TKO, submission, and decision method prices. |
| submission | `propFight.fighter1SubOdds`, `propFight.fighter2SubOdds` in imported prop row metadata | Same method distribution as KO/TKO. |

## Requires Importer Expansion

| Target | Source shape | Notes |
|---|---|---|
| over/under rounds | `OVERUNDER_0.5`, `OVERUNDER_1.5`, `OVERUNDER_2.5`, `OVERUNDER_3.5`, `OVERUNDER_4.5` paired markets | Present in `propOffers(first: 24)` before deeper method-by-round props. Import current/previous lines like DISTANCE. |

## Not In This Slice

| Target | Source shape | Reason |
|---|---|---|
| fighter-specific win by KO/TKO | `KO`, `KO_1`, `KO_2`, etc. single-sided props | Single-sided longshot markets do not provide a paired no-vig complement in the current table shape. |
| fighter-specific win by submission | `SUB`, `SUB_1`, `SUB_2`, etc. single-sided props | Use method distribution first; add single-sided EV later only if a clear complement/field is available. |
| exact round method | `KO_1`, `SUB_1`, `R_1_2`, etc. | Useful later, but too sparse and single-sided for the first market-backed binary target expansion. |
