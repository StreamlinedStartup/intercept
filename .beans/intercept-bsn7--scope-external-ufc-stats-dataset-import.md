---
# intercept-bsn7
title: Scope external UFC stats dataset import
status: completed
type: task
priority: normal
created_at: 2026-05-11T00:24:33Z
updated_at: 2026-05-11T00:25:32Z
parent: intercept-r03n
---

Document why and how Greco1899/scrape_ufc_stats should be used, source files, license boundary, target DB mapping, and backtesting/model-tuning workflow.

## Summary of Changes

- Added `docs/external_ufcstats_dataset.md` describing how to use Greco1899/scrape_ufc_stats as an external daily-refreshed CSV source for model training and backtesting.
- Documented the source CSV files, GPL boundary, local snapshot architecture, DB mapping, walk-forward backtesting plan, and relationship to our live UFC Stats scraper.
- Created the dependent Beans for download, import, walk-forward backtesting, and model-tuning report work.

## Verification

- Reviewed the upstream README, license, repository file list, and raw CSV headers/sample rows.
- Confirmed the existing repo had no ready Beans before creating the new graph.
