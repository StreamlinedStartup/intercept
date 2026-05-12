# D2-MCU Market Coverage Unlock Final Report

Generated: 2026-05-12T03:54:54Z

Report-only: true
Writes model_versions: false
Value status: research_only

## Decision

Research-only model-improvement experiments are unblocked because market coverage is now sufficient and the leakage audit passes.

Validated/value activation remains blocked because neither the model nor blend strategies beat the market favorite by the required +2pp.

## Coverage Gate

| Metric | Value |
| --- | ---: |
| Scored market-covered fights | 345/200 |
| Scored market-covered events | 37/30 |
| Source events matched | 37/37 |
| Source fights matched | 357/572 |
| Moneyline rows linked | 20,075/29,056 |

## Validation Gate

| Strategy | Simulated ROI | Accuracy | Result |
| --- | ---: | ---: | --- |
| model_pick | -10.4% | 44.1% | blocked |
| market_favorite | 16.2% | 75.1% | baseline |
| blend_50_50 | 5.9% | 68.1% | below market |
| blend_25_model_75_market | 15.9% | 74.8% | below market |
| blend_75_model_25_market | -7.8% | 49.6% | blocked |

The best blend finished 0.3pp below market favorite ROI, not +2pp above it.

## Frozen Evidence Bundle

- `data/experiments/market-coverage-unlock-validation-coverage.json`
- `data/experiments/market-coverage-unlock-leakage-audit.json`
- `data/experiments/market-coverage-unlock-simple-baselines.json`
- `data/experiments/market-coverage-unlock-market-gate-report.json`

## Next Work

Proceed to `intercept-tgq5` for research-only market-aware model improvement experiments:

- freeze this evidence bundle as the experiment input,
- evaluate calibration and model/market blend variants,
- evaluate feature and model-family variants,
- compare every candidate against the no-vig market favorite baseline.

Do not activate validated status, write active `model_versions`, or surface value claims.
