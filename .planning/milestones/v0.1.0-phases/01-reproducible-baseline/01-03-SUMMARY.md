---
phase: 01-reproducible-baseline
plan: "03"
status: complete
requirements-completed: [BASE-03, BASE-04]
provides: [live-authentication-smoke, native-seed, classified-legacy-report]
---

# Plan 03: Actual authentication and baseline evidence

- Implemented bounded stdlib HTTP smoke: real CSRF login, cookie session and login-required Users page follow-up, anonymous/wrong-password controls, generated native v2 bearer token with exact API user identity, invalid-token rejection. Runtime/version/schema/registration run first.
- `make test`: exit 0, 27 helper tests, CONFIG_OK, RUNTIME_OK, BASELINE_SMOKE_OK and SEED_IDEMPOTENT_OK. Includes four lifecycle guard tests prepared for next plan.
- Native transactional seed creates sandbox-prefixed site/manufacturer, CMTS/CPE roles/types/devices, tag and two native custom fields with values. Repeated seed preserves identities and values and does not delete user records.
- `make test-legacy` equivalent `python3 scripts/legacy_tests.py`: exit 1, classification runner-unavailable, pytest not installed. No legacy test executed; this is not a feature failure or a passing suite. Sanitized exact command/exit saved locally at .sandbox/legacy-tests.json.
- Nine smoke tests and three legacy-report tests exercise rejected credentials, missing session evidence, timeout/redaction and truthful exit classification.

## Deviations

Parent performed live Docker checks because subagent escalated calls stalled. No optional test package installation was needed for the blocking stdlib baseline. Lifecycle integration was prepared concurrently but exercised only after Plan 03 checks passed.

## Self-Check: PASSED

Live authentication, schema and idempotent seed checks passed. Legacy suite is explicitly unexecuted; no feature compatibility claim made.
