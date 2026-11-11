---
phase: 02-profile-administration-and-matching
plan: "01"
subsystem: database
tags: [netbox, django, postgresql, profiles, testing]
requires:
  - phase: 01-reproducible-baseline
    provides: Pinned native sandbox and tested migration/authentication baseline
provides:
  - Additive CustomFieldProfile and ProfileField schema
  - Read-only native All-field resolution and enabled unrestricted matching
  - Isolated native PostgreSQL profile test command with zero-test rejection
affects: [02-02, 02-03, 02-04, 02-05, 02-06, 02-07, 02-08]
tech-stack:
  added: []
  patterns: [native-generated forward migrations, plugin-owned Django tests, live snapshot preservation]
key-files:
  created:
    - netbox_custom_field_profiles/migrations/0002_profiles.py
    - netbox_custom_field_profiles/matching.py
    - netbox_custom_field_profiles/tests/__init__.py
    - netbox_custom_field_profiles/tests/test_schema.py
    - netbox_custom_field_profiles/tests/runner.py
    - scripts/test_profiles.py
  modified: [netbox_custom_field_profiles/models.py, Makefile]
key-decisions:
  - Native field ordering is delegated to CustomField.objects.get_for_model(Device).
  - Retain an isolated test database with --keepdb for focused reruns, never the live database.
requirements-completed: [PROF-02, PROF-03, PROF-05, MATCH-03, DATA-01]
actuals:
  tokens: 4797
  tasks: 2
  commits: 3
plan_head_before: 5cf424c83dc8baf579de459dfde528c5bb322f40
plan_head_after: d5be3f94515771c0bf15246bf37f3c8688c7dbac
coverage:
  - id: schema
    description: Native additive profile schema with deterministic identity, ordering and membership constraints
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles.tests.test_schema.ProfileSchemaTests
        status: pass
    human_judgment: false
  - id: resolution
    description: Enabled unrestricted profiles and dynamic active native field order
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles.tests.test_schema.ProfileSchemaTests.test_native_all_resolution_enabled_only_and_dynamic_order
        status: pass
    human_judgment: false
  - id: isolation
    description: Nonzero native suite, PostgreSQL isolation and unchanged live native/plugin snapshots
    verification:
      - kind: integration
        ref: make test-profiles
        status: pass
      - kind: integration
        ref: python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.runner (expected exit 1)
        status: pass
    human_judgment: false
duration: 10 min
completed: "2026-11-06"
status: complete
---

# Phase 2 Plan 01: Additive schema and isolated native testing Summary

**Native profile configuration tables, dynamic field resolution and a fail-closed PostgreSQL test runner are applied and verified without changing native or legacy data.**

## Performance

- Started: 2026-11-06T18:32:25Z
- Completed: 2026-11-06T18:41:52Z
- Tasks: 2; files: 8; production/test commits: 3.
- Actual tokens: 19,187 realized diff characters / 4, rounded to 4,797; excludes planning metadata.

## Accomplishments

- Generated and reviewed `0002_profiles`: two new configuration models, native reference sets, ordered memberships and per-profile field uniqueness. No legacy deletion, data migration or native model write operations.
- Device-only model validation, nonunique titles, default disabled state and display-order/title/created/PK ordering are tested in native NetBox.
- All-fields resolution follows the active native resolver, including group/weight/name ordering and newly applicable fields. Unrestricted matching excludes disabled profiles; configured criteria fail closed until Plan 02-04 expands matching.
- Added `make test-profiles` and focused `scripts/test_profiles.py --label ...`. Both use native settings and PostgreSQL, retain only the separate test database, reject empty suites, and compare live native/plugin row snapshots.

## Task Commits

1. `ee6aa94` — contract tests before schema implementation.
2. `5ce4827` — Task 1 additive schema and native read-only resolution.
3. `d5be3f9` — Task 2 isolated runner, native runner guard test and Make target.

## Verification Evidence

- Explicit native schema test command: exit 0, six schema tests discovered.
- `0002_profiles` applied successfully. `makemigrations --check --dry-run`: no changes detected.
- One-time live Device/CustomField/legacy configuration full-row snapshot SHA-256 before and after migration: `d37630c7c681485da4aea0c429bf5e96f7f9ec112d22bfb412ffb6f4c9ef94bc` on both sides.
- `make test-profiles`: seven tests passed; `PROFILE_TESTS_ISOLATED`, `PROFILE_LIVE_UNCHANGED`, `PROFILE_TESTS_OK elapsed=40.59s`. This run completed remaining test-database migration work.
- Focused `--label netbox_custom_field_profiles.tests.test_schema`: seven tests passed in 0.139s; total helper elapsed 4.56s, isolated PostgreSQL and live preservation confirmations present.
- Empty label `netbox_custom_field_profiles.tests.runner`: `Found 0 test(s)`, `PROFILE_TESTS_EMPTY`, exit 1, `PROFILE_LIVE_UNCHANGED`; guard triggers before database setup.
- Final post-restart `make test`: 35 helper tests pass, runtime NetBox 4.7.4/Docker 5.1.1 verified, migrations clean, admin session/native token/negative controls pass, seed idempotence passes.
- Python compilation and `git diff --check` pass. Dedicated web and worker were restarted to load new models.

## Deviations from Plan

- [Rule 3 — Bootstrap] Initial contract run could not import the not-yet-created matching module. This is recorded as bootstrap evidence, not a valid behavior RED assertion; no TDD gate compliance is claimed. All native behavioral tests subsequently passed.
- [Rule 3 — Verification interruption] A service restart terminated the first new-runner suite with exit 137 while test setup was active. Restart completed, then the entire suite was rerun successfully, followed by focused and baseline verification. No reset was performed; the live snapshot stayed unchanged.

## Scope and Remaining Work

No new administration UI is exposed by this preparation. The detail route and full CRUD path are intentionally supplied immediately by Plan 02-02. Fixed configured-rule matching is Plan 02-04; this slice excludes any populated criteria rather than broadening relevance. No native value editing or Parameters tab was implemented.

The existing upstream LOGIN_REQUIRED deprecation warning remains unchanged. Optional legacy pytest was not run or claimed as passed. No packages were added, no native settings/values were changed by profile code, and no legacy models were removed.

## Self-Check: PASSED

All eight planned source files exist; all three listed commits are ancestors of HEAD; required native and baseline commands passed. Shared requirement IDs remain pending until their other declaring plans finish.

## Next Plan Readiness

Ready for 02-02: native CRUD/resolution tracer. The database contains the new schema and the native test runner is usable with focused labels.
