# Additional Winner Search Summary

The expanded selected-fight search evaluated 7,777 report-only variants at `min_train_samples=20` and found 150 market-gate-clearing variants.

| Feature set | Clearing variants | Best variant |
|---|---:|---|
| `production_plus_all_research_market_context` | 67 | `log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p66` |
| `production_plus_market_context` | 83 | `log_marketctx_c1p0_temp2p4_blend60_min_confidence0p66` |

## Top Clearing Variants

| Variant | Events | Selected fights | ROI delta | Log-loss delta | Brier delta | ROI |
|---|---:|---:|---:|---:|---:|---:|
| `log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p66` | 48 | 228 | +3.67% | -0.0231 | -0.0107 | 18.0% |
| `log_marketctx_c1p0_temp2p4_blend60_min_confidence0p66` | 48 | 205 | +3.61% | -0.0196 | -0.0099 | 20.1% |
| `log_marketctx_c0p5_temp2p2_blend60_min_confidence0p66` | 48 | 208 | +3.56% | -0.0185 | -0.0095 | 20.2% |
| `log_marketctx_c1p0_temp2p6_blend60_min_confidence0p65` | 48 | 211 | +3.51% | -0.0156 | -0.0083 | 18.6% |
| `log_marketctx_c0p5_temp2p4_blend60_min_confidence0p65` | 48 | 211 | +3.51% | -0.0159 | -0.0085 | 20.0% |

All outputs remain `research_only` with `writes_model_versions=false`.
