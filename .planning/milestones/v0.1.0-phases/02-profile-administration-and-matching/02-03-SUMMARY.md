---
phase: 02-profile-administration-and-matching
plan: "03"
subsystem: ui
tags: [netbox, profiles, ordering, native-fields]
requires:
  - phase: 02-02
    provides: Native CRUD tracer and isolated native tests
provides:
  - Server-validated ordered field membership and Selected/All mode persistence
  - Packaged drag and keyboard ordering controls and profile detail configuration
affects: [02-04, 02-05, 02-06]
tech-stack:
  added: []
  patterns: [atomic aggregate form save, plugin-owned static controls]
key-files:
  created:
    - netbox_custom_field_profiles/tests/test_selection.py
    - netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js
    - netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html
    - netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html
  modified: [netbox_custom_field_profiles/forms.py, netbox_custom_field_profiles/views.py, netbox_custom_field_profiles/tests/test_tracer.py, pyproject.toml]
key-decisions:
  - Retain remembered ordered memberships on All-mode saves, including omitted browser selection inputs.
  - Native get_for_model ordering remains authoritative; selected output intersects active fields without deleting remembered memberships.
requirements-completed: []
actuals:
  tokens: 5017
  tasks: 2
  commits: 3
plan_head_before: 99ced6e729fcdbdad4b723d89ae65eb5cb7b1744
plan_head_after: d7c4a006dc5751f60b4b7465bf59e47b98e469ec
duration: 9 min
completed: "2026-11-06"
status: complete
---

# Phase 2 Plan 03: Ordered field selection Summary

**Profiles save ordered applicable native fields, preserve their manual selection across All mode, and expose packaged drag and keyboard ordering controls. Browser interaction verification remains pending.**

## Accomplishments

- Replaced the interim All-only form with explicit field mode and Device-applicable choices. Exact integer-ID order/set/uniqueness validation rejects malformed, duplicate, foreign and empty Selected payloads.
- Aggregate membership saves honor commit=False/save_m2m, use transactions and a profile row lock, and preserve native inherited form M2M behavior. All mode leaves remembered memberships untouched.
- Existing native field resolver already preserves native All ordering and selected membership order; tests establish dynamic additions and temporary inactive-field behavior without modifying that correct code.
- Added dedicated native-base edit/detail templates, draggable handles, keyboard buttons, focus restoration and a live announcement region. JavaScript synchronizes the ordered IDs and remembers selection while All mode is chosen.
- Added setuptools template/static package-data and verified the resulting wheel contains the JS and both new templates.

## Task Commits

1. `98ece36` — ordered-selection contracts.
2. `195cdae` — validated ordered membership and mode persistence.
3. `d7c4a00` — packaged browser controls and native page persistence tests.

## Verification Evidence

- Preimplementation contract run failed on expected behavior: Selected order was ignored, empty Selected input accepted, and memberships absent. A missing-field KeyError was also present; no strict machine-validated TDD RED gate compliance is claimed (global TDD mode is off).
- Final `make test-profiles`: **19 tests pass**, 1.747s test execution / 6.04s helper elapsed. `PROFILE_TESTS_ISOLATED` and `PROFILE_LIVE_UNCHANGED` confirmed isolated native PostgreSQL and unchanged live data.
- Tests cover commit=False/save_m2m, duplicate membership payloads, restricted querysets, native page save/reload, invalid response errors, remembered order, cross-profile references, native order, new applicable fields and temporary inactivity.
- `make test`: **35 helper tests pass**, runtime/schema/registration/admin-session/native-token/negative controls pass, seed idempotence passes.
- `node --check` and `git diff --check` pass. Static collected in the dedicated sandbox; JS URL returns **HTTP 200**.
- Isolated wheel built with the project's declared setuptools backend: `PROFILE_WHEEL_ASSETS_OK 3` confirms the JS plus edit/detail templates.
- **Actual browser drag/save/reload, keyboard reorder and mode-round-trip are unrun.** Computer-use inventory returned `browser access host unavailable`; native Safari targeting timed out/reset after 60 seconds. This is not claimed as passing from server tests. Parent agreed to carry this concrete check into Plan 02-06. Recorded as open `.planning/WINDOWS.md` entry 1.

## Deviations from Plan

1. **[Rule 1 — Native form clean contract]** Installed native form mixins return None from clean; used self.cleaned_data after super().clean(). All native form tests now pass.
2. **[Rule 2 — Existing tracer contract]** Updated the tracer's form payload to explicitly submit All mode now that mode is a real required field. No behavior was weakened.
3. **[Rule 3 — Static/build environment]** Static directory is root-owned, so collectstatic ran as root inside the dedicated container. Runtime lacks pip/setuptools and the offline build cache lacked the declared backend; normal isolated uv build downloaded the existing declared backend after approval. Source metadata is not writable by the container user, so built from a temporary container copy. The image root pyproject predates the bind-mounted package; copied the actual new package-data declaration into that temporary copy before verifying the wheel. No runtime dependency was added.
4. **[Unrun verification]** Browser host failure leaves actual drag/keyboard evidence for Plan 02-06; this remains visible in the broken-windows ledger and must be resolved before final phase verification.

## Self-Check: PASSED

All eight changed source paths exist, three task commits are reachable, and native/server/static/package checks pass. No native definitions, visibility settings or stored Device values were written. No new packages were added to project dependencies. The internal native event serializer is preserved. The measured realized diff is 5,017 chars/4 tokens across three pre-summary commits.

## Next Plan Readiness

Ready for fixed Device Type/role/tag filters in 02-04. Keep selection fields distinct from filter relations and preserve the aggregate _save_m2m behavior. Actual browser verification is explicitly pending for 02-06.
