# Market Residual Analysis Baseline

- Generated: `2026-05-12T05:41:13Z`
- Epic: `intercept-b6yf`
- Task: `intercept-nwg3`
- Source epic: `intercept-ftbt`
- Source commit: `78770eb`
- Value status: `research_only`
- Writes `model_versions`: `false`

## Purpose

Freeze the D2-TMC artifacts as the input baseline for D2-MRA residual analysis. Downstream tasks should read these artifacts instead of reinterpreting the corpus state from memory or ad hoc command output.

## Frozen Inputs

| Path | SHA-256 | Role |
|---|---|---|
| `data/experiments/trainable-market-corpus-final-report.json` | `de02bcb25eb4e2dc68b3bad2e0b44c1ecdff359574da4f70175eebd1ced5c348` | Final D2-TMC decision, corpus counts, gate outcomes, and next-epic recommendation. |
| `data/experiments/trainable-market-corpus-market-gate-report.json` | `e10a023cdbe541b49b14fadc9d81e0f285749d2a911f5aaeed80a65dc8d6aade` | Expanded-corpus model, market, and simple blend baselines. |
| `data/experiments/trainable-market-corpus-blend-experiments.json` | `c7d448c166226a3519e3d2995c7319fbf2fc6852854fe527342066253d63dc3c` | Report-only model-market blend and calibration variants. |
| `data/experiments/trainable-market-corpus-simple-baselines.json` | `1883928ead7a7428baace8c0a6df6c70659d00efbeaf8c66a3c00b5bca6ea1f9` | Leak-free simple model baselines over the trainable market corpus. |
| `data/experiments/trainable-market-corpus-model-family-experiments.json` | `d5799b13ac2a2f9d6a4703c6d03efb92902195d79f8f3f9c628336d7e2cc5080` | Report-only model-family comparison over model-eligible fights. |
| `data/experiments/trainable-market-corpus-coverage.json` | `262144f02610188e284970ea195a63e40f262d21ac5f20f03049bd6f896b5032` | Expanded corpus coverage snapshot. |
| `data/experiments/trainable-market-corpus-leakage-audit.json` | `9df45a2e77d05f972c6896d9f434c5c7d32bfaec6bab45f8bc759926b4c5ca19` | Leakage audit evidence used by the D2-TMC gate. |

## Corpus Counts

| Metric | Count |
|---|---:|
| Market-covered events | 51 |
| Scored fights | 486 |
| Model-eligible events | 40 |
| Model-eligible fights | 379 |
| Source events imported | 51 |
| Source events matched | 51 |
| Source events unmatched | 0 |
| Source fights imported | 781 |
| Source fights matched | 499 |
| Source fights unmatched | 282 |
| Moneyline rows imported | 40,022 |
| Moneyline rows linked | 28,038 |

## Gate Thresholds

| Threshold | Value |
|---|---:|
| Minimum scored fights | 200 |
| Minimum market-covered events | 30 |
| Minimum ROI delta vs market favorite | +2.0pp |
| Required candidate ROI on this baseline | 22.0% |

## Baselines

| Strategy | Scope | Accuracy | Log loss | Brier | ROC AUC | Sim ROI | Delta vs market |
|---|---|---:|---:|---:|---:|---:|---:|
| `market_favorite` | Full market-covered corpus | 75.1% | 0.5684 | 0.1916 | 0.7891 | 20.0% | +0.0pp |
| `model_pick` | Full market-covered corpus | 44.0% | 0.7331 | 0.2697 | 0.4413 | -11.2% | -31.2pp |
| `blend_25_model_75_market` | Full market-covered corpus | 74.3% | 0.5932 | 0.2021 | 0.7815 | 18.5% | -1.5pp |
| `blend_50_50` | Full market-covered corpus | 68.5% | 0.6286 | 0.2185 | 0.7441 | 10.1% | -9.9pp |
| `blend_75_model_25_market` | Full market-covered corpus | 51.2% | 0.6747 | 0.2411 | 0.5938 | -1.7% | -21.7pp |
| `blend_25_xgboost_75_market` | Model-eligible subset | 70.7% | 0.5995 | 0.2052 | 0.7621 | 10.5% | -8.0pp |

## Gate State

| Gate | Status | Evidence |
|---|---|---|
| Leakage audit | pass | 15/15 checks passed. |
| Coverage | pass | 51 market-covered events and 486 scored fights clear the 30-event / 200-fight floor. |
| Market gate | fail | No model or blend candidate beat market favorite ROI by the required +2pp margin. |
| Model-family gate | fail | Best model-family candidate trailed market favorite ROI and degraded log loss and Brier score. |

## Analysis Contract

D2-MRA may use this baseline to bucket model-vs-market residuals and identify pre-fight feature gaps. It must not activate value status, publish betting claims, or write active `model_versions`.
