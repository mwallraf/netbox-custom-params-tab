---
phase: 05-release-verification
plan: 01
status: automated_pass_manual_pending
requirements: [REL-01, REL-02, REL-03]
---

# Automated release verification

Added `make release-check` / `scripts/release_check.py`. The helper builds a source
distribution and wheel from a temporary clean copy of current package source and
host pyproject metadata, verifies required HTML/JavaScript/migration assets,
installs the wheel to a temporary target without replacing the editable install,
and asserts installed import provenance. It performs native system/schema drift
checks and runs all plugin tests with a new uniquely named disposable test DB.
Native test teardown removes that DB. Temporary build/install files are removed.
Live native/plugin snapshots are compared even when a check fails.

## Observed results (2026-11-10)

- Source suite: 104 tests / 22.676 s; 28.19 s including runner/snapshots.
- Required baseline: 35 helper tests pass; CONFIG_OK, RUNTIME_OK,
  BASELINE_SMOKE_OK and SEED_IDEMPOTENT_OK.
- Installed wheel: Found 104 tests, PROFILE_TESTS_ISOLATED,
  RELEASE_WHEEL_ASSETS_OK, RELEASE_INSTALLED_IMPORT_OK, no migration drift,
  RELEASE_CLEAN_INSTALL_MIGRATIONS_TESTS_OK, RELEASE_LIVE_UNCHANGED and
  RELEASE_CHECK_OK elapsed=113.40s. Fresh database setup exercises all migrations.
- After reloading sandbox netbox/worker processes, runtime/schema/authentication
  smoke passed again. No browser was used.

The initial build attempts were not passes: the read-only image egg-info prevented
in-place builds; the image's older baked pyproject lacked current asset metadata.
The final helper builds a clean temporary copy using current host metadata.
An uncached declared setuptools build dependency requires registry access.

Native tests cover CMTS/CPE/shared rules and dynamic fields, deduplicated editing,
all 13 types, native-save freshness, constrained permissions and preservation.
`docs/development/final-uat.md` combines the existing 15 display cases, eight edit
cases and integrated native interoperability checks for final manual acceptance.
README, profiles guide and CLAUDE describe the implemented editor and UAT deferral.

No published package, migration change, legacy upgrade mapping or milestone
archival is claimed. Other NetBox versions and optional historical pytest are
unverified. Final acceptance remains pending the user's manual observations.
