# D2-HOC Corpus Expansion Final Report

Generated: 2026-05-12T03:16:45.313Z

Report-only: true
Writes model_versions: false
Value status: insufficient_coverage
Model improvement unblocked: false

## Conclusion

Model-improvement work remains blocked for value claims. The corpus now has enough scored fights but only 26 scored market-covered events, below the 30-event validation threshold.

Only 235 matched fights across 26 events were scored; need at least 200 fights across 30 events.

## Coverage

| Metric | Value |
| --- | ---: |
| Target events | 30 |
| Imported target events | 30 |
| Matched source events | 26/30 |
| Scored market-covered events | 26/30 |
| Scored market-covered fights | 235/200 |
| Source fights imported | 464 |
| Source fights matched | 244 |
| Fight match rate | 52.6% |
| Moneyline rows imported | 23598 |
| Moneyline rows linked | 13759 |
| Moneyline link rate | 58.3% |
| Review rows | 220 |

## Review Reasons

| Reason | Rows |
| --- | ---: |
| source fight is cancelled and no canonical fight pair exists on the completed event | 86 |
| no canonical fight matched normalized fighter pair | 72 |
| no canonical event matched date/name/promotion | 62 |

## Verification

| Check | Result |
| --- | --- |
| Leakage audit | 15/15 passed |
| Baseline samples | 8538 |
| Market-covered baseline samples | 235 |
| Market coverage rate | 2.8% |
| Market favorite accuracy | 75.3% |
| Market favorite simulated ROI | 12.9% |

## Market Gate Strategies

| Strategy | Fights | Accuracy | Simulated ROI | Units | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| model_pick | 235 | 42.6% | -12.5% | -29.45 | simulated_research_only |
| market_favorite | 235 | 75.3% | 12.9% | 30.36 | simulated_research_only |
| blend_50_50 | 235 | 68.9% | 3.3% | 7.72 | simulated_research_only |
| blend_25_model_75_market | 235 | 76.2% | 14.9% | 35.10 | simulated_research_only |
| blend_75_model_25_market | 235 | 50.2% | -8.7% | -20.43 | simulated_research_only |

## Remaining Blockers

- Market gate remains insufficient_coverage: Only 235 matched fights across 26 events were scored; need at least 200 fights across 30 events.
- Resolve at least 4 additional market-covered scored UFC events to reach 30 scored events.
- Reduce or explain 220 unresolved historical odds review rows before using the corpus for model-value claims.

## Inputs

- data/experiments/historical-odds-target-cohort-baseline.json
- data/experiments/leakage-audit.json
- data/experiments/simple-baselines.json
- data/experiments/market-gate-report.json

