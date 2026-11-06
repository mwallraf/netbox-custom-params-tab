---
phase: 02-profile-administration-and-matching
plan: "06"
subsystem: testing
tags: [netbox, django, postgres, permissions, preservation]
requires:
  - phase: 02-05
    provides: Native profile CRUD, ordered selection, matching and lifecycle cleanup
provides:
  - Native action/object permission and aggregate rollback matrix
  - Complete native definition/applicability/Device-value preservation regressions
  - Administration guide and explicit outstanding browser acceptance procedure
affects: [02-07, 02-08, phase-verification, parameters-tab]
tech-stack:
  added: []
  patterns: [native ObjectPermission client matrix, complete native snapshots]
key-files:
  created:
    - netbox_custom_field_profiles/tests/test_permissions.py
    - netbox_custom_field_profiles/tests/test_preservation.py
    - docs/development/profiles.md
  modified: []
key-decisions:
  - Native permission/atomicity implementation passed the expanded matrix without source changes.
  - Browser interaction remains explicitly unverified while the browser access host is unavailable.
requirements-completed: [PROF-01, PROF-02, PROF-03, PROF-04, PROF-05, PROF-06, MATCH-01, MATCH-02, MATCH-03, DATA-01]
actuals:
  tokens: 6656
  tasks: 2
  commits: 2
plan_head_before: f0ea7a91385f1d66ffc80af91aeab4591d8e2c3c
plan_head_after: 8fcf74b2846d1a987685f179187b4ad29ab62ae1
coverage:
  - id: permission-matrix
    description: Native action/object constraints, direct requests, CSRF and aggregate rollback
    requirement: PROF-01
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles/tests/test_permissions.py
        status: pass
    human_judgment: false
  - id: native-preservation
    description: Profile CRUD, field modes, order and rules preserve native definitions and Device data
    requirement: DATA-01
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles/tests/test_preservation.py
        status: pass
    human_judgment: false
  - id: browser-interaction
    description: Drag/keyboard order, mode round-trip, search widgets and invalid-form retention
    verification:
      - kind: manual_procedural
        ref: docs/development/profiles.md#browser-acceptance-checks
        status: unknown
    human_judgment: true
    rationale: Browser host unavailable; native server tests do not prove live interaction.
duration: 11min
completed: 2026-11-06
status: complete
---

# Phase 2 Plan 6: Permission and Preservation Integration Summary

**Native action/object authority and complete native-data snapshots pass through real profile requests; browser interaction acceptance remains pending.**

## Task Commits

1. **Verify native action/object permissions and aggregate request integrity** — `141d5a8`
2. **Prove native-data preservation and record the user-facing workflow** — `8fcf74b`

Two test/documentation tasks completed. Their automated verification is green; the browser acceptance portion of Task 2 is unrun and must not be inferred from this summary's completion marker. No profile implementation change was needed. Commit actuals are measured over the two task commits before this metadata commit.

## Verification

- Focused permission suite: **6 tests pass**, native test time **2.257 s**, runner **6.78 s** including validation/snapshots.
- Focused preservation suite: **3 tests pass**, native test time **0.718 s**, runner **5.01 s**.
- `make test-profiles`: **46 tests pass**, native test time **7.007 s**, runner **12.52 s**. `PROFILE_TESTS_ISOLATED` and `PROFILE_LIVE_UNCHANGED` confirmed.
- `make test`: **35 helper tests pass**; native runtime/schema/registration/admin-session/token/negative controls and seed idempotence pass.
- `git diff --check` passes. No dependency or schema changes. Services were not restarted while tests ran.

## Permission and Request-Integrity Matrix

Actual native users/ObjectPermission objects cover view-only, add-only, change-only and delete-only actions. Each action's allowed GET/POST and forbidden direct URLs are checked. Anonymous and unpermitted users cannot read or mutate profile aggregates. Native view permission also controls navigation buttons.

Native constrained users see only permitted rows. Excluded detail/edit/delete GETs and mutation POSTs return 404. A permitted edit or add which would move the saved object outside its native constraint is rejected after save and the native transaction rolls back title, enabled state, field mode, rule sets and memberships together.

Forged/nonexistent field, type, rule and order payloads leave the aggregate unchanged. An injected membership-write IntegrityError proves rollback after the profile row/rules have begun saving. Enforced CSRF rejects add/edit/delete without a token; all corresponding GETs are read-only. Existing tracer/matching tests retain escaped title/filter-label coverage.

## Preservation Evidence

Snapshots include every native CustomField column (including visibility/editability), native applicability relations, and complete Device `custom_field_data`. CMTS/CPE/shared profiles reference the same native field definitions while their Devices keep different values. Create/edit/delete, enable/disable, title/display order, selected reorder, Selected/All round-trip, and all fixed rule updates leave those snapshots identical.

An external native script-style value update and newly applicable native field are resolved without copying values or changing native definitions. Native lifecycle scenarios compare unrelated definitions/values; they do not forbid intentional NetBox cleanup of the deliberately removed field. Profile membership schema stores no values.

## Administration Guide

`docs/development/profiles.md` documents the pinned version, exact commands and focused timings, native action/object permissions, standard CRUD, single duplicate-allowed title, default disabled state, deterministic ordering, selected drag/keyboard controls, native All order and remembered manual selection, fixed AND/OR/tag-any criteria, unused compatible tags, automatic disable/review and explicit re-enable.

Direct SQL/direct or bulk through-table writes do not emit native relation-manager signals and remain unsupported for synchronous cleanup/disable guarantees. Defensive field resolution excludes stale nonapplicable/inactive fields. The guide makes no Parameters-tab or native-value-editing claim.

## Browser Verification — Pending

CUA inventory was retried at the start of this plan and again after the user reported restored browser access. Both returned no browser targets and the exact error `Browsers: Error: The browser access host is unavailable`. No UI mutation or browser pass was claimed. The parent independently confirmed the same connection failure after the user's Chrome mention.

Existing `.planning/WINDOWS.md` entries **1** and **2** remain open; no duplicate issue was appended. The guide contains exact acceptance steps for three-field drag/save/reload, keyboard move/focus/announcement/save, Selected→All→Selected restoration, invalid-form retention, unused compatible/unrestricted tag search/save/reload, and dynamic unrestricted notice. No browser evidence screenshot exists for these checks. Phase verification must return human-needed until the interactions actually pass or browser access recovers.

## Decisions and Deviations

No product/architecture change. Both tasks add regression tests/docs around existing implementation; tests passed on their first run, so no artificial RED or implementation fix was manufactured. Native version-specific permission dispatch and post-save constraint enforcement were checked against the installed 4.7.4 source. Context7 tools/CLI were unavailable; no package was installed for documentation lookup.

**Unrun verification:** Required live browser evidence is blocked by the browser host. It remains explicit debt rather than a new approval checkpoint; all independent authorized automated work is complete. Requirement IDs stay pending at phase level while later declaring retirement plans remain incomplete and browser acceptance is outstanding.

## Known Stubs and Threat Surface

No implementation stubs or new endpoints/auth paths/schema trust boundaries. Threats T-02-13/14/15 have native regression evidence for authority, integrity and preservation. Existing upstream LOGIN_REQUIRED warning remains unchanged. Optional historical pytest was not run or claimed as passing.

## Self-Check: PASSED

All three created task files exist, both task commits are reachable, and required automated suites pass. Browser checks are explicitly unknown in coverage metadata and remain open in the cross-phase ledger.

## Next Plan Readiness

Ready for reversible legacy runtime retirement in 02-07. Retain the internal CustomFieldProfileSerializer required by native delete events. Do not remove browser verification debt or claim complete Phase 2 acceptance from automated suites alone.
