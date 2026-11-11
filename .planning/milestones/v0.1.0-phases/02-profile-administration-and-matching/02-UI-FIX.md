# Phase 2 — UI finding fixes

**Date:** 2026-11-06
**Scope:** Confirmed code-derived E1/C1, E2, E3 and C2 findings from `02-UI-REVIEW.md`.
**Implementation commit:** `5b99080` — `fix(02): preserve pending manual fields when saving All mode`.
**Status:** Implemented; native server regression checks passed. Browser acceptance remains pending. This report does not complete Phase 2.

## E1 / C1 — Remember current manual selection and order

- The ordering editor synchronizes an explicit `remembered_fields` JSON selection alongside `field_order`, including when All mode disables the visible selection input.
- For an explicit All-mode payload, the form rebinds remembered choices through the existing `selected_fields` model field. Its native applicability and permission-restricted queryset remains authoritative; hidden IDs do not grant access.
- Remembered IDs must be unique positive integers, must match the validated selected set, and must match the exact ordered set. Malformed, nonexistent, nonapplicable, inaccessible, duplicate and mismatched payloads are rejected.
- The validated ordered membership is persisted atomically in All mode as inactive remembered state. All-field resolution still calls native dynamic field resolution and retains native ordering. An explicitly empty remembered set is valid in All mode; Selected mode still requires an applicable field.
- All-mode requests omitting `remembered_fields` retain the previously saved membership. Existing omission-preservation tests remain green.
- A failed All-mode form retains pending choices, ordering and remembered payload for correction. Native request tests cover a missing title followed by correction/save.
- `save(commit=False)` still defers membership writes until `save_m2m()`. Injected membership-write failure through the native edit view rolls back the profile and membership aggregate.
- Mode help and the development guide now explicitly describe remembering pending additions, removals and ordering when saving All mode.

New native tests cover pending reorder, addition and removal followed by All save/reopen/Selected save, failed-form recovery, invalid All payload aggregate preservation, native choice permission restrictions, explicit empty state, deferred persistence and transactional rollback. The initial run against the old implementation reproduced 18 assertion failures across these cases; the corrected selection suite passes.

## E2 — Announce applicability scope changes

The edit template includes an always-present polite, atomic status region. The existing selector change handler updates it for both unrestricted and restricted scope. The visible unrestricted notice retains the exact text **Applies to all Devices**. Actual assistive-technology announcements require the pending browser verification.

## E3 — Explain unavailable ordering controls

A visible loading message directs administrators to reload and check JavaScript before changing selected fields/order if initialization does not finish. The ordering script hides it only after successful initial rendering. A noscript message supplies the recovery action when JavaScript is disabled. No dependency or separate non-JavaScript ordering feature was added.

## C2 — Distinguish inactive remembered fields

The detail page labels the All-mode membership list **Remembered selected fields**, alongside the existing explanation that effective fields are dynamically resolved in native order.

## Verification

| Check | Result |
|-------|--------|
| `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_selection` | 12 tests passed; Django 1.836 s, end to end 6.69 s |
| `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_permissions` | 6 tests passed; Django 2.388 s, end to end 7.03 s |
| `make test-profiles` | 55 tests passed; Django 7.939 s, end to end 12.87 s |
| Native test isolation and live preservation | Every successful run reported `PROFILE_TESTS_ISOLATED` and `PROFILE_LIVE_UNCHANGED` |
| `node --check netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js` | Passed |
| `git diff --check` | Passed |

The existing NetBox `LOGIN_REQUIRED` deprecation warning remains unrelated to these changes. Baseline runtime wiring, models, migrations and endpoints were unchanged, so the baseline-only suite was not rerun for this focused fix. The optional historical pytest suite remains outside this follow-up.

## Remaining verification

Browser-host access was already unavailable in the parent review session. No live browser interaction, screenshots, drag/keyboard behavior, viewport rendering or actual screen-reader announcement is claimed here. Existing WINDOWS entries 1/2 remain open. The development guide's pending browser checklist now includes pending manual changes across an All save, invalid All-form recovery, scope announcements and unavailable-script guidance.

## Self-check

- All six implementation/documentation files exist in the canonical repository root; no branch or worktree was created.
- Commit `5b99080` is present in the current branch and contains no tracked-file deletion.
- No shared STATE, ROADMAP, requirement or phase-completion artifact was changed by this fix.
