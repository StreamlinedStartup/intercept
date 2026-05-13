# Market Experiment Harness

- Generated: `2026-05-12T23:59:44.706548+00:00`
- Config: `configs/experiments/market-grid-selection-threshold-v1.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 40
- Model-eligible fights: 379

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p65 | +2.7% | -0.0032 | -0.0026 | false | unstable_coverage |
| 2 | log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p64 | +2.7% | -0.0019 | -0.0021 | false | unstable_coverage |
| 3 | log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p65 | +2.7% | -0.0053 | -0.0035 | false | unstable_coverage |
| 4 | log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p64 | +2.6% | -0.0032 | -0.0026 | false | unstable_coverage |
| 5 | log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p63 | +2.6% | -0.0006 | -0.0015 | false | unstable_coverage |
| 6 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 | +2.5% | -0.0011 | -0.0015 | true |  |
| 7 | log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p62 | +2.4% | 0.0022 | -0.0001 | false | log_loss_worse_than_market |
| 8 | log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p65 | +1.9% | -0.0060 | -0.0037 | false | roi_delta_below_market_gate, unstable_coverage |
| 9 | log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p65 | +1.8% | -0.0007 | -0.0014 | false | roi_delta_below_market_gate, unstable_coverage |
| 10 | log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p65 | +1.8% | -0.0087 | -0.0049 | false | roi_delta_below_market_gate, unstable_coverage |
| 11 | log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p64 | +1.8% | 0.0009 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 12 | log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p65 | +1.8% | -0.0072 | -0.0043 | false | roi_delta_below_market_gate, unstable_coverage |
| 13 | log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p63 | +1.7% | 0.0015 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 14 | log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p63 | +1.7% | 0.0021 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 15 | log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p65 | +1.7% | -0.0087 | -0.0049 | false | roi_delta_below_market_gate, unstable_coverage |
| 16 | log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p64 | +1.7% | -0.0022 | -0.0021 | false | roi_delta_below_market_gate, unstable_coverage |
| 17 | log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p64 | +1.6% | -0.0025 | -0.0023 | false | roi_delta_below_market_gate, unstable_coverage |
| 18 | log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p65 | +1.6% | -0.0007 | -0.0014 | false | roi_delta_below_market_gate, unstable_coverage |
| 19 | log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p65 | +1.6% | -0.0032 | -0.0025 | false | roi_delta_below_market_gate, unstable_coverage |
| 20 | log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p63 | +1.6% | 0.0007 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 21 | log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p64 | +1.6% | -0.0001 | -0.0012 | false | roi_delta_below_market_gate, unstable_coverage |
| 22 | log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p63 | +1.6% | -0.0008 | -0.0015 | false | roi_delta_below_market_gate, unstable_coverage |
| 23 | log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p65 | +1.6% | -0.0016 | -0.0018 | false | roi_delta_below_market_gate, unstable_coverage |
| 24 | log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p64 | +1.6% | -0.0019 | -0.0019 | false | roi_delta_below_market_gate, unstable_coverage |
| 25 | log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p62 | +1.6% | 0.0037 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 26 | log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p65 | +1.6% | -0.0032 | -0.0025 | false | roi_delta_below_market_gate, unstable_coverage |
| 27 | log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p63 | +1.6% | 0.0006 | -0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 28 | log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p64 | +1.6% | -0.0021 | -0.0020 | false | roi_delta_below_market_gate, unstable_coverage |
| 29 | log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p63 | +1.5% | -0.0015 | -0.0017 | false | roi_delta_below_market_gate |
| 30 | log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p61 | +1.5% | 0.0008 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 31 | log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p63 | +1.4% | -0.0028 | -0.0022 | false | roi_delta_below_market_gate |
| 32 | log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p62 | +1.4% | -0.0020 | -0.0018 | false | roi_delta_below_market_gate |
| 33 | log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p61 | +1.4% | -0.0011 | -0.0014 | false | roi_delta_below_market_gate |
| 34 | log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p61 | +1.4% | -0.0026 | -0.0020 | false | roi_delta_below_market_gate |
| 35 | log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p65 | +1.3% | -0.0014 | -0.0017 | false | roi_delta_below_market_gate, unstable_coverage |
| 36 | log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p62 | +1.3% | 0.0044 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 37 | log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p64 | +1.3% | -0.0006 | -0.0012 | false | roi_delta_below_market_gate, unstable_coverage |
| 38 | log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p65 | +1.1% | 0.0023 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 39 | log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p64 | +1.0% | 0.0023 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 40 | log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p62 | +1.0% | 0.0029 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 41 | log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p65 | +1.0% | -0.0064 | -0.0037 | false | roi_delta_below_market_gate, unstable_coverage |
| 42 | log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p61 | +0.9% | 0.0020 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 43 | log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p65 | +0.9% | -0.0058 | -0.0034 | false | roi_delta_below_market_gate, unstable_coverage |
| 44 | log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p64 | +0.9% | -0.0037 | -0.0025 | false | roi_delta_below_market_gate, unstable_coverage |
| 45 | log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p63 | +0.9% | 0.0043 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 46 | log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p65 | +0.9% | -0.0013 | -0.0014 | false | roi_delta_below_market_gate, unstable_coverage |
| 47 | log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p65 | +0.9% | -0.0029 | -0.0021 | false | roi_delta_below_market_gate, unstable_coverage |
| 48 | log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p63 | +0.8% | -0.0006 | -0.0011 | false | roi_delta_below_market_gate |
| 49 | log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p61 | +0.8% | 0.0040 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 50 | log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p62 | +0.8% | 0.0009 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 51 | log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p61 | +0.8% | 0.0017 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 52 | log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p62 | +0.8% | -0.0043 | -0.0028 | false | roi_delta_below_market_gate |
| 53 | log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p62 | +0.8% | -0.0060 | -0.0036 | false | roi_delta_below_market_gate |
| 54 | log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p61 | +0.8% | -0.0025 | -0.0020 | false | roi_delta_below_market_gate |
| 55 | log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p65 | +0.7% | 0.0007 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 56 | log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p65 | +0.7% | 0.0016 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 57 | log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p64 | +0.7% | 0.0007 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 58 | log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p64 | +0.7% | 0.0015 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 59 | log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p65 | +0.7% | 0.0005 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 60 | log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p64 | +0.7% | 0.0010 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 61 | log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p63 | +0.7% | 0.0004 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 62 | log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p64 | +0.7% | -0.0014 | -0.0016 | false | roi_delta_below_market_gate |
| 63 | log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p65 | +0.7% | -0.0008 | -0.0014 | false | roi_delta_below_market_gate |
| 64 | log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p64 | +0.7% | -0.0014 | -0.0016 | false | roi_delta_below_market_gate |
| 65 | log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p64 | +0.7% | -0.0008 | -0.0014 | false | roi_delta_below_market_gate |
| 66 | log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p62 | +0.7% | 0.0038 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 67 | log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p64 | +0.6% | -0.0026 | -0.0021 | false | roi_delta_below_market_gate |
| 68 | log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p63 | +0.6% | -0.0003 | -0.0010 | false | roi_delta_below_market_gate |
| 69 | log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p63 | +0.6% | 0.0008 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 70 | log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p63 | +0.6% | 0.0000 | -0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 71 | log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p63 | +0.6% | 0.0006 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 72 | log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p62 | +0.6% | 0.0010 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 73 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p62 | +0.6% | 0.0011 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 74 | log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p64 | +0.6% | 0.0006 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 75 | log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p64 | +0.6% | 0.0007 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 76 | log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p63 | +0.6% | 0.0007 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 77 | log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p62 | +0.6% | 0.0005 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 78 | log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p61 | +0.6% | 0.0030 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 79 | log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p62 | +0.6% | 0.0009 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 80 | log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p63 | +0.6% | 0.0010 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 81 | log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p61 | +0.6% | 0.0012 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 82 | log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p61 | +0.6% | 0.0018 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 83 | log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p63 | +0.6% | -0.0017 | -0.0017 | false | roi_delta_below_market_gate |
| 84 | log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p62 | +0.6% | 0.0007 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 85 | log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p62 | +0.6% | -0.0016 | -0.0016 | false | roi_delta_below_market_gate |
| 86 | log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p61 | +0.6% | -0.0000 | -0.0009 | false | roi_delta_below_market_gate |
| 87 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p61 | +0.6% | 0.0013 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 88 | log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p61 | +0.6% | -0.0011 | -0.0013 | false | roi_delta_below_market_gate |
| 89 | log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p62 | +0.6% | -0.0041 | -0.0027 | false | roi_delta_below_market_gate |
| 90 | log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p61 | +0.6% | -0.0034 | -0.0024 | false | roi_delta_below_market_gate |
| 91 | log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p61 | +0.6% | -0.0011 | -0.0013 | false | roi_delta_below_market_gate |
| 92 | log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p61 | +0.6% | -0.0005 | -0.0010 | false | roi_delta_below_market_gate |
| 93 | log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p61 | +0.6% | -0.0051 | -0.0032 | false | roi_delta_below_market_gate |
| 94 | log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p61 | +0.6% | -0.0012 | -0.0013 | false | roi_delta_below_market_gate |
| 95 | log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p65 | +0.5% | 0.0055 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 96 | log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p65 | +0.5% | -0.0026 | -0.0021 | false | roi_delta_below_market_gate |
| 97 | log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p64 | +0.5% | -0.0036 | -0.0025 | false | roi_delta_below_market_gate |
| 98 | log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p61 | +0.5% | 0.0028 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 99 | log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p62 | +0.5% | 0.0027 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 100 | log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p63 | +0.5% | -0.0019 | -0.0017 | false | roi_delta_below_market_gate |
| 101 | log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p65 | +0.5% | 0.0068 | 0.0024 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 102 | log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p64 | +0.5% | 0.0073 | 0.0026 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 103 | log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p62 | +0.5% | 0.0001 | -0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 104 | log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p61 | +0.5% | 0.0015 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 105 | log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p65 | +0.5% | 0.0048 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 106 | log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p64 | +0.5% | 0.0049 | 0.0015 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 107 | log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p64 | +0.5% | 0.0088 | 0.0032 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 108 | log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p63 | +0.5% | 0.0062 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 109 | log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p64 | +0.5% | 0.0022 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 110 | log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p62 | +0.5% | 0.0107 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 111 | log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p63 | +0.5% | 0.0047 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 112 | log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p64 | +0.5% | 0.0087 | 0.0031 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 113 | log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p63 | +0.4% | 0.0087 | 0.0032 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 114 | log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p61 | +0.4% | 0.0106 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 115 | log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p62 | +0.4% | 0.0084 | 0.0031 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 116 | log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p65 | +0.4% | 0.0006 | -0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 117 | log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p62 | +0.4% | 0.0066 | 0.0022 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 118 | log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p61 | +0.4% | 0.0072 | 0.0025 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 119 | log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p65 | +0.4% | 0.0008 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 120 | log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p64 | +0.4% | 0.0020 | 0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 121 | log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p65 | +0.3% | 0.0066 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 122 | log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p64 | +0.3% | 0.0070 | 0.0022 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 123 | log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p63 | +0.3% | 0.0079 | 0.0028 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 124 | log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p62 | +0.3% | 0.0075 | 0.0026 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 125 | log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p61 | +0.3% | 0.0062 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 126 | log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p63 | +0.2% | -0.0014 | -0.0015 | false | roi_delta_below_market_gate |
| 127 | log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p63 | +0.2% | 0.0044 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 128 | log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p62 | +0.2% | -0.0012 | -0.0014 | false | roi_delta_below_market_gate |
| 129 | log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p65 | +0.2% | -0.0090 | -0.0051 | false | roi_delta_below_market_gate, unstable_coverage |
| 130 | log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p65 | +0.2% | -0.0053 | -0.0033 | false | roi_delta_below_market_gate, unstable_coverage |
| 131 | log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p65 | +0.2% | -0.0029 | -0.0022 | false | roi_delta_below_market_gate |
| 132 | log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p61 | +0.2% | -0.0041 | -0.0026 | false | roi_delta_below_market_gate |
| 133 | log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p65 | +0.2% | -0.0068 | -0.0039 | false | roi_delta_below_market_gate, unstable_coverage |
| 134 | log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p65 | +0.2% | -0.0049 | -0.0031 | false | roi_delta_below_market_gate, unstable_coverage |
| 135 | log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p64 | +0.2% | -0.0029 | -0.0023 | false | roi_delta_below_market_gate, unstable_coverage |
| 136 | log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p64 | +0.2% | -0.0007 | -0.0015 | false | roi_delta_below_market_gate, unstable_coverage |
| 137 | log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p62 | +0.2% | 0.0008 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 138 | log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p65 | +0.2% | -0.0048 | -0.0031 | false | roi_delta_below_market_gate, unstable_coverage |
| 139 | log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p65 | +0.2% | -0.0011 | -0.0014 | false | roi_delta_below_market_gate, unstable_coverage |
| 140 | log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p65 | +0.2% | 0.0021 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 141 | log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p64 | +0.2% | -0.0023 | -0.0021 | false | roi_delta_below_market_gate, unstable_coverage |
| 142 | log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p61 | +0.2% | 0.0027 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 143 | log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p65 | +0.2% | -0.0036 | -0.0026 | false | roi_delta_below_market_gate, unstable_coverage |
| 144 | log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p65 | +0.2% | -0.0046 | -0.0030 | false | roi_delta_below_market_gate, unstable_coverage |
| 145 | log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p63 | +0.2% | 0.0023 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 146 | log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p65 | +0.2% | -0.0070 | -0.0040 | false | roi_delta_below_market_gate, unstable_coverage |
| 147 | log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p64 | +0.2% | -0.0004 | -0.0012 | false | roi_delta_below_market_gate, unstable_coverage |
| 148 | log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p63 | +0.2% | 0.0023 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 149 | log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p64 | +0.2% | -0.0040 | -0.0028 | false | roi_delta_below_market_gate, unstable_coverage |
| 150 | log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p64 | +0.2% | -0.0029 | -0.0022 | false | roi_delta_below_market_gate, unstable_coverage |
| 151 | log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p65 | +0.2% | -0.0014 | -0.0016 | false | roi_delta_below_market_gate, unstable_coverage |
| 152 | log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p65 | +0.2% | -0.0006 | -0.0011 | false | roi_delta_below_market_gate, unstable_coverage |
| 153 | log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p64 | +0.2% | 0.0006 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 154 | log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p64 | +0.2% | -0.0002 | -0.0010 | false | roi_delta_below_market_gate, unstable_coverage |
| 155 | log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p63 | +0.2% | -0.0018 | -0.0018 | false | roi_delta_below_market_gate, unstable_coverage |
| 156 | log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p63 | +0.2% | -0.0023 | -0.0021 | false | roi_delta_below_market_gate, unstable_coverage |
| 157 | log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p64 | +0.2% | -0.0055 | -0.0034 | false | roi_delta_below_market_gate, unstable_coverage |
| 158 | log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p65 | +0.2% | -0.0072 | -0.0042 | false | roi_delta_below_market_gate, unstable_coverage |
| 159 | log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p65 | +0.2% | -0.0034 | -0.0024 | false | roi_delta_below_market_gate, unstable_coverage |
| 160 | log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p62 | +0.2% | 0.0015 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 161 | log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p63 | +0.2% | 0.0026 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 162 | log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p62 | +0.2% | 0.0029 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 163 | log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p63 | +0.2% | 0.0009 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 164 | log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p64 | +0.2% | -0.0021 | -0.0018 | false | roi_delta_below_market_gate |
| 165 | log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p63 | +0.2% | 0.0023 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 166 | log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p63 | +0.2% | -0.0026 | -0.0021 | false | roi_delta_below_market_gate |
| 167 | log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p62 | +0.2% | 0.0035 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 168 | log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p64 | +0.2% | -0.0056 | -0.0034 | false | roi_delta_below_market_gate |
| 169 | log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p63 | +0.2% | -0.0008 | -0.0012 | false | roi_delta_below_market_gate |
| 170 | log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p63 | +0.2% | 0.0005 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 171 | log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p62 | +0.2% | 0.0055 | 0.0016 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 172 | log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p63 | +0.2% | -0.0040 | -0.0027 | false | roi_delta_below_market_gate |
| 173 | log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p62 | +0.2% | -0.0003 | -0.0011 | false | roi_delta_below_market_gate |
| 174 | log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p62 | +0.2% | 0.0002 | -0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 175 | log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p61 | +0.2% | 0.0026 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 176 | log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p62 | +0.2% | -0.0023 | -0.0020 | false | roi_delta_below_market_gate |
| 177 | log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p61 | +0.2% | 0.0025 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 178 | log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p61 | +0.2% | 0.0038 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 179 | log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p61 | +0.2% | -0.0001 | -0.0011 | false | roi_delta_below_market_gate |
| 180 | log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p62 | +0.2% | -0.0044 | -0.0028 | false | roi_delta_below_market_gate |
| 181 | log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p61 | +0.2% | -0.0034 | -0.0023 | false | roi_delta_below_market_gate |
| 182 | log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p65 | +0.1% | 0.0009 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 183 | log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p64 | +0.1% | 0.0026 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 184 | log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p63 | +0.1% | 0.0038 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 185 | log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p65 | +0.1% | 0.0028 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 186 | log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p64 | +0.1% | 0.0029 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 187 | log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p63 | +0.1% | 0.0034 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 188 | log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p62 | +0.1% | 0.0020 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 189 | log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p62 | +0.1% | 0.0021 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 190 | log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p61 | +0.1% | 0.0043 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 191 | log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p65 | +0.1% | 0.0096 | 0.0035 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 192 | log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p65 | +0.0% | -0.0063 | -0.0038 | false | roi_delta_below_market_gate, unstable_coverage |
| 193 | log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p65 | +0.0% | -0.0031 | -0.0024 | false | roi_delta_below_market_gate, unstable_coverage |
| 194 | log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p65 | +0.0% | -0.0010 | -0.0015 | false | roi_delta_below_market_gate, unstable_coverage |
| 195 | log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p64 | +0.0% | -0.0003 | -0.0012 | false | roi_delta_below_market_gate, unstable_coverage |
| 196 | log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p64 | +0.0% | 0.0012 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 197 | log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p65 | +0.0% | 0.0021 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 198 | log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p63 | +0.0% | 0.0027 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 199 | log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p65 | +0.0% | 0.0031 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 200 | log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p65 | +0.0% | 0.0032 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 201 | log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p64 | +0.0% | 0.0034 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 202 | log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p61 | -0.0% | 0.0013 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 203 | log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p62 | -0.0% | 0.0036 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 204 | log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p64 | -0.0% | 0.0031 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 205 | log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p61 | -0.0% | -0.0048 | -0.0030 | false | roi_delta_below_market_gate |
| 206 | log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p63 | -0.0% | -0.0038 | -0.0026 | false | roi_delta_below_market_gate |
| 207 | log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p61 | -0.1% | -0.0004 | -0.0009 | false | roi_delta_below_market_gate |
| 208 | log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p61 | -0.1% | 0.0011 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 209 | log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p62 | -0.1% | 0.0016 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 210 | log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p62 | -0.1% | 0.0049 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 211 | log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p63 | -0.1% | 0.0024 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 212 | log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p64 | -0.1% | 0.0034 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 213 | log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p65 | -0.1% | 0.0030 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 214 | log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p62 | -0.1% | 0.0077 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 215 | log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p63 | -0.1% | 0.0097 | 0.0035 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 216 | log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p61 | -0.1% | -0.0002 | -0.0008 | false | roi_delta_below_market_gate |
| 217 | log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p64 | -0.2% | 0.0023 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 218 | log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p61 | -0.2% | -0.0039 | -0.0026 | false | roi_delta_below_market_gate |
| 219 | log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p61 | -0.2% | 0.0018 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 220 | log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p62 | -0.2% | -0.0018 | -0.0017 | false | roi_delta_below_market_gate |
| 221 | log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p63 | -0.2% | -0.0030 | -0.0022 | false | roi_delta_below_market_gate |
| 222 | log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p61 | -0.2% | 0.0045 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 223 | log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p64 | -0.2% | -0.0039 | -0.0027 | false | roi_delta_below_market_gate |
| 224 | log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p63 | -0.2% | 0.0025 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 225 | log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p62 | -0.2% | 0.0035 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 226 | log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p62 | -0.2% | 0.0003 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 227 | log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p65 | -0.2% | -0.0037 | -0.0025 | false | roi_delta_below_market_gate, unstable_coverage |
| 228 | log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p63 | -0.2% | 0.0011 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 229 | log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p64 | -0.2% | 0.0025 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 230 | log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p64 | -0.2% | -0.0021 | -0.0016 | false | roi_delta_below_market_gate, unstable_coverage |
| 231 | log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p65 | -0.2% | -0.0035 | -0.0023 | false | roi_delta_below_market_gate, unstable_coverage |
| 232 | log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p64 | -0.2% | 0.0017 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 233 | log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p65 | -0.2% | -0.0019 | -0.0016 | false | roi_delta_below_market_gate, unstable_coverage |
| 234 | log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p65 | -0.2% | -0.0041 | -0.0025 | false | roi_delta_below_market_gate, unstable_coverage |
| 235 | log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p61 | -0.3% | 0.0142 | 0.0057 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 236 | log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p61 | -0.3% | 0.0129 | 0.0051 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 237 | log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p62 | -0.3% | 0.0101 | 0.0038 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 238 | log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p63 | -0.3% | 0.0103 | 0.0039 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 239 | log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p63 | -0.3% | 0.0112 | 0.0043 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 240 | log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p62 | -0.3% | 0.0132 | 0.0052 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 241 | log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p64 | -0.3% | 0.0111 | 0.0042 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 242 | log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p65 | -0.3% | 0.0102 | 0.0038 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 243 | log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p63 | -0.3% | 0.0100 | 0.0039 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 244 | log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p63 | -0.3% | 0.0073 | 0.0025 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 245 | log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p64 | -0.3% | 0.0087 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 246 | log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p64 | -0.3% | 0.0108 | 0.0041 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 247 | log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p63 | -0.3% | 0.0114 | 0.0044 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 248 | log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p63 | -0.3% | 0.0120 | 0.0047 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 249 | log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p62 | -0.3% | 0.0101 | 0.0039 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 250 | log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p64 | -0.3% | 0.0107 | 0.0042 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 251 | log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p63 | -0.3% | 0.0082 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 252 | log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p65 | -0.3% | 0.0093 | 0.0035 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 253 | log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p65 | -0.3% | 0.0095 | 0.0034 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 254 | log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p61 | -0.3% | 0.0057 | 0.0018 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 255 | log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p65 | -0.3% | 0.0082 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 256 | log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p64 | -0.3% | 0.0091 | 0.0034 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 257 | log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p63 | -0.3% | 0.0039 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 258 | log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p62 | -0.4% | 0.0076 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 259 | log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p63 | -0.4% | 0.0071 | 0.0024 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 260 | log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p65 | -0.4% | 0.0055 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 261 | log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p62 | -0.4% | 0.0028 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 262 | log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p61 | -0.4% | 0.0027 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 263 | log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p61 | -0.4% | 0.0059 | 0.0020 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 264 | log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p61 | -0.4% | 0.0070 | 0.0025 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 265 | log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p62 | -0.5% | 0.0076 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 266 | log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p63 | -0.5% | 0.0083 | 0.0029 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 267 | log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p61 | -0.5% | 0.0041 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 268 | log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p62 | -0.5% | 0.0043 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 269 | log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p61 | -0.5% | -0.0008 | -0.0011 | false | roi_delta_below_market_gate |
| 270 | log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p61 | -0.5% | 0.0010 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 271 | log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p61 | -0.5% | -0.0003 | -0.0008 | false | roi_delta_below_market_gate |
| 272 | log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p65 | -0.5% | 0.0035 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 273 | log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p62 | -0.5% | 0.0000 | -0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 274 | log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p62 | -0.5% | 0.0003 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 275 | log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p61 | -0.5% | 0.0008 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 276 | log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p61 | -0.5% | 0.0018 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 277 | log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p61 | -0.5% | 0.0024 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 278 | log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p62 | -0.5% | -0.0008 | -0.0011 | false | roi_delta_below_market_gate |
| 279 | log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p62 | -0.5% | -0.0014 | -0.0014 | false | roi_delta_below_market_gate |
| 280 | log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p62 | -0.5% | 0.0021 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 281 | log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p62 | -0.6% | -0.0001 | -0.0008 | false | roi_delta_below_market_gate |
| 282 | log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p62 | -0.6% | 0.0009 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 283 | log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p61 | -0.6% | 0.0027 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 284 | log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p63 | -0.6% | 0.0019 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 285 | log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p61 | -0.6% | 0.0023 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 286 | log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p63 | -0.6% | 0.0011 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 287 | log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p63 | -0.6% | 0.0009 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 288 | log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p64 | -0.6% | -0.0016 | -0.0015 | false | roi_delta_below_market_gate, unstable_coverage |
| 289 | log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p63 | -0.6% | 0.0032 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 290 | log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p64 | -0.6% | 0.0011 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 291 | log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p65 | -0.6% | -0.0048 | -0.0028 | false | roi_delta_below_market_gate, unstable_coverage |
| 292 | log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p64 | -0.6% | 0.0060 | 0.0022 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 293 | log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p65 | -0.6% | 0.0038 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 294 | log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p64 | -0.6% | 0.0019 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 295 | log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p65 | -0.6% | 0.0016 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 296 | log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p65 | -0.6% | 0.0024 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 297 | log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p65 | -0.6% | 0.0014 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 298 | log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p63 | -0.6% | 0.0000 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 299 | log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p61 | -0.6% | 0.0141 | 0.0057 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 300 | log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p62 | -0.7% | 0.0150 | 0.0061 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 301 | log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p61 | -0.7% | 0.0012 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 302 | log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p61 | -0.7% | -0.0046 | -0.0029 | false | roi_delta_below_market_gate |
| 303 | log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p61 | -0.7% | -0.0046 | -0.0029 | false | roi_delta_below_market_gate |
| 304 | log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p61 | -0.7% | -0.0015 | -0.0014 | false | roi_delta_below_market_gate |
| 305 | log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p61 | -0.7% | 0.0001 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 306 | log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p61 | -0.7% | -0.0026 | -0.0020 | false | roi_delta_below_market_gate |
| 307 | log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p62 | -0.7% | 0.0031 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 308 | log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p63 | -0.7% | 0.0133 | 0.0053 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 309 | log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p64 | -0.7% | 0.0147 | 0.0058 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 310 | log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p62 | -0.7% | 0.0156 | 0.0063 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 311 | log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p63 | -0.7% | 0.0023 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 312 | log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p61 | -0.7% | 0.0058 | 0.0019 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 313 | log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p65 | -0.7% | 0.0160 | 0.0063 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 314 | log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p62 | -0.7% | -0.0016 | -0.0015 | false | roi_delta_below_market_gate |
| 315 | log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p63 | -0.7% | 0.0150 | 0.0061 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 316 | log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p62 | -0.7% | -0.0044 | -0.0028 | false | roi_delta_below_market_gate |
| 317 | log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p61 | -0.7% | -0.0012 | -0.0014 | false | roi_delta_below_market_gate |
| 318 | log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p62 | -0.7% | 0.0060 | 0.0020 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 319 | log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p61 | -0.7% | 0.0004 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 320 | log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p61 | -0.7% | 0.0087 | 0.0032 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 321 | log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p62 | -0.7% | -0.0004 | -0.0009 | false | roi_delta_below_market_gate |
| 322 | log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p63 | -0.7% | 0.0056 | 0.0018 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 323 | log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p62 | -0.7% | 0.0075 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 324 | log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p64 | -0.7% | 0.0145 | 0.0058 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 325 | log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p62 | -0.7% | -0.0030 | -0.0022 | false | roi_delta_below_market_gate |
| 326 | log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p63 | -0.7% | -0.0005 | -0.0010 | false | roi_delta_below_market_gate |
| 327 | log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p61 | -0.7% | -0.0001 | -0.0009 | false | roi_delta_below_market_gate |
| 328 | log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p63 | -0.7% | -0.0043 | -0.0028 | false | roi_delta_below_market_gate |
| 329 | log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p61 | -0.7% | 0.0026 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 330 | log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p63 | -0.7% | 0.0053 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 331 | log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p62 | -0.7% | 0.0056 | 0.0018 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 332 | log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p62 | -0.7% | -0.0023 | -0.0019 | false | roi_delta_below_market_gate |
| 333 | log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p61 | -0.7% | 0.0014 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 334 | log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p63 | -0.7% | -0.0029 | -0.0021 | false | roi_delta_below_market_gate |
| 335 | log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p62 | -0.7% | 0.0002 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 336 | log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p62 | -0.7% | 0.0080 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 337 | log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p62 | -0.7% | -0.0001 | -0.0009 | false | roi_delta_below_market_gate |
| 338 | log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p63 | -0.8% | -0.0008 | -0.0012 | false | roi_delta_below_market_gate |
| 339 | log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p62 | -0.8% | 0.0035 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 340 | log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p64 | -0.8% | -0.0002 | -0.0009 | false | roi_delta_below_market_gate |
| 341 | log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p61 | -0.8% | 0.0049 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 342 | log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p61 | -0.8% | 0.0024 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 343 | log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p63 | -0.8% | 0.0041 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 344 | log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p63 | -0.8% | -0.0018 | -0.0016 | false | roi_delta_below_market_gate |
| 345 | log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p64 | -0.8% | 0.0037 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 346 | log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p64 | -0.8% | -0.0030 | -0.0022 | false | roi_delta_below_market_gate |
| 347 | log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p63 | -0.8% | 0.0068 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 348 | log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p62 | -0.8% | 0.0087 | 0.0031 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 349 | log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p61 | -0.8% | 0.0026 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 350 | log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p61 | -0.8% | 0.0015 | -0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 351 | log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p64 | -0.8% | 0.0011 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 352 | log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p65 | -0.8% | 0.0021 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 353 | log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p62 | -0.8% | 0.0019 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 354 | log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p64 | -0.8% | 0.0059 | 0.0020 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 355 | log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p62 | -0.8% | 0.0006 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 356 | log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p61 | -0.8% | 0.0047 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 357 | log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p65 | -0.8% | 0.0010 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 358 | log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p62 | -0.8% | 0.0010 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 359 | log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p61 | -0.8% | 0.0033 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 360 | log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p65 | -0.8% | 0.0044 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 361 | log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p63 | -0.8% | 0.0092 | 0.0033 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 362 | log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p62 | -0.8% | 0.0004 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 363 | log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p64 | -0.8% | 0.0010 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 364 | log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p63 | -0.8% | 0.0012 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 365 | log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p64 | -0.8% | 0.0068 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 366 | log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p63 | -0.8% | 0.0024 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 367 | log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p63 | -0.8% | 0.0085 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 368 | log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p61 | -0.8% | 0.0045 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 369 | log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p62 | -0.8% | 0.0037 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 370 | log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p62 | -0.8% | 0.0026 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 371 | log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p63 | -0.8% | 0.0044 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 372 | log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p64 | -0.8% | -0.0015 | -0.0014 | false | roi_delta_below_market_gate |
| 373 | log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p65 | -0.8% | 0.0039 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 374 | log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p65 | -0.8% | 0.0039 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 375 | log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p63 | -0.8% | 0.0042 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 376 | log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p62 | -0.8% | 0.0042 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 377 | log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p63 | -0.8% | 0.0036 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 378 | log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p64 | -0.8% | 0.0066 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 379 | log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p64 | -0.8% | 0.0081 | 0.0028 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 380 | log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p63 | -0.8% | 0.0049 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 381 | log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p65 | -0.9% | 0.0054 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 382 | log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p65 | -0.9% | 0.0038 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 383 | log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p61 | -0.9% | 0.0029 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 384 | log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p61 | -0.9% | 0.0055 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 385 | log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p61 | -0.9% | 0.0005 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 386 | log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p61 | -0.9% | 0.0019 | 0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 387 | log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p61 | -0.9% | 0.0053 | 0.0016 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 388 | log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p63 | -0.9% | 0.0076 | 0.0026 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 389 | log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p62 | -0.9% | -0.0008 | -0.0011 | false | roi_delta_below_market_gate |
| 390 | log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p62 | -0.9% | 0.0017 | 0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 391 | log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p61 | -0.9% | 0.0026 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 392 | log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p61 | -0.9% | 0.0054 | 0.0016 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 393 | log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p61 | -0.9% | 0.0064 | 0.0018 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 394 | log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p62 | -0.9% | -0.0015 | -0.0015 | false | roi_delta_below_market_gate |
| 395 | log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p62 | -0.9% | 0.0003 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 396 | log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p64 | -0.9% | 0.0017 | -0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 397 | log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p63 | -0.9% | 0.0019 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 398 | log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p62 | -0.9% | 0.0020 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 399 | log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p61 | -0.9% | 0.0048 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 400 | log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p61 | -0.9% | 0.0042 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 401 | log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p65 | -0.9% | 0.0060 | 0.0018 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 402 | log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p62 | -0.9% | 0.0037 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 403 | log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p63 | -0.9% | -0.0037 | -0.0024 | false | roi_delta_below_market_gate |
| 404 | log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p62 | -0.9% | 0.0004 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 405 | log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p65 | -0.9% | 0.0074 | 0.0024 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 406 | log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p62 | -0.9% | 0.0010 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 407 | log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p63 | -0.9% | 0.0010 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 408 | log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p62 | -0.9% | 0.0049 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 409 | log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p63 | -0.9% | -0.0003 | -0.0009 | false | roi_delta_below_market_gate |
| 410 | log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p62 | -0.9% | 0.0033 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 411 | log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p63 | -0.9% | 0.0041 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 412 | log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p63 | -0.9% | 0.0048 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 413 | log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p62 | -0.9% | 0.0051 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 414 | log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p63 | -0.9% | -0.0013 | -0.0013 | false | roi_delta_below_market_gate |
| 415 | log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p64 | -0.9% | 0.0003 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 416 | log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p62 | -0.9% | 0.0034 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 417 | log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p64 | -0.9% | -0.0011 | -0.0013 | false | roi_delta_below_market_gate |
| 418 | log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p64 | -0.9% | -0.0024 | -0.0018 | false | roi_delta_below_market_gate |
| 419 | log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p62 | -0.9% | 0.0027 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 420 | log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p61 | -0.9% | 0.0125 | 0.0049 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 421 | log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p63 | -0.9% | 0.0021 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 422 | log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p63 | -0.9% | 0.0033 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 423 | log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p62 | -0.9% | 0.0053 | 0.0015 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 424 | log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p62 | -0.9% | 0.0057 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 425 | log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p62 | -0.9% | 0.0066 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 426 | log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p64 | -0.9% | 0.0056 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 427 | log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p64 | -0.9% | 0.0033 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 428 | log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p63 | -0.9% | -0.0002 | -0.0009 | false | roi_delta_below_market_gate |
| 429 | log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p62 | -0.9% | 0.0046 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 430 | log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p62 | -0.9% | 0.0040 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 431 | log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p63 | -0.9% | 0.0043 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 432 | log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p63 | -0.9% | 0.0048 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 433 | log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p64 | -0.9% | 0.0042 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 434 | log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p65 | -0.9% | 0.0062 | 0.0019 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 435 | log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p63 | -0.9% | 0.0037 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 436 | log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p63 | -0.9% | 0.0023 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 437 | log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p64 | -0.9% | 0.0005 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 438 | log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p64 | -0.9% | 0.0018 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 439 | log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p63 | -0.9% | 0.0031 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 440 | log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p64 | -0.9% | 0.0071 | 0.0024 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 441 | log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p62 | -0.9% | 0.0051 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 442 | log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p64 | -0.9% | -0.0025 | -0.0019 | false | roi_delta_below_market_gate, unstable_coverage |
| 443 | log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p63 | -0.9% | -0.0004 | -0.0010 | false | roi_delta_below_market_gate, unstable_coverage |
| 444 | log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p63 | -0.9% | 0.0011 | -0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 445 | log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p65 | -0.9% | 0.0037 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 446 | log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p65 | -1.0% | 0.0022 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 447 | log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p65 | -1.0% | -0.0042 | -0.0027 | false | roi_delta_below_market_gate, unstable_coverage |
| 448 | log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p65 | -1.0% | 0.0011 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 449 | log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p62 | -1.0% | 0.0042 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 450 | log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p65 | -1.0% | -0.0011 | -0.0012 | false | roi_delta_below_market_gate, unstable_coverage |
| 451 | log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p64 | -1.0% | 0.0015 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 452 | log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p64 | -1.0% | 0.0020 | 0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 453 | log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p64 | -1.0% | 0.0102 | 0.0039 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 454 | log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p63 | -1.0% | 0.0027 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 455 | log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p63 | -1.0% | 0.0053 | 0.0015 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 456 | log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p64 | -1.0% | -0.0020 | -0.0017 | false | roi_delta_below_market_gate, unstable_coverage |
| 457 | log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p64 | -1.0% | 0.0001 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 458 | log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p64 | -1.0% | 0.0003 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 459 | log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p63 | -1.0% | 0.0007 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 460 | log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p64 | -1.0% | 0.0011 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 461 | log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p63 | -1.0% | 0.0111 | 0.0043 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 462 | log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p63 | -1.0% | 0.0039 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 463 | log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p64 | -1.0% | -0.0011 | -0.0013 | false | roi_delta_below_market_gate, unstable_coverage |
| 464 | log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p63 | -1.0% | 0.0066 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 465 | log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p64 | -1.0% | 0.0025 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 466 | log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p63 | -1.0% | 0.0028 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 467 | log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p63 | -1.0% | 0.0042 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 468 | log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p64 | -1.0% | 0.0053 | 0.0016 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 469 | log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p63 | -1.0% | 0.0048 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 470 | log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p63 | -1.0% | 0.0054 | 0.0016 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 471 | log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p63 | -1.0% | 0.0056 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 472 | log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p61 | -1.0% | 0.0021 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 473 | log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p61 | -1.0% | 0.0051 | 0.0016 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 474 | log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p65 | -1.0% | -0.0045 | -0.0028 | false | roi_delta_below_market_gate, unstable_coverage |
| 475 | log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p65 | -1.0% | 0.0014 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 476 | log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p64 | -1.0% | 0.0032 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 477 | log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p64 | -1.0% | 0.0042 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 478 | log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p61 | -1.0% | 0.0114 | 0.0045 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 479 | log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p63 | -1.0% | 0.0035 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 480 | log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p65 | -1.0% | 0.0015 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 481 | log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p64 | -1.0% | 0.0036 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 482 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p64 | -1.0% | 0.0036 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 483 | log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p65 | -1.0% | -0.0005 | -0.0010 | false | roi_delta_below_market_gate, unstable_coverage |
| 484 | log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p65 | -1.0% | 0.0016 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 485 | log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p64 | -1.0% | -0.0012 | -0.0014 | false | roi_delta_below_market_gate, unstable_coverage |
| 486 | log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p64 | -1.0% | 0.0015 | -0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 487 | log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p65 | -1.0% | 0.0006 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 488 | log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p63 | -1.0% | 0.0037 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 489 | log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p62 | -1.0% | 0.0121 | 0.0049 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 490 | log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p65 | -1.0% | -0.0022 | -0.0018 | false | roi_delta_below_market_gate, unstable_coverage |
| 491 | log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p65 | -1.0% | -0.0003 | -0.0010 | false | roi_delta_below_market_gate, unstable_coverage |
| 492 | log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p64 | -1.0% | 0.0018 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 493 | log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p64 | -1.0% | 0.0027 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 494 | log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p64 | -1.0% | -0.0020 | -0.0018 | false | roi_delta_below_market_gate, unstable_coverage |
| 495 | log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p65 | -1.0% | 0.0007 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 496 | log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p65 | -1.0% | 0.0049 | 0.0015 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 497 | log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p64 | -1.0% | 0.0042 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 498 | log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p65 | -1.0% | 0.0018 | -0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 499 | log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p65 | -1.0% | 0.0027 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 500 | log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p63 | -1.0% | 0.0029 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 501 | log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p64 | -1.0% | -0.0011 | -0.0015 | false | roi_delta_below_market_gate, unstable_coverage |
| 502 | log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p64 | -1.0% | 0.0007 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 503 | log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p65 | -1.0% | 0.0030 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 504 | log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p65 | -1.0% | 0.0037 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 505 | log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p64 | -1.0% | 0.0052 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 506 | log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p64 | -1.0% | 0.0058 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 507 | log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p64 | -1.0% | 0.0064 | 0.0019 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 508 | log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p65 | -1.0% | -0.0041 | -0.0027 | false | roi_delta_below_market_gate, unstable_coverage |
| 509 | log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p64 | -1.0% | 0.0038 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 510 | log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p65 | -1.0% | 0.0001 | -0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 511 | log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p64 | -1.0% | 0.0007 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 512 | log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p63 | -1.0% | 0.0098 | 0.0037 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 513 | log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p63 | -1.0% | 0.0125 | 0.0051 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 514 | log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p65 | -1.0% | 0.0037 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 515 | log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p65 | -1.0% | 0.0045 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 516 | log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p64 | -1.0% | 0.0042 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 517 | log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p64 | -1.0% | 0.0047 | 0.0011 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 518 | log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p64 | -1.0% | 0.0030 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 519 | log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p64 | -1.0% | 0.0035 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 520 | log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p61 | -1.0% | 0.0091 | 0.0035 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 521 | log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p65 | -1.0% | 0.0032 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 522 | log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p65 | -1.0% | 0.0043 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 523 | log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p65 | -1.0% | 0.0047 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 524 | log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p61 | -1.0% | 0.0062 | 0.0022 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 525 | log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p65 | -1.0% | 0.0025 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 526 | log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p65 | -1.0% | 0.0012 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 527 | log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p64 | -1.0% | 0.0030 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 528 | log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p62 | -1.0% | 0.0133 | 0.0053 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 529 | log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p64 | -1.0% | 0.0108 | 0.0042 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 530 | log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p61 | -1.1% | 0.0036 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 531 | log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p64 | -1.1% | 0.0039 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 532 | log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p65 | -1.1% | -0.0019 | -0.0018 | false | roi_delta_below_market_gate, unstable_coverage |
| 533 | log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p64 | -1.1% | 0.0034 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 534 | log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p65 | -1.1% | 0.0020 | 0.0000 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 535 | log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p65 | -1.1% | 0.0027 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 536 | log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p65 | -1.1% | -0.0015 | -0.0016 | false | roi_delta_below_market_gate, unstable_coverage |
| 537 | log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p61 | -1.1% | 0.0141 | 0.0057 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 538 | log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p65 | -1.1% | 0.0005 | -0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 539 | log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p62 | -1.1% | 0.0064 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 540 | log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p61 | -1.1% | 0.0093 | 0.0036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 541 | log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p63 | -1.1% | 0.0069 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 542 | log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p65 | -1.1% | 0.0017 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 543 | log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p65 | -1.1% | 0.0068 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 544 | log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p65 | -1.1% | 0.0005 | -0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 545 | log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p65 | -1.1% | 0.0009 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 546 | log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p64 | -1.1% | 0.0134 | 0.0052 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 547 | log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p62 | -1.1% | 0.0086 | 0.0033 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 548 | log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p64 | -1.1% | 0.0032 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 549 | log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p65 | -1.1% | -0.0012 | -0.0016 | false | roi_delta_below_market_gate, unstable_coverage |
| 550 | log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p65 | -1.1% | 0.0010 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 551 | log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p65 | -1.1% | 0.0044 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 552 | log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p65 | -1.1% | 0.0048 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 553 | log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p65 | -1.1% | 0.0060 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 554 | log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p65 | -1.1% | 0.0036 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 555 | log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p65 | -1.1% | 0.0038 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 556 | log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p64 | -1.1% | 0.0086 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 557 | log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p65 | -1.1% | 0.0038 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 558 | log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p65 | -1.1% | 0.0050 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 559 | log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p65 | -1.1% | 0.0054 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 560 | log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p64 | -1.1% | 0.0135 | 0.0055 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 561 | log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p65 | -1.1% | 0.0022 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 562 | log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p65 | -1.1% | 0.0039 | 0.0007 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 563 | log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p65 | -1.1% | 0.0016 | -0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 564 | log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p65 | -1.1% | 0.0025 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market, unstable_coverage |
| 565 | log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p65 | -1.2% | 0.0085 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 566 | log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p65 | -1.2% | -0.0020 | -0.0019 | false | roi_delta_below_market_gate, unstable_coverage |
| 567 | log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p61 | -1.2% | 0.0027 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 568 | log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p61 | -1.3% | 0.0090 | 0.0034 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 569 | log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p62 | -1.3% | 0.0086 | 0.0033 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 570 | log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p61 | -1.3% | 0.0119 | 0.0047 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 571 | log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p61 | -1.3% | 0.0020 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 572 | log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p61 | -1.3% | 0.0112 | 0.0044 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 573 | log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p63 | -1.3% | 0.0076 | 0.0028 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 574 | log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p61 | -1.3% | 0.0026 | 0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 575 | log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p61 | -1.4% | 0.0043 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 576 | log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p64 | -1.4% | 0.0020 | 0.0002 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 577 | log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p62 | -1.4% | 0.0100 | 0.0038 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 578 | log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p63 | -1.4% | 0.0079 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 579 | log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p61 | -1.4% | 0.0053 | 0.0017 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 580 | log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p63 | -1.4% | 0.0165 | 0.0067 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 581 | log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p64 | -1.4% | 0.0061 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 582 | log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p64 | -1.4% | 0.0162 | 0.0064 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 583 | log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p62 | -1.4% | 0.0056 | 0.0018 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 584 | log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p65 | -1.4% | 0.0063 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 585 | log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p62 | -1.4% | 0.0040 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 586 | log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p61 | -1.5% | 0.0087 | 0.0033 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 587 | log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p61 | -1.5% | 0.0092 | 0.0034 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 588 | log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p63 | -1.5% | 0.0093 | 0.0036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 589 | log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p62 | -1.5% | 0.0087 | 0.0033 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 590 | log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p61 | -1.5% | 0.0108 | 0.0042 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 591 | log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p62 | -1.5% | 0.0100 | 0.0038 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 592 | log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p64 | -1.5% | 0.0005 | -0.0005 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 593 | log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p63 | -1.5% | 0.0013 | -0.0001 | false | roi_delta_below_market_gate, log_loss_worse_than_market |
| 594 | log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p62 | -1.5% | 0.0102 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 595 | log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p63 | -1.5% | 0.0086 | 0.0032 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 596 | log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p62 | -1.5% | 0.0050 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 597 | log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p64 | -1.5% | 0.0080 | 0.0028 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 598 | log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p63 | -1.5% | 0.0090 | 0.0034 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 599 | log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p63 | -1.5% | 0.0078 | 0.0028 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 600 | log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p64 | -1.5% | 0.0071 | 0.0025 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 601 | log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p64 | -1.5% | 0.0080 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 602 | log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p64 | -1.6% | 0.0082 | 0.0029 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 603 | log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p64 | -1.6% | 0.0077 | 0.0028 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 604 | log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p64 | -1.6% | 0.0098 | 0.0037 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 605 | log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p62 | -1.6% | 0.0110 | 0.0043 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 606 | log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p63 | -1.6% | 0.0079 | 0.0029 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 607 | log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p62 | -1.6% | 0.0065 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 608 | log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p64 | -1.6% | 0.0067 | 0.0025 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 609 | log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p62 | -1.6% | 0.0030 | 0.0006 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 610 | log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p65 | -1.6% | 0.0060 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 611 | log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p63 | -1.6% | 0.0025 | 0.0004 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 612 | log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p64 | -1.6% | 0.0096 | 0.0036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 613 | log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p65 | -1.6% | 0.0072 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 614 | log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p64 | -1.6% | 0.0034 | 0.0008 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 615 | log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p61 | -1.6% | 0.0153 | 0.0063 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 616 | log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p64 | -1.6% | 0.0108 | 0.0041 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 617 | log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p63 | -1.6% | 0.0110 | 0.0041 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 618 | log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p61 | -1.6% | 0.0081 | 0.0030 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 619 | log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p64 | -1.7% | 0.0105 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 620 | log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p62 | -1.7% | 0.0156 | 0.0064 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 621 | log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p62 | -1.7% | 0.0116 | 0.0046 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 622 | log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p65 | -1.7% | 0.0073 | 0.0027 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 623 | log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p63 | -1.7% | 0.0142 | 0.0057 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 624 | log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p62 | -1.7% | 0.0143 | 0.0057 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 625 | log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p61 | -1.7% | 0.0071 | 0.0026 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 626 | log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p64 | -1.7% | 0.0135 | 0.0052 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 627 | log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p61 | -1.7% | 0.0163 | 0.0067 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 628 | log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p62 | -1.7% | 0.0150 | 0.0062 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 629 | log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p65 | -1.8% | 0.0079 | 0.0029 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 630 | log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p62 | -1.8% | 0.0087 | 0.0033 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 631 | log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p65 | -1.8% | 0.0157 | 0.0063 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 632 | log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p63 | -1.8% | -0.0007 | -0.0010 | false | roi_delta_below_market_gate |
| 633 | log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p63 | -1.8% | 0.0143 | 0.0059 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 634 | log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p64 | -1.8% | 0.0154 | 0.0064 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 635 | log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p65 | -1.8% | 0.0170 | 0.0069 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 636 | log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p65 | -1.9% | 0.0171 | 0.0071 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 637 | log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p63 | -1.9% | 0.0102 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 638 | log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p62 | -2.0% | 0.0033 | 0.0009 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 639 | log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p61 | -2.0% | 0.0199 | 0.0084 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 640 | log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p61 | -2.0% | 0.0058 | 0.0020 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 641 | log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p62 | -2.0% | 0.0203 | 0.0086 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 642 | log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p62 | -2.1% | 0.0118 | 0.0048 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 643 | log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p65 | -2.1% | 0.0219 | 0.0091 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 644 | log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p63 | -2.1% | 0.0117 | 0.0047 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 645 | log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p62 | -2.1% | 0.0042 | 0.0012 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 646 | log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p62 | -2.2% | 0.0146 | 0.0059 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 647 | log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p63 | -2.2% | 0.0130 | 0.0052 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 648 | log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p62 | -2.2% | 0.0142 | 0.0058 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 649 | log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p62 | -2.2% | 0.0103 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 650 | log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p61 | -2.3% | 0.0035 | 0.0010 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 651 | log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p65 | -2.3% | 0.0120 | 0.0046 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 652 | log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p64 | -2.3% | 0.0108 | 0.0045 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 653 | log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p65 | -2.4% | 0.0101 | 0.0041 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 654 | log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p62 | -2.4% | 0.0094 | 0.0036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 655 | log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p65 | -2.4% | 0.0089 | 0.0036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 656 | log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p64 | -2.4% | 0.0108 | 0.0043 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 657 | log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p63 | -2.5% | 0.0056 | 0.0019 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 658 | log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p65 | -2.5% | 0.0100 | 0.0039 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 659 | log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p65 | -2.5% | 0.0112 | 0.0046 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market, unstable_coverage |
| 660 | log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p62 | -2.7% | 0.0237 | 0.0102 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 661 | log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p61 | -2.7% | 0.0133 | 0.0055 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 662 | log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p63 | -2.7% | 0.0244 | 0.0105 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 663 | log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p63 | -2.7% | 0.0217 | 0.0093 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 664 | log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p61 | -2.7% | 0.0163 | 0.0069 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 665 | log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p62 | -2.8% | 0.0059 | 0.0021 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 666 | log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p61 | -2.9% | 0.0119 | 0.0049 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 667 | log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p62 | -2.9% | 0.0136 | 0.0055 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 668 | log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p61 | -2.9% | 0.0100 | 0.0040 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 669 | log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p63 | -3.1% | 0.0201 | 0.0086 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 670 | log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p63 | -3.2% | 0.0157 | 0.0065 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 671 | log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p64 | -3.2% | 0.0147 | 0.0061 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 672 | log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p62 | -3.4% | 0.0197 | 0.0084 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 673 | log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p61 | -3.5% | 0.0125 | 0.0051 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 674 | log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p64 | -3.5% | 0.0252 | 0.0108 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 675 | log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p64 | -3.7% | 0.0244 | 0.0103 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 676 | log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p61 | -3.7% | 0.0193 | 0.0084 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 677 | log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p61 | -3.7% | 0.0168 | 0.0072 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 678 | log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p62 | -3.8% | 0.0177 | 0.0075 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 679 | log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p61 | -3.8% | 0.0198 | 0.0085 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 680 | log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p64 | -3.8% | 0.0219 | 0.0094 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 681 | log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p61 | -3.9% | 0.0171 | 0.0072 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 682 | log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p61 | -3.9% | 0.0247 | 0.0108 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 683 | log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p61 | -3.9% | 0.0160 | 0.0068 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 684 | log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p61 | -4.0% | 0.0198 | 0.0086 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 685 | log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p61 | -4.0% | 0.0156 | 0.0067 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 686 | log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p62 | -4.0% | 0.0242 | 0.0105 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 687 | log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p62 | -4.1% | 0.0222 | 0.0096 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 688 | log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p61 | -4.1% | 0.0118 | 0.0050 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 689 | log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p63 | -4.1% | 0.0247 | 0.0106 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 690 | log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p63 | -4.2% | 0.0223 | 0.0094 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 691 | log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p61 | -4.2% | 0.0169 | 0.0073 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 692 | log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p61 | -4.3% | 0.0182 | 0.0080 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 693 | log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p65 | -4.3% | 0.0295 | 0.0125 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 694 | log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p62 | -4.3% | 0.0190 | 0.0083 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 695 | log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p63 | -4.3% | 0.0200 | 0.0085 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 696 | log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p64 | -4.4% | 0.0290 | 0.0125 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 697 | log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p63 | -4.4% | 0.0216 | 0.0092 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 698 | log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p62 | -4.4% | 0.0235 | 0.0101 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 699 | log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p61 | -4.4% | 0.0251 | 0.0110 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 700 | log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p61 | -4.4% | 0.0216 | 0.0094 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 701 | log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p62 | -4.5% | 0.0261 | 0.0114 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 702 | log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p65 | -4.6% | 0.0251 | 0.0108 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 703 | log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p61 | -4.6% | 0.0272 | 0.0120 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 704 | log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p63 | -4.7% | 0.0263 | 0.0113 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 705 | log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p61 | -4.7% | 0.0204 | 0.0090 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 706 | log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p62 | -4.8% | 0.0213 | 0.0092 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 707 | log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p62 | -4.8% | 0.0278 | 0.0122 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 708 | log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p61 | -4.8% | 0.0228 | 0.0100 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 709 | log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p64 | -4.9% | 0.0279 | 0.0119 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 710 | log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p63 | -4.9% | 0.0286 | 0.0124 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 711 | log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p61 | -4.9% | 0.0238 | 0.0105 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 712 | log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p62 | -5.0% | 0.0288 | 0.0125 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 713 | log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p62 | -5.1% | 0.0245 | 0.0108 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 714 | log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p62 | -5.1% | 0.0230 | 0.0101 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 715 | log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p62 | -5.1% | 0.0272 | 0.0118 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 716 | log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p65 | -5.2% | 0.0333 | 0.0142 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 717 | log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p63 | -5.2% | 0.0253 | 0.0111 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 718 | log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p61 | -5.2% | 0.0232 | 0.0101 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 719 | log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p61 | -5.2% | 0.0221 | 0.0096 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 720 | log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p64 | -5.3% | 0.0256 | 0.0111 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 721 | log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p61 | -5.3% | 0.0256 | 0.0113 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 722 | log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p65 | -5.3% | 0.0287 | 0.0123 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 723 | log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p62 | -5.5% | 0.0241 | 0.0105 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 724 | log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p62 | -5.5% | 0.0253 | 0.0111 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 725 | log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p63 | -5.5% | 0.0276 | 0.0119 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 726 | log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p61 | -5.5% | 0.0240 | 0.0104 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 727 | log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p61 | -5.6% | 0.0295 | 0.0130 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 728 | log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p61 | -5.7% | 0.0305 | 0.0136 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 729 | log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p61 | -5.7% | 0.0259 | 0.0114 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 730 | log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p63 | -5.9% | 0.0316 | 0.0137 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 731 | log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p63 | -6.1% | 0.0343 | 0.0151 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 732 | log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p61 | -6.1% | 0.0298 | 0.0131 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 733 | log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p61 | -6.1% | 0.0267 | 0.0117 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 734 | log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p61 | -6.1% | 0.0285 | 0.0124 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 735 | log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p64 | -6.2% | 0.0383 | 0.0166 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 736 | log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p64 | -6.2% | 0.0353 | 0.0153 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 737 | log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p62 | -6.2% | 0.0332 | 0.0146 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 738 | log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p62 | -6.3% | 0.0308 | 0.0135 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 739 | log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p63 | -6.3% | 0.0376 | 0.0164 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 740 | log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p62 | -6.7% | 0.0377 | 0.0165 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 741 | log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p61 | -6.7% | 0.0359 | 0.0159 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 742 | log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p61 | -6.7% | 0.0351 | 0.0157 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 743 | log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p62 | -6.9% | 0.0363 | 0.0161 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 744 | log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p63 | -6.9% | 0.0402 | 0.0175 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 745 | log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p61 | -7.1% | 0.0375 | 0.0166 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 746 | log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p61 | -7.1% | 0.0371 | 0.0163 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 747 | log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p62 | -7.3% | 0.0416 | 0.0182 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 748 | log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p62 | -7.3% | 0.0409 | 0.0180 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 749 | log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p61 | -7.8% | 0.0384 | 0.0169 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 750 | log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p61 | -7.8% | 0.0407 | 0.0178 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 751 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 234 | 77.8% | 0.5342 | 0.1752 | 16.0% |
| log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 217 | 77.9% | 0.5292 | 0.1730 | 14.8% |
| log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 208 | 78.4% | 0.5245 | 0.1708 | 14.9% |
| log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 204 | 77.9% | 0.5259 | 0.1716 | 13.9% |
| log_allmarketctx_c0p5_temp1p6_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 190 | 79.5% | 0.5135 | 0.1658 | 15.9% |
| log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 237 | 77.6% | 0.5363 | 0.1761 | 16.1% |
| log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 222 | 77.5% | 0.5333 | 0.1749 | 14.9% |
| log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 212 | 77.8% | 0.5290 | 0.1729 | 14.6% |
| log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 204 | 78.4% | 0.5239 | 0.1705 | 15.5% |
| log_allmarketctx_c0p5_temp1p6_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 196 | 78.1% | 0.5244 | 0.1709 | 14.5% |
| log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 242 | 77.3% | 0.5399 | 0.1778 | 16.6% |
| log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 228 | 77.6% | 0.5348 | 0.1755 | 16.5% |
| log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 216 | 77.8% | 0.5313 | 0.1739 | 15.3% |
| log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 206 | 77.7% | 0.5297 | 0.1733 | 14.6% |
| log_allmarketctx_c0p5_temp1p6_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 198 | 78.3% | 0.5242 | 0.1708 | 15.5% |
| log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 247 | 75.7% | 0.5499 | 0.1825 | 14.6% |
| log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 235 | 75.7% | 0.5471 | 0.1813 | 13.8% |
| log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 223 | 77.1% | 0.5377 | 0.1768 | 15.7% |
| log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 208 | 76.9% | 0.5358 | 0.1761 | 14.7% |
| log_allmarketctx_c0p5_temp1p6_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 199 | 77.4% | 0.5313 | 0.1741 | 15.1% |
| log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 254 | 74.4% | 0.5598 | 0.1872 | 13.6% |
| log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 243 | 75.3% | 0.5535 | 0.1842 | 14.5% |
| log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 227 | 75.8% | 0.5481 | 0.1817 | 14.4% |
| log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 213 | 75.6% | 0.5465 | 0.1811 | 13.5% |
| log_allmarketctx_c0p5_temp1p6_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 202 | 77.2% | 0.5347 | 0.1755 | 15.8% |
| log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 221 | 78.3% | 0.5297 | 0.1731 | 15.6% |
| log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 210 | 78.6% | 0.5252 | 0.1711 | 15.1% |
| log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 205 | 78.0% | 0.5266 | 0.1718 | 14.1% |
| log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 193 | 79.3% | 0.5167 | 0.1672 | 15.5% |
| log_allmarketctx_c0p5_temp1p8_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 183 | 79.8% | 0.5112 | 0.1647 | 16.2% |
| log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 228 | 77.6% | 0.5352 | 0.1756 | 15.3% |
| log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 213 | 77.9% | 0.5297 | 0.1732 | 14.9% |
| log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 207 | 78.3% | 0.5266 | 0.1718 | 15.1% |
| log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 198 | 78.3% | 0.5244 | 0.1709 | 14.7% |
| log_allmarketctx_c0p5_temp1p8_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 183 | 79.2% | 0.5151 | 0.1666 | 15.7% |
| log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 233 | 77.3% | 0.5389 | 0.1774 | 15.9% |
| log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 218 | 78.0% | 0.5317 | 0.1741 | 15.6% |
| log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 207 | 77.8% | 0.5300 | 0.1734 | 14.7% |
| log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 197 | 78.2% | 0.5255 | 0.1714 | 15.1% |
| log_allmarketctx_c0p5_temp1p8_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 185 | 79.5% | 0.5150 | 0.1665 | 16.6% |
| log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 237 | 75.9% | 0.5468 | 0.1812 | 14.1% |
| log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 223 | 77.6% | 0.5361 | 0.1761 | 16.3% |
| log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 211 | 77.7% | 0.5325 | 0.1745 | 15.7% |
| log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 202 | 77.2% | 0.5331 | 0.1750 | 14.0% |
| log_allmarketctx_c0p5_temp1p8_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 187 | 79.1% | 0.5182 | 0.1680 | 16.8% |
| log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 242 | 75.6% | 0.5516 | 0.1834 | 14.9% |
| log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 228 | 75.9% | 0.5473 | 0.1815 | 14.0% |
| log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 213 | 76.5% | 0.5409 | 0.1785 | 14.7% |
| log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 201 | 77.1% | 0.5351 | 0.1759 | 15.3% |
| log_allmarketctx_c0p5_temp1p8_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 191 | 77.0% | 0.5340 | 0.1755 | 14.6% |
| log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 213 | 78.4% | 0.5282 | 0.1724 | 14.9% |
| log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 208 | 78.4% | 0.5270 | 0.1719 | 14.7% |
| log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 198 | 78.3% | 0.5247 | 0.1709 | 14.0% |
| log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 188 | 79.8% | 0.5140 | 0.1658 | 16.1% |
| log_allmarketctx_c0p5_temp2p0_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 176 | 80.1% | 0.5090 | 0.1636 | 16.4% |
| log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 216 | 77.8% | 0.5325 | 0.1744 | 14.6% |
| log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 209 | 78.5% | 0.5275 | 0.1721 | 15.4% |
| log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 202 | 78.7% | 0.5243 | 0.1706 | 15.3% |
| log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 186 | 79.0% | 0.5184 | 0.1680 | 15.3% |
| log_allmarketctx_c0p5_temp2p0_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 178 | 80.3% | 0.5086 | 0.1634 | 17.1% |
| log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 222 | 77.5% | 0.5364 | 0.1762 | 14.9% |
| log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 212 | 77.8% | 0.5322 | 0.1743 | 14.6% |
| log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 202 | 78.7% | 0.5251 | 0.1710 | 15.9% |
| log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 188 | 78.7% | 0.5215 | 0.1695 | 15.5% |
| log_allmarketctx_c0p5_temp2p0_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 178 | 79.8% | 0.5128 | 0.1654 | 16.5% |
| log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 228 | 77.6% | 0.5383 | 0.1771 | 16.5% |
| log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 214 | 77.6% | 0.5351 | 0.1757 | 15.4% |
| log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 202 | 77.2% | 0.5339 | 0.1753 | 14.0% |
| log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 191 | 79.1% | 0.5210 | 0.1692 | 16.4% |
| log_allmarketctx_c0p5_temp2p0_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 179 | 79.3% | 0.5165 | 0.1672 | 16.7% |
| log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 231 | 76.2% | 0.5471 | 0.1813 | 14.4% |
| log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 216 | 77.3% | 0.5383 | 0.1772 | 15.7% |
| log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 205 | 77.1% | 0.5368 | 0.1767 | 14.6% |
| log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 193 | 77.2% | 0.5334 | 0.1752 | 14.9% |
| log_allmarketctx_c0p5_temp2p0_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 181 | 78.5% | 0.5233 | 0.1705 | 16.3% |
| log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 211 | 78.7% | 0.5278 | 0.1721 | 15.1% |
| log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 204 | 77.9% | 0.5293 | 0.1729 | 13.6% |
| log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 193 | 79.8% | 0.5168 | 0.1670 | 16.1% |
| log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 185 | 80.0% | 0.5136 | 0.1656 | 16.1% |
| log_allmarketctx_c0p5_temp2p2_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 172 | 79.7% | 0.5124 | 0.1652 | 13.2% |
| log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 212 | 78.8% | 0.5285 | 0.1724 | 15.9% |
| log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 207 | 78.3% | 0.5295 | 0.1730 | 14.7% |
| log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 194 | 78.9% | 0.5229 | 0.1699 | 14.9% |
| log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 184 | 79.9% | 0.5146 | 0.1661 | 16.5% |
| log_allmarketctx_c0p5_temp2p2_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 171 | 79.5% | 0.5134 | 0.1657 | 13.3% |
| log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 213 | 77.9% | 0.5334 | 0.1748 | 14.9% |
| log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 207 | 78.3% | 0.5303 | 0.1733 | 15.1% |
| log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 196 | 78.6% | 0.5259 | 0.1714 | 15.6% |
| log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 182 | 79.7% | 0.5161 | 0.1668 | 16.3% |
| log_allmarketctx_c0p5_temp2p2_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 171 | 80.1% | 0.5107 | 0.1644 | 14.7% |
| log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 218 | 77.5% | 0.5378 | 0.1768 | 15.2% |
| log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 207 | 77.3% | 0.5360 | 0.1761 | 14.0% |
| log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 196 | 78.1% | 0.5294 | 0.1731 | 14.9% |
| log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 182 | 79.1% | 0.5202 | 0.1688 | 16.3% |
| log_allmarketctx_c0p5_temp2p2_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 172 | 79.7% | 0.5146 | 0.1663 | 17.1% |
| log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 222 | 77.0% | 0.5424 | 0.1790 | 15.3% |
| log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 204 | 77.5% | 0.5359 | 0.1761 | 15.2% |
| log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 198 | 77.3% | 0.5353 | 0.1759 | 14.7% |
| log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 183 | 78.7% | 0.5238 | 0.1706 | 16.4% |
| log_allmarketctx_c0p5_temp2p2_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 172 | 79.1% | 0.5188 | 0.1683 | 17.0% |
| log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 211 | 78.7% | 0.5298 | 0.1729 | 14.9% |
| log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 198 | 79.3% | 0.5231 | 0.1698 | 15.1% |
| log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 187 | 80.2% | 0.5155 | 0.1663 | 16.5% |
| log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 178 | 80.3% | 0.5123 | 0.1649 | 16.3% |
| log_allmarketctx_c0p5_temp2p5_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 160 | 81.2% | 0.5017 | 0.1601 | 15.0% |
| log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 209 | 78.5% | 0.5315 | 0.1737 | 15.0% |
| log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 196 | 79.1% | 0.5247 | 0.1706 | 15.2% |
| log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 187 | 79.7% | 0.5193 | 0.1681 | 15.9% |
| log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 175 | 80.0% | 0.5143 | 0.1658 | 16.3% |
| log_allmarketctx_c0p5_temp2p5_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 164 | 81.1% | 0.5048 | 0.1614 | 15.2% |
| log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 208 | 78.4% | 0.5327 | 0.1743 | 15.2% |
| log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 201 | 78.6% | 0.5297 | 0.1729 | 15.5% |
| log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 184 | 79.3% | 0.5212 | 0.1690 | 15.8% |
| log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 173 | 79.8% | 0.5161 | 0.1667 | 16.1% |
| log_allmarketctx_c0p5_temp2p5_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 166 | 80.7% | 0.5086 | 0.1632 | 15.3% |
| log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 210 | 77.6% | 0.5377 | 0.1767 | 14.3% |
| log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 198 | 78.3% | 0.5315 | 0.1738 | 15.2% |
| log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 185 | 79.5% | 0.5220 | 0.1694 | 16.6% |
| log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 172 | 80.2% | 0.5142 | 0.1658 | 17.7% |
| log_allmarketctx_c0p5_temp2p5_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 161 | 80.1% | 0.5119 | 0.1649 | 15.1% |
| log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 209 | 77.5% | 0.5394 | 0.1775 | 15.1% |
| log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 199 | 77.4% | 0.5374 | 0.1767 | 14.2% |
| log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 183 | 78.7% | 0.5266 | 0.1717 | 15.9% |
| log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 172 | 79.1% | 0.5218 | 0.1695 | 16.8% |
| log_allmarketctx_c0p5_temp2p5_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 159 | 79.9% | 0.5135 | 0.1657 | 15.9% |
| log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 240 | 77.5% | 0.5390 | 0.1774 | 18.8% |
| log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 223 | 77.1% | 0.5368 | 0.1766 | 17.0% |
| log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 210 | 77.6% | 0.5312 | 0.1740 | 14.0% |
| log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 205 | 77.6% | 0.5304 | 0.1737 | 13.6% |
| log_allmarketctx_c1p0_temp1p6_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 195 | 77.4% | 0.5289 | 0.1731 | 13.0% |
| log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 244 | 77.0% | 0.5428 | 0.1791 | 18.8% |
| log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 231 | 77.1% | 0.5402 | 0.1780 | 18.3% |
| log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 217 | 77.0% | 0.5377 | 0.1769 | 13.9% |
| log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 210 | 77.1% | 0.5352 | 0.1758 | 13.6% |
| log_allmarketctx_c1p0_temp1p6_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 198 | 76.8% | 0.5351 | 0.1760 | 12.9% |
| log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 253 | 75.9% | 0.5520 | 0.1834 | 18.2% |
| log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 238 | 76.1% | 0.5482 | 0.1817 | 14.4% |
| log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 225 | 76.0% | 0.5461 | 0.1809 | 13.7% |
| log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 211 | 76.8% | 0.5390 | 0.1776 | 14.2% |
| log_allmarketctx_c1p0_temp1p6_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 203 | 76.8% | 0.5372 | 0.1768 | 14.0% |
| log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 257 | 74.3% | 0.5630 | 0.1886 | 15.8% |
| log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 245 | 75.1% | 0.5571 | 0.1858 | 14.2% |
| log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 233 | 75.1% | 0.5551 | 0.1849 | 13.9% |
| log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 219 | 75.3% | 0.5513 | 0.1833 | 13.3% |
| log_allmarketctx_c1p0_temp1p6_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 204 | 75.5% | 0.5480 | 0.1818 | 12.9% |
| log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 261 | 73.6% | 0.5717 | 0.1925 | 14.7% |
| log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 250 | 73.2% | 0.5718 | 0.1927 | 11.4% |
| log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 242 | 73.6% | 0.5689 | 0.1913 | 11.9% |
| log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 224 | 73.2% | 0.5681 | 0.1911 | 11.7% |
| log_allmarketctx_c1p0_temp1p6_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 214 | 73.8% | 0.5631 | 0.1888 | 12.3% |
| log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 231 | 77.5% | 0.5378 | 0.1769 | 17.9% |
| log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 211 | 78.2% | 0.5291 | 0.1729 | 14.8% |
| log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 206 | 77.7% | 0.5306 | 0.1737 | 13.8% |
| log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 199 | 77.4% | 0.5304 | 0.1738 | 12.9% |
| log_allmarketctx_c1p0_temp1p8_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 186 | 78.5% | 0.5209 | 0.1694 | 14.4% |
| log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 237 | 77.6% | 0.5395 | 0.1776 | 19.4% |
| log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 219 | 77.2% | 0.5374 | 0.1768 | 14.3% |
| log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 210 | 77.6% | 0.5329 | 0.1747 | 14.3% |
| log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 202 | 77.2% | 0.5333 | 0.1751 | 13.5% |
| log_allmarketctx_c1p0_temp1p8_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 186 | 78.5% | 0.5220 | 0.1698 | 14.6% |
| log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 240 | 76.7% | 0.5459 | 0.1806 | 18.2% |
| log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 226 | 76.1% | 0.5456 | 0.1806 | 13.7% |
| log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 214 | 77.1% | 0.5378 | 0.1770 | 14.6% |
| log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 205 | 76.6% | 0.5389 | 0.1777 | 13.6% |
| log_allmarketctx_c1p0_temp1p8_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 192 | 77.6% | 0.5301 | 0.1736 | 14.1% |
| log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 248 | 75.4% | 0.5557 | 0.1852 | 14.8% |
| log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 235 | 75.3% | 0.5536 | 0.1843 | 14.2% |
| log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 218 | 75.2% | 0.5508 | 0.1832 | 12.3% |
| log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 208 | 76.0% | 0.5448 | 0.1804 | 13.2% |
| log_allmarketctx_c1p0_temp1p8_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 195 | 76.4% | 0.5397 | 0.1781 | 13.9% |
| log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 253 | 73.5% | 0.5688 | 0.1914 | 11.8% |
| log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 242 | 73.6% | 0.5668 | 0.1906 | 11.7% |
| log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 224 | 74.1% | 0.5610 | 0.1879 | 12.6% |
| log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 213 | 75.1% | 0.5534 | 0.1844 | 14.1% |
| log_allmarketctx_c1p0_temp1p8_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 200 | 75.5% | 0.5489 | 0.1824 | 13.2% |
| log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 221 | 76.9% | 0.5386 | 0.1773 | 16.3% |
| log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 209 | 78.0% | 0.5305 | 0.1736 | 14.4% |
| log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 203 | 77.3% | 0.5322 | 0.1745 | 12.8% |
| log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 192 | 78.6% | 0.5223 | 0.1699 | 14.7% |
| log_allmarketctx_c1p0_temp2p0_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 177 | 79.7% | 0.5125 | 0.1654 | 15.7% |
| log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 225 | 77.3% | 0.5389 | 0.1774 | 18.1% |
| log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 211 | 77.7% | 0.5333 | 0.1749 | 14.5% |
| log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 206 | 77.7% | 0.5324 | 0.1745 | 14.2% |
| log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 193 | 77.7% | 0.5289 | 0.1730 | 13.5% |
| log_allmarketctx_c1p0_temp2p0_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 182 | 79.7% | 0.5147 | 0.1663 | 16.2% |
| log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 229 | 76.9% | 0.5432 | 0.1794 | 15.0% |
| log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 217 | 77.0% | 0.5397 | 0.1779 | 14.3% |
| log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 208 | 76.9% | 0.5380 | 0.1772 | 14.0% |
| log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 195 | 76.9% | 0.5350 | 0.1759 | 13.0% |
| log_allmarketctx_c1p0_temp2p0_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 183 | 79.2% | 0.5187 | 0.1682 | 16.6% |
| log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 239 | 75.7% | 0.5524 | 0.1838 | 14.9% |
| log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 224 | 75.4% | 0.5507 | 0.1831 | 12.6% |
| log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 209 | 76.1% | 0.5442 | 0.1802 | 13.3% |
| log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 197 | 76.6% | 0.5386 | 0.1776 | 13.6% |
| log_allmarketctx_c1p0_temp2p0_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 185 | 77.3% | 0.5322 | 0.1747 | 14.8% |
| log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 244 | 73.8% | 0.5650 | 0.1898 | 12.0% |
| log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 230 | 74.8% | 0.5578 | 0.1864 | 13.4% |
| log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 214 | 75.2% | 0.5523 | 0.1839 | 13.8% |
| log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 201 | 75.6% | 0.5476 | 0.1818 | 13.3% |
| log_allmarketctx_c1p0_temp2p0_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 186 | 75.8% | 0.5434 | 0.1800 | 13.3% |
| log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 213 | 77.9% | 0.5328 | 0.1746 | 17.3% |
| log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 205 | 77.6% | 0.5325 | 0.1745 | 13.3% |
| log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 198 | 78.8% | 0.5242 | 0.1706 | 14.9% |
| log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 187 | 78.6% | 0.5224 | 0.1699 | 14.1% |
| log_allmarketctx_c1p0_temp2p2_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 175 | 80.0% | 0.5111 | 0.1646 | 14.0% |
| log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 214 | 77.6% | 0.5359 | 0.1760 | 14.2% |
| log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 208 | 77.9% | 0.5328 | 0.1746 | 14.6% |
| log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 199 | 77.4% | 0.5330 | 0.1749 | 12.9% |
| log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 184 | 79.3% | 0.5183 | 0.1679 | 15.9% |
| log_allmarketctx_c1p0_temp2p2_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 174 | 79.9% | 0.5126 | 0.1654 | 14.2% |
| log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 221 | 76.9% | 0.5418 | 0.1788 | 14.5% |
| log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 211 | 77.3% | 0.5378 | 0.1770 | 14.3% |
| log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 201 | 77.1% | 0.5361 | 0.1763 | 13.2% |
| log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 187 | 79.1% | 0.5214 | 0.1694 | 16.2% |
| log_allmarketctx_c1p0_temp2p2_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 174 | 79.3% | 0.5174 | 0.1676 | 13.7% |
| log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 226 | 75.7% | 0.5504 | 0.1829 | 13.0% |
| log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 215 | 76.3% | 0.5450 | 0.1804 | 13.4% |
| log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 204 | 76.5% | 0.5416 | 0.1789 | 13.4% |
| log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 188 | 77.7% | 0.5313 | 0.1741 | 14.9% |
| log_allmarketctx_c1p0_temp2p2_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 176 | 79.0% | 0.5208 | 0.1692 | 15.3% |
| log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 234 | 75.2% | 0.5566 | 0.1858 | 14.0% |
| log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 215 | 75.8% | 0.5496 | 0.1826 | 14.5% |
| log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 205 | 75.6% | 0.5484 | 0.1822 | 12.9% |
| log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 190 | 75.8% | 0.5442 | 0.1803 | 13.0% |
| log_allmarketctx_c1p0_temp2p2_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 175 | 77.7% | 0.5295 | 0.1734 | 13.7% |
| log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 209 | 77.5% | 0.5353 | 0.1757 | 13.2% |
| log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 201 | 78.1% | 0.5302 | 0.1733 | 13.9% |
| log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 189 | 78.8% | 0.5234 | 0.1702 | 14.4% |
| log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 179 | 79.3% | 0.5180 | 0.1677 | 15.1% |
| log_allmarketctx_c1p0_temp2p5_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 166 | 80.1% | 0.5100 | 0.1641 | 13.7% |
| log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 210 | 78.1% | 0.5343 | 0.1751 | 14.9% |
| log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 203 | 77.3% | 0.5358 | 0.1760 | 12.8% |
| log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 191 | 78.5% | 0.5267 | 0.1717 | 14.5% |
| log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 178 | 79.8% | 0.5164 | 0.1669 | 16.1% |
| log_allmarketctx_c1p0_temp2p5_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 167 | 79.6% | 0.5143 | 0.1661 | 13.3% |
| log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 212 | 77.8% | 0.5371 | 0.1765 | 15.2% |
| log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 203 | 77.3% | 0.5371 | 0.1766 | 13.5% |
| log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 187 | 78.6% | 0.5264 | 0.1716 | 15.2% |
| log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 178 | 79.2% | 0.5209 | 0.1691 | 15.6% |
| log_allmarketctx_c1p0_temp2p5_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 167 | 79.6% | 0.5156 | 0.1667 | 13.8% |
| log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 214 | 77.1% | 0.5424 | 0.1790 | 14.6% |
| log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 204 | 76.5% | 0.5429 | 0.1794 | 13.2% |
| log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 187 | 79.1% | 0.5247 | 0.1708 | 16.9% |
| log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 178 | 79.2% | 0.5221 | 0.1696 | 15.0% |
| log_allmarketctx_c1p0_temp2p5_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 165 | 78.2% | 0.5251 | 0.1713 | 13.2% |
| log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 219 | 75.8% | 0.5517 | 0.1834 | 13.0% |
| log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 208 | 75.5% | 0.5505 | 0.1830 | 12.5% |
| log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 188 | 77.1% | 0.5373 | 0.1769 | 14.2% |
| log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 175 | 78.3% | 0.5277 | 0.1724 | 14.5% |
| log_allmarketctx_c1p0_temp2p5_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 164 | 77.4% | 0.5301 | 0.1738 | 13.1% |
| log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 241 | 76.3% | 0.5457 | 0.1806 | 16.8% |
| log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 230 | 77.0% | 0.5405 | 0.1782 | 17.2% |
| log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 218 | 77.1% | 0.5374 | 0.1768 | 16.9% |
| log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 205 | 77.6% | 0.5319 | 0.1743 | 13.7% |
| log_allmarketctx_c1p5_temp1p6_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 196 | 77.0% | 0.5331 | 0.1751 | 12.5% |
| log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 248 | 75.8% | 0.5511 | 0.1830 | 17.0% |
| log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 236 | 76.7% | 0.5445 | 0.1799 | 18.1% |
| log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 223 | 77.1% | 0.5396 | 0.1777 | 17.9% |
| log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 215 | 76.7% | 0.5402 | 0.1781 | 13.6% |
| log_allmarketctx_c1p5_temp1p6_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 198 | 76.8% | 0.5369 | 0.1767 | 12.9% |
| log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 258 | 74.4% | 0.5618 | 0.1880 | 16.9% |
| log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 243 | 75.7% | 0.5531 | 0.1839 | 17.7% |
| log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 229 | 76.0% | 0.5493 | 0.1822 | 17.1% |
| log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 217 | 75.1% | 0.5521 | 0.1837 | 12.0% |
| log_allmarketctx_c1p5_temp1p6_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 208 | 76.4% | 0.5426 | 0.1792 | 14.0% |
| log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 260 | 73.5% | 0.5708 | 0.1922 | 15.4% |
| log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 252 | 73.4% | 0.5698 | 0.1917 | 15.2% |
| log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 239 | 74.1% | 0.5646 | 0.1893 | 15.1% |
| log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 223 | 74.9% | 0.5577 | 0.1861 | 13.5% |
| log_allmarketctx_c1p5_temp1p6_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 211 | 74.9% | 0.5559 | 0.1854 | 13.5% |
| log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 264 | 72.7% | 0.5802 | 0.1964 | 14.7% |
| log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 255 | 72.9% | 0.5781 | 0.1954 | 14.8% |
| log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 247 | 72.9% | 0.5774 | 0.1951 | 14.5% |
| log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 227 | 72.2% | 0.5785 | 0.1958 | 10.2% |
| log_allmarketctx_c1p5_temp1p6_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 222 | 72.1% | 0.5790 | 0.1961 | 9.8% |
| log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 235 | 76.6% | 0.5437 | 0.1797 | 16.8% |
| log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 220 | 76.8% | 0.5394 | 0.1778 | 16.5% |
| log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 207 | 77.8% | 0.5314 | 0.1741 | 17.1% |
| log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 199 | 77.4% | 0.5317 | 0.1744 | 12.9% |
| log_allmarketctx_c1p5_temp1p8_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 188 | 78.2% | 0.5244 | 0.1710 | 14.1% |
| log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 240 | 76.7% | 0.5458 | 0.1806 | 17.9% |
| log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 224 | 77.2% | 0.5395 | 0.1777 | 18.1% |
| log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 217 | 77.4% | 0.5370 | 0.1765 | 18.2% |
| log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 203 | 76.8% | 0.5372 | 0.1769 | 12.9% |
| log_allmarketctx_c1p5_temp1p8_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 188 | 78.2% | 0.5259 | 0.1716 | 14.2% |
| log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 246 | 75.6% | 0.5538 | 0.1843 | 17.5% |
| log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 231 | 76.2% | 0.5482 | 0.1818 | 17.0% |
| log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 221 | 76.0% | 0.5470 | 0.1813 | 16.2% |
| log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 206 | 76.7% | 0.5402 | 0.1782 | 14.2% |
| log_allmarketctx_c1p5_temp1p8_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 197 | 77.2% | 0.5356 | 0.1761 | 14.3% |
| log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 254 | 73.6% | 0.5675 | 0.1908 | 15.6% |
| log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 240 | 75.0% | 0.5585 | 0.1866 | 16.4% |
| log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 227 | 74.9% | 0.5570 | 0.1859 | 13.4% |
| log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 215 | 74.9% | 0.5550 | 0.1851 | 12.2% |
| log_allmarketctx_c1p5_temp1p8_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 199 | 75.4% | 0.5494 | 0.1826 | 12.7% |
| log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 257 | 73.5% | 0.5731 | 0.1933 | 15.5% |
| log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 248 | 73.0% | 0.5743 | 0.1939 | 14.6% |
| log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 231 | 72.7% | 0.5732 | 0.1936 | 10.5% |
| log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 217 | 73.7% | 0.5654 | 0.1899 | 12.1% |
| log_allmarketctx_c1p5_temp1p8_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 205 | 75.1% | 0.5553 | 0.1852 | 14.1% |
| log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 229 | 76.9% | 0.5420 | 0.1789 | 16.7% |
| log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 209 | 77.5% | 0.5339 | 0.1752 | 16.7% |
| log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 203 | 77.3% | 0.5333 | 0.1750 | 12.8% |
| log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 193 | 78.2% | 0.5259 | 0.1716 | 14.1% |
| log_allmarketctx_c1p5_temp2p0_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 179 | 78.8% | 0.5194 | 0.1687 | 14.4% |
| log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 230 | 77.4% | 0.5408 | 0.1782 | 18.4% |
| log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 220 | 77.3% | 0.5389 | 0.1775 | 18.0% |
| log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 206 | 77.7% | 0.5337 | 0.1751 | 14.2% |
| log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 191 | 77.5% | 0.5311 | 0.1741 | 13.1% |
| log_allmarketctx_c1p5_temp2p0_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 185 | 78.4% | 0.5245 | 0.1710 | 14.5% |
| log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 234 | 76.5% | 0.5476 | 0.1814 | 17.7% |
| log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 223 | 76.2% | 0.5463 | 0.1810 | 16.4% |
| log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 212 | 76.4% | 0.5430 | 0.1795 | 13.7% |
| log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 198 | 76.8% | 0.5381 | 0.1773 | 13.8% |
| log_allmarketctx_c1p5_temp2p0_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 189 | 78.3% | 0.5272 | 0.1722 | 15.6% |
| log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 240 | 75.4% | 0.5562 | 0.1855 | 17.1% |
| log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 231 | 75.8% | 0.5529 | 0.1840 | 17.4% |
| log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 215 | 74.9% | 0.5542 | 0.1848 | 11.7% |
| log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 202 | 75.7% | 0.5470 | 0.1815 | 12.9% |
| log_allmarketctx_c1p5_temp2p0_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 192 | 76.0% | 0.5433 | 0.1798 | 13.2% |
| log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 249 | 73.5% | 0.5704 | 0.1922 | 15.3% |
| log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 237 | 73.0% | 0.5707 | 0.1925 | 13.5% |
| log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 218 | 74.8% | 0.5585 | 0.1867 | 13.4% |
| log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 207 | 75.4% | 0.5531 | 0.1842 | 14.3% |
| log_allmarketctx_c1p5_temp2p0_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 193 | 74.1% | 0.5583 | 0.1870 | 11.2% |
| log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 216 | 77.8% | 0.5353 | 0.1757 | 17.2% |
| log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 206 | 77.7% | 0.5331 | 0.1748 | 16.8% |
| log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 199 | 78.4% | 0.5275 | 0.1722 | 14.3% |
| log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 190 | 77.9% | 0.5280 | 0.1726 | 13.2% |
| log_allmarketctx_c1p5_temp2p2_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 178 | 78.7% | 0.5207 | 0.1692 | 12.1% |
| log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 223 | 77.1% | 0.5412 | 0.1785 | 17.7% |
| log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 210 | 77.1% | 0.5380 | 0.1771 | 16.5% |
| log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 200 | 77.0% | 0.5365 | 0.1765 | 12.7% |
| log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 186 | 78.5% | 0.5248 | 0.1710 | 14.6% |
| log_allmarketctx_c1p5_temp2p2_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 179 | 78.8% | 0.5215 | 0.1695 | 12.7% |
| log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 225 | 76.4% | 0.5462 | 0.1808 | 16.9% |
| log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 217 | 76.5% | 0.5441 | 0.1799 | 13.8% |
| log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 203 | 76.8% | 0.5393 | 0.1778 | 13.8% |
| log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 190 | 78.4% | 0.5275 | 0.1722 | 15.7% |
| log_allmarketctx_c1p5_temp2p2_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 179 | 78.8% | 0.5229 | 0.1702 | 13.6% |
| log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 232 | 75.9% | 0.5528 | 0.1839 | 17.5% |
| log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 219 | 74.9% | 0.5547 | 0.1850 | 11.6% |
| log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 207 | 75.8% | 0.5473 | 0.1816 | 12.9% |
| log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 193 | 76.7% | 0.5396 | 0.1780 | 13.9% |
| log_allmarketctx_c1p5_temp2p2_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 180 | 77.2% | 0.5337 | 0.1754 | 12.7% |
| log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 239 | 74.1% | 0.5652 | 0.1898 | 15.0% |
| log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 221 | 74.7% | 0.5591 | 0.1870 | 13.0% |
| log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 212 | 75.0% | 0.5556 | 0.1855 | 13.5% |
| log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 197 | 74.6% | 0.5549 | 0.1853 | 11.6% |
| log_allmarketctx_c1p5_temp2p2_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 181 | 75.1% | 0.5488 | 0.1826 | 10.4% |
| log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 211 | 77.7% | 0.5355 | 0.1758 | 16.7% |
| log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 202 | 77.7% | 0.5331 | 0.1747 | 13.4% |
| log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 191 | 78.0% | 0.5289 | 0.1728 | 13.4% |
| log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 181 | 78.5% | 0.5240 | 0.1706 | 13.9% |
| log_allmarketctx_c1p5_temp2p5_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 169 | 79.9% | 0.5124 | 0.1652 | 13.6% |
| log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 210 | 77.6% | 0.5371 | 0.1765 | 17.2% |
| log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 203 | 77.3% | 0.5367 | 0.1764 | 12.8% |
| log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 192 | 78.1% | 0.5299 | 0.1732 | 13.9% |
| log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 181 | 78.5% | 0.5253 | 0.1712 | 14.1% |
| log_allmarketctx_c1p5_temp2p5_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 168 | 79.8% | 0.5143 | 0.1661 | 13.4% |
| log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 219 | 77.2% | 0.5427 | 0.1791 | 17.8% |
| log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 206 | 77.2% | 0.5395 | 0.1777 | 13.9% |
| log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 189 | 78.3% | 0.5295 | 0.1731 | 15.4% |
| log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 181 | 78.5% | 0.5268 | 0.1719 | 12.5% |
| log_allmarketctx_c1p5_temp2p5_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 166 | 78.9% | 0.5206 | 0.1691 | 12.9% |
| log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 222 | 75.7% | 0.5522 | 0.1836 | 15.6% |
| log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 207 | 75.8% | 0.5480 | 0.1818 | 12.7% |
| log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 194 | 77.3% | 0.5373 | 0.1768 | 14.5% |
| log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 182 | 78.0% | 0.5307 | 0.1737 | 13.6% |
| log_allmarketctx_c1p5_temp2p5_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 167 | 78.4% | 0.5247 | 0.1711 | 14.4% |
| log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 222 | 75.2% | 0.5569 | 0.1859 | 13.3% |
| log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 211 | 75.4% | 0.5539 | 0.1846 | 12.3% |
| log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 195 | 75.9% | 0.5475 | 0.1817 | 13.2% |
| log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 182 | 75.3% | 0.5481 | 0.1822 | 10.5% |
| log_allmarketctx_c1p5_temp2p5_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 168 | 77.4% | 0.5325 | 0.1748 | 13.4% |
| log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 246 | 76.0% | 0.5494 | 0.1823 | 16.7% |
| log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 232 | 76.3% | 0.5451 | 0.1804 | 16.4% |
| log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 220 | 76.8% | 0.5400 | 0.1780 | 16.8% |
| log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 209 | 77.5% | 0.5340 | 0.1752 | 16.8% |
| log_allmarketctx_c2p0_temp1p6_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 196 | 76.5% | 0.5372 | 0.1770 | 11.8% |
| log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 253 | 75.1% | 0.5567 | 0.1857 | 17.3% |
| log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 237 | 76.4% | 0.5476 | 0.1814 | 18.6% |
| log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 225 | 76.4% | 0.5448 | 0.1802 | 16.9% |
| log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 218 | 76.6% | 0.5428 | 0.1792 | 17.0% |
| log_allmarketctx_c2p0_temp1p6_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 204 | 76.5% | 0.5411 | 0.1786 | 16.5% |
| log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 260 | 73.5% | 0.5684 | 0.1911 | 15.4% |
| log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 248 | 75.0% | 0.5590 | 0.1866 | 17.7% |
| log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 236 | 75.8% | 0.5528 | 0.1837 | 18.6% |
| log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 218 | 75.2% | 0.5533 | 0.1842 | 15.3% |
| log_allmarketctx_c2p0_temp1p6_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 211 | 75.4% | 0.5515 | 0.1834 | 15.6% |
| log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 265 | 72.5% | 0.5785 | 0.1957 | 14.3% |
| log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 255 | 73.3% | 0.5729 | 0.1931 | 15.4% |
| log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 244 | 73.4% | 0.5714 | 0.1924 | 15.1% |
| log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 226 | 74.3% | 0.5634 | 0.1887 | 16.9% |
| log_allmarketctx_c2p0_temp1p6_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 215 | 74.4% | 0.5615 | 0.1879 | 15.9% |
| log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 268 | 71.6% | 0.5888 | 0.2003 | 13.0% |
| log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 259 | 72.2% | 0.5852 | 0.1986 | 13.6% |
| log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 248 | 71.8% | 0.5863 | 0.1992 | 13.4% |
| log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 232 | 72.0% | 0.5836 | 0.1980 | 14.2% |
| log_allmarketctx_c2p0_temp1p6_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 225 | 72.0% | 0.5829 | 0.1977 | 13.7% |
| log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 237 | 75.9% | 0.5481 | 0.1818 | 15.8% |
| log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 225 | 76.4% | 0.5432 | 0.1795 | 16.3% |
| log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 209 | 77.5% | 0.5342 | 0.1754 | 16.8% |
| log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 202 | 76.7% | 0.5371 | 0.1769 | 15.4% |
| log_allmarketctx_c2p0_temp1p8_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 187 | 78.6% | 0.5226 | 0.1701 | 14.7% |
| log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 243 | 75.7% | 0.5519 | 0.1835 | 16.4% |
| log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 226 | 77.0% | 0.5422 | 0.1789 | 17.7% |
| log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 219 | 76.7% | 0.5422 | 0.1790 | 17.1% |
| log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 207 | 76.3% | 0.5421 | 0.1791 | 15.9% |
| log_allmarketctx_c2p0_temp1p8_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 191 | 78.5% | 0.5255 | 0.1713 | 15.5% |
| log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 251 | 74.5% | 0.5612 | 0.1878 | 17.0% |
| log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 235 | 76.2% | 0.5505 | 0.1828 | 19.0% |
| log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 223 | 75.8% | 0.5502 | 0.1827 | 15.9% |
| log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 212 | 75.5% | 0.5498 | 0.1827 | 15.6% |
| log_allmarketctx_c2p0_temp1p8_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 198 | 76.3% | 0.5427 | 0.1794 | 13.4% |
| log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 256 | 73.4% | 0.5707 | 0.1922 | 15.6% |
| log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 244 | 74.2% | 0.5653 | 0.1897 | 16.2% |
| log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 228 | 74.6% | 0.5608 | 0.1876 | 17.0% |
| log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 216 | 75.0% | 0.5564 | 0.1857 | 16.3% |
| log_allmarketctx_c2p0_temp1p8_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 204 | 75.0% | 0.5545 | 0.1849 | 12.9% |
| log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 260 | 73.1% | 0.5782 | 0.1956 | 15.1% |
| log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 249 | 72.7% | 0.5785 | 0.1958 | 14.6% |
| log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 234 | 72.6% | 0.5768 | 0.1951 | 14.8% |
| log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 224 | 72.8% | 0.5747 | 0.1942 | 14.9% |
| log_allmarketctx_c2p0_temp1p8_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 209 | 73.2% | 0.5703 | 0.1922 | 11.1% |
| log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 233 | 76.8% | 0.5438 | 0.1797 | 17.1% |
| log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 211 | 77.3% | 0.5365 | 0.1764 | 16.5% |
| log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 206 | 77.2% | 0.5356 | 0.1761 | 15.9% |
| log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 193 | 78.2% | 0.5267 | 0.1720 | 14.1% |
| log_allmarketctx_c2p0_temp2p0_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 183 | 78.1% | 0.5250 | 0.1713 | 13.7% |
| log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 233 | 76.4% | 0.5469 | 0.1811 | 17.0% |
| log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 220 | 76.8% | 0.5421 | 0.1789 | 17.3% |
| log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 213 | 77.0% | 0.5397 | 0.1779 | 17.2% |
| log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 193 | 77.7% | 0.5312 | 0.1740 | 14.0% |
| log_allmarketctx_c2p0_temp2p0_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 184 | 78.3% | 0.5260 | 0.1717 | 14.3% |
| log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 239 | 76.2% | 0.5515 | 0.1832 | 19.2% |
| log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 225 | 76.0% | 0.5492 | 0.1823 | 16.1% |
| log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 215 | 75.8% | 0.5481 | 0.1819 | 16.0% |
| log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 201 | 76.1% | 0.5437 | 0.1799 | 13.0% |
| log_allmarketctx_c2p0_temp2p0_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 190 | 78.4% | 0.5277 | 0.1723 | 16.4% |
| log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 248 | 74.2% | 0.5650 | 0.1896 | 16.4% |
| log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 234 | 74.8% | 0.5598 | 0.1872 | 16.8% |
| log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 218 | 75.2% | 0.5547 | 0.1849 | 16.5% |
| log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 206 | 75.2% | 0.5524 | 0.1839 | 12.3% |
| log_allmarketctx_c2p0_temp2p0_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 192 | 76.0% | 0.5449 | 0.1805 | 13.5% |
| log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 255 | 73.3% | 0.5745 | 0.1940 | 15.4% |
| log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 238 | 72.7% | 0.5749 | 0.1944 | 14.2% |
| log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 224 | 73.7% | 0.5677 | 0.1910 | 15.6% |
| log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 210 | 73.8% | 0.5647 | 0.1897 | 11.8% |
| log_allmarketctx_c2p0_temp2p0_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 199 | 74.4% | 0.5597 | 0.1874 | 12.9% |
| log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 222 | 77.0% | 0.5410 | 0.1784 | 16.5% |
| log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 208 | 76.9% | 0.5380 | 0.1771 | 15.7% |
| log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 200 | 78.0% | 0.5305 | 0.1736 | 17.1% |
| log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 189 | 77.8% | 0.5291 | 0.1731 | 13.1% |
| log_allmarketctx_c2p0_temp2p2_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 178 | 78.7% | 0.5213 | 0.1695 | 12.1% |
| log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 227 | 76.7% | 0.5450 | 0.1803 | 17.1% |
| log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 215 | 77.2% | 0.5396 | 0.1778 | 17.7% |
| log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 202 | 76.7% | 0.5392 | 0.1778 | 15.9% |
| log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 186 | 78.5% | 0.5257 | 0.1714 | 14.6% |
| log_allmarketctx_c2p0_temp2p2_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 181 | 77.9% | 0.5281 | 0.1727 | 11.5% |
| log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 228 | 76.3% | 0.5487 | 0.1820 | 16.7% |
| log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 220 | 75.9% | 0.5488 | 0.1821 | 15.9% |
| log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 205 | 76.1% | 0.5447 | 0.1803 | 16.1% |
| log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 192 | 78.6% | 0.5276 | 0.1722 | 16.5% |
| log_allmarketctx_c2p0_temp2p2_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 183 | 78.1% | 0.5286 | 0.1728 | 13.4% |
| log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 237 | 75.1% | 0.5587 | 0.1867 | 17.4% |
| log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 223 | 75.3% | 0.5549 | 0.1850 | 16.5% |
| log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 211 | 74.9% | 0.5548 | 0.1851 | 11.6% |
| log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 197 | 76.1% | 0.5450 | 0.1805 | 13.3% |
| log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 185 | 75.7% | 0.5456 | 0.1810 | 10.8% |
| log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 244 | 73.4% | 0.5715 | 0.1927 | 15.1% |
| log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 224 | 74.1% | 0.5644 | 0.1895 | 16.3% |
| log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 210 | 73.8% | 0.5635 | 0.1892 | 11.8% |
| log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 201 | 74.6% | 0.5576 | 0.1864 | 13.1% |
| log_allmarketctx_c2p0_temp2p2_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 187 | 74.9% | 0.5537 | 0.1847 | 12.3% |
| log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 213 | 77.0% | 0.5400 | 0.1779 | 15.7% |
| log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 203 | 77.8% | 0.5333 | 0.1748 | 16.8% |
| log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 191 | 78.0% | 0.5295 | 0.1731 | 13.4% |
| log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 181 | 78.5% | 0.5244 | 0.1709 | 13.9% |
| log_allmarketctx_c2p0_temp2p5_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 170 | 79.4% | 0.5159 | 0.1669 | 12.9% |
| log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 215 | 77.2% | 0.5409 | 0.1783 | 17.5% |
| log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 207 | 77.3% | 0.5386 | 0.1773 | 16.5% |
| log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 191 | 78.0% | 0.5309 | 0.1738 | 13.8% |
| log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 183 | 78.1% | 0.5283 | 0.1726 | 13.8% |
| log_allmarketctx_c2p0_temp2p5_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 168 | 79.8% | 0.5147 | 0.1663 | 13.4% |
| log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 222 | 76.1% | 0.5490 | 0.1821 | 16.2% |
| log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 210 | 76.7% | 0.5438 | 0.1797 | 16.7% |
| log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 192 | 78.6% | 0.5292 | 0.1728 | 16.3% |
| log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 186 | 78.5% | 0.5285 | 0.1726 | 15.7% |
| log_allmarketctx_c2p0_temp2p5_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 170 | 78.2% | 0.5263 | 0.1718 | 12.1% |
| log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 225 | 75.6% | 0.5548 | 0.1848 | 16.0% |
| log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 212 | 75.5% | 0.5522 | 0.1837 | 15.5% |
| log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 196 | 76.5% | 0.5431 | 0.1795 | 13.6% |
| log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 187 | 77.0% | 0.5386 | 0.1775 | 12.4% |
| log_allmarketctx_c2p0_temp2p5_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 169 | 77.5% | 0.5316 | 0.1744 | 13.1% |
| log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 223 | 74.4% | 0.5623 | 0.1884 | 15.2% |
| log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 213 | 74.6% | 0.5594 | 0.1871 | 12.6% |
| log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 200 | 74.5% | 0.5577 | 0.1865 | 11.6% |
| log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 185 | 75.1% | 0.5513 | 0.1836 | 10.3% |
| log_allmarketctx_c2p0_temp2p5_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 174 | 75.3% | 0.5480 | 0.1822 | 11.0% |
| log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 247 | 75.7% | 0.5519 | 0.1835 | 17.4% |
| log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 233 | 76.0% | 0.5478 | 0.1816 | 15.9% |
| log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 222 | 76.6% | 0.5424 | 0.1791 | 16.5% |
| log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 213 | 77.5% | 0.5357 | 0.1760 | 17.3% |
| log_allmarketctx_c2p5_temp1p6_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 198 | 76.3% | 0.5401 | 0.1783 | 14.8% |
| log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 254 | 74.8% | 0.5594 | 0.1869 | 17.5% |
| log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 241 | 75.5% | 0.5536 | 0.1842 | 17.3% |
| log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 228 | 76.3% | 0.5471 | 0.1812 | 17.9% |
| log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 218 | 76.6% | 0.5437 | 0.1796 | 17.1% |
| log_allmarketctx_c2p5_temp1p6_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 205 | 76.6% | 0.5415 | 0.1787 | 16.7% |
| log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 264 | 72.7% | 0.5740 | 0.1937 | 14.5% |
| log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 254 | 73.6% | 0.5681 | 0.1910 | 15.9% |
| log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 238 | 75.6% | 0.5556 | 0.1850 | 18.1% |
| log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 220 | 75.0% | 0.5562 | 0.1855 | 16.6% |
| log_allmarketctx_c2p5_temp1p6_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 210 | 75.2% | 0.5534 | 0.1842 | 15.4% |
| log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 269 | 71.7% | 0.5843 | 0.1984 | 13.2% |
| log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 258 | 72.5% | 0.5793 | 0.1961 | 14.1% |
| log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 246 | 73.2% | 0.5744 | 0.1937 | 15.2% |
| log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 230 | 73.9% | 0.5682 | 0.1908 | 16.5% |
| log_allmarketctx_c2p5_temp1p6_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 216 | 73.6% | 0.5683 | 0.1910 | 15.8% |
| log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 273 | 71.1% | 0.5946 | 0.2029 | 12.2% |
| log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 262 | 71.4% | 0.5921 | 0.2018 | 12.5% |
| log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 251 | 71.3% | 0.5914 | 0.2015 | 12.6% |
| log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 236 | 71.2% | 0.5909 | 0.2013 | 12.8% |
| log_allmarketctx_c2p5_temp1p6_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 226 | 71.7% | 0.5871 | 0.1995 | 13.6% |
| log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 239 | 76.2% | 0.5484 | 0.1819 | 16.6% |
| log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 225 | 76.4% | 0.5439 | 0.1798 | 16.2% |
| log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 213 | 77.5% | 0.5359 | 0.1761 | 17.3% |
| log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 201 | 76.6% | 0.5383 | 0.1774 | 15.2% |
| log_allmarketctx_c2p5_temp1p8_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 189 | 77.8% | 0.5289 | 0.1730 | 17.1% |
| log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 245 | 75.1% | 0.5561 | 0.1855 | 16.6% |
| log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 232 | 75.9% | 0.5499 | 0.1826 | 17.2% |
| log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 220 | 76.8% | 0.5426 | 0.1792 | 17.3% |
| log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 209 | 76.6% | 0.5420 | 0.1790 | 17.0% |
| log_allmarketctx_c2p5_temp1p8_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 194 | 78.4% | 0.5281 | 0.1725 | 18.9% |
| log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 255 | 73.3% | 0.5685 | 0.1913 | 15.1% |
| log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 238 | 75.6% | 0.5548 | 0.1848 | 18.1% |
| log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 224 | 75.9% | 0.5510 | 0.1830 | 17.6% |
| log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 212 | 75.0% | 0.5538 | 0.1845 | 14.9% |
| log_allmarketctx_c2p5_temp1p8_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 202 | 76.2% | 0.5447 | 0.1802 | 16.8% |
| log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 261 | 72.0% | 0.5795 | 0.1964 | 13.4% |
| log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 249 | 73.9% | 0.5691 | 0.1914 | 16.1% |
| log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 229 | 73.8% | 0.5666 | 0.1904 | 15.8% |
| log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 218 | 74.3% | 0.5621 | 0.1883 | 16.4% |
| log_allmarketctx_c2p5_temp1p8_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 207 | 74.9% | 0.5572 | 0.1860 | 16.6% |
| log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 264 | 72.0% | 0.5861 | 0.1992 | 13.4% |
| log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 254 | 72.0% | 0.5844 | 0.1985 | 13.8% |
| log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 237 | 72.2% | 0.5818 | 0.1973 | 14.0% |
| log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 223 | 72.2% | 0.5799 | 0.1965 | 14.1% |
| log_allmarketctx_c2p5_temp1p8_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 212 | 73.6% | 0.5703 | 0.1920 | 16.1% |
| log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 233 | 76.0% | 0.5483 | 0.1819 | 15.7% |
| log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 217 | 77.0% | 0.5399 | 0.1780 | 16.5% |
| log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 206 | 77.2% | 0.5363 | 0.1764 | 15.9% |
| log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 195 | 77.9% | 0.5295 | 0.1732 | 17.2% |
| log_allmarketctx_c2p5_temp2p0_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 183 | 78.1% | 0.5257 | 0.1716 | 13.7% |
| log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 237 | 75.5% | 0.5526 | 0.1838 | 16.8% |
| log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 223 | 76.7% | 0.5441 | 0.1798 | 17.1% |
| log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 214 | 77.1% | 0.5401 | 0.1780 | 17.7% |
| log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 197 | 77.7% | 0.5331 | 0.1749 | 17.8% |
| log_allmarketctx_c2p5_temp2p0_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 184 | 78.3% | 0.5269 | 0.1720 | 14.3% |
| log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 244 | 74.6% | 0.5606 | 0.1875 | 16.7% |
| log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 227 | 75.8% | 0.5518 | 0.1835 | 17.3% |
| log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 217 | 75.1% | 0.5533 | 0.1843 | 14.9% |
| log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 205 | 76.1% | 0.5456 | 0.1807 | 16.4% |
| log_allmarketctx_c2p5_temp2p0_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 193 | 77.2% | 0.5368 | 0.1766 | 14.5% |
| log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 250 | 74.4% | 0.5658 | 0.1899 | 17.0% |
| log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 235 | 74.5% | 0.5630 | 0.1887 | 16.3% |
| log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 218 | 74.8% | 0.5585 | 0.1866 | 17.1% |
| log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 211 | 75.4% | 0.5539 | 0.1845 | 16.9% |
| log_allmarketctx_c2p5_temp2p0_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 194 | 75.3% | 0.5517 | 0.1836 | 12.6% |
| log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 258 | 72.5% | 0.5806 | 0.1968 | 14.1% |
| log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 239 | 72.4% | 0.5784 | 0.1959 | 14.2% |
| log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 224 | 73.2% | 0.5720 | 0.1929 | 15.4% |
| log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 213 | 73.7% | 0.5676 | 0.1909 | 16.2% |
| log_allmarketctx_c2p5_temp2p0_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 199 | 74.4% | 0.5616 | 0.1881 | 13.1% |
| log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 224 | 76.8% | 0.5431 | 0.1794 | 16.6% |
| log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 212 | 76.9% | 0.5398 | 0.1779 | 16.0% |
| log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 201 | 77.6% | 0.5334 | 0.1750 | 16.6% |
| log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 190 | 77.9% | 0.5293 | 0.1732 | 16.7% |
| log_allmarketctx_c2p5_temp2p2_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 180 | 78.3% | 0.5243 | 0.1709 | 11.8% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 227 | 76.2% | 0.5477 | 0.1815 | 16.4% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 216 | 77.3% | 0.5399 | 0.1779 | 17.9% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 204 | 77.0% | 0.5391 | 0.1777 | 17.1% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 189 | 78.3% | 0.5282 | 0.1726 | 18.0% |
| log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 181 | 77.9% | 0.5289 | 0.1730 | 11.5% |
| log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 233 | 75.5% | 0.5542 | 0.1846 | 17.1% |
| log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 223 | 75.8% | 0.5510 | 0.1831 | 15.7% |
| log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 209 | 76.1% | 0.5465 | 0.1811 | 16.4% |
| log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 195 | 77.4% | 0.5360 | 0.1762 | 18.3% |
| log_allmarketctx_c2p5_temp2p2_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 185 | 78.4% | 0.5283 | 0.1726 | 14.0% |
| log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 239 | 74.9% | 0.5613 | 0.1878 | 16.9% |
| log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 222 | 74.8% | 0.5587 | 0.1868 | 16.9% |
| log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 212 | 75.0% | 0.5556 | 0.1854 | 15.5% |
| log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 200 | 76.0% | 0.5478 | 0.1817 | 13.1% |
| log_allmarketctx_c2p5_temp2p2_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 187 | 75.4% | 0.5489 | 0.1825 | 10.5% |
| log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 248 | 73.4% | 0.5738 | 0.1937 | 15.3% |
| log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 227 | 73.1% | 0.5714 | 0.1927 | 15.0% |
| log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 215 | 73.5% | 0.5678 | 0.1911 | 15.7% |
| log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 203 | 74.4% | 0.5609 | 0.1879 | 12.8% |
| log_allmarketctx_c2p5_temp2p2_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 189 | 74.6% | 0.5573 | 0.1863 | 13.2% |
| log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 214 | 77.1% | 0.5403 | 0.1781 | 16.0% |
| log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 206 | 77.2% | 0.5378 | 0.1769 | 15.9% |
| log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 191 | 78.0% | 0.5300 | 0.1734 | 16.8% |
| log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 183 | 78.1% | 0.5273 | 0.1722 | 13.6% |
| log_allmarketctx_c2p5_temp2p5_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 171 | 78.9% | 0.5194 | 0.1686 | 12.3% |
| log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 220 | 76.8% | 0.5444 | 0.1799 | 17.1% |
| log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 209 | 77.5% | 0.5386 | 0.1772 | 17.6% |
| log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 194 | 77.8% | 0.5332 | 0.1748 | 17.0% |
| log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 183 | 78.1% | 0.5289 | 0.1729 | 13.8% |
| log_allmarketctx_c2p5_temp2p5_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 171 | 78.9% | 0.5211 | 0.1693 | 12.3% |
| log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 224 | 75.9% | 0.5512 | 0.1831 | 15.9% |
| log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 213 | 76.5% | 0.5458 | 0.1806 | 16.8% |
| log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 196 | 78.1% | 0.5339 | 0.1750 | 19.0% |
| log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 186 | 78.5% | 0.5291 | 0.1729 | 16.1% |
| log_allmarketctx_c2p5_temp2p5_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 173 | 77.5% | 0.5325 | 0.1747 | 11.8% |
| log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 229 | 75.5% | 0.5566 | 0.1856 | 17.6% |
| log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 213 | 75.1% | 0.5552 | 0.1851 | 15.0% |
| log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 199 | 76.4% | 0.5457 | 0.1807 | 16.8% |
| log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 189 | 76.2% | 0.5447 | 0.1803 | 11.4% |
| log_allmarketctx_c2p5_temp2p5_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 173 | 76.9% | 0.5372 | 0.1769 | 12.7% |
| log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 226 | 73.9% | 0.5667 | 0.1905 | 15.7% |
| log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 216 | 74.5% | 0.5618 | 0.1882 | 16.7% |
| log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 204 | 75.0% | 0.5572 | 0.1861 | 16.6% |
| log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 187 | 74.3% | 0.5578 | 0.1866 | 9.5% |
| log_allmarketctx_c2p5_temp2p5_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 177 | 74.6% | 0.5544 | 0.1851 | 9.8% |
| log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 249 | 75.1% | 0.5558 | 0.1853 | 16.5% |
| log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 233 | 76.0% | 0.5485 | 0.1819 | 16.9% |
| log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 224 | 75.9% | 0.5471 | 0.1814 | 15.4% |
| log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 214 | 77.1% | 0.5386 | 0.1773 | 16.7% |
| log_allmarketctx_c3p0_temp1p6_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 199 | 76.4% | 0.5402 | 0.1783 | 15.2% |
| log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 256 | 74.6% | 0.5618 | 0.1880 | 17.5% |
| log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 244 | 75.0% | 0.5577 | 0.1861 | 16.8% |
| log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 231 | 75.3% | 0.5537 | 0.1843 | 16.3% |
| log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 219 | 76.3% | 0.5466 | 0.1810 | 17.8% |
| log_allmarketctx_c3p0_temp1p6_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 205 | 76.6% | 0.5422 | 0.1790 | 16.7% |
| log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 265 | 72.8% | 0.5751 | 0.1942 | 14.8% |
| log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 256 | 73.0% | 0.5726 | 0.1930 | 15.0% |
| log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 243 | 74.9% | 0.5613 | 0.1876 | 17.5% |
| log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 221 | 74.7% | 0.5594 | 0.1869 | 16.9% |
| log_allmarketctx_c3p0_temp1p6_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 214 | 74.8% | 0.5578 | 0.1862 | 16.0% |
| log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 269 | 71.7% | 0.5861 | 0.1992 | 13.2% |
| log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 262 | 71.4% | 0.5870 | 0.1997 | 12.3% |
| log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 246 | 72.0% | 0.5824 | 0.1975 | 13.5% |
| log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 233 | 72.5% | 0.5778 | 0.1954 | 14.3% |
| log_allmarketctx_c3p0_temp1p6_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 219 | 73.5% | 0.5705 | 0.1919 | 15.9% |
| log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 273 | 71.1% | 0.5968 | 0.2038 | 12.2% |
| log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 263 | 71.1% | 0.5957 | 0.2034 | 12.2% |
| log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 255 | 71.0% | 0.5956 | 0.2033 | 12.2% |
| log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 237 | 70.9% | 0.5947 | 0.2030 | 12.3% |
| log_allmarketctx_c3p0_temp1p6_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 225 | 71.1% | 0.5923 | 0.2019 | 12.8% |
| log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 239 | 75.7% | 0.5510 | 0.1831 | 17.2% |
| log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 227 | 75.8% | 0.5483 | 0.1819 | 15.2% |
| log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 217 | 76.5% | 0.5425 | 0.1792 | 15.8% |
| log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 202 | 76.7% | 0.5384 | 0.1774 | 15.7% |
| log_allmarketctx_c3p0_temp1p8_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 190 | 77.9% | 0.5290 | 0.1730 | 17.3% |
| log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 247 | 74.9% | 0.5584 | 0.1865 | 16.7% |
| log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 232 | 75.4% | 0.5528 | 0.1840 | 16.5% |
| log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 224 | 76.3% | 0.5466 | 0.1810 | 17.8% |
| log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 209 | 76.6% | 0.5426 | 0.1793 | 17.0% |
| log_allmarketctx_c3p0_temp1p8_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 194 | 77.8% | 0.5320 | 0.1743 | 18.3% |
| log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 258 | 72.9% | 0.5724 | 0.1931 | 14.7% |
| log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 245 | 74.3% | 0.5637 | 0.1890 | 16.5% |
| log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 227 | 75.3% | 0.5554 | 0.1851 | 17.4% |
| log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 213 | 75.1% | 0.5541 | 0.1846 | 16.6% |
| log_allmarketctx_c3p0_temp1p8_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 203 | 75.9% | 0.5480 | 0.1818 | 16.2% |
| log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 263 | 71.5% | 0.5839 | 0.1984 | 12.5% |
| log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 254 | 72.8% | 0.5764 | 0.1948 | 14.5% |
| log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 232 | 73.3% | 0.5711 | 0.1924 | 15.2% |
| log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 220 | 74.1% | 0.5649 | 0.1895 | 16.4% |
| log_allmarketctx_c3p0_temp1p8_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 210 | 74.3% | 0.5624 | 0.1884 | 17.0% |
| log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 269 | 71.0% | 0.5930 | 0.2025 | 11.9% |
| log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 255 | 71.0% | 0.5917 | 0.2019 | 12.2% |
| log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 240 | 71.2% | 0.5887 | 0.2005 | 12.7% |
| log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 225 | 71.6% | 0.5854 | 0.1990 | 13.1% |
| log_allmarketctx_c3p0_temp1p8_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 215 | 73.0% | 0.5756 | 0.1944 | 15.6% |
| log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 233 | 76.0% | 0.5490 | 0.1822 | 15.7% |
| log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 220 | 76.4% | 0.5441 | 0.1800 | 15.7% |
| log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 208 | 77.4% | 0.5361 | 0.1762 | 16.7% |
| log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 195 | 77.9% | 0.5301 | 0.1735 | 17.2% |
| log_allmarketctx_c3p0_temp2p0_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 185 | 77.8% | 0.5286 | 0.1729 | 16.8% |
| log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 238 | 74.8% | 0.5569 | 0.1859 | 15.6% |
| log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 228 | 75.4% | 0.5519 | 0.1836 | 16.4% |
| log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 214 | 77.1% | 0.5407 | 0.1783 | 17.7% |
| log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 200 | 76.5% | 0.5411 | 0.1787 | 16.0% |
| log_allmarketctx_c3p0_temp2p0_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 187 | 78.1% | 0.5293 | 0.1731 | 18.1% |
| log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 244 | 74.6% | 0.5616 | 0.1880 | 16.7% |
| log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 231 | 75.3% | 0.5556 | 0.1852 | 17.3% |
| log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 217 | 75.1% | 0.5542 | 0.1847 | 16.3% |
| log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 205 | 75.6% | 0.5492 | 0.1824 | 15.8% |
| log_allmarketctx_c3p0_temp2p0_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 193 | 77.2% | 0.5377 | 0.1770 | 17.9% |
| log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 256 | 72.7% | 0.5760 | 0.1948 | 14.3% |
| log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 235 | 74.0% | 0.5663 | 0.1902 | 16.1% |
| log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 220 | 74.1% | 0.5635 | 0.1890 | 16.4% |
| log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 213 | 75.1% | 0.5567 | 0.1858 | 17.7% |
| log_allmarketctx_c3p0_temp2p0_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 198 | 75.3% | 0.5535 | 0.1844 | 16.0% |
| log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 262 | 71.4% | 0.5879 | 0.2003 | 12.3% |
| log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 242 | 71.9% | 0.5828 | 0.1979 | 13.4% |
| log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 225 | 72.4% | 0.5776 | 0.1955 | 14.2% |
| log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 214 | 73.8% | 0.5684 | 0.1911 | 16.8% |
| log_allmarketctx_c3p0_temp2p0_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 203 | 74.4% | 0.5635 | 0.1889 | 18.1% |
| log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 225 | 76.4% | 0.5454 | 0.1805 | 16.0% |
| log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 214 | 77.1% | 0.5397 | 0.1778 | 16.4% |
| log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 201 | 77.6% | 0.5339 | 0.1752 | 16.6% |
| log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 191 | 77.5% | 0.5324 | 0.1746 | 16.1% |
| log_allmarketctx_c3p0_temp2p2_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 180 | 77.8% | 0.5282 | 0.1728 | 11.1% |
| log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 232 | 75.4% | 0.5530 | 0.1840 | 16.4% |
| log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 219 | 76.7% | 0.5441 | 0.1798 | 17.0% |
| log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 207 | 76.8% | 0.5411 | 0.1786 | 16.9% |
| log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 190 | 78.4% | 0.5283 | 0.1726 | 18.5% |
| log_allmarketctx_c3p0_temp2p2_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 180 | 77.8% | 0.5301 | 0.1736 | 11.4% |
| log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 236 | 75.0% | 0.5581 | 0.1864 | 16.9% |
| log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 224 | 75.9% | 0.5514 | 0.1833 | 17.1% |
| log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 211 | 75.4% | 0.5515 | 0.1835 | 15.3% |
| log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 195 | 77.4% | 0.5368 | 0.1765 | 18.3% |
| log_allmarketctx_c3p0_temp2p2_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 186 | 77.4% | 0.5352 | 0.1759 | 12.8% |
| log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 243 | 74.1% | 0.5668 | 0.1904 | 16.0% |
| log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 224 | 74.1% | 0.5633 | 0.1889 | 15.8% |
| log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 216 | 74.5% | 0.5598 | 0.1873 | 16.7% |
| log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 202 | 76.2% | 0.5478 | 0.1816 | 16.8% |
| log_allmarketctx_c3p0_temp2p2_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 189 | 75.1% | 0.5521 | 0.1839 | 10.3% |
| log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 250 | 72.4% | 0.5799 | 0.1966 | 13.9% |
| log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 228 | 72.8% | 0.5745 | 0.1941 | 14.5% |
| log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 218 | 73.9% | 0.5676 | 0.1909 | 16.3% |
| log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 205 | 74.6% | 0.5611 | 0.1879 | 17.7% |
| log_allmarketctx_c3p0_temp2p2_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 191 | 73.8% | 0.5640 | 0.1894 | 10.5% |
| log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.4 | 216 | 77.3% | 0.5403 | 0.1780 | 16.6% |
| log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.4 | 207 | 76.8% | 0.5404 | 0.1782 | 15.4% |
| log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.4 | 192 | 77.6% | 0.5328 | 0.1747 | 16.2% |
| log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.4 | 184 | 78.3% | 0.5272 | 0.1721 | 17.3% |
| log_allmarketctx_c3p0_temp2p5_blend40_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.4 | 171 | 78.9% | 0.5198 | 0.1687 | 12.3% |
| log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.45 | 222 | 76.6% | 0.5465 | 0.1809 | 16.8% |
| log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.45 | 210 | 77.1% | 0.5410 | 0.1784 | 17.2% |
| log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.45 | 196 | 78.1% | 0.5330 | 0.1746 | 17.7% |
| log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.45 | 183 | 78.1% | 0.5295 | 0.1731 | 13.8% |
| log_allmarketctx_c3p0_temp2p5_blend45_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.45 | 174 | 78.2% | 0.5271 | 0.1721 | 11.6% |
| log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.5 | 228 | 75.4% | 0.5549 | 0.1848 | 16.4% |
| log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.5 | 213 | 76.1% | 0.5488 | 0.1820 | 16.1% |
| log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.5 | 196 | 78.1% | 0.5345 | 0.1753 | 19.0% |
| log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.5 | 188 | 77.7% | 0.5349 | 0.1756 | 13.0% |
| log_allmarketctx_c3p0_temp2p5_blend50_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.5 | 174 | 77.6% | 0.5325 | 0.1747 | 12.4% |
| log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.55 | 231 | 75.3% | 0.5589 | 0.1867 | 17.3% |
| log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.55 | 216 | 75.0% | 0.5573 | 0.1861 | 16.6% |
| log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.55 | 202 | 76.2% | 0.5480 | 0.1817 | 16.8% |
| log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.55 | 189 | 75.7% | 0.5487 | 0.1822 | 10.6% |
| log_allmarketctx_c3p0_temp2p5_blend55_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.55 | 174 | 75.9% | 0.5445 | 0.1804 | 11.1% |
| log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p61 | logistic_regression | production_plus_all_research_market_context | 0.6 | 229 | 73.4% | 0.5708 | 0.1924 | 15.2% |
| log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p62 | logistic_regression | production_plus_all_research_market_context | 0.6 | 220 | 74.1% | 0.5658 | 0.1900 | 16.4% |
| log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p63 | logistic_regression | production_plus_all_research_market_context | 0.6 | 204 | 75.0% | 0.5584 | 0.1866 | 18.0% |
| log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p64 | logistic_regression | production_plus_all_research_market_context | 0.6 | 190 | 74.2% | 0.5604 | 0.1877 | 10.7% |
| log_allmarketctx_c3p0_temp2p5_blend60_min_confidence0p65 | logistic_regression | production_plus_all_research_market_context | 0.6 | 180 | 73.9% | 0.5605 | 0.1879 | 8.9% |

## Recommendation

- Status: `candidate_for_locked_evaluation`
- Reason: log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63 clears the configured discovery gate; evaluate on a locked future slice before activation.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
