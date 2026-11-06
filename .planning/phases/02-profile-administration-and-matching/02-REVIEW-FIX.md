---
phase: 02-profile-administration-and-matching
fixed_at: 2026-11-06T20:59:05Z
review_path: .planning/phases/02-profile-administration-and-matching/02-REVIEW.md
iteration: 1
findings_in_scope: 2
fixed: 2
skipped: 0
status: all_fixed
---

# Phase 2: Code Review Fix Report

**Fixed at:** 2026-11-06T20:59:05Z  
**Source review:** `.planning/phases/02-profile-administration-and-matching/02-REVIEW.md`  
**Iteration:** 1

**Summary:**

- Findings in scope: 2
- Fixed: 2
- Skipped: 0

## Fixed Issues

### CR-01: A validated save can restore membership removed by native applicability cleanup

**Status:** fixed: requires human verification  
**Files modified:** `netbox_custom_field_profiles/forms.py`, `netbox_custom_field_profiles/models.py`, `netbox_custom_field_profiles/signals.py`, `netbox_custom_field_profiles/tests/test_selection.py`, `netbox_custom_field_profiles/tests/test_lifecycle.py`  
**Commit:** `1f97946`  
**Applied fix:** Form persistence and native cleanup acquire sorted native field row locks before profile row locks. Applicability removal/clear locks before changing the native relation, and queryset field deletion locks its full field set before aggregate cleanup. The form checks current Device applicability inside the save transaction before either the model UPDATE or membership replacement. Stale submissions raise native `AbortRequest`; NetBox's generic edit view returns an actionable form error and rolls back the attempted aggregate save instead of restoring an invalid selection or stale enabled state.

The bounded additional model change invokes a transient form-owned guard before model persistence, including the `commit=False` path. Ordinary model saves have no callback and retain their native behavior. Split form saves must run `obj.save()` and `form.save_m2m()` in the caller's same `transaction.atomic()` block; a split save outside a transaction is rejected before any model write. No transaction is held open across form API calls.

**Evidence:** Selected and explicit All-mode remembered payloads are validated, then native applicability is removed, then both normal and split saves reject the stale input while leaving cleanup's disabled state and removed memberships intact. A real native edit POST returns HTTP 200 with the stale-selection error and preserves the cleanup result. A real two-connection PostgreSQL regression pauses an inserting form under its field lock, observes native cleanup's `Lock` wait in `pg_stat_activity`, releases the form, and verifies cleanup removes the newly inserted membership and disables the resulting empty Selected profile. A separate regression confirms the split-save transaction contract and ordinary model saves after completing it.

### CR-02: Fresh forms allow selecting a field whose native deletion has already begun

**Status:** fixed: requires human verification  
**Files modified:** `netbox_custom_field_profiles/forms.py`, `netbox_custom_field_profiles/tests/test_selection.py`, `netbox_custom_field_profiles/tests/test_lifecycle.py`  
**Commit:** `07a223c`  
**Applied fix:** Selectable fields and the protected current-state save check exclude native `CustomFieldStatusChoices.STATUS_DELETING`. All-mode remembered payloads use the same native choice validation. Provisioning fields remain selectable and remembered, consistent with the temporary-inactivity decision; resolution continues to omit them until native activation.

**Evidence:** Actual native deferred deletion retains the field row with deleting status. Fresh Selected and All remembered-selection forms and their native add POSTs reject that field without profile/native changes. A deletion beginning after validation is rejected for both modes through normal and split saves, preserving native cleanup's removed memberships and disabled state. Provisioning-mode Selected and remembered memberships still persist. A second real PostgreSQL concurrency regression confirms native field deletion waits for an inserting form and then cleans its new membership and disables the empty profile.

## Verification

All checks ran from the canonical **main checkout**, `/Users/mwallraf/Developer/netbox-custom-params-tab`; no worktree or branch was created. Native tests executed inside the pinned project NetBox 4.7.4 sandbox against its isolated PostgreSQL test database. Each focused run confirmed `PROFILE_TESTS_ISOLATED`, `PROFILE_LIVE_UNCHANGED`, and `PROFILE_TESTS_OK`.

- CR-01 focused selection module: 14 tests passed; lifecycle module: 13 tests passed.
- CR-02 focused selection module: 17 tests passed; lifecycle module: 14 tests passed.
- Full `make test-profiles`: **63 tests passed** in 12.066 seconds; wrapper elapsed 17.09 seconds. `PROFILE_TESTS_ISOLATED`, `PROFILE_LIVE_UNCHANGED`, and `PROFILE_TESTS_OK` confirmed.
- Modified Python sections were reread and parsed with `ast.parse`; `git diff --check` passed before each fix commit. Both commits used normal hooks.

These are logic fixes, so the status above retains the fixer's required human-verification flag despite the behavioral regression coverage. Independent re-review remains the orchestrator's next step. Browser interaction acceptance in WINDOWS entries 1/2 remains pending; no drag/drop, keyboard, dynamic-search, or assistive-technology pass is claimed. The baseline suite and optional historical pytest suite were not rerun: no runtime wiring or baseline helper changed.

---

_Fixed: 2026-11-06T20:59:05Z_  
_Fixer: the agent (gsd-code-fixer)_  
_Iteration: 1_

## Orchestrator re-review outcome

The independent reviewer subsequently reproduced both original cases successfully and set 02-REVIEW.md to clean with zero active findings. The two original findings remain recorded as resolved. The final restarted-sandbox make test baseline also passed: 35 helper tests plus runtime/schema/authentication/negative controls/seed idempotence. Existing browser acceptance remains pending.
