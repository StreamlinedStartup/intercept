---
# intercept-n89z
title: Download external UFC stats CSV snapshot
status: completed
type: task
priority: normal
created_at: 2026-05-11T00:24:38Z
updated_at: 2026-05-11T00:33:02Z
parent: intercept-r03n
blocked_by:
    - intercept-bsn7
---

Add a repo-native command to download the upstream CSV files into ignored local data, record source URL/commit/ETag metadata, and avoid committing copied data by default.

## Summary of Changes

- Added `pnpm data:ufcstats:snapshot` backed by `scripts/download-ufcstats-snapshot.mjs`.
- Downloader resolves the upstream commit SHA, downloads only the six published CSV files, and writes per-file URL, ETag, size, content type, and SHA-256 metadata.
- Documented snapshot usage and clarified that `data/external/ufcstats/` remains ignored local data.

## Verification

- `pnpm data:ufcstats:snapshot -- --snapshot-id codex-verify-n89z-2`
- Confirmed all six CSVs plus `metadata.json` exist under `data/external/ufcstats/codex-verify-n89z-2/`.
- Confirmed metadata records source commit `7dc63908a74905decdf8e2f58fcede3ae027dd98`, file sizes, ETags, and SHA-256 hashes.
- `pnpm biome check scripts/download-ufcstats-snapshot.mjs package.json docs/external_ufcstats_dataset.md .gitignore`
