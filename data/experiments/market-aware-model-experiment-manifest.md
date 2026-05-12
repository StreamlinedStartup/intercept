# D2-MIX Experiment Manifest

Generated: 2026-05-12T03:58:40Z

Report-only: true
Writes model_versions: false
Activation allowed: false

## Frozen Evidence Bundle

- `data/experiments/market-coverage-unlock-validation-coverage.json`
- `data/experiments/market-coverage-unlock-leakage-audit.json`
- `data/experiments/market-coverage-unlock-simple-baselines.json`
- `data/experiments/market-coverage-unlock-market-gate-report.json`

## Dataset Contract

Use the D2-MCU coverage-passing research-only corpus:

| Metric | Value |
| --- | ---: |
| Source events imported | 37 |
| Source events matched | 37 |
| Scored market-covered events | 37 |
| Scored market-covered fights | 345 |

Chronology: walk-forward-compatible chronological event order.

Split policy: all training, calibration, and selection logic must use only fights before the evaluated fight/event.

Inclusion rules:

- UFC canonical events only.
- Completed fights only.
- Historical odds rows must be linked to both canonical fighters for market-comparison metrics.
- Cancelled source fights remain excluded from scored market metrics and reportable as review rows.
- Rows with unresolved fighter-pair matching remain excluded from scored market metrics and reportable as review rows.

Exclusion rules:

- No future fight stats, future market odds, post-fight results, or same-event later-bout labels may be used in features for an evaluated fight.
- No unlinked moneyline rows may be used for ROI or market-baseline comparisons.
- No active `model_versions` writes are allowed in D2-MIX.

## Metric Contract

Primary baseline: no-vig market favorite.

Activation threshold: candidate simulated ROI must exceed no-vig market favorite by at least +2pp after passing coverage and leakage gates.

Required metrics:

- log loss
- Brier score
- accuracy
- ROC AUC
- calibration gap
- absolute calibration error
- simulated research ROI

ROI policy:

| Metric | Value |
| --- | ---: |
| Stake | flat 1u |
| Status | simulated_research_only |
| Market favorite ROI | 16.2% |
| Minimum candidate ROI for activation | 18.2% |

## Starting Gate

| Strategy | Simulated ROI |
| --- | ---: |
| model_pick | -10.4% |
| market_favorite | 16.2% |
| blend_25_model_75_market | 15.9% |

The prior best blend is still 0.3pp below market favorite, so this epic is research-only. A separate activation epic is required before writing active `model_versions` or surfacing value claims.
