# Device profile administration

The exercised runtime is NetBox **4.7.4**, Docker packaging **5.1.1**. Phase 2
provides profile administration and reusable matching/field resolution. The Device
Parameters tab and native-value editing are later phases; this guide does not
claim those workflows are available.

## Manage profiles

Start the dedicated sandbox with `make up`, then open
<http://127.0.0.1:18047/plugins/custom-field-profiles/>. Use the generated local
administrator credentials described in [sandbox.md](sandbox.md); there is no
fixed/default password. The Custom Field Profiles menu links to the same list.

Users need the native profile `view`, `add`, `change`, or `delete` permissions
for the corresponding operation. NetBox object constraints apply to list results
and direct URLs. Relevance filters grant no authority. Native permissions also
restrict referenced choices; an editor cannot silently clear a saved rule whose
reference they cannot access. Such a profile needs review by an authorized
administrator.

Choose **Add** to create a profile. Devices are the only supported Object Type.
The title identifies the profile and will supply its eventual section heading;
duplicate titles are allowed. New profiles start **disabled**. Set display order,
configure fields/rules, and explicitly enable the profile when ready. The list
shows title, enabled state, display order, field mode, and readable applicability.
Profile order is display order, alphabetical title, creation time (oldest first),
then primary key for exact timestamp ties.

### Fields and ordering

- **Selected fields** requires at least one applicable native field on save.
  Choose fields, then drag the handle on a selected field to another row.
  The **Move up** and **Move down** buttons provide the keyboard alternative:
  tab to a button and activate it with Enter or Space. A status message announces
  the new position. Save and reload to confirm persisted order.
- **All applicable fields** resolves the currently active Device fields in native
  NetBox order (`group_name`, `weight`, `name`). New applicable fields appear
  dynamically. This mode disables the manual field controls and keeps their saved
  selection/order; switching back to Selected restores them.
- The same native field may be selected in several profiles. Memberships refer to
  one native field definition and never store a separate value.

The server revalidates choices and exact selected-field order. Invalid saves
show errors and do not partially change the profile. Native field definitions,
visibility/editability settings, and Device `custom_field_data` remain unchanged
when profiles are managed or deleted.

### Applicability

Device Type, device role, and Device tags are optional searchable multi-selects.
Each populated selector accepts **any** selected value (OR); populated selectors
must **all** match (AND). The tag rule accepts any selected tag on the Device.
Empty selectors impose no restriction. When all are empty, the edit page shows
**Applies to all Devices**, with no extra unrestricted-save confirmation.

The tag selector includes unused tags compatible with Devices and unrestricted
tags. It does not require a tag to be currently assigned to a Device. Native
object permissions still determine which of these choices the editor may access.
Only enabled matching profiles apply. There is no per-Device manual assignment.

### Native changes and review

Deleting a referenced Device Type, role, or tag disables every affected profile,
even if some other selected values remain. Review the remaining rules and
explicitly enable the profile again. Correcting rules never automatically
re-enables a profile.

Deleting a selected custom field or removing its Device applicability removes
invalid selected membership. A Selected-mode profile remains usable with valid
remaining fields; losing its last valid selected field disables it. All mode
keeps valid remembered memberships and continues resolving current applicable
fields. Temporary inactive/provisioning fields are excluded from resolution
without destroying remembered selection merely because they are inactive.

Cleanup supports native instance/queryset deletion and relation-manager
applicability changes in both directions, including remove/clear/set. It is
transactional and idempotent. **Direct SQL or direct/bulk through-table writes do
not emit the required relation-manager signals**, so they do not provide
synchronous cleanup/automatic disable guarantees. Use supported native lifecycle
operations. Defensive field resolution excludes nonapplicable/inactive fields
if stale memberships were introduced by a bypass. NetBox retains ownership of
its own field-data cleanup; the plugin does not write native definitions/values.

## Repeatable checks

Run from the canonical repository root:

```sh
make test-profiles
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_permissions
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_preservation
make test
```

The profile runner uses native Django/PostgreSQL, a separate test database, and
only plugin-owned tests. It rejects an empty suite and compares live native/plugin
snapshots around the run. It never resets the live sandbox. The permissions suite
covers action-only users, native object constraints, denied/invalid direct
requests, post-save constraint rollback, membership-write rollback, CSRF, and
read-only GET requests. Preservation tests snapshot complete native field
definitions/applicability and Device values across CRUD, enable state, order,
mode and rule changes, CMTS/CPE/shared memberships, and external native updates.
Lifecycle tests assert preservation of unrelated state rather than forbidding
NetBox's intentional native cleanup.

Measured focused runs in Plan 02-06: permissions **6 tests / 6.78 s** end to end;
preservation **3 tests / 5.01 s** end to end, using the retained isolated test
database. Timings include sandbox validation and live snapshots. Full-suite and
baseline results are recorded in
`.planning/phases/02-profile-administration-and-matching/02-06-SUMMARY.md`.
The optional historical pytest suite is separate and is not claimed as passing.

## Browser acceptance checks

Server tests do not prove drag/drop, keyboard interaction, or live search widget
behavior. Browser automation was retried during Plan 02-06 but returned
`Browsers: Error: The browser access host is unavailable` with no browser targets.
The following checks remain **pending**, tracked by `.planning/WINDOWS.md` entries
1 and 2. Do not treat this guide as browser acceptance evidence.

In the dedicated sandbox, using disposable verification profiles:

1. Create a Selected profile with at least three applicable fields. Drag its last
   field before the first. Save, reopen Edit, and verify the exact order survives.
2. Tab to **Move down** or **Move up**, activate with Enter/Space, and verify focus
   and the announced position. Save and reopen to confirm persistence.
3. Switch Selected → All, save/reopen, then switch back to Selected. Verify the
   manual selection and order are restored. All mode should disable manual
   controls without losing them.
4. Submit with an empty title while retaining several selected fields, their
   order, and at least one rule. Verify the required-title error appears and the
   choices/order/rules remain available for correction. Correct and save.
5. Through native tag administration, create an unused tag compatible with
   Devices. Search for it in Device tags on the profile form, select/save/reopen,
   and verify it is retained. Do the same with an unrestricted unused tag.
6. Clear all three rule selectors and verify **Applies to all Devices** appears
   immediately. Add a rule and verify it hides; clear the rule and verify it
   returns. Save without an extra unrestricted-profile confirmation.
7. Record the browser/version, profile IDs, exact observed outcomes and redacted
   screenshot paths. Leave ledger entries open until these interactions have
   actually passed. No native field settings or values need changing for these
   tests.
