---
phase: 02-profile-administration-and-matching
plan: "05"
subsystem: lifecycle
tags: [netbox, profiles, signals, native-data, transactions]
requires:
  - phase: 02-04
    provides: Native fixed applicability relations and reusable matching
provides:
  - Same-transaction disabling when native filter targets are deleted
  - Idempotent selected membership cleanup on field deletion and applicability loss
  - Defensive live status/applicability resolution with native ordering
affects: [02-06, 02-07, 03-parameters-tab, 04-edit-parameters]
tech-stack:
  added: []
  patterns: [native pre_delete receivers, bidirectional m2m lifecycle capture, plugin-only transactional cleanup]
key-files:
  created: [netbox_custom_field_profiles/signals.py, netbox_custom_field_profiles/tests/test_lifecycle.py]
  modified: [netbox_custom_field_profiles/__init__.py, netbox_custom_field_profiles/matching.py]
key-decisions:
  - Cleanup writes only plugin tables and never implicitly re-enables profiles.
  - Direct SQL and bulk through-table mutations bypass synchronous cleanup; fresh resolution still excludes invalid or inactive fields.
requirements-completed: []
coverage:
  - id: lifecycle-filter-targets
    description: Deleting native filter targets disables affected profiles without broadening relevance.
    requirement: MATCH-01
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles/tests/test_lifecycle.py#test_filter_target_deletion_matrix
        status: pass
    human_judgment: false
  - id: lifecycle-selected-fields
    description: Field deletion and applicability loss clean selected memberships safely in both relation directions.
    requirement: PROF-04
    verification:
      - kind: integration
        ref: make test-profiles
        status: pass
    human_judgment: false
  - id: lifecycle-native-preservation
    description: Cleanup preserves unrelated native settings and values; isolated tests leave live data unchanged.
    requirement: DATA-01
    verification:
      - kind: integration
        ref: make test-profiles
        status: pass
    human_judgment: false
actuals:
  tokens: 5389
  tasks: 2
  commits: 4
plan_head_before: 830fe88ce91cf45ae720510771d041bd7a8f4ba2
plan_head_after: f3e69c5256ddfff2b523bd4a81b9a055570dd5ba
duration: 20 min
completed: "2026-11-06"
status: complete
---

# Phase 2 Plan 05: Native lifecycle safety Summary

**Native reference deletion now disables affected profiles, while field lifecycle changes remove invalid memberships without writing native definitions or Device values.**

## Accomplishments

- Registered filter-target `pre_delete` receivers through plugin `ready()`. Instance and queryset deletion of Device Types, roles and tags disables all affected profiles while references still exist, including profiles retaining other values in the same criterion. Deliberate form/relation removal is unchanged.
- Added transactional membership cleanup that locks affected profile aggregates, removes invalid rows and disables only Selected profiles left empty. All-mode profiles remain enabled; remaining Selected fields remain usable. Cleanup never re-enables any profile.
- Handled native CustomField `pre_delete` explicitly, including deferred deletion where the field row is still present. Added forward/reverse applicability remove/clear/set handling, with instance/database-scoped `pre_clear` capture when `pk_set` is absent.
- Preserved native field ordering while intersecting resolution with fresh active/Device-applicable IDs. Temporary provisioning hides a field without destroying its remembered selection. Direct through-table writes cannot make stale fields appear.

## Task Commits

1. `68b9106` — lifecycle contract matrix (RED).
2. `efbdff4` — Task 1 native filter-target deletion safeguards.
3. `9cc6e28` — Task 2 field deletion/applicability cleanup and defensive resolution.
4. `f3e69c5` — complete rollback matrix and native preservation assertions.

## Verification Evidence

- Initial native run: **9 tests executed, 17 expected assertion failures** from absent disabling/cleanup. No collection/import errors are used as RED evidence. `PROFILE_LIVE_UNCHANGED` held.
- Task 1 focused checks passed for all three target kinds, instance/queryset deletion, remaining criteria values, multiple affected/unrelated profiles, rollback, intentional rule removal and explicit form re-enable.
- Final `make test-profiles`: **37 tests pass**, 3.466s execution / **7.85s** helper elapsed. `PROFILE_TESTS_ISOLATED` and `PROFILE_LIVE_UNCHANGED` confirm isolated PostgreSQL and identical live native/plugin snapshots.
- **11 lifecycle tests** include ordinary/queryset/deferred field deletion, partial/last selected membership, All mode, both relation directions for remove/clear/set, unrelated type removal/no-op set, rollback, repeated cleanup/registration, explicit-only re-enable, temporary provisioning and direct through-table bypass exclusion.
- Native unrelated field definitions and Device sentinel values remain unchanged during deletion/applicability scenarios. The deleted/unassigned field's own data remains subject to NetBox's normal cleanup, as intended.
- Dedicated web/worker services restarted only after feature tests had finished. Final `make test`: **35 helper tests pass**, native runtime/schema/registration/admin-session/token/negative controls pass, and seed idempotence passes.
- `git diff --check` passes. No new dependencies, schema migration, native storage writes or extra browser claims.

## Signal Registration and Boundaries

Stable dispatch IDs:

- `custom_field_profiles.disable_deleted_device_type`
- `custom_field_profiles.disable_deleted_device_role`
- `custom_field_profiles.disable_deleted_tag`
- `custom_field_profiles.remove_deleted_field`
- `custom_field_profiles.field_applicability`

Receivers use the signal's database alias. Delete and relation-manager operations supply the native transaction; multi-write membership cleanup also uses `transaction.atomic(using=...)`. Repeated registration is deduplicated by dispatch ID. Repeated deletion/cleanup is harmless and never restores enabled state.

Direct SQL and direct/bulk through-table writes do not emit relation-manager signals and are unsupported for synchronous membership cleanup. Defensive resolution excludes currently nonapplicable/inactive fields even when invalid remembered membership survives such a bypass. Native supported lifecycle operations retain their own field-data cleanup; plugin receivers do not call native field save/data-removal or Device save methods.

## Decisions and Deviations

No product decisions changed. Cleanup and resolution implement D-13/D-14/D-16. Task 1 and Task 2 contracts were written together in one test module, then implemented in separate task commits. An additional test-only commit completed rollback coverage for every target kind. No scope expansion or dependency addition.

Requirement IDs remain pending at phase level because Plan 02-06 and subsequent verified retirement plans still declare them. Browser verification debt from prior plans remains with Plan 02-06; this plan introduces no browser interaction.

## Known Stubs and Threat Surface

None. Lifecycle hooks introduce no new endpoint or authorization layer. T-02-10/11/12 mitigations are covered by transactional cleanup, the native lifecycle matrix and preservation/isolation checks. Existing upstream LOGIN_REQUIRED deprecation warning remains unchanged; optional legacy pytest was not run or claimed as passing.

## Self-Check: PASSED

All four planned source files exist. All four listed task/test commits are reachable from HEAD. Native profile and required baseline checks pass; no unrun verification was introduced by this plan.

## Next Plan Readiness

Ready for Plan 02-06: permission/preservation integration and outstanding real browser checks. Preserve the internal profile event serializer through later API retirement.
