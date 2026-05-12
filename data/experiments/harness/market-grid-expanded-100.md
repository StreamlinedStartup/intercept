# Market Experiment Harness

- Generated: `2026-05-12T06:40:39.171584+00:00`
- Config: `configs/experiments/market-grid-expanded-100.json`
- Value status: `research_only`
- Writes `model_versions`: `false`
- Model-eligible events: 40
- Model-eligible fights: 379

## Ranking

| Rank | Variant | ROI delta vs market | Log-loss delta | Brier delta | Clears gate | Rejection reasons |
|---:|---|---:|---:|---:|---|---|
| 1 | xgb_prod_blend_01_model_99_market | +0.0% | 0.0008 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 2 | xgb_avail_blend_01_model_99_market | +0.0% | 0.0008 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 3 | log_prod_blend_01_model_99_market | -1.1% | 0.0008 | 0.0003 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 4 | xgb_prod_blend_04_model_96_market | -1.1% | 0.0031 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 5 | xgb_avail_blend_04_model_96_market | -1.1% | 0.0033 | 0.0013 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 6 | xgb_prod_blend_07_model_93_market | -2.2% | 0.0056 | 0.0023 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 7 | xgb_avail_blend_07_model_93_market | -2.6% | 0.0059 | 0.0024 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 8 | xgb_prod_blend_10_model_90_market | -3.2% | 0.0082 | 0.0034 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 9 | log_prod_blend_13_model_87_market | -3.5% | 0.0126 | 0.0054 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 10 | log_prod_blend_04_model_96_market | -3.7% | 0.0034 | 0.0014 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 11 | xgb_avail_blend_10_model_90_market | -3.7% | 0.0086 | 0.0036 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 12 | xgb_prod_blend_19_model_81_market | -4.1% | 0.0167 | 0.0071 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 13 | xgb_avail_blend_19_model_81_market | -4.1% | 0.0174 | 0.0074 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 14 | log_prod_blend_10_model_90_market | -4.1% | 0.0093 | 0.0039 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 15 | log_prod_blend_07_model_93_market | -4.2% | 0.0063 | 0.0026 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 16 | xgb_prod_blend_13_model_87_market | -4.2% | 0.0109 | 0.0046 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 17 | xgb_avail_blend_13_model_87_market | -4.2% | 0.0114 | 0.0048 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 18 | xgb_prod_blend_16_model_84_market | -4.7% | 0.0137 | 0.0058 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 19 | xgb_avail_blend_16_model_84_market | -4.7% | 0.0144 | 0.0061 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 20 | log_prod_blend_16_model_84_market | -4.7% | 0.0162 | 0.0070 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 21 | xgb_avail_blend_22_model_78_market | -5.1% | 0.0206 | 0.0088 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 22 | xgb_prod_blend_22_model_78_market | -5.5% | 0.0197 | 0.0085 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 23 | log_prod_blend_22_model_78_market | -5.5% | 0.0240 | 0.0106 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 24 | log_prod_blend_19_model_81_market | -5.6% | 0.0199 | 0.0087 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 25 | xgb_avail_blend_25_model_75_market | -6.9% | 0.0239 | 0.0103 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 26 | xgb_avail_blend_28_model_72_market | -7.2% | 0.0273 | 0.0119 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 27 | xgb_avail_blend_31_model_69_market | -7.6% | 0.0309 | 0.0135 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 28 | xgb_avail_blend_34_model_66_market | -7.6% | 0.0345 | 0.0152 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 29 | xgb_prod_blend_31_model_69_market | -7.6% | 0.0297 | 0.0130 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 30 | xgb_prod_blend_25_model_75_market | -8.0% | 0.0230 | 0.0099 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 31 | xgb_prod_blend_28_model_72_market | -8.4% | 0.0263 | 0.0114 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 32 | log_prod_blend_25_model_75_market | -8.5% | 0.0282 | 0.0126 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 33 | xgb_prod_blend_34_model_66_market | -8.5% | 0.0333 | 0.0147 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 34 | xgb_prod_blend_37_model_63_market | -8.9% | 0.0370 | 0.0164 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 35 | log_prod_blend_28_model_72_market | -9.6% | 0.0328 | 0.0148 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 36 | xgb_avail_blend_37_model_63_market | -9.7% | 0.0383 | 0.0170 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 37 | xgb_prod_blend_40_model_60_market | -10.2% | 0.0408 | 0.0182 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 38 | xgb_prod_blend_55_model_45_market | -10.7% | 0.0618 | 0.0283 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 39 | xgb_prod_blend_43_model_57_market | -11.0% | 0.0447 | 0.0201 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 40 | xgb_avail_blend_49_model_51_market | -11.0% | 0.0547 | 0.0248 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 41 | xgb_prod_blend_46_model_54_market | -11.2% | 0.0488 | 0.0220 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 42 | xgb_prod_blend_61_model_39_market | -11.2% | 0.0712 | 0.0328 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 43 | xgb_avail_blend_43_model_57_market | -11.2% | 0.0463 | 0.0207 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 44 | xgb_prod_blend_52_model_48_market | -11.8% | 0.0573 | 0.0261 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 45 | xgb_prod_blend_58_model_42_market | -11.9% | 0.0664 | 0.0305 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 46 | xgb_avail_blend_52_model_48_market | -11.9% | 0.0591 | 0.0269 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 47 | xgb_avail_blend_46_model_54_market | -12.1% | 0.0504 | 0.0227 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 48 | xgb_avail_blend_40_model_60_market | -12.2% | 0.0422 | 0.0188 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 49 | xgb_prod_blend_49_model_51_market | -12.3% | 0.0530 | 0.0240 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 50 | log_prod_blend_34_model_66_market | -12.5% | 0.0426 | 0.0195 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 51 | log_prod_blend_31_model_69_market | -12.8% | 0.0375 | 0.0170 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 52 | xgb_avail_blend_55_model_45_market | -12.9% | 0.0637 | 0.0291 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 53 | xgb_avail_blend_61_model_39_market | -13.9% | 0.0732 | 0.0336 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 54 | log_prod_blend_37_model_63_market | -14.8% | 0.0480 | 0.0221 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 55 | xgb_avail_blend_58_model_42_market | -15.3% | 0.0684 | 0.0313 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 56 | xgb_prod_blend_64_model_36_market | -16.4% | 0.0761 | 0.0351 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 57 | xgb_prod_blend_67_model_33_market | -16.6% | 0.0812 | 0.0376 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 58 | xgb_avail_blend_70_model_30_market | -17.3% | 0.0886 | 0.0410 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 59 | xgb_avail_blend_64_model_36_market | -17.5% | 0.0782 | 0.0360 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 60 | log_prod_blend_40_model_60_market | -17.9% | 0.0536 | 0.0248 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 61 | xgb_avail_blend_67_model_33_market | -18.6% | 0.0833 | 0.0385 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 62 | log_prod_blend_43_model_57_market | -18.8% | 0.0595 | 0.0276 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 63 | xgb_avail_blend_73_model_27_market | -18.9% | 0.0941 | 0.0436 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 64 | xgb_prod_blend_70_model_30_market | -19.4% | 0.0864 | 0.0401 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 65 | log_prod_blend_52_model_48_market | -19.5% | 0.0794 | 0.0370 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 66 | xgb_prod_blend_73_model_27_market | -19.8% | 0.0918 | 0.0426 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 67 | log_prod_blend_46_model_54_market | -19.9% | 0.0658 | 0.0306 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 68 | xgb_avail_blend_79_model_21_market | -20.2% | 0.1055 | 0.0490 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 69 | log_prod_blend_58_model_42_market | -20.2% | 0.0944 | 0.0439 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 70 | xgb_avail_blend_76_model_24_market | -20.2% | 0.0997 | 0.0463 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 71 | log_prod_blend_61_model_39_market | -21.0% | 0.1026 | 0.0476 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 72 | log_prod_blend_49_model_51_market | -21.1% | 0.0724 | 0.0337 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 73 | xgb_avail_blend_91_model_09_market | -21.2% | 0.1309 | 0.0606 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 74 | log_prod_blend_55_model_45_market | -21.5% | 0.0867 | 0.0404 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 75 | xgb_prod_blend_76_model_24_market | -22.1% | 0.0974 | 0.0453 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 76 | xgb_avail_blend_88_model_12_market | -22.2% | 0.1242 | 0.0576 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 77 | xgb_avail_blend_82_model_18_market | -22.3% | 0.1115 | 0.0518 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 78 | xgb_prod_blend_79_model_21_market | -22.4% | 0.1032 | 0.0480 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 79 | xgb_avail_blend_97_model_03_market | -22.5% | 0.1450 | 0.0668 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 80 | xgb_avail_blend_94_model_06_market | -22.6% | 0.1378 | 0.0637 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 81 | xgb_prod_blend_82_model_18_market | -23.1% | 0.1091 | 0.0508 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 82 | log_prod_blend_64_model_36_market | -23.7% | 0.1113 | 0.0514 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 83 | xgb_avail_blend_85_model_15_market | -23.7% | 0.1177 | 0.0547 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 84 | xgb_avail_unblended | -23.9% | 0.1525 | 0.0701 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 85 | log_prod_blend_67_model_33_market | -24.2% | 0.1204 | 0.0553 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 86 | log_prod_blend_70_model_30_market | -26.0% | 0.1302 | 0.0594 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 87 | xgb_prod_blend_85_model_15_market | -26.1% | 0.1153 | 0.0536 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 88 | log_prod_blend_91_model_09_market | -26.8% | 0.2223 | 0.0919 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 89 | log_prod_blend_73_model_27_market | -26.9% | 0.1405 | 0.0637 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 90 | xgb_prod_blend_97_model_03_market | -26.9% | 0.1424 | 0.0657 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 91 | log_prod_blend_76_model_24_market | -27.0% | 0.1516 | 0.0680 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 92 | log_prod_blend_94_model_06_market | -27.0% | 0.2415 | 0.0971 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 93 | log_prod_blend_97_model_03_market | -27.0% | 0.2641 | 0.1024 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 94 | log_prod_blend_79_model_21_market | -27.2% | 0.1635 | 0.0725 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 95 | xgb_prod_unblended | -27.4% | 0.1500 | 0.0689 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 96 | log_prod_blend_82_model_18_market | -27.5% | 0.1763 | 0.0772 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 97 | xgb_prod_blend_91_model_09_market | -27.6% | 0.1283 | 0.0595 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 98 | log_prod_unblended | -27.7% | 0.2934 | 0.1079 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 99 | xgb_prod_blend_94_model_06_market | -28.1% | 0.1352 | 0.0626 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 100 | log_prod_blend_85_model_15_market | -28.1% | 0.1902 | 0.0819 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 101 | xgb_prod_blend_88_model_12_market | -28.2% | 0.1217 | 0.0565 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 102 | log_prod_blend_88_model_12_market | -28.5% | 0.2054 | 0.0869 | false | roi_delta_below_market_gate, log_loss_worse_than_market, brier_worse_than_market |
| 103 | market_favorite | +0.0% | 0.0000 | 0.0000 | false | baseline_not_candidate |

## Variants

| Variant | Model | Features | Blend weight | Count | Accuracy | Log loss | Brier | ROI |
|---|---|---|---:|---:|---:|---:|---:|---:|
| market_favorite | market_favorite | none |  | 379 | 74.7% | 0.5766 | 0.1952 | 18.5% |
| xgb_prod_unblended | xgboost | production |  | 379 | 52.0% | 0.7266 | 0.2641 | -8.9% |
| xgb_prod_blend_01_model_99_market | xgboost | production | 0.01 | 379 | 74.7% | 0.5773 | 0.1955 | 18.5% |
| xgb_prod_blend_04_model_96_market | xgboost | production | 0.04 | 379 | 74.1% | 0.5797 | 0.1965 | 17.4% |
| xgb_prod_blend_07_model_93_market | xgboost | production | 0.07 | 379 | 73.6% | 0.5822 | 0.1975 | 16.3% |
| xgb_prod_blend_10_model_90_market | xgboost | production | 0.1 | 379 | 73.1% | 0.5847 | 0.1986 | 15.3% |
| xgb_prod_blend_13_model_87_market | xgboost | production | 0.13 | 379 | 72.6% | 0.5875 | 0.1998 | 14.3% |
| xgb_prod_blend_16_model_84_market | xgboost | production | 0.16 | 379 | 72.3% | 0.5903 | 0.2010 | 13.8% |
| xgb_prod_blend_19_model_81_market | xgboost | production | 0.19 | 379 | 72.6% | 0.5933 | 0.2023 | 14.4% |
| xgb_prod_blend_22_model_78_market | xgboost | production | 0.22 | 379 | 71.8% | 0.5963 | 0.2037 | 13.0% |
| xgb_prod_blend_25_model_75_market | xgboost | production | 0.25 | 379 | 70.7% | 0.5995 | 0.2052 | 10.5% |
| xgb_prod_blend_28_model_72_market | xgboost | production | 0.28 | 379 | 70.4% | 0.6029 | 0.2067 | 10.1% |
| xgb_prod_blend_31_model_69_market | xgboost | production | 0.31 | 379 | 70.7% | 0.6063 | 0.2083 | 10.9% |
| xgb_prod_blend_34_model_66_market | xgboost | production | 0.34 | 379 | 70.2% | 0.6099 | 0.2099 | 10.0% |
| xgb_prod_blend_37_model_63_market | xgboost | production | 0.37 | 379 | 69.9% | 0.6136 | 0.2117 | 9.6% |
| xgb_prod_blend_40_model_60_market | xgboost | production | 0.4 | 379 | 68.3% | 0.6174 | 0.2135 | 8.2% |
| xgb_prod_blend_43_model_57_market | xgboost | production | 0.43 | 379 | 67.8% | 0.6213 | 0.2153 | 7.5% |
| xgb_prod_blend_46_model_54_market | xgboost | production | 0.46 | 379 | 67.3% | 0.6254 | 0.2173 | 7.3% |
| xgb_prod_blend_49_model_51_market | xgboost | production | 0.49 | 379 | 66.5% | 0.6296 | 0.2193 | 6.2% |
| xgb_prod_blend_52_model_48_market | xgboost | production | 0.52 | 379 | 66.5% | 0.6339 | 0.2213 | 6.7% |
| xgb_prod_blend_55_model_45_market | xgboost | production | 0.55 | 379 | 66.8% | 0.6384 | 0.2235 | 7.7% |
| xgb_prod_blend_58_model_42_market | xgboost | production | 0.58 | 379 | 65.7% | 0.6430 | 0.2257 | 6.6% |
| xgb_prod_blend_61_model_39_market | xgboost | production | 0.61 | 379 | 65.7% | 0.6478 | 0.2280 | 7.3% |
| xgb_prod_blend_64_model_36_market | xgboost | production | 0.64 | 379 | 63.3% | 0.6527 | 0.2304 | 2.0% |
| xgb_prod_blend_67_model_33_market | xgboost | production | 0.67 | 379 | 62.0% | 0.6578 | 0.2328 | 1.9% |
| xgb_prod_blend_70_model_30_market | xgboost | production | 0.7 | 379 | 60.2% | 0.6630 | 0.2353 | -0.9% |
| xgb_prod_blend_73_model_27_market | xgboost | production | 0.73 | 379 | 59.4% | 0.6684 | 0.2379 | -1.3% |
| xgb_prod_blend_76_model_24_market | xgboost | production | 0.76 | 379 | 57.8% | 0.6740 | 0.2405 | -3.6% |
| xgb_prod_blend_79_model_21_market | xgboost | production | 0.79 | 379 | 57.5% | 0.6798 | 0.2432 | -4.0% |
| xgb_prod_blend_82_model_18_market | xgboost | production | 0.82 | 379 | 57.0% | 0.6857 | 0.2460 | -4.7% |
| xgb_prod_blend_85_model_15_market | xgboost | production | 0.85 | 379 | 55.4% | 0.6919 | 0.2488 | -7.6% |
| xgb_prod_blend_88_model_12_market | xgboost | production | 0.88 | 379 | 53.8% | 0.6983 | 0.2518 | -9.8% |
| xgb_prod_blend_91_model_09_market | xgboost | production | 0.91 | 379 | 53.0% | 0.7049 | 0.2548 | -9.1% |
| xgb_prod_blend_94_model_06_market | xgboost | production | 0.94 | 379 | 52.2% | 0.7118 | 0.2578 | -9.7% |
| xgb_prod_blend_97_model_03_market | xgboost | production | 0.97 | 379 | 52.2% | 0.7190 | 0.2609 | -8.4% |
| xgb_avail_unblended | xgboost | production_plus_availability |  | 379 | 53.8% | 0.7291 | 0.2653 | -5.5% |
| xgb_avail_blend_01_model_99_market | xgboost | production_plus_availability | 0.01 | 379 | 74.7% | 0.5774 | 0.1956 | 18.5% |
| xgb_avail_blend_04_model_96_market | xgboost | production_plus_availability | 0.04 | 379 | 74.1% | 0.5799 | 0.1966 | 17.4% |
| xgb_avail_blend_07_model_93_market | xgboost | production_plus_availability | 0.07 | 379 | 73.4% | 0.5825 | 0.1976 | 15.8% |
| xgb_avail_blend_10_model_90_market | xgboost | production_plus_availability | 0.1 | 379 | 72.8% | 0.5852 | 0.1988 | 14.7% |
| xgb_avail_blend_13_model_87_market | xgboost | production_plus_availability | 0.13 | 379 | 72.6% | 0.5880 | 0.2000 | 14.3% |
| xgb_avail_blend_16_model_84_market | xgboost | production_plus_availability | 0.16 | 379 | 72.3% | 0.5910 | 0.2013 | 13.8% |
| xgb_avail_blend_19_model_81_market | xgboost | production_plus_availability | 0.19 | 379 | 72.6% | 0.5940 | 0.2027 | 14.4% |
| xgb_avail_blend_22_model_78_market | xgboost | production_plus_availability | 0.22 | 379 | 72.0% | 0.5972 | 0.2041 | 13.4% |
| xgb_avail_blend_25_model_75_market | xgboost | production_plus_availability | 0.25 | 379 | 71.0% | 0.6005 | 0.2056 | 11.6% |
| xgb_avail_blend_28_model_72_market | xgboost | production_plus_availability | 0.28 | 379 | 70.7% | 0.6039 | 0.2071 | 11.3% |
| xgb_avail_blend_31_model_69_market | xgboost | production_plus_availability | 0.31 | 379 | 70.4% | 0.6075 | 0.2088 | 10.9% |
| xgb_avail_blend_34_model_66_market | xgboost | production_plus_availability | 0.34 | 379 | 70.4% | 0.6111 | 0.2105 | 10.9% |
| xgb_avail_blend_37_model_63_market | xgboost | production_plus_availability | 0.37 | 379 | 69.1% | 0.6149 | 0.2122 | 8.7% |
| xgb_avail_blend_40_model_60_market | xgboost | production_plus_availability | 0.4 | 379 | 67.5% | 0.6188 | 0.2141 | 6.3% |
| xgb_avail_blend_43_model_57_market | xgboost | production_plus_availability | 0.43 | 379 | 67.3% | 0.6228 | 0.2160 | 7.3% |
| xgb_avail_blend_46_model_54_market | xgboost | production_plus_availability | 0.46 | 379 | 66.8% | 0.6270 | 0.2179 | 6.4% |
| xgb_avail_blend_49_model_51_market | xgboost | production_plus_availability | 0.49 | 379 | 66.5% | 0.6313 | 0.2200 | 7.4% |
| xgb_avail_blend_52_model_48_market | xgboost | production_plus_availability | 0.52 | 379 | 66.0% | 0.6357 | 0.2221 | 6.6% |
| xgb_avail_blend_55_model_45_market | xgboost | production_plus_availability | 0.55 | 379 | 64.9% | 0.6403 | 0.2243 | 5.6% |
| xgb_avail_blend_58_model_42_market | xgboost | production_plus_availability | 0.58 | 379 | 63.1% | 0.6449 | 0.2265 | 3.2% |
| xgb_avail_blend_61_model_39_market | xgboost | production_plus_availability | 0.61 | 379 | 63.3% | 0.6498 | 0.2289 | 4.6% |
| xgb_avail_blend_64_model_36_market | xgboost | production_plus_availability | 0.64 | 379 | 62.0% | 0.6548 | 0.2312 | 1.0% |
| xgb_avail_blend_67_model_33_market | xgboost | production_plus_availability | 0.67 | 379 | 61.2% | 0.6599 | 0.2337 | -0.1% |
| xgb_avail_blend_70_model_30_market | xgboost | production_plus_availability | 0.7 | 379 | 61.2% | 0.6652 | 0.2362 | 1.1% |
| xgb_avail_blend_73_model_27_market | xgboost | production_plus_availability | 0.73 | 379 | 59.9% | 0.6707 | 0.2388 | -0.5% |
| xgb_avail_blend_76_model_24_market | xgboost | production_plus_availability | 0.76 | 379 | 59.1% | 0.6763 | 0.2415 | -1.8% |
| xgb_avail_blend_79_model_21_market | xgboost | production_plus_availability | 0.79 | 379 | 58.8% | 0.6821 | 0.2442 | -1.7% |
| xgb_avail_blend_82_model_18_market | xgboost | production_plus_availability | 0.82 | 379 | 57.8% | 0.6881 | 0.2470 | -3.8% |
| xgb_avail_blend_85_model_15_market | xgboost | production_plus_availability | 0.85 | 379 | 56.7% | 0.6943 | 0.2499 | -5.2% |
| xgb_avail_blend_88_model_12_market | xgboost | production_plus_availability | 0.88 | 379 | 56.7% | 0.7008 | 0.2528 | -3.7% |
| xgb_avail_blend_91_model_09_market | xgboost | production_plus_availability | 0.91 | 379 | 56.2% | 0.7074 | 0.2558 | -2.7% |
| xgb_avail_blend_94_model_06_market | xgboost | production_plus_availability | 0.94 | 379 | 55.1% | 0.7144 | 0.2589 | -4.1% |
| xgb_avail_blend_97_model_03_market | xgboost | production_plus_availability | 0.97 | 379 | 54.9% | 0.7216 | 0.2621 | -4.0% |
| log_prod_unblended | logistic_regression | production |  | 379 | 50.4% | 0.8700 | 0.3031 | -9.2% |
| log_prod_blend_01_model_99_market | logistic_regression | production | 0.01 | 379 | 74.1% | 0.5774 | 0.1956 | 17.4% |
| log_prod_blend_04_model_96_market | logistic_regression | production | 0.04 | 379 | 72.8% | 0.5800 | 0.1966 | 14.8% |
| log_prod_blend_07_model_93_market | logistic_regression | production | 0.07 | 379 | 72.6% | 0.5829 | 0.1978 | 14.3% |
| log_prod_blend_10_model_90_market | logistic_regression | production | 0.1 | 379 | 72.6% | 0.5859 | 0.1991 | 14.3% |
| log_prod_blend_13_model_87_market | logistic_regression | production | 0.13 | 379 | 72.8% | 0.5892 | 0.2006 | 15.0% |
| log_prod_blend_16_model_84_market | logistic_regression | production | 0.16 | 379 | 72.0% | 0.5928 | 0.2022 | 13.8% |
| log_prod_blend_19_model_81_market | logistic_regression | production | 0.19 | 379 | 71.5% | 0.5965 | 0.2039 | 12.9% |
| log_prod_blend_22_model_78_market | logistic_regression | production | 0.22 | 379 | 71.2% | 0.6006 | 0.2058 | 12.9% |
| log_prod_blend_25_model_75_market | logistic_regression | production | 0.25 | 379 | 69.4% | 0.6048 | 0.2078 | 10.0% |
| log_prod_blend_28_model_72_market | logistic_regression | production | 0.28 | 379 | 68.3% | 0.6094 | 0.2100 | 8.8% |
| log_prod_blend_31_model_69_market | logistic_regression | production | 0.31 | 379 | 67.3% | 0.6141 | 0.2123 | 5.7% |
| log_prod_blend_34_model_66_market | logistic_regression | production | 0.34 | 379 | 66.8% | 0.6192 | 0.2147 | 6.0% |
| log_prod_blend_37_model_63_market | logistic_regression | production | 0.37 | 379 | 65.2% | 0.6245 | 0.2173 | 3.6% |
| log_prod_blend_40_model_60_market | logistic_regression | production | 0.4 | 379 | 63.1% | 0.6302 | 0.2200 | 0.5% |
| log_prod_blend_43_model_57_market | logistic_regression | production | 0.43 | 379 | 62.5% | 0.6361 | 0.2228 | -0.3% |
| log_prod_blend_46_model_54_market | logistic_regression | production | 0.46 | 379 | 61.2% | 0.6424 | 0.2258 | -1.4% |
| log_prod_blend_49_model_51_market | logistic_regression | production | 0.49 | 379 | 60.4% | 0.6490 | 0.2289 | -2.6% |
| log_prod_blend_52_model_48_market | logistic_regression | production | 0.52 | 379 | 60.7% | 0.6559 | 0.2322 | -1.0% |
| log_prod_blend_55_model_45_market | logistic_regression | production | 0.55 | 379 | 59.1% | 0.6633 | 0.2356 | -3.0% |
| log_prod_blend_58_model_42_market | logistic_regression | production | 0.58 | 379 | 59.1% | 0.6710 | 0.2391 | -1.7% |
| log_prod_blend_61_model_39_market | logistic_regression | production | 0.61 | 379 | 58.0% | 0.6792 | 0.2428 | -2.5% |
| log_prod_blend_64_model_36_market | logistic_regression | production | 0.64 | 379 | 56.2% | 0.6879 | 0.2466 | -5.2% |
| log_prod_blend_67_model_33_market | logistic_regression | production | 0.67 | 379 | 55.4% | 0.6970 | 0.2506 | -5.8% |
| log_prod_blend_70_model_30_market | logistic_regression | production | 0.7 | 379 | 54.1% | 0.7068 | 0.2547 | -7.6% |
| log_prod_blend_73_model_27_market | logistic_regression | production | 0.73 | 379 | 53.6% | 0.7171 | 0.2589 | -8.4% |
| log_prod_blend_76_model_24_market | logistic_regression | production | 0.76 | 379 | 52.8% | 0.7282 | 0.2633 | -8.5% |
| log_prod_blend_79_model_21_market | logistic_regression | production | 0.79 | 379 | 52.0% | 0.7401 | 0.2678 | -8.7% |
| log_prod_blend_82_model_18_market | logistic_regression | production | 0.82 | 379 | 51.7% | 0.7529 | 0.2724 | -9.0% |
| log_prod_blend_85_model_15_market | logistic_regression | production | 0.85 | 379 | 51.2% | 0.7667 | 0.2772 | -9.7% |
| log_prod_blend_88_model_12_market | logistic_regression | production | 0.88 | 379 | 50.9% | 0.7820 | 0.2821 | -10.0% |
| log_prod_blend_91_model_09_market | logistic_regression | production | 0.91 | 379 | 51.5% | 0.7989 | 0.2872 | -8.3% |
| log_prod_blend_94_model_06_market | logistic_regression | production | 0.94 | 379 | 50.9% | 0.8181 | 0.2923 | -8.5% |
| log_prod_blend_97_model_03_market | logistic_regression | production | 0.97 | 379 | 50.9% | 0.8407 | 0.2977 | -8.5% |

## Recommendation

- Status: `research_only`
- Reason: xgb_prod_blend_01_model_99_market is the best configured candidate but does not clear the market gate.

## Policy

This harness is for report-only discovery. A candidate from the current corpus is not activation proof; validated status requires a locked future evaluation slice and a passing market gate.
