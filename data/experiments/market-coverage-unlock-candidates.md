# D2-MCU Coverage-Completion Candidates

Generated: 2026-05-12T03:41:54Z

Report-only: true
Writes model_versions: false

## Starting Point

The D2-HOC final report reached 235 scored market-covered fights across 26 scored market-covered events. The fight threshold is satisfied, but the market gate still needs 30 scored market-covered events.

## Candidate Strategy

Use two deterministic paths:

- Primary: rematch four already-imported FightOdds events that failed event resolution because FightOdds uses `UFC on ESPN` or numbered `Fight Night` names while the canonical UFCStats events use Fight Night names.
- Supplemental: if rematching does not close the full gap, import the seven immediately prior UFC FightOdds events before the D2-HOC target window.

This gives enough margin to reach 30 scored events without tuning the model or using newer post-UFC-299 market data.

## Primary Rematch Candidates

| Source ID | Source Event | Date | Canonical Event | Canonical Fights | Risk |
| --- | --- | --- | --- | ---: | --- |
| 4751 | UFC on ESPN 50: Sandhagen vs. Font | 2023-08-05 | UFC Fight Night: Sandhagen vs. Font | 12 | low |
| 4738 | UFC on ESPN 51: Luque vs. dos Anjos | 2023-08-12 | UFC Fight Night: Luque vs. Dos Anjos | 13 | low |
| 4802 | UFC Fight Night 226: Gane vs. Spivak | 2023-09-02 | UFC Fight Night: Gane vs. Spivac | 11 | low |
| 5251 | UFC on ESPN 52: Dariush vs. Tsarukyan | 2023-12-02 | UFC Fight Night: Dariush vs. Tsarukyan | 12 | low |

## Supplemental Import Candidates

| FightOdds PK | Source Slug | Canonical Event | Date | Canonical Fights | Risk |
| --- | --- | --- | --- | ---: | --- |
| 4594 | ufc-288-sterling-vs-cejudo | UFC 288: Sterling vs. Cejudo | 2023-05-06 | 12 | low |
| 4615 | ufc-on-abc-4-rozenstruik-vs-almeida | UFC Fight Night: Rozenstruik vs. Almeida | 2023-05-13 | 11 | low |
| 4627 | ufc-fight-night-dern-vs-hill | UFC Fight Night: Dern vs. Hill | 2023-05-20 | 12 | low |
| 4643 | ufc-fight-night-kara-france-vs-albazi | UFC Fight Night: Kara-France vs. Albazi | 2023-06-03 | 13 | low |
| 4654 | ufc-289-nunes-vs-aldana | UFC 289: Nunes vs. Aldana | 2023-06-10 | 11 | low |
| 4666 | ufc-fight-night-vettori-vs-cannonier | UFC Fight Night: Vettori vs. Cannonier | 2023-06-17 | 12 | low |
| 4668 | ufc-on-abc-5-emmett-vs-topuria | UFC Fight Night: Emmett vs. Topuria | 2023-06-24 | 13 | low |

## Next Commands

```bash
pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 4594,4615,4627,4643,4654,4666,4668 --delay-ms 1500 --continue-on-error
pnpm --filter @interceptor/db match:fightodds:all
```

Model-improvement experiments remain blocked by this task. The next tasks must import/rematch, rerun coverage, and rerun the market gate.
