# FightOdds Prop Coverage

- Generated: `2026-05-16T02:10:53.989Z`
- Report only: `true`
- Writes `model_versions`: `false`
- Source events with prop rows: 31
- Fights matched: 322/452 (71.2%)
- Distance markets: 398
- Prop rows linked: 12379/15215 (81.4%)
- Current/previous rows: 8338/6877
- Decision/finish baselines ready: `false`

## Readiness

- Not ready: imported prop rows are missing, or some rows are not linked to canonical fights.

## Timestamp Limits

- Imported prop rows use line_kind source_current or source_previous only.
- FightOdds exposes oddsPrev but no previous-price timestamp in this query shape.
- oddsOpen, oddsBest, and oddsWorst are preserved in raw_metadata but are not treated as model-ready timestamps.

## Events

| Source event | Date | Fights matched | Distance markets | Prop rows linked |
| --- | --- | ---: | ---: | ---: |
| UFC Fight Night 237: Moreno vs. Royval 2 (5362) | 2024-02-24 | 12/14 | 12 | 294/294 |
| UFC 319: Du Plessis vs. Chimaev (6488) | 2025-08-16 | 10/16 | 12 | 299/353 |
| UFC Fight Night: Walker vs. Zhang (6511) | 2025-08-23 | 6/12 | 12 | 137/269 |
| UFC Fight Night: Imavov vs. Borralho (6547) | 2025-09-06 | 12/15 | 13 | 311/339 |
| UFC Fight Night: Lopes vs. Silva (6414) | 2025-09-13 | 12/15 | 14 | 356/406 |
| UFC Fight Night: Ulberg vs. Reyes (6602) | 2025-09-27 | 11/16 | 12 | 339/371 |
| UFC 320: Ankalaev vs. Pereira 2 (6552) | 2025-10-04 | 9/15 | 14 | 286/432 |
| UFC Fight Night 261: Oliveira vs. Gamrot (6619) | 2025-10-11 | 10/13 | 12 | 310/369 |
| UFC Fight Night: de Ridder vs. Allen (6553) | 2025-10-18 | 10/14 | 13 | 308/400 |
| UFC 321: Aspinall vs. Gane (6593) | 2025-10-25 | 10/14 | 13 | 305/399 |
| UFC Fight Night: Garcia vs. Onama (6668) | 2025-11-01 | 9/16 | 13 | 338/487 |
| UFC Fight Night: Bonfim vs. Brown (8596) | 2025-11-08 | 10/15 | 12 | 410/493 |
| UFC 322: Della Maddalena vs. Makhachev (8597) | 2025-11-15 | 11/15 | 14 | 475/595 |
| UFC Fight Night 265: Tsarukyan vs. Hooker (6603) | 2025-11-22 | 10/15 | 14 | 397/565 |
| UFC 323: Dvalishvili vs. Yan 2 (8620) | 2025-12-06 | 13/14 | 14 | 551/597 |
| UFC Fight Night: Royval vs. Kape (8609) | 2025-12-13 | 11/14 | 12 | 447/483 |
| UFC 324: Gaethje vs. Pimblett (8768) | 2026-01-24 | 9/14 | 11 | 407/491 |
| UFC 325: Volkanovski vs. Lopes 2 (8805) | 2026-01-31 | 7/16 | 13 | 309/566 |
| UFC Fight Night: Bautista vs. Oliveira (8813) | 2026-02-07 | 10/15 | 13 | 432/535 |
| UFC Fight Night: Strickland vs. Hernandez (8828) | 2026-02-21 | 12/15 | 14 | 521/601 |
| UFC Mexico: Moreno vs. Kavanagh (8814) | 2026-02-28 | 10/14 | 13 | 428/555 |
| UFC 326: Holloway vs. Oliveira 2 (8823) | 2026-03-07 | 11/16 | 12 | 475/519 |
| UFC Fight Night: Emmett vs. Vallejos (8830) | 2026-03-14 | 12/14 | 14 | 513/594 |
| UFC London: Evloev vs. Murphy (8822) | 2026-03-21 | 13/14 | 13 | 512/512 |
| UFC Seattle: Adesanya vs. Pyfer (8832) | 2026-03-28 | 10/17 | 13 | 429/561 |
| UFC Fight Night: Moicano vs. Duncan (8898) | 2026-04-04 | 12/14 | 13 | 557/603 |
| UFC 327: Procházka vs. Ulberg (8861) | 2026-04-11 | 10/13 | 12 | 444/537 |
| UFC Fight Night: Burns vs. Malott (8946) | 2026-04-18 | 10/14 | 12 | 445/531 |
| UFC Fight Night: Sterling vs. Zalal (8959) | 2026-04-25 | 11/14 | 13 | 512/606 |
| UFC Perth: Della Maddalena vs. Prates (8994) | 2026-05-02 | 12/15 | 13 | 511/549 |
| UFC 328: Chimaev vs. Strickland (9010) | 2026-05-09 | 7/14 | 13 | 321/603 |

## Outcomes

| Side | Is not | Outcome | Rows |
| --- | --- | --- | ---: |
| outcome1 | false | Yes | 1565 |
| outcome1 | false | Will the fight go the distance? - Yes | 1518 |
| outcome1 | false | Will The Fight Go The Distance - Yes | 1001 |
| outcome1 | false | Goes the Distance - Yes | 747 |
| outcome1 | false | Fight Goes To Decision - Yes | 647 |
| outcome1 | false | Fight to Go the Distance - Yes | 639 |
| outcome1 | false | Fight to go the Distance | 628 |
| outcome1 | false | To go the distance - Yes | 503 |
| outcome1 | false | Fight to Go the Distance? - Yes | 481 |
| outcome1 | false | Fight To Go The Distance - Yes | 133 |
| outcome1 | false | Fight Goes To Decision? - Yes | 44 |
| outcome2 | true | No | 1562 |
| outcome2 | true | Will the fight go the distance? - No | 1513 |
| outcome2 | true | Will The Fight Go The Distance - No | 996 |
| outcome2 | true | Goes the Distance - No | 748 |
| outcome2 | true | Fight to Go the Distance - No | 684 |
| outcome2 | true | Fight Goes To Decision - No | 646 |
| outcome2 | true | To go the distance - No | 503 |
| outcome2 | true | Fight to Go the Distance? - No | 481 |
| outcome2 | true | Fight To Go The Distance - No | 132 |
| outcome2 | true | Fight Goes To Decision? - No | 44 |
