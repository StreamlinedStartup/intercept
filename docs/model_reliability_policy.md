# Model Reliability Policy

This policy governs `value_status` and all UFC Fight Predictor market language.

## Current Status

The current product status is `insufficient_coverage`.

The market gate scored 30 matched historical fights across 3 FightOdds events. A validated status requires at least 200 scored matched fights across 30 market-covered events and a model ROI at least 2 percentage points above the market-favorite baseline. Until those gates pass, UI, API, and docs must describe market output as research-only.

## Status Meanings

| value_status | Meaning | Allowed product language |
|---|---|---|
| `insufficient_coverage` | Market history is too small to evaluate value claims. | Market comparison, research edge, simulated research ROI. |
| `research_only` | Coverage is large enough to evaluate, but the model has not beaten the market gate. | Market comparison, research edge, simulated research ROI. |
| `validated` | Coverage and market-gate criteria pass in a report-only walk-forward evaluation. | Validated may be shown, but no auto-betting language is allowed. |

## Validation Gate

`value_status` may become `validated` only when all of these are true:

- Leakage audit passes with zero failed checks.
- Historical odds coverage includes at least 200 scored fights across at least 30 matched market events.
- The model or approved model blend beats the no-vig market-favorite baseline by at least 2 percentage points of simulated flat-stake ROI.
- Report artifacts include accuracy, calibration gap, log loss, Brier score, ROC AUC, simulated ROI, and coverage sample sizes.
- The evaluation is report-only and does not write active `model_versions`.
- UI/API wording remains explicit that historical ROI is simulated and that no automated betting action is implied.

## Current Evidence

| Artifact | Result |
|---|---|
| `data/experiments/leakage-audit.md` | Pass, 15 checks, 0 failed. |
| `data/experiments/simple-baselines.md` | Research-only simple baselines, 8 events and 99 samples. |
| `data/experiments/historical-odds-coverage.md` | 3 matched events, 30 matched fights, 1,553 linked moneyline rows. |
| `data/experiments/market-gate-report.md` | `insufficient_coverage`, 30 scored fights across 3 events. |
| `data/experiments/model-reliability-final-report.md` | Final D2-RV rollup and status decision. |

## Product Rules

- Do not use "value pick" or "betting edge" for unvalidated surfaces.
- Keep numeric `edge_pct`, `market_prob`, odds, and simulated ROI available for research and audit.
- Show `value_status_reason` anywhere `value_status` is displayed or used for filtering.
- Treat edge filters such as `>5%` and `>10%` as research cohorts, not action thresholds.
- Do not write active `model_versions` from audit, baseline, odds coverage, market-gate, or final-report commands.
