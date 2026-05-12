---
# intercept-tjvc
title: 'D2-RV-B: Build full leakage audit harness'
status: completed
type: task
priority: high
created_at: 2026-05-12T00:21:11Z
updated_at: 2026-05-12T00:58:40Z
parent: intercept-dmyw
blocked_by:
    - intercept-5nbu
---

Build report-only leakage audit tooling before any downstream value validation.

Acceptance criteria:
- [x] Audit point-in-time feature construction for target leakage.
- [ ] Audit train/test event chronology and future-data boundaries.
- [ ] Produce machine-readable and markdown reports.
- [ ] Do not write active model_versions.



## Summary of Changes
- Added `ml.leakage_audit`, a report-only audit harness for source-level point-in-time feature checks, chronological train/test boundaries, walk-forward future-data boundaries, and optional DB sample boundaries.
- Added focused tests for the audit report and Markdown policy rendering.
- Generated `data/experiments/leakage-audit.json` and `data/experiments/leakage-audit.md` with 15/15 checks passing and `writes_model_versions=false`.

## Verification
- `PYTHONPATH=services/python services/python/.venv/bin/python -m ml.leakage_audit --output data/experiments/leakage-audit.json --markdown data/experiments/leakage-audit.md`
- `DATABASE_URL=postgres://interceptor:interceptor@localhost:5434/interceptor PYTHONPATH=services/python services/python/.venv/bin/python -m ml.leakage_audit --include-db --max-events 5 --output data/experiments/leakage-audit.json --markdown data/experiments/leakage-audit.md --stdout summary`
- `PYTHONPATH=services/python services/python/.venv/bin/python -m pytest services/python/test_leakage_audit.py -q`
- `services/python/.venv/bin/python -m compileall -q services/python/ml/leakage_audit.py services/python/test_leakage_audit.py`
