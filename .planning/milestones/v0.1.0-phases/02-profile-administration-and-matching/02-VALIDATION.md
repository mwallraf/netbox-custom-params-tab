---
phase: "02"
slug: "profile-administration-and-matching"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-06"
---

# Phase 2 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Native Django TestCase on pinned NetBox 4.7.4 PostgreSQL |
| Config file | Native NetBox settings; bounded preparation establishes isolated test database |
| Quick run command | `make test-profiles`; focused: `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_selection` |
| Full suite command | `make test-profiles` followed by `make test` |
| Estimated runtime | Final 02-08: 49 native tests in 7.117 s; runner 12.27 s. Focused: schema 4.56 s, matching 5.19 s, permissions 6.78 s (runner elapsed). |

## Sampling Rate

- After every task commit: focused native profile tests, once runner exists.
- After each wave: profile suite and existing baseline.
- Before verification: full suite and native migration checks must pass.
- Feedback latency target: 120 seconds for focused reruns; measure rather than claim.

## Per-Task Verification Map

All commands execute from repository root. Bounded preparation 02-01 creates the additive native schema/resolver and isolated runner. The first meaningful end-to-end user tracer is 02-02 and must pass before feature expansions 03–08.

| Task ID | Plan | Wave | Requirements | Threat Ref | Secure behavior | Test type | Automated command | File exists | Status |
|---------|------|------|--------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | PROF-02/03/05, MATCH-03, DATA-01 | T-02-03 | Additive schema, native snapshots | Native ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_schema | yes | green |
| 02-01-02 | 01 | 1 | DATA-01 | T-02-03 | Separate test DB; zero tests reject | Runner/baseline | make test-profiles; make test | yes | green |
| 02-02-01 | 02 | 2 | PROF-01/02/03/05, MATCH-03, DATA-01 | T-02-01/02 | Native CRUD/form/resolution tracer | Native client/ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_tracer | yes | green |
| 02-02-02 | 02 | 2 | PROF-01 | T-02-01 | Permission-aware native navigation | Native client | make test-profiles; make test | yes | green |
| 02-03-01 | 03 | 3 | PROF-02/04/05/06, DATA-01 | T-02-04/05/06 | Exact ordered-ID validation and rollback | Native form/ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_selection | yes | green |
| 02-03-02 | 03 | 3 | PROF-04/05 | T-02-04 | Packaged browser order and templates | Native plus browser | make test-profiles | yes | green |
| 02-04-01 | 04 | 4 | MATCH-01/02/03, DATA-01 | T-02-07/08 | Restricted references and fixed matching | Native form/ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_matching | yes | green |
| 02-04-02 | 04 | 4 | PROF-01/03, MATCH-01/03 | T-02-09 | Escaped summaries/native widget | Native client/browser | make test-profiles | yes | green |
| 02-05-01 | 05 | 5 | MATCH-01/03, DATA-01 | T-02-10 | Disable before cascade; rollback | Native transaction | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_lifecycle | yes | green |
| 02-05-02 | 05 | 5 | PROF-04/05, DATA-01 | T-02-11/12 | Idempotent plugin-only cleanup | Native transaction | make test-profiles | yes | green |
| 02-06-01 | 06 | 6 | PROF-01/02, DATA-01 | T-02-13/14 | Action/constraint/CSRF enforcement | Native client | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_permissions | yes | green |
| 02-06-02 | 06 | 6 | All Phase 2 IDs | T-02-15 | Native snapshots unchanged | Native integration/browser | make test-profiles; make test | yes | green |
| 02-07-01 | 07 | 7 | PROF-01, DATA-01 | T-02-17 | Retire obsolete runtime consumers | Native integration | make test-profiles; make check | yes | green |
| 02-07-02 | 07 | 7 | PROF-01, DATA-01 | T-02-17 | Durable native/new-profile preservation; one-time old-row evidence in summary | Native integration | make test-profiles; make test | yes | green |
| 02-08-01 | 08 | 8 | DATA-01 | T-02-16 | Explicit one-way deletion decision | Human plus baseline | make check | yes | green |
| 02-08-02 | 08 | 8 | PROF-01/02, DATA-01 | T-02-16 | Legacy-only migration, final absence introspection/schema tests, native/new-profile snapshots | Native schema | python3 scripts/sandbox.py compose exec -T netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py makemigrations netbox_custom_field_profiles --check --dry-run; make test-profiles; make test | yes | green |

Automated statuses above reuse the final post-0003 execution evidence in `02-08-SUMMARY.md`: 49 native tests and 35 helper tests pass; native migration/system checks pass. No redundant full-suite run was performed during this audit. `green` records the automated portion only; browser portions of 02-03-02, 02-04-02 and 02-06-02 remain pending below. The explicit 02-08-01 decision is recorded in `02-08-DECISION.md`; its human authorization is separate from the green baseline command.

## Requirement Coverage

Test modules are under `netbox_custom_field_profiles/tests/`. All commands run through the isolated native runner; use `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.<module>` for a focused module.

| Requirement | Behavioral tests (module: method) | Automated status |
|-------------|-----------------------------------|------------------|
| PROF-01 | test_tracer: test_real_admin_crud_and_native_resolution; test_permissions: test_each_native_action_controls_get_post_and_navigation, test_constrained_lists_direct_urls_and_post_save_rollback | COVERED |
| PROF-02 | test_schema: test_device_only_validation; test_selection: test_invalid_selection_payloads_rejected_atomically, test_restricted_choices_reject_even_otherwise_applicable_field; test_permissions: test_forged_aggregate_payloads_preserve_every_component | COVERED |
| PROF-03 | test_schema: test_duplicate_titles_default_disabled_and_total_order; test_tracer: test_real_admin_crud_and_native_resolution | COVERED |
| PROF-04 | test_selection: test_selected_order_mode_roundtrip_and_dynamic_all, test_native_page_saves_selection_and_restores_manual_order; test_lifecycle: test_applicability_remove_clear_set_both_directions | COVERED; browser reorder pending |
| PROF-05 | test_schema: test_native_all_resolution_enabled_only_and_dynamic_order; test_selection: test_all_empty_and_temporary_inactive_preserve_membership; test_preservation: test_external_native_changes_are_resolved_without_copying_values | COVERED |
| PROF-06 | test_schema: test_membership_unique_per_profile_not_per_native_field; test_preservation: test_all_management_operations_preserve_full_native_snapshots | COVERED |
| MATCH-01 | test_matching: test_searchable_fields_unused_tags_and_invalid_post_preservation, test_restricted_saved_references_cannot_be_silently_cleared; test_lifecycle: test_filter_target_deletion_matrix | COVERED; browser widget pending |
| MATCH-02 | test_matching: test_fixed_and_or_any_tag_matrix | COVERED |
| MATCH-03 | test_matching: test_empty_disabled_and_deterministic_ties, test_fixed_and_or_any_tag_matrix; test_lifecycle: test_each_filter_target_deletion_rolls_back_with_profile_state | COVERED |
| DATA-01 | test_preservation: test_all_management_operations_preserve_full_native_snapshots, test_native_lifecycle_preserves_unrelated_definitions_and_values; test_schema: test_schema_matches_applied_retirement_state | COVERED |

## Decision Coverage

| Decision | Behavioral evidence | Status / limit |
|----------|---------------------|----------------|
| D-01 | tracer CRUD and permissions action/constraint matrix | automated green |
| D-02 | tracer CRUD single title; schema duplicate-title test | automated green |
| D-03 | schema duplicate-title test and tracer separate creates | automated green |
| D-04 | matching test_scope_columns_notice_and_escaped_labels | automated green |
| D-05 | selection native page persistence/order; actual drag and keyboard interaction | server green; browser pending WINDOWS 1 |
| D-06 | schema native All ordering/dynamic additions against native get_for_model | automated green |
| D-07 | selection mode round-trip and remembered-order page reload | server green; interactive mode switch pending WINDOWS 1 |
| D-08 | selection invalid empty payload/atomic rejection | automated green |
| D-09 | matching fixed AND/OR matrix and native dynamic selector/API tests | server/API green; live search pending WINDOWS 2 |
| D-10 | matching scope/notice test and unrestricted saves | server green; dynamic notice pending WINDOWS 2 |
| D-11 | schema default-disabled and tracer explicit enable | automated green |
| D-12 | matching unused compatible/unrestricted tag API discovery and foreign-tag rejection | server/API green; widget search pending WINDOWS 2 |
| D-13 | lifecycle deletion matrix, all-target rollback, intentional removal distinction | automated green |
| D-14 | lifecycle ordinary/queryset/deferred deletion, partial/last/All membership, both relation directions | automated green |
| D-15 | schema total order; matching empty/disabled/deterministic ties | automated green |
| D-16 | lifecycle explicit re-enable and applicability rollback/no-re-enable | automated green |

## Wave 0 Requirements

- Preparation 02-01 creates plugin-owned native schema tests, isolated runner and make test-profiles.
- Runner proves isolated native PostgreSQL use and rejects zero discovered tests.
- Tracer 02-02 proves real administration CRUD/navigation and reusable matching before expansion.
- No optional historical pytest or SQLite settings dependency.

## Manual-Only Verifications

**Pending, not passed or waived.** These are existing planned browser checks, not newly discovered automated gaps. Browser host was unavailable in 02-03/04/06. WINDOWS entries 1 and 2 remain open; follow `docs/development/profiles.md#browser-acceptance-checks`. No browser retry or browser acceptance is claimed by this audit.


| Behavior | Requirement | Why manual | Test instructions |
|----------|-------------|------------|-------------------|
| Drag order and accessible alternative persist | PROF-04 / D-05 | Server tests cannot prove browser interaction | Drag three fields, save/reload; repeat using keyboard controls |
| Search unused Device-compatible tag | MATCH-01 / D-12 | Native widget integration | Search a compatible unused tag, select/save/reload |
| Error and mode-switch interaction | PROF-02, PROF-04, PROF-05 | Browser state and errors | Invalid submission retains choices; Selected → All → Selected restores order |

## Validation Sign-Off

- [x] Every task has automated verification or explicit first-tracer dependencies.
- [x] No three consecutive tasks lack automated checks.
- [x] Missing references are created before use.
- [x] No watch-mode commands; zero-test false greens rejected.
- [x] Focused runtime measured.
- [x] Native values/settings remain unchanged by plugin management.

Nyquist audit: automated coverage satisfied for all 10 Phase 2 requirements and all 16 tasks. `nyquist_compliant: true` follows the validate-phase no-automated-gap contract; it is not full Phase 2 acceptance. Browser-dependent decisions/checks above remain unverified and require human/browser evidence. Independent phase review/verification gates remain separate.

Evidence reused: `02-01-SUMMARY.md` (focused timing, empty-suite rejection), `02-04-SUMMARY.md` (matching/API), `02-05-SUMMARY.md` (lifecycle), `02-06-SUMMARY.md` (permissions/preservation), and final `02-08-SUMMARY.md` (49 native tests, 35 helpers, migration checks and live snapshot equality after retirement). Optional historical pytest remains unexecuted. Direct SQL/bulk through-table writes remain outside synchronous lifecycle guarantees; defensive field resolution has automated coverage.

## Validation Audit

**Date:** 2026-11-06

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

10/10 requirement behaviors have existing passing automated coverage. No tests created, weakened, skipped or newly run during this audit. Existing manual browser acceptance remains pending in WINDOWS 1/2; no implementation bug was established by this coverage audit.

## Post-review regression coverage

The final profile suite now has **63 passing native tests**, including new pending-All-state cases, stale form/applicability changes, real two-connection PostgreSQL insertion/cleanup locking, deferred deletion and provisioning behavior. See 02-UI-FIX.md, 02-REVIEW-FIX.md and independent clean 02-REVIEW.md for exact runs/commits. Earlier task counts remain historical execution evidence. No automated requirement gap remains; live browser acceptance is still pending in WINDOWS 1/2.
