# D2-MCU Import Batch Report

Generated: 2026-05-12T03:45:15Z

Report-only: true
Writes model_versions: false

## Import Result

Imported the supplemental FightOdds event batch from `intercept-zlwa`.

| Metric | Value |
| --- | ---: |
| Events imported | 7 |
| Events failed | 0 |
| Fights read | 108 |
| Moneyline rows read | 5,458 |
| Import-time unmatched rows created | 108 |
| Cancelled fights | 24 |

## Match Result

After `match:fightodds:all`, the corpus reached:

| Metric | Value |
| --- | ---: |
| Source events | 37 |
| Matched source events | 31 |
| Source fights | 572 |
| Matched fights | 299 |
| Ambiguous fights | 0 |
| Moneyline rows | 29,056 |
| Linked moneyline rows | 16,912 |
| Review rows | 273 |

## Supplemental Event Outcomes

| Source ID | Event | Date | Status |
| --- | --- | --- | --- |
| 4594 | UFC 288: Sterling vs. Cejudo | 2023-05-06 | matched |
| 4615 | UFC on ABC 4: Rozenstruik vs. Almeida | 2023-05-13 | unmatched |
| 4627 | UFC Fight Night: Dern vs. Hill | 2023-05-20 | matched |
| 4643 | UFC Fight Night: Kara-France vs. Albazi | 2023-06-03 | matched |
| 4654 | UFC 289: Nunes vs. Aldana | 2023-06-10 | matched |
| 4666 | UFC Fight Night: Vettori vs. Cannonier | 2023-06-17 | matched |
| 4668 | UFC on ABC 5: Emmett vs. Topuria | 2023-06-24 | unmatched |

## Next Blocker

Two supplemental UFC on ABC events and four primary D2-HOC alias events still need deterministic event-alias rematching in `intercept-p6v3`.

Model-improvement experiments remain blocked by this task.
