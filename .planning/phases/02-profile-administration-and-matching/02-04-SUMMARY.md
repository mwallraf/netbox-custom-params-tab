---
phase: 02-profile-administration-and-matching
plan: "04"
subsystem: matching
tags: [netbox, profiles, filters, native-permissions]
requires:
  - phase: 02-03
    provides: Ordered selection and native administration
provides:
  - Native searchable Device Type, role and Device-compatible tag selectors
  - Fixed AND/OR applicability matching with stable duplicate-free results
  - Escaped readable scope summaries and dynamic unrestricted feedback
affects: [02-05, 02-06, 03-parameters-tab]
tech-stack:
  added: []
  patterns: [native dynamic choices, prefetched fixed-rule matching, restricted aggregate form save]
key-files:
  created: [netbox_custom_field_profiles/tests/test_matching.py]
  modified:
    - netbox_custom_field_profiles/forms.py
    - netbox_custom_field_profiles/matching.py
    - netbox_custom_field_profiles/tables.py
    - netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html
    - netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html
key-decisions:
  - Use native for_object_type_id tag discovery, including unused compatible and unrestricted tags.
  - Reject edits carrying inaccessible saved applicability references rather than silently clearing them.
requirements-completed: []
actuals:
  tokens: 5594
  tasks: 2
  commits: 3
plan_head_before: 68815a5b7f42b4a05d6f2d9e53228a4e162a1653
plan_head_after: 632716866753d62d4dbc04a502db6d172046b204
duration: 10 min
completed: "2026-11-06"
status: complete
---

# Phase 2 Plan 04: Profile applicability Summary

**Profiles now match native Devices through three searchable fixed criteria, with exact AND/OR semantics, compatible unused-tag discovery and readable escaped administration summaries.**

## Accomplishments

- Added optional native dynamic multi-selects for Device Types, device roles and applicability tags. The native tag API uses `for_object_type_id`; server validation accepts Device-restricted and unrestricted tags, including unused tags, and rejects foreign restricted tags.
- Implemented enabled-first fixed matching: empty criterion imposes no restriction; any selected type, role or tag satisfies its criterion; all populated criteria must match. Prefetched relations avoid per-profile matcher lookups and each profile appears once in model ordering.
- Preserved aggregate-save atomicity and native reference restrictions. Editors unable to access a saved reference get an explicit form error; omitted options cannot silently broaden scope.
- Added list applicability summaries, human field-mode labels, escaped detail criteria, AND/OR guidance and the exact inline `Applies to all Devices` notice. Change listeners update that notice without a confirmation step.

## Task Commits

1. `be49fb8` — native fixed-rule matching contracts.
2. `dc7ff0e` — native selectors, restricted validation and matcher.
3. `6327168` — scope summaries, notice and native client tests.

## Verification Evidence

- Preimplementation native run: five tests executed, expected fixed-rule mismatch (four matching profiles missing), plus missing-selector errors. The assertion failure is behavioral RED evidence; missing-selector errors are not claimed as valid strict RED evidence. Global TDD mode is off.
- Focused matching suite: **7 tests pass**, 0.913s execution / **5.19s** helper elapsed.
- Final `make test-profiles`: **26 tests pass**, 2.814s execution / **7.58s** helper elapsed. `PROFILE_TESTS_ISOLATED` and `PROFILE_LIVE_UNCHANGED` confirm separate native PostgreSQL testing and unchanged live snapshots.
- Matrix covers no rules, single/multiple type and role choices, combined AND, tag-any, duplicate matching tags, disabled profiles, non-Device input, empty results, stable ties/idempotence, transaction rollback and native definition/value preservation.
- Native client tests cover real rule POST/save, unused compatible/unrestricted tag API discovery, foreign-tag rejection without clearing prior rules, native permission-restricted reference rejection, escaped labels, list columns and unrestricted notice responses.
- Dedicated web/worker services restarted before final suites; `make up` confirmed readiness. `make test`: **35 helper tests pass**, runtime/schema/registration/admin-session/native-token/negative controls and seed idempotence pass.
- `git diff --check` passes. No schema migration or package addition was needed.
- **Actual live widget search/save/reload and interactive notice verification remain unrun.** CUA inventory again reported `The browser access host is unavailable`. Server/API checks are not represented as browser evidence. Recorded in `.planning/WINDOWS.md` entry 2 for Plan 02-06.

## Deviations from Plan

1. **[Rule 1 — Native dynamic-field queryset lifecycle]** Native dynamic fields narrow their queryset while constructing BoundFields, including empty submitted values. Comparing saved rules against that narrowed queryset incorrectly rejected intentional clearing. Capture the already permission-restricted queryset before `full_clean`, then validate saved-reference authority against its clone. Native restricted POST and rollback tests pass.
2. **[Verification environment]** Browser host remained unavailable. The concrete live-widget check is preserved as open verification debt for the planned integration/browser pass, not silently accepted.

## Remaining Scope

Target deletion and field-applicability cleanup are Plan 02-05. Broader permission/preservation/browser evidence is Plan 02-06. Shared requirement IDs remain pending until all declaring plans and final phase verification finish. No Device Parameters tab, native value editor, independent field storage or external API endpoint was introduced.

## Self-Check: PASSED

All six modified source paths exist, all three task commits are ancestors of HEAD, both native suites and the existing baseline pass. The pending browser interaction is explicitly recorded and is not claimed as passed.

## Next Plan Readiness

Ready for 02-05 lifecycle cleanup. Preserve native event serializer from Plan 02-02. Plan 02-06 must close WINDOWS entries 1 and 2 or surface them as human verification needs.
