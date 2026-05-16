# Indicator Promotion Gate

Indicator retraining and promotion are manual operations. Daily and weekly maintenance jobs are report-only and must not write production model artifacts or `model_versions`.

## Candidate Retrain Artifact

After newly labeled fights are imported and the weekly evaluation report is generated, create a candidate evidence bundle:

```bash
DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor \
pnpm --filter @interceptor/db report:market-indicators -- \
  --output data/experiments/candidate-market-indicators.json \
  --markdown data/experiments/candidate-market-indicators.md
```

This artifact is experimental evidence only. Weak candidates stay in `data/experiments/` with recommendation notes; they are not copied into `data/models/`.

## Required Gates

Promotion requires all of the following:

- No-leakage chronology: training data must end before the locked evaluation window.
- Market coverage: enough matched market rows to compare against the market baseline.
- Calibration: Brier score and calibration buckets must not show obvious overconfidence.
- ROI/edge diagnostics: candidate edge behavior must beat or explain the market baseline, not just raw model accuracy.
- Locked validation: no threshold or feature tuning after the candidate list is frozen.
- Evidence record: model version, source data window, feature set, threshold, calibration, and validation artifact paths must be recorded.

## Manual Approval

A frozen artifact can be promoted only after an operator explicitly approves the evidence bundle in review. The approval record must include:

- Candidate artifact path.
- Validation report path.
- Source data window.
- Feature set and target.
- Threshold and calibration settings.
- Reason promotion is justified against the market baseline.

If any gate fails, the candidate remains report-only and the recommendation should say why it was rejected.
