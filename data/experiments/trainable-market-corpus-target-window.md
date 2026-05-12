# Trainable Market-Corpus Target Window

- Generated: `2026-05-12T04:25:10Z`
- Report-only: `true`
- Writes `model_versions`: `false`

## Baseline

| Metric | Count |
|---|---:|
| Imported FightOdds events | 37 |
| Matched FightOdds events | 37 |
| Scored market-covered fights | 345 |
| Scored market-covered events | 37 |
| Model-eligible fights | 241 |
| Model-eligible events | 26 |

The current imported corpus starts at `2023-05-06` with `UFC 288: Sterling vs. Cejudo`. Under the D2-MIX model-family contract, an evaluated event needs 100 prior market-covered training samples. That leaves only 26 model-eligible events, below the 30-event stability floor.

## Target Window

Import the unique UFC FightOdds events from `2023-01-01 <= event date < 2023-05-06`.

| Date | PK | Event |
|---|---:|---|
| 2023-04-29 | 4592 | UFC Fight Night: Song vs. Simon |
| 2023-04-22 | 4579 | UFC Fight Night: Pavlovich vs. Blaydes |
| 2023-04-15 | 4580 | UFC Fight Night: Holloway vs. Allen |
| 2023-04-08 | 4556 | UFC 287: Pereira vs Adesanya 2 |
| 2023-03-25 | 4501 | UFC Fight Night: Vera vs. Sandhagen |
| 2023-03-18 | 4483 | UFC 286: Edwards vs. Usman 3 |
| 2023-03-11 | 4486 | UFC Fight Night: Yan vs. Dvalishvili |
| 2023-03-04 | 4450 | UFC 285: Jones vs. Gane |
| 2023-02-25 | 4469 | UFC Fight Night: Krylov vs. Spann |
| 2023-02-18 | 4460 | UFC Fight Night: Andrade vs. Blanchfield |
| 2023-02-11 | 4438 | UFC 284: Makhachev vs. Volkanovski |
| 2023-02-04 | 4441 | UFC Fight Night: Lewis vs. Spivac |
| 2023-01-21 | 4382 | UFC 283: Teixeira vs. Hill |
| 2023-01-14 | 4426 | UFC Fight Night: Strickland vs. Imavov |

## Next Commands

```bash
pnpm --filter @interceptor/db import:fightodds:event -- --event-pks 4592,4579,4580,4556,4501,4483,4486,4450,4469,4460,4438,4441,4382,4426 --delay-ms 1500 --continue-on-error
pnpm --filter @interceptor/db match:fightodds:all
pnpm --filter @interceptor/db report:fightodds:coverage
```

## Rationale

D2-MIX needs at least four more model-eligible events to cross the 30-event stability floor. A 14-event older UFC window provides enough buffer for unmatched or cancelled bouts while keeping the next import slice narrow and auditable.
