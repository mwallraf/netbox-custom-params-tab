---
phase: "03"
slug: "parameters-tab"
status: automated-passed-manual-pending
nyquist_compliant: false
wave_0_complete: true
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
| 03-01-T1 | TAB-01 | Fresh-process reverse/resolve, native navigation, active tab, no panel | test_parameters | T-03-01, T-03-04 | automated pass; 03-01 summary and final regression |
| 03-01-T2 | TAB-01/AUTH-01 | Match/zero-field/no-match states; Device authority before resolution; Device-only/profile-admin-only subjects; unsupported POST | test_parameters, test_parameter_permissions | T-03-01, T-03-02, T-03-03 | automated pass; 03-01 summary and final regression |
| 03-02-T1 | TAB-02/TAB-03 | CMTS/CPE/shared matching, duplicate titles/order, Selected/All order/dynamic fields, fresh duplicate native values | test_parameters | T-03-06 | automated pass; 03-02 summary and final regression |
| 03-02-T2 | TAB-03/AUTH-01 | All 13 types; false/zero/JSON empties; Hidden/If Set; native label/help and settings preservation | test_parameter_rendering | T-03-05, T-03-07 | automated pass; 03-02 summary and final regression |
| 03-03-T1 | AUTH-01 | Scalar missing/denied, mixed/all-denied multiobjects; no ID/label/link/count leaks; alternating users | test_parameter_permissions | T-03-04, T-03-08, T-03-09 | automated pass; 03-03 summary and final regression |
| 03-03-T2 | TAB-03/AUTH-01 | Full URL text/native scheme safety, sanitized Markdown/line breaks, escaped JSON/metadata, local overflow markup | test_parameter_rendering, test_parameter_permissions | T-03-07, T-03-10, T-03-11, T-03-12 | automated pass; visual presentation pending |
| 03-04-T1 | TAB-01/TAB-02/TAB-03/AUTH-01 | Complete native/profile snapshots, legitimate native-write freshness, excluded-value retention, native baseline | cases owned by test_parameter_permissions; all three focused modules as regression gates; make test-profiles; make test | T-03-03, T-03-05, T-03-13, T-03-14 | automated pass; measured results below |
| 03-04-T2 | TAB-01/TAB-02/TAB-03/AUTH-01 | Actual browser acceptance, fixture restoration, accurate docs and evidence | scoped git diff --check HEAD before task commit plus manual matrix below | T-03-12, T-03-14, T-03-15, T-03-16 | docs/whitespace pass; 15 browser cases pending in 03-UAT.md |

Module names above expand to the exact focused commands in Test Infrastructure.
All automated behavioral commands must exit zero, report nonzero executed tests,
and emit PROFILE_TESTS_ISOLATED and PROFILE_LIVE_UNCHANGED. Each plan also carries
T-03-SC: no installs/upgrades; any newly proposed install requires a legitimacy
audit before execution. ASVS 5.0.0 L1 applies; unresolved high/critical threats
block acceptance. Execution results and their actual limits are recorded below.
Plan 04 owns only test_parameter_permissions.py and five documentation/evidence
files. Production defects reopen their original owning implementation task;
existing ordering/type modules remain unchanged regression inputs to this plan.

## Wave 0 Requirements

03-01-T1 creates test_parameters; 03-01-T2 creates test_parameter_permissions;
03-02-T2 creates test_parameter_rendering, reusing native Device fixture and
ObjectPermission patterns. The first tracer must pass cold-start
reverse/resolve/navigation without a test-side view import before expansion.
No framework installation or standalone test-infrastructure plan is needed.
All three modules now exist and have executed successfully in their owning plans
and in the final Plan 03-04 regression. This establishes wave_0_complete, not
Nyquist compliance or browser acceptance.

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

- [x] All tasks have automated verification or owning test creation dependencies
- [x] No three consecutive tasks without automated verification
- [x] No missing test references at execution time
- [x] No watch flags or zero-test passes
- [x] Runtime measured and feedback latency reviewed
- [x] Full native suite and required baseline green
- [ ] Browser evidence recorded
- [ ] nyquist_compliant set only after validation audit

**Approval:** automated gates pass; browser acceptance pending; no validation audit
has granted Nyquist compliance.

## Actual Plan 03-04 Execution — 2026-11-07

| Command | Actual result | Native test time | Runner elapsed |
|---------|---------------|------------------|----------------|
| `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameters` | 7 pass | 1.146 s | 5.98 s |
| `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_rendering` | 8 pass | 1.154 s | 5.56 s |
| `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_permissions` | 11 pass | 4.881 s | 9.60 s |
| `make test-profiles` | 89 pass | 17.229 s | 21.83 s |
| `make test` | 35 helper tests pass; required baseline pass | 0.112 s helper suite | whole-command elapsed not instrumented |

All four profile runs emitted `PROFILE_TESTS_ISOLATED` (PostgreSQL test database
differs from live) and `PROFILE_LIVE_UNCHANGED`. No zero-test runs, live reset,
dependency installation, service restart or migration was introduced. `make test`
reported `CONFIG_OK`, `RUNTIME_OK NetBox=4.7.4-Docker-5.1.1`,
`BASELINE_SMOKE_OK runtime/schema/registration/admin-session/native-token/negative-controls`
and `SEED_IDEMPOTENT_OK`. The existing LOGIN_REQUIRED deprecation is unchanged.
The focused feedback is below the planned 30-second target; the full runner is
also below that target on this run. Prior-plan timings are in their summaries.

03-04 adds three test methods, with no production correction needed. The complete
native snapshot includes every CustomField column, field/object-type through row,
CustomFieldChoiceSet column and Device custom_field_data; the plugin aggregate
includes complete profiles, memberships and all three fixed-rule through tables.
Every allowed, constrained-denied, no-authority and anonymous Device/Parameters
GET, related-denied response, no-match/zero-field GET and forged unsupported POST
is checked against a snapshot around that individual request. Native saves update
text, integer, boolean, JSON and choice values between two ordinary GETs, with both
duplicate sections refreshed and no additional writes; unrelated stored values and
native definitions/settings/choices/applicability stay unchanged. Membership,
filter relevance and enable-state changes retain excluded stored values.

| Threat | Observed evidence/status |
|--------|--------------------------|
| T-03-13 | Complete individual request snapshots pass, including populated fixed-rule tables, native applicability and choice settings |
| T-03-14 | All profile runs isolated and live-unchanged; browser discovery created no fixture or live change; future fixture restoration remains required before UI acceptance |
| T-03-15 | No generated credential output or browser authentication performed; documentation/evidence contains no credentials |
| T-03-16 | Actual counts/timings and browser failure recorded; UAT-01–15 pending with fixture/actions/expected outcomes, no invented observations |
| T-03-SC | No install, upgrade or dependency change |

`mcp__cua_repl` discovery returned no browsers and the exact error **The browser
access host is unavailable**. No visual test ran. `03-UAT.md` contains all D-01
through D-15 cases, proposed desktop/narrow viewports and the observed blocker.
WINDOWS entry 3 tracks this unrun verification. The documentation whitespace
check against HEAD passed before the task commit. No manual pass or phase
verification is inferred from these automated results.
