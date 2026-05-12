# Simple Leak-Free Baselines

- Generated: `2026-05-12T04:37:46.758657+00:00`
- Report-only: `true`
- Writes `model_versions`: `false`
- Value status: `research_only`
- Events evaluated: 777
- Samples evaluated: 8538
- Market-covered samples: 486

## Baselines

| Baseline | Count | Accuracy | Log loss | Brier | ROC AUC | Sim entries | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|
| ufc_experience | 8538 | 51.5% | 0.7052 | 0.2559 | 0.5152 | 346 | -22.8% |
| recent_form_wins_last_3 | 8538 | 52.5% | 0.6893 | 0.2481 | 0.5458 | 226 | -23.3% |
| younger_fighter | 8538 | 56.7% | 0.6844 | 0.2456 | 0.5697 | 218 | -13.6% |
| market_favorite | 486 | 75.1% | 0.5684 | 0.1916 | 0.7891 | 486 | 20.0% |

## Policy

Baseline ROI is simulated research output until leakage audits, market coverage, and market-gated validation pass.
These baselines do not train, save model files, write `model_versions`, or activate value claims.
