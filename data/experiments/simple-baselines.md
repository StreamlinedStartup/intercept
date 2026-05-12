# Simple Leak-Free Baselines

- Generated: `2026-05-12T03:11:31.702139+00:00`
- Report-only: `true`
- Writes `model_versions`: `false`
- Value status: `research_only`
- Events evaluated: 777
- Samples evaluated: 8538
- Market-covered samples: 235

## Baselines

| Baseline | Count | Accuracy | Log loss | Brier | ROC AUC | Sim entries | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|
| ufc_experience | 8538 | 51.5% | 0.7052 | 0.2559 | 0.5152 | 168 | -22.2% |
| recent_form_wins_last_3 | 8538 | 52.5% | 0.6893 | 0.2481 | 0.5458 | 103 | -11.5% |
| younger_fighter | 8538 | 56.7% | 0.6844 | 0.2456 | 0.5697 | 89 | -26.1% |
| market_favorite | 235 | 75.3% | 0.5616 | 0.1886 | 0.7916 | 235 | 12.9% |

## Policy

Baseline ROI is simulated research output until leakage audits, market coverage, and market-gated validation pass.
These baselines do not train, save model files, write `model_versions`, or activate value claims.
