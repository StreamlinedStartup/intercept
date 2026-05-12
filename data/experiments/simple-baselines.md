# Simple Leak-Free Baselines

- Generated: `2026-05-12T01:03:41.395969+00:00`
- Report-only: `true`
- Writes `model_versions`: `false`
- Value status: `research_only`
- Events evaluated: 8
- Samples evaluated: 99
- Market-covered samples: 12

## Baselines

| Baseline | Count | Accuracy | Log loss | Brier | ROC AUC | Sim entries | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|
| ufc_experience | 99 | 43.4% | 0.7340 | 0.2701 | 0.4376 | 8 | -74.2% |
| recent_form_wins_last_3 | 99 | 57.6% | 0.6841 | 0.2455 | 0.5896 | 7 | -29.0% |
| younger_fighter | 99 | 53.5% | 0.6911 | 0.2490 | 0.5352 | 6 | -70.6% |
| market_favorite | 12 | 83.3% | 0.5101 | 0.1670 | 0.8857 | 12 | 31.4% |

## Policy

Baseline ROI is simulated research output until leakage audits, market coverage, and market-gated validation pass.
These baselines do not train, save model files, write `model_versions`, or activate value claims.
