---
# intercept-r03n
title: External UFC stats dataset integration
status: completed
type: epic
priority: high
created_at: 2026-05-11T00:24:23Z
updated_at: 2026-05-11T01:06:16Z
---

Use Greco1899/scrape_ufc_stats CSV exports as an external historical corpus for model tuning and walk-forward backtesting, without copying GPL scraper code into this repo.



## Summary of Changes

- Added external UFC Stats dataset documentation, local snapshot download, canonical DB import, walk-forward backtesting, and saved-report summaries.
- Kept upstream GPL scraper code out of this repo; only operator-downloaded CSV snapshots are used as ignored local data.
- Completed child beans `intercept-bsn7`, `intercept-n89z`, `intercept-0vfw`, `intercept-pqsx`, and `intercept-u1vf` with one commit per task.

## Verification

- `pnpm data:ufcstats:snapshot -- --snapshot-id codex-verify-n89z-2`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor pnpm --filter @interceptor/db import:ufcstats data/external/ufcstats/codex-verify-n89z-2`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest --start-date 2024-01-01 --max-events 2 --output data/backtests/smoke-walk-forward.json`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.backtest_report data/backtests/smoke-walk-forward.json --format json`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor services/python/.venv/bin/python -m pytest services/python -q`
- `./scripts/ci-local.sh` passed install, lint, build, typecheck, Vitest, and Python tests, then blocked in E2E port cleanup on an uninterruptible `lsof -ti:3004`; direct Playwright coverage passed with `CI=true E2E_PORT=3014 PLAYWRIGHT_HTML_OPEN=never npx playwright test`.
