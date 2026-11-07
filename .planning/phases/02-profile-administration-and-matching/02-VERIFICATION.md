---
phase: 02-profile-administration-and-matching
verified: 2026-11-06T21:07:39Z
status: human_needed
score: 37/39 must-haves verified
covered_files: [".planning/phases/02-profile-administration-and-matching/02-01-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-01-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-02-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-02-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-03-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-03-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-04-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-04-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-05-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-05-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-06-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-06-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-07-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-07-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/02-08-PLAN.md",".planning/phases/02-profile-administration-and-matching/02-08-SUMMARY.md",".planning/phases/02-profile-administration-and-matching/evidence/profile-retirement-after.json",".planning/phases/02-profile-administration-and-matching/evidence/profile-retirement-before.json",".planning/phases/02-profile-administration-and-matching/evidence/profile-runtime-after.json",".planning/phases/02-profile-administration-and-matching/evidence/profile-runtime-before.json","CLAUDE.md","Makefile","README.md","docker-compose.yml","docker/Dockerfile","docs/development/profiles.md","netbox_custom_field_profiles/__init__.py","netbox_custom_field_profiles/api/serializers.py","netbox_custom_field_profiles/api/urls.py","netbox_custom_field_profiles/api/views.py","netbox_custom_field_profiles/forms.py","netbox_custom_field_profiles/matching.py","netbox_custom_field_profiles/migrations/0001_initial.py","netbox_custom_field_profiles/migrations/0002_profiles.py","netbox_custom_field_profiles/migrations/0003_retire_legacy_configuration.py","netbox_custom_field_profiles/models.py","netbox_custom_field_profiles/navigation.py","netbox_custom_field_profiles/signals.py","netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js","netbox_custom_field_profiles/tables.py","netbox_custom_field_profiles/template_content.py","netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html","netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html","netbox_custom_field_profiles/tests/__init__.py","netbox_custom_field_profiles/tests/runner.py","netbox_custom_field_profiles/tests/test_lifecycle.py","netbox_custom_field_profiles/tests/test_matching.py","netbox_custom_field_profiles/tests/test_permissions.py","netbox_custom_field_profiles/tests/test_preservation.py","netbox_custom_field_profiles/tests/test_schema.py","netbox_custom_field_profiles/tests/test_selection.py","netbox_custom_field_profiles/tests/test_tracer.py","netbox_custom_field_profiles/urls.py","netbox_custom_field_profiles/views.py","pyproject.toml","scripts/sandbox.py","scripts/smoke_sandbox.py","scripts/test_profiles.py"]
covered_digest: "v4:sha256:d34a38473575b75fa5d661fcd5215100da4ac9ffeab0654b53c209d3c594eaa3"
behavior_unverified: 2
overrides_applied: 0
decision_coverage:
  honored: 16
  total: 16
  not_honored: []
behavior_unverified_items:
  - truth: "D-05: Administrators drag selected fields into an order, save and reload that same order; keyboard move controls provide the same result."
    test: "With three applicable selected fields, drag last to first and save/reopen; repeat with keyboard Move up/down."
    expected: "Exact order persists; keyboard focus remains usable and the new position is announced."
    why_human: "The native persistence tests pass, but no browser test or direct observation exercises drag/drop, keyboard events, focus or announcements."
  - truth: "Real browser evidence proves drag/keyboard order, unused-tag search and invalid-form state retention."
    test: "Execute the browser acceptance checks below, including pending manual changes across All save, invalid-form recovery and unused compatible/unrestricted tag search."
    expected: "Browser interactions reach the validated server path, preserve inputs and order, and save/reload correctly."
    why_human: "Browser access host was unavailable in the parent execution/review attempts. Server/API tests do not execute the browser widgets or DOM state transitions."
human_verification:
  - test: "Drag three selected fields, save, and reopen Edit."
    expected: "Dragging the last field before the first persists the exact order."
    why_human: "No executed browser drag/drop evidence; WINDOWS 1."
  - test: "Use Tab and Enter/Space on Move up/down, save, and reopen."
    expected: "The moved field retains usable focus, position is announced, boundary actions are disabled correctly, and order persists."
    why_human: "Native POST tests do not exercise keyboard focus or assistive technology; WINDOWS 1."
  - test: "Change pending manual membership/order, switch to All, save/reopen, then switch back to Selected."
    expected: "Pending additions/removals/order survive; All disables manual controls and retains native effective ordering."
    why_human: "Server regression passes; actual selector/hidden-payload synchronization remains unobserved; WINDOWS 1."
  - test: "Submit empty title with selected fields/order/rules; correct and save. Repeat after pending manual changes followed by switching to All."
    expected: "Actionable title error, unchanged persisted aggregate, retained pending choices/order/rules, and successful correction."
    why_human: "Server bound-form recovery is tested, but browser reconstruction and input usability are unverified."
  - test: "Search unused Device-compatible and unrestricted tags in the native profile widget; select/save/reopen."
    expected: "Both tags are discoverable and retained without needing prior Device assignment."
    why_human: "Native API/queryset proof does not execute the live search widget; WINDOWS 2."
  - test: "Clear all three rule selectors, add a rule, then clear it again; save."
    expected: "Applies to all Devices immediately appears/hides/returns, scope changes are politely announced, and no extra unrestricted-save confirmation appears."
    why_human: "Source and server rendering are present; actual change events and announcements are unobserved; WINDOWS 2."
  - test: "Disable JavaScript, then separately block the ordering asset; restore and reload."
    expected: "Actionable noscript/loading guidance remains visible on failure and clears after successful initialization."
    why_human: "The recovery copy exists, but the actual degraded browser paths have not been observed."
  - test: "Review list, detail and edit pages at desktop 1440x900, tablet 768x1024 and mobile 375x812 with long field/filter labels."
    expected: "Readable layout and errors, usable controls and visible focus, no obstructive overflow, and acceptable native-theme contrast."
    why_human: "No screenshots or rendered visual assessment exist; the UI review left four visual pillars unassessed."
---

# Phase 2: Profile administration and matching Verification Report

**Phase Goal:** Administrators can define reusable Device profiles and determine which profiles match a Device.
**Verified:** 2026-11-06T21:07:39Z
**Status:** human_needed
**Re-verification:** No — initial verification; no previous Phase 2 VERIFICATION.md existed.

## Goal Achievement

The implementation supports the four roadmap success criteria in native server tests. Complete Phase 2 acceptance is **not established**: two explicit PLAN truths require browser behavior that has not been exercised. There are no demonstrated implementation blockers, but eight manual checks remain. Do not mark the phase complete or treat this report as permission to bypass browser acceptance.

This verification read the actual models, forms, matching, signals, views, routes, navigation, tables, templates, JavaScript, migrations, test runner and all seven test modules. SUMMARY documents supplied scope/history only. Behavioral evidence comes from verifier-owned named native tests, raw current-session command results supplied by the orchestrator/fixer, and inspected saved count/hash captures. No browser pass is inferred from HTTP 200, source presence or the native test client.

The mandatory project documents, all eight PLAN/SUMMARY pairs, CONTEXT/RESEARCH, validation/security/review/fix/disposition/UI artifacts, WINDOWS ledger and Phase 1 VERIFICATION were read. There are no project skill directories or configured gsd-verifier skill entries. Phase mode is absent, so MVP narrowing does not apply. No override, prohibition block or backstop-tier truth is declared.

### Observable Truths

Rows 1–4 retain the roadmap contract verbatim. The 54 PLAN truth declarations are merged below without reducing scope: repeated default/title/order/no-rule/native-preservation claims are consolidated; added edge and lifecycle details remain. Evidence test names refer to netbox_custom_field_profiles/tests. The current 63-test result covers all active tests named below; four independently rerun tests are detailed under Behavioral Spot-Checks.

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | An authorized administrator can create multiple Device profiles with title, enable state, order, and only Device-applicable field choices. | VERIFIED | models.py:9–40; forms.py:16–151; native generic CRUD in views.py. test_tracer.test_real_admin_crud_and_native_resolution creates distinct same-title profiles and enables explicitly; test_permissions exercises action/object authority; test_selection rejects foreign/inaccessible fields. |
| 2 | Selected mode preserves ordered membership; all-fields mode includes a newly created applicable field without editing the profile. | VERIFIED | ProfileField position ordering; forms._save_m2m writes validated positions; matching.get_profile_fields uses fresh native resolution. test_selected_order_mode_roundtrip_and_dynamic_all and test_native_all_resolution_enabled_only_and_dynamic_order assert exact order/new-field inclusion. |
| 3 | Profiles support Device Type, role, and tag filters; tests demonstrate AND across rules, OR within values, and no-rules matching all Devices. | VERIFIED | Three separate M2M sets and native optional selectors; matching.py:9–28 uses exact IDs, empty=true and tag intersection. Verifier independently ran test_fixed_and_or_any_tag_matrix successfully. |
| 4 | Profiles allow duplicate native fields across sections and managing profiles changes neither native settings nor values. | VERIFIED | Membership uniqueness is profile+field only, with no value column. test_membership_unique_per_profile_not_per_native_field and test_all_management_operations_preserve_full_native_snapshots assert shared native objects plus complete native definition/applicability/Device-value equality across management. “Sections” here means configured future sections; Device rendering belongs to Phase 3. |
| 5 | D-02/D-03/D-11/D-15 and PROF-01/03 adjacency/ordering: single nonunique title, default disabled state, distinct identities, and display_order/title/created/pk ordering in administration and matching. | VERIFIED | Model fields/Meta enforce declared defaults and ordering. Schema duplicate-title/total-order, tracer duplicate creates, and matching deterministic-ties tests assert identity and order. Consolidates 01 schema truth; 02 title/default/order and adjacency/ordering repetitions; 04 D-15/ordering. |
| 6 | Additive 0002 preserves 0001 history, existing legacy configuration and native definitions/Device data at its boundary. | VERIFIED | 0002 only creates profile/membership structures and constraint. Git diff proves 0001 unchanged from phase start. Inspected runtime-before capture still contains all three legacy rows after additive preparation; native preservation tests and captured execution history support the boundary. Later approved removal is separately verified in rows 35–38. |
| 7 | Native tests use separate PostgreSQL, reject zero tests and leave the live sandbox unchanged. | VERIFIED | runner.py rejects empty suites before setup and checks vendor/live-vs-test names before/after activation. scripts/test_profiles.py compares complete native/plugin table hashes. All four verifier-owned runs and raw 63-test execution emit PROFILE_TESTS_ISOLATED and PROFILE_LIVE_UNCHANGED; active empty-suite unit test covers rejection. |
| 8 | D-01 and PROF-01 empty: permitted users can list, create, inspect, update and delete multiple profiles through standard plugin pages; empty list and single profile are valid. | VERIFIED | URL→native view→aggregate form chain is active. Six tracer tests include real client CRUD, empty list, detail and repeat edits; internal serializer enables native delete events. |
| 9 | PROF-01 idempotency: unchanged edits preserve identity, while two explicit creates remain separate. | VERIFIED | test_real_admin_crud_and_native_resolution creates two objects, repeats edits twice and compares ordered persisted objects, then deletes exactly one. |
| 10 | PROF-01 concurrency / invalid or denied aggregate saves leave title, mode, enabled, rule sets and memberships unchanged. | VERIFIED | Native transaction plus aggregate validation and ordered field-before-profile locking. Permission tests compare full aggregates after forged/denied/post-save-constrained mutations and injected membership failure. Verifier independently reran test_constrained_lists_direct_urls_and_post_save_rollback. Stale-save/deletion and real two-connection regressions are included in the current 63-test run. |
| 11 | PROF-03 empty: blank title is rejected and a valid new profile starts disabled. | VERIFIED | Required native ModelForm title; model enabled=False. test_invalid_posts_preserve_existing_configuration and schema/tracer assertions verify rejection and unchanged stored state. |
| 12 | D-05: Administrators drag selected fields into an order, save and reload that same order; keyboard move controls provide the same result. | PRESENT_BEHAVIOR_UNVERIFIED — WARNING / UNCERTAIN | profile_fields.js implements move, drag/drop, hidden order synchronization, focus and live status; edit template loads it; native server order persists. No executed browser test exercises these DOM events. WINDOWS 1 remains open; human checks 1–2. |
| 13 | D-06 / PROF-05 ordering: dynamic All mode preserves native group_name/weight/name order on each resolution, including additions. | VERIFIED | matching.py calls CustomField.objects.get_for_model(Device) without a new sort, guarded by live active applicable IDs. Schema test expects explicitly ordered [new,z,a], intentionally different from name order, and also compares native manager output. |
| 14 | D-07: Selected → All → Selected preserves remembered manual membership/order, including pending changes submitted with All. | VERIFIED | Explicit remembered_fields rebinding/validation and atomic membership persistence; omitted payload preserves saved rows. Verifier independently reran test_pending_manual_changes_survive_native_all_save_and_selected_reopen (reorder/add/remove subcases). This proves the server transition; actual browser mode switching is retained in row 33. |
| 15 | D-08: Selected mode requires at least one applicable field and atomically rejects forged/duplicate/malformed membership/order IDs. | VERIFIED | forms._parse_field_ids demands unique positive integer list, exact chosen/order sets and scoped native choices; Selected empty rejected. Selection and permission tests assert stored aggregate equality for invalid inputs; current-state guard rejects stale applicability/deleting fields. |
| 16 | Each profile has at most one membership for a native field, while separate profiles remain separate and may share it. | VERIFIED | unique_profile_field DB constraint; test_membership_unique_per_profile_not_per_native_field asserts cross-profile success and same-profile IntegrityError. Preservation test uses CMTS/CPE/shared profiles with one field definition. Covers PROF-05 adjacency. |
| 17 | PROF-05 empty: All mode can resolve no active applicable fields without erasing remembered membership. | VERIFIED | test_all_empty_and_temporary_inactive_preserve_membership changes the native field to provisioning, observes empty result and retained rows before/after All save. Explicit empty remembered All state is separately tested. |
| 18 | D-09: Exactly three optional searchable selectors configure Device Types, roles and applicability tags. | VERIFIED | forms.py:16–28 declares three DynamicModelMultipleChoiceFields with separate rule_fields; native API/queryset test asserts type, optionality, real POST persistence and discovery. Live widget interaction is unverified in row 33. |
| 19 | D-10: Empty criteria render Applies to all Devices and save without extra unrestricted confirmation. | VERIFIED | Form predicate, escaped server template notice, native save path and test_scope_columns_notice_and_escaped_labels prove response and save behavior. Dynamic DOM notice changes/announcements require human check 6. |
| 20 | D-12: Unused Device-compatible and unrestricted tags are offered; other-type-only tags are excluded. | VERIFIED | Tag queryset uses object_types=Device OR unrestricted, distinct; native widget query_params uses for_object_type_id. test_searchable_fields_unused_tags_and_invalid_post_preservation exercises actual /api/extras/tags/ response and saved tags, and rejects foreign tag POST. Browser widget proof remains row 33. |
| 21 | D-04: List shows title, enabled state, display order, field mode and readable applicability summary. | VERIFIED | tables.py Meta/default_columns and render_applicability call matching summary; native list test checks columns/summary and escaped labels. Rendered visual quality remains human check 8. |
| 22 | MATCH-02 precision: matching uses native integer identities and exact tag-set membership, with no rounding/tolerance. | VERIFIED | Direct ID-set membership and intersection in matching.py; fixed-rule test asserts exact ordered profile identities for two distinct Device types/roles/tag sets. |
| 23 | MATCH-03 adjacency: two matching tags yield one occurrence; distinct profiles remain distinct. | VERIFIED | Matcher appends each candidate once; native matrix has two matching tags and asserts exact list without duplicates. Duplicate-title schema/tracer cases preserve separate objects. |
| 24 | MATCH-03 empty: no enabled profiles returns empty; enabled no-rule profiles match any Device. | VERIFIED | Enabled/content-type candidate filter and empty-set checks; schema/tracer and test_empty_disabled_and_deterministic_ties cover empty/all-disabled/unrestricted cases. |
| 25 | MATCH-03 idempotency: repeating resolution against unchanged data yields identical ordered profile IDs. | VERIFIED | Read-only resolver, deterministic model ordering; test_fixed_and_or_any_tag_matrix explicitly repeats and compares results. |
| 26 | MATCH-03 concurrency: failed configuration transactions publish no partial rules; committed native target deletion leaves affected profiles disabled. | VERIFIED | test_failed_transaction_does_not_publish_partial_rules raises after form save and verifies original rules. Native target deletion/rollback matrix verifies disable-before-reference-loss. |
| 27 | D-13: Deleting any referenced Device Type, role or tag disables every affected profile even if selected values remain. | VERIFIED | signals.disable_target_profiles runs pre_delete using the native DB alias; ready() registers all three senders. test_filter_target_deletion_matrix covers instance/queryset, multiple affected and unrelated profiles, and retained filter values. |
| 28 | D-14: Field deletion/applicability loss removes invalid memberships; newly empty Selected disables, partial Selected and All remain usable. | VERIFIED | signals.remove_field_memberships plus native deletion and both-direction relation handlers. Verifier independently ran test_applicability_remove_clear_set_both_directions, all six forward/reverse remove/clear/set subcases. Full suite additionally covers deferred/queryset deletion, partial/last/All, stale-save and insertion/cleanup races. |
| 29 | D-16: Cleanup never re-enables; correcting references requires explicit administrator enablement. | VERIFIED | Cleanup only updates enabled=False. test_filter_deletion_rollback_and_explicit_reenable and test_applicability_partial_all_rollback_and_no_reenable prove correction remains disabled and explicit form enable succeeds. |
| 30 | Cleanup is idempotent and transactional; rollback restores memberships and enable state. | VERIFIED | Stable dispatch_uid, same native transaction and nested atomic cleanup; tests replay registration/cleanup and roll back field/filter/applicability deletion, including every target kind. Raw current 63-test run includes these behavioral assertions. |
| 31 | Plugin cleanup writes only plugin tables and leaves native definition/value cleanup to NetBox. | VERIFIED | signals.py mutations target CustomFieldProfile/ProfileField only; CustomField queries/locks are read-only. Preservation tests compare unrelated native definitions/values during native deletion and complete snapshots across profile operations. Direct SQL/through-table bypass is explicitly excluded, with defensive resolver tests. |
| 32 | Native action/constrained-object authority applies to navigation, direct GETs and POSTs. | VERIFIED | Native generic views/restricted form references, menu permissions and CSRF middleware retained. Six permission tests use non-superusers with each action and object constraints, compare aggregate state, and reject excluded GET/POST/CSRF. Verifier's constrained rollback rerun passed. |
| 33 | Real browser evidence proves drag/keyboard order, unused-tag search and invalid-form state retention. | PRESENT_BEHAVIOR_UNVERIFIED — WARNING / UNCERTAIN | No browser screenshots or interaction capture exist. Native request tests prove server state, not DOM/widget behavior. Required PLAN human-check blocks from 02-03/04/06 are harvested into the manual checklist; WINDOWS 1/2 remain open. |
| 34 | CustomFieldProfile is the sole active configuration representation; old API/panel is retired without implementing the Device Parameters tab. | VERIFIED | Only new CRUD routes/menu; empty API urlpatterns and template_extensions; no legacy runtime model imports. test_retired_runtime_has_no_legacy_api_or_panel_registration plus native Device-page template-not-used assertion and serializer CRUD test cover live registration. Intentional inert discovery modules are not stubs. |
| 35 | Runtime consumer retirement preserves old configuration rows and native data before schema deletion. | VERIFIED | Inspected original metadata captures, now copied under evidence/profile-runtime-before.json and profile-runtime-after.json: identical counts, all three legacy tables retain one row, identical full-row hash 2ca44fe941993eb135d159952ca56812021a9fb9a63617f1c424c4636c17861e. Inspected capture script hashes ordered complete Device/native-field/plugin rows. |
| 36 | Restarted sandbox reaches native profile pages before the destructive schema decision. | VERIFIED | Raw parent execution evidence establishes successful pre-decision restart/HTTP route checks; runtime-retirement native route/event tests exercise the same active pages. The committed 02-08 decision follows the separately verified runtime boundary; no destructive action was rerun by this verifier. |
| 37 | After explicit execution decision, a native forward migration removes only obsolete plugin structures while preserving native definitions/Device values. | VERIFIED | User decision is committed in 1ca2e53. 0003 removes constraints/fields only on CustomTabConfig/Group/Field and deletes those models. Original retirement captures show old counts 1/1/1 → absent, unchanged native/new-profile counts and full-row hash a9eea3c6e89766d10110e8ad3087930607b5318e4d28ce065350254cab9207f3. |
| 38 | 0001 history remains intact; native system/migration checks and complete profile/baseline suites pass. | VERIFIED | 0001 unchanged in phase diff. Raw make test-profiles exit 0: 63 tests/12.066s, isolated DB/live unchanged. Raw final bounded make test exit 0: 35 helpers, schema/runtime/registration/auth/negative controls/seed. sandbox.runtime runs check, migrate --check and plugin makemigrations --check --dry-run. |
| 39 | Post-retirement sandbox boots, profile administration is reachable, and selection/matching behavior remains. | VERIFIED | Final restarted parent baseline emits RUNTIME_OK/BASELINE_SMOKE_OK; current 63-test run exercises migrated schema, actual CRUD and populated profile behavior. Four verifier-owned native runs pass afterward. The live profile tables being empty is not used as populated feature proof. |

**Score:** 37/39 truths verified; 2 present, behavior-unverified. No FAILED truths or accepted overrides. The passing backend score does not certify the browser checks.

### Required Artifacts

All 17 PLAN artifact declarations passed query verify.artifacts: plan totals 3/3, 3/3, 2/2, 1/1, 2/2, 3/3, 2/2, 1/1. Repeated paths are counted as declarations. Manual substance and consumer checks:

| Artifact | Expected | Status | Substance and wiring |
| --- | --- | --- | --- |
| models.py / 0002_profiles.py | Plural profile and ordered membership schema | VERIFIED | Native model, FK/M2M references, per-profile field uniqueness and total ordering; migration creates exactly these structures; used by views/forms/matching/signals/tests. |
| matching.py | Reusable enabled matching/native field resolution | VERIFIED | Real native/profile queries and exact rule logic; consumed by summaries/table and native feature tests; available boundary for later phases. No Device tab consumer required yet. |
| forms.py | Native scoped aggregate form | VERIFIED | Actual native CRUD edit form; strict payload and reference validation, remembered state, transaction/current-state guards and ordered membership writes. |
| views.py / urls.py / navigation.py / tables.py | Standard reachable CRUD | VERIFIED | Named menu→route→native generic views, permission-aware controls, actual model queryset/table data. |
| profile_fields.js / edit template | Drag/keyboard/state synchronization | VERIFIED artifact; behavior WARNING | Packaged script is loaded by active edit view/template; listeners and hidden payload are substantive. Runtime DOM behavior remains untested. |
| detail template | Actual profile configuration | VERIFIED | Active detail view renders DB-backed title/mode/order/enable, rule sets and memberships; dynamic All mode clearly distinguishes remembered fields. |
| signals.py / plugin ready() | Native lifecycle integration | VERIFIED | Stable registered native deletion/relation receivers; same-transaction plugin-only cleanup and coordinated locks. |
| api/urls.py / views.py / serializers.py / template_content.py | Runtime retirement and native event compatibility | VERIFIED | Intentionally empty public API/template extension resources; internal read-only event serializer remains wired by native events. |
| 0003_retire_legacy_configuration.py | Approved legacy-only retirement | VERIFIED | Depends on 0002, removes compound constraints before their fields, then three legacy models only; schema-state test and captured native counts substantiate application. |
| tests/*.py / tests/runner.py | Durable native schema/CRUD/selection/matching/lifecycle/authority/preservation proof | VERIFIED | 63 active assertions run under native Django/PostgreSQL; no legacy model imports or unconditional old-table-presence invariant. |
| scripts/test_profiles.py / Makefile | Isolated fail-closed entry point | VERIFIED | Make invokes script; script invokes named ProfileTestRunner, compares live snapshots and rejects zero tests/nonzero result. |
| pyproject.toml | Packaged static/template assets | VERIFIED declaration | setuptools package-data includes templates/**/*.html and static/**/*.js; no runtime dependency added. Earlier wheel/static delivery was checked during execution; no wheel rebuild was repeated here. |
| docs/development/profiles.md | Actual administration/limits/checks | VERIFIED | Matches current source, native commands, lifecycle bypass boundary and explicit browser-pending status. |

Paths in this and the following source tables are relative to netbox_custom_field_profiles unless prefixed otherwise.

### Key Link Verification

The literal-path helper returned unverified for all 13 key-link declarations: relative Python imports, URL names, CLI runner labels and symbolic native components do not contain the target filesystem strings it expects; two source declarations are component descriptions rather than paths. These helper results were not treated as runtime defects or silently counted as wired. Each actual connection was independently traced below.

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| models.py | 0002 schema | Native migration graph | WIRED | Matching fields/constraints and 0002→0001 dependency; schema tests check final tables; baseline checks migration drift. |
| Makefile / scripts/test_profiles.py | tests/runner.py | --testrunner netbox_custom_field_profiles.tests.runner.ProfileTestRunner | WIRED | Exact runner label at subprocess invocation; observed isolation marker proves execution. |
| navigation.py | urls.py | Named list/add plugin URLs | WIRED | Native reverse/navigation tracer checks URL targets; routes name actual native views. |
| views.py | forms.py / model/table/templates | Imports and form/queryset/table/template_name | WIRED | Real client CRUD persists through native ObjectEditView; permissions/rollback tests exercise dispatch. |
| edit template / profile_fields.js | forms.py | selected_fields, field_order, remembered_fields and field_mode | WIRED; browser behavior unverified | DOM IDs match bound native fields; JS syncs JSON at render/change/submit; native payload tests exercise the receiving backend. |
| matching.py | native CustomField manager | get_for_model(Device) plus fresh active/applicable IDs | WIRED | Exact returned native list order retained; selected output maps real membership IDs to native fields. |
| forms.py | native extras tag API/queryset | DynamicModelMultipleChoiceField / for_object_type_id | WIRED; live widget unverified | API test returns unused compatible/unrestricted tags; server validates equivalent scoped query. |
| matching.py | models.py/native Device | Enabled queryset and reference intersections | WIRED | Real profile/type/role/tag fixtures yield exact expected profiles. |
| plugin __init__.py | signals.py | ready() → signals.register() | WIRED | Explicit import/call; stable dispatch IDs; native lifecycle tests run actual signals. Covers repeated 02-05/07/08 declarations. |
| native pre_delete/m2m_changed | plugin tables | Registered sender-specific callbacks | WIRED | Instance/queryset/deferred/reverse/clear/remove/set and rollback tests observe changed plugin rows. |
| native ObjectPermission | CRUD querysets/forms | Inherited native generic views | WIRED | Direct excluded GET/POST and post-save constrained rollback verified with real non-superusers. |
| native event serialization | internal profile serializer | NetBox serializer convention | WIRED | Delete/create/edit requests pass; preservation suite asserts serialized title and no public profile API. |

No key link is observably NOT_WIRED or PARTIAL. Browser behavior warnings are tracked separately from source wiring.

### Data-Flow Trace (Level 4)

| Artifact | Data variable | Real source | Produces real data | Status |
| --- | --- | --- | --- | --- |
| Generic profile list / table | table records and applicability | CustomFieldProfile queryset; actual related DeviceType/DeviceRole/Tag rows | Yes; native client tests create and render populated rows | FLOWING |
| Profile detail | object title/mode/order/enabled/rules/profile_fields | Native ObjectView restricted DB queryset and related memberships/fields | Yes; escaped values and actual persisted memberships | FLOWING |
| Profile edit | initial/bound choices, ordered and remembered IDs | Saved ProfileField rows or submitted bound input, validated against native reference querysets | Yes; test client save/reopen/error recovery asserts values | FLOWING |
| Tag search selector | search options | Native /api/extras/tags/ with for_object_type_id | Yes; unused compatible/unrestricted fixtures returned by real native API | FLOWING; browser widget unverified |
| Selected ordering DOM | field labels and IDs | Rendered native select options plus field_order bound value | Source is connected and JS uses textContent | FLOWING source; DOM transition unverified |
| Matching/field service | matching profiles and effective fields | Enabled profiles/reference sets, Device facts/tags and live native CustomField manager | Yes; populated native fixture matrix and dynamic additions | FLOWING |

No hardcoded empty rendered data source, hollow prop or mock replacement for production querying was found. Non-Device guard returns [] and intentionally retired empty discovery lists are deliberate supported behavior.

### Behavioral Spot-Checks

Each verifier-owned command ran exactly one named native test, completed in under 10 seconds, returned exit 0 and confirmed PROFILE_TESTS_ISOLATED / PROFILE_LIVE_UNCHANGED / PROFILE_TESTS_OK. Writes were confined to the separate native test database; no live service was started, reset or restarted by this verifier.

Command prefix for each named check: python3 scripts/test_profiles.py --label

| Behavior | Exact label / command | Observed result | Status |
| --- | --- | --- | --- |
| Pending manual order/add/remove persists across All save and Selected reopen | netbox_custom_field_profiles.tests.test_selection.ProfileSelectionTests.test_pending_manual_changes_survive_native_all_save_and_selected_reopen | Ran 1 test in 0.717s; OK; wrapper 5.02s | PASS |
| Fixed AND/OR/tag-any/no-rule/disabled/dedup matrix | netbox_custom_field_profiles.tests.test_matching.ProfileMatchingTests.test_fixed_and_or_any_tag_matrix | Ran 1 test in 0.327s; OK; wrapper 4.52s | PASS |
| Native constrained list/direct URL/post-save rollback | netbox_custom_field_profiles.tests.test_permissions.ProfilePermissionTests.test_constrained_lists_direct_urls_and_post_save_rollback | Ran 1 test in 0.744s; OK; wrapper 5.07s | PASS |
| Applicability cleanup forward/reverse remove/clear/set | netbox_custom_field_profiles.tests.test_lifecycle.ProfileLifecycleTests.test_applicability_remove_clear_set_both_directions | Ran 1 test in 0.308s; OK; wrapper 4.41s | PASS |
| JavaScript syntax | node --check netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js | Exit 0 | PASS |
| Whitespace/integrity | git diff --check | Exit 0 | PASS |
| Current complete native suite — raw supplied tool output, not rerun here | make test-profiles; fixer tool session 63589, exit 0 | Found/Ran 63 tests; 12.066s; OK; isolated PostgreSQL and live unchanged; wrapper 17.09s | PASS |
| Final restarted native/baseline — raw supplied parent tool output | node /Users/mwallraf/.codex/gsd-core/bin/gsd-tools.cjs run-with-timeout 600 -- make test; parent tool session 97104, exit 0 | 35 helpers/0.121s; OK; PRE_BOOTSTRAP_SCHEMA_ABSENT, SANDBOX_READY, CONFIG_OK, RUNTIME_OK NetBox=4.7.4-Docker-5.1.1, BASELINE_SMOKE_OK runtime/schema/registration/admin-session/native-token/negative-controls, SEED_IDEMPOTENT_OK | PASS |
| Browser drag/keyboard/modes/search/error recovery/rendering | Planned checks in 02-03/04/06 and profiles.md | Browser access host unavailable in parent attempts; no target/screenshots/interaction evidence. This verifier did not repeat the unavailable browser path. | SKIP → human verification |

No broad suite was repeated merely to recreate captured evidence. The optional historical pytest suite remains unexecuted and is not claimed to pass. The existing LOGIN_REQUIRED FutureWarning is recorded separately from failures.

### Probe Execution

No executable probe-*.sh is declared by these plans/summaries or present conventionally under scripts. Mentions of deterministic planning probes are assumption-classification inputs, not runnable shell probes. Step 7c is N/A; native named tests and actual baseline commands above provide behavioral execution evidence. No SUMMARY PASS count substitutes for a probe.

### Requirements Coverage

All ten Phase 2 requirement IDs occur in PLAN frontmatter and in the roadmap/REQUIREMENTS traceability table. There are **zero orphaned Phase 2 requirements**. Existing completion checkboxes are workflow metadata and were not used as proof.

| Requirement | Source plans | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| PROF-01 | 02,04,06,07,08 | Native list/create/edit/delete multiple Device profiles | SATISFIED, automated | Real tracer requests, action/object permissions and active menu/routes. Visual/manual flow quality remains in human checklist. |
| PROF-02 | 01,02,03,06,08 | Device-only selector and applicable native field choices | SATISFIED | Device content-type queryset/model clean, native scoped choices, forged/restricted/deleting ID rejection. |
| PROF-03 | 01,02,04,06 | Title, order, enabled state | SATISFIED | Model defaults/nonuniqueness/ordering and persisted client edits. |
| PROF-04 | 03,05,06 | Ordered explicit selected fields | NEEDS HUMAN for browser acceptance; server SATISFIED | Exact persisted positions, mode/invalid payload/race tests pass; actual drag/keyboard unrun (truth 12). |
| PROF-05 | 01,02,03,05,06 | Dynamically include new applicable fields | SATISFIED | Native resolver with explicit new-field order assertions and empty/provisioning guard; browser mode-switch check retained separately. |
| PROF-06 | 03,06 | Native field shared across profiles | SATISFIED | DB uniqueness only within profile and CMTS/CPE/shared native-object preservation test. |
| MATCH-01 | 04,05,06 | Zero or more fixed type/role/tag rules | NEEDS HUMAN for live widget acceptance; server/API SATISFIED | Real rules save and native tag search API; live unused-tag widget unrun (truth 33). |
| MATCH-02 | 04,06 | AND across rules, OR within values, tags-any | SATISFIED | Exact native matrix independently rerun by verifier. |
| MATCH-03 | 01,02,04,05,06 | Unrestricted no-rule matching; enabled matches only | SATISFIED | Empty/disabled/non-Device/dedup/order tests and native lifecycle disable/explicit re-enable. |
| DATA-01 | 01–08 | Profile management preserves native definitions/visibility/values | SATISFIED | Full native snapshot regression, plugin-only mutation inspection and saved runtime/retirement full-row hash equality. |

No Parameter tab or Edit Parameters implementation is demanded by Phase 2. Phase 3/4 explicitly own those capabilities. Phase 5's end-to-end release testing does not specifically defer the Phase 2 drag/keyboard/widget acceptance; those warnings remain here.

### Decision Coverage

All trackable CONTEXT.md decisions are honored by shipped artifacts.

The owner command query check.decision-coverage-verify returned skipped=false, blocking=false, total=16, honored=16, not_honored=[] and message: **All trackable CONTEXT.md decisions are honored by shipped artifacts.** This advisory translation/implementation count is not proof of browser behavior.

| Decision | Source/test evidence | Verification limit |
| --- | --- | --- |
| D-01 | Native CRUD/navigation and permission matrix | Automated verified |
| D-02 | Single title field and native tracer | Verified |
| D-03 | No unique title/type constraint; duplicate persisted profiles | Verified |
| D-04 | Table columns/filter summary and escaped native client response | Visual quality pending |
| D-05 | JS drag/move payload plus server ordered persistence | Browser behavior unverified |
| D-06 | Native manager order, explicit nonalphabetic expected fixture | Verified |
| D-07 | Remembered payload through All save, pending changes/error recovery and omission preservation | Server verified; browser switch pending |
| D-08 | Minimum selection and exact ID/type/set validation | Verified |
| D-09 | Exactly three optional native dynamic selectors/API | Live widget pending |
| D-10 | Inline notice and ordinary native save | Dynamic notice/announcement pending |
| D-11 | Default False and explicit enable tests | Verified |
| D-12 | Correct native API parameter, unused/unrestricted fixtures | Live widget pending |
| D-13 | Native pre_delete matrix, retained values and all-target rollback | Verified |
| D-14 | Partial/last/All and both-direction field lifecycle, stale-save and concurrent insertion tests | Verified |
| D-15 | Model ordering plus native list/matcher tie tests | Verified |
| D-16 | Cleanup never enables; correction stays disabled; explicit form enable succeeds | Verified |

### Test Quality Audit

| Native test file | Linked requirement | Active | Skipped | Circular | Strongest assertion | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| test_schema.py | PROF-02/03/05/06, MATCH-03, DATA-01 | 7 | 0 | No | Exact values/identities/schema/default/order plus constraint failure | Sound |
| test_tracer.py | PROF-01/02/03, MATCH-03, DATA-01 | 6 | 0 | No | Multi-step real client CRUD and native resolution/snapshot equality | Sound |
| test_selection.py | PROF-02/04/05/06, DATA-01 | 17 | 0 | No | Native POST/reopen, exact membership/order, errors and stale-save/rollback invariants | Sound; no browser engine |
| test_matching.py | PROF-01/03, MATCH-01/02/03, DATA-01 | 7 | 0 | No | Exact match lists plus native API IDs and saved-rule preservation | Sound; no live widget |
| test_lifecycle.py | PROF-04/05, MATCH-01/03, DATA-01 | 14 | 0 | No | Native delete/relation rollback plus real two-connection PostgreSQL Lock wait and final rows | Sound |
| test_permissions.py | PROF-01/02, DATA-01 | 6 | 0 | No | Non-superuser action/constraint/CSRF matrix and complete aggregate equality | Sound |
| test_preservation.py | All Phase 2 native-data and retirement contracts | 6 | 0 | No | Full native snapshots across operations, real route/registration/serialization behavior | Sound |

**63 active tests; 0 disabled requirement tests; 0 circular expected-output generators; 0 server requirements supported only by weak existence/status assertions.** Native order parity uses the actual external/native NetBox manager and independent explicit order expectations, not plugin-produced expected fixtures. Preservation expectations are the native rows before the operation; exact equality is the requirement being tested. Mocks inject failure, force native deferred-deletion mode or pause a transaction; they do not replace the matcher, native permission engine or database oracle. Threaded regressions observe an actual pg_stat_activity Lock wait before release, rather than relying on incidental thread scheduling.

Reliance review found no specific undeclared precondition, incidental ordering or fixture-only premise needing an advisory. Native reference fields and Device facts are real caller inputs; setup explicitly establishes the supported runtime. Field-before-profile lock ordering and same-transaction split-save requirements are enforced by code.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| matching.py | 12,43 | Guard returns [] for unsupported object type | Info | Deliberate supported-scope behavior; normal Device path issues real queries. |
| api/urls.py / template_content.py | 3 / 4 | Empty discovery lists | Info | Intentional legacy API/panel retirement, covered by native registry tests. |
| profile_fields.js / edit template | — | Browser state transitions not executed | WARNING | Code is substantive/wired; truths 12/33 remain present-behavior-unverified. |
| .planning/WINDOWS.md | entries 1/2 | Unrun browser acceptance | WARNING | Existing unwaived evidence needs; no claim of closure or browser pass. |

No unreferenced TBD/FIXME/XXX, TODO/HACK/PLACEHOLDER, console-only handler, empty live data source or disabled test was found in changed active implementation/test files. Broad marker matching found sys.exit as an irrelevant substring, not a disabled test. No code was changed by this verification.

The review's two original BLOCKERs are fixed in 1f97946/07a223c and independently re-reviewed clean. Source/tests now reject stale applicability and deleting fields under coordinated locks while retaining provisioning membership. UI findings E1/C1, E2, E3 and C2 are corrected in 5b99080; current code includes validated remembered state, scope status, unavailable-script guidance and clear All-mode labels. Their historical review text is not an active defect. Security audit reports 18/18 authored threats closed at ASVS level 1; this verifier's source/test trace found no contradicting open mitigation.

### Phase 1 Regression Boundary

The prior Phase 1 report passed 24/24. Its root-checkout/preservation/environment constraints remain intact: canonical branch is retained, no worktree was created, recovery source and local secrets were not edited, 0001 and Docker/runtime/auth helper files are unchanged in the Phase 2 diff. Final real make test passes on the pinned native runtime. The baseline is intentionally evolved by additive 0002 and explicitly approved legacy-only 0003; no old installation upgrade is claimed. Optional legacy pytest remains an acknowledged unexecuted check. No destructive Phase 1 lifecycle/reset was repeated.

### Human Verification Required

The items below merge the explicit deferred human-check blocks in plans 02-03, 02-04 and 02-06 with current UI-fix/visual evidence needs. They are acceptance checks for this user-facing phase. Browser-host unavailability is an evidence limit, not proof that any interaction is broken.

Use the dedicated sandbox at http://127.0.0.1:18047/plugins/custom-field-profiles/ with authorized local credentials and disposable profiles; do not capture credentials. Record browser/version, profile IDs, observed outcomes and redacted screenshot paths.

#### 1. Drag persistence

**Test:** Select at least three applicable native fields. Drag the last before the first, save, and reopen Edit.
**Expected:** The exact new order survives, with each field present once.
**Why human:** The server accepts/persists ordered input, but no executed browser test generated it through drag events. WINDOWS 1.

#### 2. Keyboard order, focus and announcement

**Test:** Tab to Move up/down; activate with Enter/Space, move near a boundary, save and reopen.
**Expected:** Exact persisted order, usable focus after rerender, announced new position, correctly disabled boundary/All-mode controls.
**Why human:** Focus, keyboard events and assistive-technology output need a real browser. WINDOWS 1.

#### 3. Pending manual state through All mode

**Test:** Reorder, add and remove manual fields before switching to All. Save/reopen, switch back to Selected, save/reopen again.
**Expected:** Pending membership/order is remembered; All disables manual controls while using native effective ordering.
**Why human:** The named native test proves the receiving form/persistence transition, but not JS synchronization of disabled selector and hidden payloads. WINDOWS 1.

#### 4. Invalid-form recovery in both modes

**Test:** Keep several fields/order and a rule, clear the title and submit. Correct/save. Repeat after changing manual selection/order and switching to All before the invalid submit.
**Expected:** Clear required-title error, persisted aggregate unchanged until correction, pending selection/order/rules retained and usable after response/reinitialization.
**Why human:** Actual DOM/widget reconstruction and error usability remain unobserved.

#### 5. Unused-tag live widget

**Test:** Create an unused Device-compatible tag and an unused unrestricted tag through native tag administration. Search/select both on the profile form, save and reopen.
**Expected:** Both are searchable without prior Device assignment and remain selected after reload.
**Why human:** Native API/queryset tests do not execute the dynamic widget. WINDOWS 2.

#### 6. Dynamic applicability notice

**Test:** Clear all selectors, add a rule, clear it again; use assistive technology and save unrestricted.
**Expected:** Applies to all Devices appears/hides/returns immediately; polite restricted/unrestricted announcement occurs; save has no extra confirmation.
**Why human:** Source status semantics and server HTML do not prove event/announcement behavior. WINDOWS 2.

#### 7. Unavailable ordering editor

**Test:** Separately disable JavaScript and block profile_fields.js; then restore and reload.
**Expected:** Actionable noscript/loading recovery guidance; failure message remains if initialization fails and clears only after successful initialization.
**Why human:** The degraded browser states have not been exercised.

#### 8. Rendered administration quality

**Test:** Inspect list/detail/edit and validation errors at 1440×900, 768×1024 and 375×812 with long labels, including native light/dark presentation where available.
**Expected:** Readable hierarchy/errors, visible focus, usable reorder/search controls, adequate contrast and no obstructive overflow.
**Why human:** No screenshots/rendered evidence; four UI-review visual pillars remain unassessed.

### Gaps Summary

**No demonstrated implementation gap remains.** The status is human_needed because two must-have truths are present and wired but browser behavior is unverified, and the human checklist is nonempty. These are WARNING/UNCERTAIN findings, not FAILED/BLOCKER findings.

Later Phase 3/4 work explicitly owns Device tab/native editing; their absence is outside this phase. No Phase 2 browser item was deferred to a later phase or waived. WINDOWS entries 1/2 stay open. Do not mark Phase 2 complete until the listed interactions have actual evidence or the developer explicitly resolves the acceptance decision through the workflow.

Saved evidence/profile-runtime-*.json and evidence/profile-retirement-*.json are verbatim copies of the inspected original /tmp command captures, not reconstructed from SUMMARY claims. They contain only table counts and full-row digests, no native values or credentials. Temporary capture-script inspection confirmed hash scope. The verification fingerprint is generated by the CLI owner over implementation/evidence files and automatic PLAN/SUMMARY coverage; the report itself is excluded.

---

_Verified: 2026-11-06T21:07:39Z_
_Verifier: the agent (gsd-verifier)_
