---
phase: "01"
slug: "reproducible-baseline"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-06"
---

# Phase 1 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Python stdlib helper tests; native NetBox/Django and real HTTP integration |
| Config | Docker sandbox and Makefile created during this phase |
| Quick command | `make check` once the target exists |
| Blocking baseline | `make test` and `make smoke` against the dedicated sandbox |
| Legacy report | `make test-legacy`; real failures recorded separately |
| Runtime | Quick checks target <30s; cold image build/setup can take minutes |

All listed baseline commands exist and were exercised. See summaries and baseline-status.md.

## Sampling Rate

- After source consolidation: verify tracked source manifest and retained docs.
- After helper/config changes: quick helper/static checks, with no secrets printed.
- After first runnable sandbox slice and lifecycle changes: real baseline smoke.
- Before phase verification: all baseline startup/install checks must be green.
- Feature-only legacy suite failures may be documented/deferred per D-14; boot,
  migrations, registration, authentication, or test infrastructure failures cannot
  be represented as passing baseline checks.
- No watch mode. Bound readiness waits and surface actionable failures.

## Per-Task Verification Map

All commands run from the canonical repository root. A helper marked new is
created in the same task before its verify command runs; later tasks depend on
the preceding plan's verified artifacts. All baseline commands below passed; legacy runner absence was classified honestly.

| Task ID | Plan | Wave | Requirement | Threat Ref | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | BASE-01 | T-01-01/02 | Git/filesystem | `python3 scripts/source_snapshot.py verify --manifest docs/development/source-recovery.md --root . --commit 4dba67e` | New in task | Passed |
| 01-01-02 | 01 | 1 | BASE-01 | T-01-01/02 | Git/filesystem | `python3 scripts/source_snapshot.py verify-layout --root .` | Prior task | Passed |
| 01-02-01 | 02 | 2 | BASE-02 | T-01-03 | Unit + env tracer | `python3 -m unittest discover -s tests/sandbox -p test_config.py -v` and `make env` | New in task | Passed |
| 01-02-02 | 02 | 2 | BASE-02/03 | T-01-04 | Compose configuration | `python3 scripts/sandbox.py compose config --quiet` and `make check` | Prior task + config in task | Passed |
| 01-02-03 | 02 | 2 | BASE-03 | T-01-05 | Unit sequencing + real container | `make setup`, `python3 scripts/sandbox.py verify-runtime`, `python3 -m unittest discover -s tests/sandbox -p test_config.py -v` | New in task | Passed |
| 01-03-01 | 03 | 3 | BASE-03/04 | T-01-06/07 | Unit + real HTTP/container | `make test` and `make smoke` | New in task | Passed |
| 01-03-02 | 03 | 3 | BASE-04 | T-01-07 | Real ORM | `make seed-check` and `make smoke` | New in task | Passed |
| 01-03-03 | 03 | 3 | BASE-04 | T-01-06/07 | Unit + legacy report | `python3 -m unittest discover -s tests/sandbox -p test_legacy_report.py -v` and `make test-legacy` | New in task | Passed |
| 01-04-01 | 04 | 4 | BASE-02/04 | T-01-08 | Unit + real lifecycle | `python3 -m unittest discover -s tests/sandbox -p test_lifecycle.py -v` and `make lifecycle-check` | New in task | Passed |
| 01-04-02 | 04 | 4 | BASE-01..04 | T-01-09 | Baseline + docs | `make check`, `make test`, `git diff --check b090288` | Prior tasks | Passed |

Legacy outcome contract: make test-legacy returns its real runner status. Nonzero
legacy feature/setup outcomes are recorded, never silently treated as tests
passing; a missing or dishonest report is a blocking reporting defect. make test
and make smoke remain independently blocking baseline commands.

## Wave 0 Requirements

- Create baseline helper tests alongside configuration/credential generation.
- Create real HTTP/login and Django registration/migration smoke checks before
  declaring the sandbox complete. An HTTP GET of login alone is insufficient.
- Initial schema correction must use a direct native-interpreter one-off after
  healthy dependencies, never bootstrap first. Unit command-order checks and
  actual pre-bootstrap plugin-schema absence evidence establish that corrected
  migration generation precedes application; normal service bootstrap stays native.
- Create source reconciliation evidence before abandoning the ignored snapshot.
- Add idempotent seed and lifecycle/reset checks with project-only scoping.
- Map every automated command to a helper created in that task or an earlier
  dependency. Add an explicit observable `<fails_when>` after each command.

## Manual-Only Verifications

Real browser admin login may supplement automated CSRF-aware login/session checks.
It does not replace automated registration/schema/authentication assertions.
Do not alter or inspect credentials of the user's other NetBox installation.

## Validation Sign-Off

- [x] Every task has automated verification or a concrete prerequisite.
- [x] No three consecutive tasks lack automated checks.
- [x] All missing helpers are created before use.
- [x] No watch flags or unbounded readiness waits.
- [x] Real boot/migrate/register/login evidence recorded.
- [x] No secrets in outputs or version control.
- [x] Set `nyquist_compliant: true` only after the validation contract is satisfied.

**Approval:** Validated 2026-11-06. All four BASE requirements have automated evidence; 29 helper tests plus real runtime/auth/seed/lifecycle checks. Legacy pytest is runner-unavailable (exit 1), not a passed feature suite.

## Validation Audit

2026-11-06: 4 requirements covered, 0 baseline gaps, 0 manual-only blockers. Source checks, runtime and actual authentication, idempotent seed, and real persistence/project reset passed. Optional legacy suite is explicitly unexecuted.
