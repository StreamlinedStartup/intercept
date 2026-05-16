# Simple Leak-Free Baselines

- Generated: `2026-05-12T03:53:36.604118+00:00`
- Report-only: `true`
- Writes `model_versions`: `false`
- Value status: `research_only`
- Events evaluated: 777
- Samples evaluated: 8538
- Market-covered samples: 345

## Baselines

| Baseline | Count | Accuracy | Log loss | Brier | ROC AUC | Sim entries | Sim ROI |
|---|---:|---:|---:|---:|---:|---:|---:|
| ufc_experience | 8538 | 51.5% | 0.7052 | 0.2559 | 0.5152 | 242 | -22.2% |
| recent_form_wins_last_3 | 8538 | 52.5% | 0.6893 | 0.2481 | 0.5458 | 153 | -12.9% |
| younger_fighter | 8538 | 56.7% | 0.6844 | 0.2456 | 0.5697 | 141 | -19.2% |
| market_favorite | 345 | 75.1% | 0.5707 | 0.1925 | 0.7849 | 345 | 16.2% |

## Policy

Baseline ROI is simulated research output until leakage audits, market coverage, and market-gated validation pass.
These baselines do not train, save model files, write `model_versions`, or activate value claims.
