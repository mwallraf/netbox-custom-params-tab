---
phase: 01-reproducible-baseline
plan: "01"
status: complete
subsystem: source-recovery
tags: [git, recovery]
requires: []
provides: [canonical-root-source]
affects: [01-02]
key-files:
  created: [scripts/source_snapshot.py, docs/development/source-recovery.md]
  modified: [README.md, AGENTS.md, CLAUDE.md, .gitignore]
key-decisions:
  - Preserve the complete original directory in ignored .recovery instead of deleting it.
plan_head_before: a6b9d5f2a422cff6d7bab54a65a98d6e8ed9d753
plan_head_after: 19e26e4fb4be0e4a301992c1b5cd3084c94a631f
actuals:
  tasks: 2
  commits: 22
  tokens: 21350
---

# Phase 1 Plan 1: Source recovery summary

The renamed snapshot is tracked at root with feature history retained by merge and an explicit SHA256 inventory.

## Tasks and evidence

- Task 1: `4dba67e` retains feature `42ad9c2` and all 36 inventoried source/config/test files without changing their bytes.
- Task 2: `19e26e4` moves the original directory unchanged into ignored `.recovery/implement-plugin`, updates canonical source guidance, and retains the pending historical spec deletion.
- `python3 scripts/source_snapshot.py verify --commit 4dba67e`: SOURCE_SNAPSHOT_OK.
- `python3 scripts/source_snapshot.py verify-layout`: SOURCE_LAYOUT_OK.
- Branch: milestone/custom-field-profiles. Only the normal checkout is registered.
- Current authoritative product requirements and planning survived the history merge.

## Deviations from Plan

Original directory retained locally rather than removed, preserving generated/unrelated files as well as source. No prune or reset ran.

`git diff --check b090288` reports two preexisting trailing spaces in 01-PATTERNS.md lines 3–4; recovery added no whitespace errors. This existing planning formatting is recorded rather than discarded.

## Self-Check: PASSED

Canonical source, provenance manifest, both task commits and feature-history ancestry verified.
