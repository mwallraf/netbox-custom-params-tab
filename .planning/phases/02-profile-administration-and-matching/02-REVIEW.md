---
phase: 02-profile-administration-and-matching
reviewed: 2026-11-06T20:50:37Z
rereviewed: 2026-11-06T21:01:10Z
resolved_findings: 2
depth: standard
files_reviewed: 33
files_reviewed_list:
  - CLAUDE.md
  - Makefile
  - README.md
  - docs/development/profiles.md
  - netbox_custom_field_profiles/__init__.py
  - netbox_custom_field_profiles/api/serializers.py
  - netbox_custom_field_profiles/api/urls.py
  - netbox_custom_field_profiles/api/views.py
  - netbox_custom_field_profiles/forms.py
  - netbox_custom_field_profiles/matching.py
  - netbox_custom_field_profiles/migrations/0002_profiles.py
  - netbox_custom_field_profiles/migrations/0003_retire_legacy_configuration.py
  - netbox_custom_field_profiles/models.py
  - netbox_custom_field_profiles/navigation.py
  - netbox_custom_field_profiles/signals.py
  - netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js
  - netbox_custom_field_profiles/tables.py
  - netbox_custom_field_profiles/template_content.py
  - netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html
  - netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html
  - netbox_custom_field_profiles/tests/__init__.py
  - netbox_custom_field_profiles/tests/runner.py
  - netbox_custom_field_profiles/tests/test_lifecycle.py
  - netbox_custom_field_profiles/tests/test_matching.py
  - netbox_custom_field_profiles/tests/test_permissions.py
  - netbox_custom_field_profiles/tests/test_preservation.py
  - netbox_custom_field_profiles/tests/test_schema.py
  - netbox_custom_field_profiles/tests/test_selection.py
  - netbox_custom_field_profiles/tests/test_tracer.py
  - netbox_custom_field_profiles/urls.py
  - netbox_custom_field_profiles/views.py
  - pyproject.toml
  - scripts/test_profiles.py
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
---

# Phase 2: Code Review Report

**Reviewed:** 2026-11-06T20:50:37Z  
**Re-reviewed:** 2026-11-06T21:01:10Z  
**Depth:** standard  
**Files Reviewed:** 33  
**Status:** clean — both original findings resolved

## Narrative Findings (AI reviewer)

The original explicit 33-file scope was reviewed against the agreed requirements and locked Phase 2 context. Native generic-view permission restriction, form restriction, dynamic-choice behavior, custom-field resolution, and deferred deletion were also inspected in the installed NetBox runtime. The two original lifecycle defects below were independently reproduced before correction and are retained as resolved history. No active BLOCKER, WARNING, or Info findings remain after targeted independent re-review of commits `1f979460a5f4e47066257fb51ad5cc990c0af23d` and `07a223cb73b166691c58d07954863a7ac1b32332`.

### Targeted re-review outcome

Re-read the current `forms.py`, `models.py`, `signals.py`, selection/lifecycle regression tests, both fix diffs, and `02-REVIEW-FIX.md`. Rechecked the pinned native queryset deletion, field status row locking, and the previously inspected native `ObjectEditView` transaction/`AbortRequest` handling. Form persistence now locks sorted native field rows before the profile row and checks fresh applicability/deletion state before the model update and again before membership persistence. Native pre-remove/pre-clear and deletion cleanup use the same field-before-profile ordering; queryset field deletion locks its field set before aggregate cleanup. The transient model guard covers supported split saves, requiring `obj.save()` and `form.save_m2m()` within the caller's same atomic transaction. Ordinary model saves without a form guard retain their native behavior.

The original two in-memory PostgreSQL reproductions were independently rerun against the fixes and both passed: `CR01_REPRO_NOW_REJECTED` and `CR02_REPRO_NOW_REJECTED`, with `PROFILE_TESTS_ISOLATED` and command exit 0. The stale applicability save now raises native `AbortRequest` before restoring the title, enabled state, or membership. A fresh form excludes and rejects a field whose deferred native deletion has begun. The added regressions also cover normal/split saves, explicit All-mode remembered payloads, native HTTP rollback, preserved provisioning memberships, and actual two-connection cleanup/deletion lock waits. The supplied fix report records 63 native tests passing; this re-review reran only the two original probes, not the full suite.

Browser interaction acceptance remains pending and is independent of this code-review result.

### Resolved CR-01: A validated save can restore membership removed by native applicability cleanup

**Original classification:** BLOCKER  
**Resolution:** Resolved in `1f97946`, with deleting-state protection completed by `07a223c`; independently verified at re-review. The details and pre-fix reproduction below are retained as history.  
**File:** `/Users/mwallraf/Developer/netbox-custom-params-tab/netbox_custom_field_profiles/forms.py:143-159`  
**Related:** `/Users/mwallraf/Developer/netbox-custom-params-tab/netbox_custom_field_profiles/signals.py:27-42`

**Issue:** The form validates Device applicability before entering its save transaction, then retains only the resulting IDs in `ordered_field_ids`. The profile row lock at line 148 occurs after the ordinary model save and never rechecks those IDs against current applicability. If another operation removes Device applicability between validation and persistence, native cleanup correctly removes the old membership and disables an empty Selected profile, but the pending form subsequently writes its stale enabled value and reinserts the now-invalid membership. No further applicability signal runs to repair that insertion. Defensive resolution hides the field, leaving the profile enabled with an empty resolved selection. This breaks D-14 under supported native operations; the documented direct-SQL exclusion does not cover it.

**Reproduction:** In a native `TestCase`, create an enabled Selected profile with one Device field, instantiate its valid edit form with that field and `enabled=True`, and call:

```python
assert form.is_valid()
field.object_types.remove(device_content_type)
# Database now has enabled=False and zero memberships.
form.save()
profile.refresh_from_db()
# Actual: enabled=True, one invalid membership, get_profile_fields(profile) == [].
```

The focused PostgreSQL probe confirmed `AFTER_NATIVE_CHANGE [False] 0`, followed by `AFTER_FORM_SAVE True 1 0`; the assertion that the profile must remain disabled failed.

**Fix:** Coordinate aggregate persistence and native applicability/deletion cleanup through a shared locking strategy, with a consistent lock order. Re-read and revalidate the selected field IDs against current Device applicability inside that protected save operation before replacing memberships; reject a stale form instead of restoring invalid references or stale enable state. Cover the deferred `commit=False/save_m2m()` path too. Add a deterministic regression that interleaves native applicability removal between validation and save, plus the concurrent insertion/cleanup case.

### Resolved CR-02: Fresh forms allow selecting a field whose native deletion has already begun

**Original classification:** BLOCKER  
**Resolution:** Resolved in `07a223c`; both the visible choice queryset and protected persistence reject deleting fields. Provisioning fields remain selectable/remembered. Independently verified at re-review. The details and pre-fix reproduction below are retained as history.  
**File:** `/Users/mwallraf/Developer/netbox-custom-params-tab/netbox_custom_field_profiles/forms.py:66-67`

**Issue:** The selected-field queryset restricts only object type and includes `CustomField.status == deleting`. Native NetBox deferred deletion intentionally retains the field row and its applicability while a background job purges values; it dispatches deletion signals immediately. The plugin removes existing memberships at that point, but a fresh administration form can then select the same deleted field again, including as the sole field of an enabled Selected profile. The form accepts and saves it even though native resolution excludes it. This is reachable without a validation/save race whenever the purge job is queued or delayed, and defeats the deletion-cleanup invariant until a later worker replay.

**Reproduction:** Use the same native deferred-deletion trigger already exercised by `test_lifecycle.py`:

```python
with patch.object(CustomField, '_exceeds_inline_limit', return_value=True):
    field.delete()
field.refresh_from_db()
assert field.status == 'deleting'
form = CustomFieldProfileForm(data={
    'title': 'Deleted selection',
    'content_type': device_content_type.pk,
    'display_order': 10,
    'field_mode': 'selected',
    'enabled': True,
    'selected_fields': [field.pk],
    'field_order': json.dumps([field.pk]),
})
# Actual: form.is_valid() is True; saving creates enabled membership.
# get_profile_fields(form.instance) returns [].
```

The focused PostgreSQL probe confirmed `DELETING_FIELD_VISIBLE True`, `DELETING_FIELD_VALID True {}`, and `DELETING_FIELD_SAVED True 1 0`; the rejection assertion failed.

**Fix:** Exclude the native deleting status from selectable and remembered-field validation, while retaining the intended behavior for temporary inactive/provisioning fields:

```python
from extras.choices import CustomFieldStatusChoices

self.fields['selected_fields'].queryset = (
    CustomField.objects.filter(
        object_types__app_label='dcim',
        object_types__model='device',
    )
    .exclude(status=CustomFieldStatusChoices.STATUS_DELETING)
    .distinct()
)
```

Apply the equivalent current-status guard during the protected persistence in CR-01 so a deletion that starts after validation cannot reintroduce the same defect. Add fresh Selected-form and All-mode remembered-payload regressions after deferred deletion.

## Verification scope and limits

At the original review, each finding was reproduced by a separate, single-test in-memory suite using `ProfileTestRunner`, its isolated PostgreSQL database, and transactional `TestCase` fixtures. Both emitted `PROFILE_TESTS_ISOLATED` and failed on the stated behavioral assertion. At re-review, the two original cases were adapted to assert rejection and preservation, and both passed in the isolated database. All independent probes were created in memory; no source or test files were changed. The full suite was not repeated by the reviewer.

No structural pre-pass or external reviewer evidence was supplied. None of the 33 scope paths is Git-ignored. Browser interaction acceptance remains pending; no drag/drop, keyboard, search-widget, or assistive-technology pass is claimed. The optional historical pytest suite was not run.

---

_Reviewer: gsd-code-reviewer_  
_Depth: standard_

