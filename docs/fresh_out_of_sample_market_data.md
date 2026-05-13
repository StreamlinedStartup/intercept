# Fresh Out-of-Sample Market Data Validation

This epic validates frozen market-gate candidates on UFC FightOdds events after the
locked historical holdout.

## Scope

- Fresh window: events after `2024-03-09`.
- Source: existing FightOdds GraphQL importer in `packages/db/src/import-fightodds-event.ts`.
- Matching: existing canonical matcher in `packages/db/src/match-historical-odds.ts`.
- Evaluation: existing report-only config harness in `services/python/ml/experiment_harness.py`.
- Candidate policy: evaluate frozen candidates only; do not tune on the fresh slice.
- Persistence policy: JSON/Markdown artifacts only, `writes_model_versions=false`.

## Route

1. Import fresh UFC FightOdds events:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
pnpm --filter @interceptor/db import:fightodds:range -- \
  --from 2024-03-10 \
  --to 2026-05-14 \
  --limit 30 \
  --delay-ms 1500 \
  --continue-on-error
```

2. Match imported FightOdds rows to canonical fights:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
pnpm --filter @interceptor/db match:fightodds:all
```

3. Generate coverage evidence:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
pnpm --filter @interceptor/db report:fightodds:coverage -- \
  --output data/experiments/fresh-market-coverage.json \
  --markdown data/experiments/fresh-market-coverage.md
```

4. Run the frozen candidate config against the fresh market-covered slice only.

The current locked config already freezes the candidates and gate. This epic may add
a fresh-slice config that reuses those variants with an explicit `after_date`
filter if the current harness cannot isolate imported post-holdout events.
