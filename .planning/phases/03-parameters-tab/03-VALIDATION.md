---
phase: "03"
slug: "parameters-tab"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-07"
---

# Phase 03 — Validation Strategy

## Test Infrastructure

Native Django TestCase/Client with isolated PostgreSQL through ProfileTestRunner.
No framework installation is needed. New modules must be created by their first
owning plan before its verification command runs.

- Quick: `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameters`
- Rendering: `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_rendering`
- Permissions: `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_permissions`
- Full: `make test-profiles`; final baseline: `make test`.

## Sampling Rate

Run the owning focused module after each behavioral task and affected existing
tests when shared code changes. Run the native suite after each integrated wave;
run the required baseline at the final gate. Target focused feedback below 30
seconds where practical; actual runtime must be measured during execution, not
claimed here. Zero-test runs and nonzero exits are failures. Preserve live data;
never reset the sandbox for feature tests or restart services during tests.

## Verification Map

| Task | Requirement | Behavior | Test module / command | Threat Ref | Status |
|------|-------------|----------|-----------------------|------------|--------|
| 03-01-T1 | TAB-01 | Fresh-process reverse/resolve, native navigation, active tab, no panel | test_parameters | T-03-01, T-03-04 | pending; creates module |
| 03-01-T2 | TAB-01/AUTH-01 | Match/zero-field/no-match states; Device authority before resolution; Device-only/profile-admin-only subjects; unsupported POST | test_parameters, test_parameter_permissions | T-03-01, T-03-02, T-03-03 | pending; creates permissions module |
| 03-02-T1 | TAB-02/TAB-03 | CMTS/CPE/shared matching, duplicate titles/order, Selected/All order/dynamic fields, fresh duplicate native values | test_parameters | T-03-06 | pending |
| 03-02-T2 | TAB-03/AUTH-01 | All 13 types; false/zero/JSON empties; Hidden/If Set; native label/help and settings preservation | test_parameter_rendering | T-03-05, T-03-07 | pending; creates rendering module |
| 03-03-T1 | AUTH-01 | Scalar missing/denied, mixed/all-denied multiobjects; no ID/label/link/count leaks; alternating users | test_parameter_permissions | T-03-04, T-03-08, T-03-09 | pending |
| 03-03-T2 | TAB-03/AUTH-01 | Full URL text/native scheme safety, sanitized Markdown/line breaks, escaped JSON/metadata, local overflow markup | test_parameter_rendering, test_parameter_permissions | T-03-07, T-03-10, T-03-11, T-03-12 | pending |
| 03-04-T1 | TAB-01/TAB-02/TAB-03/AUTH-01 | Complete native/profile snapshots, legitimate native-write freshness, excluded-value retention, native baseline | cases owned by test_parameter_permissions; all three focused modules as regression gates; make test-profiles; make test | T-03-03, T-03-05, T-03-13, T-03-14 | pending |
| 03-04-T2 | TAB-01/TAB-02/TAB-03/AUTH-01 | Actual browser acceptance, fixture restoration, accurate docs and evidence | scoped git diff --check HEAD before task commit plus manual matrix below | T-03-12, T-03-14, T-03-15, T-03-16 | pending |

Module names above expand to the exact focused commands in Test Infrastructure.
All automated behavioral commands must exit zero, report nonzero executed tests,
and emit PROFILE_TESTS_ISOLATED and PROFILE_LIVE_UNCHANGED. Each plan also carries
T-03-SC: no installs/upgrades; any newly proposed install requires a legitimacy
audit before execution. ASVS 5.0.0 L1 applies; unresolved high/critical threats
block acceptance. No task has executed and no test/runtime result is claimed.
Plan 04 owns only test_parameter_permissions.py and five documentation/evidence
files. Production defects reopen their original owning implementation task;
existing ordering/type modules remain unchanged regression inputs to this plan.

## Wave 0 Requirements

03-01-T1 creates test_parameters; 03-01-T2 creates test_parameter_permissions;
03-02-T2 creates test_parameter_rendering, reusing native Device fixture and
ObjectPermission patterns. The first tracer must pass cold-start
reverse/resolve/navigation without a test-side view import before expansion.
No framework installation or standalone test-infrastructure plan is needed.
wave_0_complete stays false until those owning tasks actually create/run tests.

## Manual-Only Verifications

| Behavior | Requirement | Instructions |
|----------|-------------|--------------|
| Desktop/narrow layout | TAB-01/TAB-03 | Inspect real Device tab with 20–30 fields, multiple sections, long text/URLs/JSON; verify wrapping and local overflow |
| Help and empty states | TAB-03 | Check native help presentation, muted Not set, empty section, no-match direct page |
| Native navigation | TAB-01/AUTH-01 | Confirm active tab, visibility on matching/nonmatching Devices, viewer/restricted-user behavior |
| Complete section contract | TAB-02/TAB-03 | Inspect duplicate-title sections, repeated fields, Selected/All ordering, Hidden/unset If Set rows and false/zero/JSON empties |
| Read-only presentation | TAB-01/AUTH-01 | Confirm no Parameters edit action or profile administration metadata; inspect keyboard focus/help behavior |

Record real browser evidence during execution; server HTML cannot prove layout.
If browser unavailable, report manual acceptance pending rather than claim pass.
03-04-T2 owns `.planning/phases/03-parameters-tab/03-UAT.md`: record fixture,
viewport, action, expected/actual result, timestamp and evidence reference. Extra
browser fixtures require exact baseline restoration; otherwise keep acceptance
pending. Services may restart only outside active tests, with health readiness.

## Planning Assumptions

The spec-less edge classifier left all four requirement IDs unclassified and
unresolved because no SPEC exists. The concrete edge tests above derive from
CONTEXT/research; they do not imply the classifier ran successfully or cleared
its unresolved items. UI gate frontend=true/hasUiSpec=false/block=false requires
no new UI-SPEC, while actual visual acceptance remains pending. See
03-SOURCE-AUDIT.md for four-source coverage, contribution decisions and file
ownership. No schema, external service or package addition is planned.

## Validation Sign-Off

- [ ] All tasks have automated verification or owning test creation dependencies
- [ ] No three consecutive tasks without automated verification
- [ ] No missing test references at execution time
- [ ] No watch flags or zero-test passes
- [ ] Runtime measured and feedback latency reviewed
- [ ] Full native suite and required baseline green
- [ ] Browser evidence recorded
- [ ] nyquist_compliant set only after validation audit

**Approval:** pending execution
