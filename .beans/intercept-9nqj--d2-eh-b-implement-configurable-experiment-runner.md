---
# intercept-9nqj
title: 'D2-EH-B: Implement configurable experiment runner'
status: todo
type: task
priority: high
created_at: 2026-05-12T06:13:36Z
updated_at: 2026-05-12T06:13:50Z
parent: intercept-ls80
blocked_by:
    - intercept-28c6
---

Acceptance criteria:\n- [ ] Implement a Python CLI that reads the config and executes chronological market-covered experiments.\n- [ ] Support at least model families, feature sets/availability transforms, and market blend weights.\n- [ ] Persist run registry JSON/Markdown artifacts with params, metrics, gates, and rejection reasons.\n- [ ] Add focused tests for config parsing, feature alignment, and gate behavior; no model_versions writes.
