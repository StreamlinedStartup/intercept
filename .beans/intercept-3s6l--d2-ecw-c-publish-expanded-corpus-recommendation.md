---
# intercept-3s6l
title: 'D2-ECW-C: Publish expanded-corpus recommendation'
status: completed
type: task
priority: high
created_at: 2026-05-13T00:21:40Z
updated_at: 2026-05-13T00:48:00Z
parent: intercept-gzb7
blocked_by:
    - intercept-5iu2
---

Acceptance criteria:

- [x] Summarizes whether the original winner survives expanded corpus windows.
- [x] Summarizes additional winners and their metrics.
- [x] Confirms research_only/no model_versions writes.
- [x] Closes the epic with verification and smoke-gate note.

## Summary of Changes

- Published `docs/expanded_corpus_winner_validation.md`.
- Confirmed the original winner clears all expanded windows from `min_train_samples=20` through 100.
- Summarized the additional 150 gate-clearing variants from the expanded selected-fight search.
- No HTTP/UI smoke gate is required because this epic only changes Python research harness configs, artifacts, and docs.

## Verification

- `jq -e '.windows | length == 5 and all(.[]; .clears_market_gate == true and .roi_delta_vs_market >= 0.02 and .log_loss_delta_vs_market <= 0 and .brier_delta_vs_market <= 0 and .selected_fights >= 200)' data/experiments/harness/winner-expanded-corpus-summary.json` -> true.
- `jq -e '.clearing_variant_count == 150 and .report_only == true and .writes_model_versions == false and .value_status == "research_only"' data/experiments/harness/additional-winner-search-summary.json` -> true.
- `rg -n "research_only|150|log_allmarketctx_c2p0_temp2p2_blend55_min_confidence0p66|log_allmarketctx_c2p5_temp2p2_blend45_min_confidence0p63" docs/expanded_corpus_winner_validation.md`.
