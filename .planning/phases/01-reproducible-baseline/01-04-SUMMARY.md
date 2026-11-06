---
phase: 01-reproducible-baseline
plan: "04"
status: complete
requirements-completed: [BASE-01, BASE-02, BASE-03, BASE-04]
provides: [persistent-isolated-lifecycle, baseline-guide]
---

# Plan 04: Persistent lifecycle and reproducible guide

The real lifecycle check passed with PERSISTENCE_OK, PROJECT_RESET_OK,
RESET_RECREATED_DATABASE_OK, CREDENTIALS_STABLE and LIFECYCLE_OK.
Two setup runs and down/up retained the sentinel database identity; reset removed
only validated project-owned volumes, recreated the database and seed, retained
the env-file bytes, and left unrelated container identities unchanged. Native
schema/registration and real admin/API smoke passed again after reset. Web and
worker end healthy and running on localhost 18047.

33 helper tests pass (ten lifecycle guards); git diff --check b090288 passes.
Source snapshot at 4dba67e and current layout verification pass. Final make test
runs the helper suite, rendered configuration validation, real native runtime,
CSRF session/API auth with negative controls, and seed-check.

README and sandbox.md document every Make target, native configuration split,
version floor versus tested exact image, local credential retrieval, ordinary
non-destructive stop/start, and explicitly destructive project-only reset.
Baseline-status.md records exact evidence and unexecuted legacy suite
(runner-unavailable, exit 1). No profiles/tab/edit feature code was added.

## Deviations

Lifecycle implementation is separated into scripts/lifecycle_sandbox.py, called
by the shared sandbox CLI, to keep project scoping and reset checks inspectable.
Added build-context secret/recovery exclusions and matching regression checks.
No global cleanup or additional branch/worktree was created.

## Self-Check: PASSED

All blocking real lifecycle checks passed. Independent goal verification follows.

## Review corrections

CR-01/02 and WR-01 fixed: one Docker environment for inspection and mutation; exact service mount maps including symlink/readonly/driver controls; read-only random-marker sentinel plus seed identity/native-value snapshots. Ten lifecycle regression tests pass; independent focused fix review found no remaining issues.
