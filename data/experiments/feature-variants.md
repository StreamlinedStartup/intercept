# Feature-Variant Experiment

Generated: 2026-05-11T16:43:05.216089+00:00
Winner: baseline
Recommended next action: Keep the production feature set and use the report as baseline evidence.

## Ranked Summary

| Rank | Variant | Events | Predictions | Log loss | Brier | Abs calib err | ROC AUC | Accuracy | 70%+ count | 70%+ accuracy | 70%+ gap | Flag |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | baseline | 273 | 3172 | 0.6619 | 0.2347 | 0.0232 | 0.6448 | 0.6053 | 138 | 0.7609 | 0.0350 |  |
| 2 | no_weight_class | 273 | 3172 | 0.6621 | 0.2348 | 0.0241 | 0.6443 | 0.6062 | 135 | 0.7778 | 0.0528 |  |
| 3 | no_stance | 273 | 3172 | 0.6624 | 0.2350 | 0.0266 | 0.6439 | 0.6091 | 131 | 0.7786 | 0.0523 |  |
| 4 | no_common_opponents | 273 | 3172 | 0.6625 | 0.2350 | 0.0254 | 0.6430 | 0.6072 | 156 | 0.7564 | 0.0318 |  |
| 5 | no_recent_form | 273 | 3172 | 0.6639 | 0.2357 | 0.0206 | 0.6418 | 0.6006 | 105 | 0.7619 | 0.0396 |  |

## Baseline vs Winner

| Metric | Baseline | Winner | Delta |
|---|---:|---:|---:|
| log_loss | 0.6619 | 0.6619 | 0.0000 |
| brier_score | 0.2347 | 0.2347 | 0.0000 |
| abs_calibration_error | 0.0232 | 0.0232 | 0.0000 |
| roc_auc | 0.6448 | 0.6448 | 0.0000 |
| accuracy | 0.6053 | 0.6053 | 0.0000 |

## 70%+ Bucket

| Variant | Count | Accuracy | Avg confidence | Calibration gap | Abs calib err |
|---|---:|---:|---:|---:|---:|
| baseline | 138 | 0.7609 | 0.7259 | 0.0350 | 0.0350 |
| no_weight_class | 135 | 0.7778 | 0.7250 | 0.0528 | 0.0528 |
| no_stance | 131 | 0.7786 | 0.7263 | 0.0523 | 0.0523 |
| no_common_opponents | 156 | 0.7564 | 0.7246 | 0.0318 | 0.0318 |
| no_recent_form | 105 | 0.7619 | 0.7223 | 0.0396 | 0.0396 |
