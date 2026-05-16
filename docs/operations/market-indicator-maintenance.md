# Market Indicator Maintenance

Daily operator command:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
API_BASE_URL=http://localhost:3001 \
pnpm ops:market-indicators:daily
```

Dry run:

```bash
pnpm ops:market-indicators:daily -- --dry-run
```

The job is report-only. It does not retrain models, write `model_versions`, promote artifacts, or activate betting decisions.

## Daily Flow

1. `POST /api/predict/sync/upcoming-cards`
2. `POST /api/predict/backfill/seed?scope=in-window`
3. `GET /api/odds-mma/snapshot?refresh=1`
4. `pnpm --filter @interceptor/db import:fightodds:event -- --event-pks "$FIGHTODDS_EVENT_PKS" --include-props`
5. `pnpm --filter @interceptor/db match:fightodds:all`
6. `pnpm --filter @interceptor/db refresh:market-indicators`

Steps 4 and 5 require `FIGHTODDS_EVENT_PKS` because FightOdds historical prop import is event-scoped. If that variable is absent, the job records an explicit skipped step instead of silently pretending prop markets were refreshed.

## Cron Example

```cron
15 13 * * * cd /Users/vulturestudio/intercept && DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor API_BASE_URL=http://localhost:3001 /opt/homebrew/bin/pnpm ops:market-indicators:daily >> /tmp/interceptor-market-indicators.log 2>&1
```

The command exits non-zero on hard failures. Keep `ODDS_API_KEY` available to the API service before enabling the cron entry.
