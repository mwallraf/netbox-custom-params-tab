# Device profiles and Parameters

The exercised runtime is NetBox **4.7.4**, Docker packaging **5.1.1**. Phase 2
provides profile administration and reusable matching/field resolution. Phase 3
adds the Device **Parameters** tab. Phase 4 adds **Edit Parameters** using native values.
Phase 2 is verified complete; Phase 3 browser acceptance is pending as recorded
in `.planning/phases/03-parameters-tab/03-UAT.md`.

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
The title identifies the profile and supplies its Parameters section heading;
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
  dynamically. This mode disables the manual field controls. Saving remembers
  the current manual selection/order, including pending additions, removals and
  reordering made before switching to All. Switching back to Selected restores
  that remembered state; an empty remembered selection is allowed in All mode.
  The All-mode detail page labels this inactive list **Remembered selected fields**.
- The same native field may be selected in several profiles. Memberships refer to
  one native field definition and never store a separate value.

The server revalidates remembered choices against the same native applicable-field
and permission restrictions as Selected mode, and validates exact field order.
Older All-mode requests without remembered state preserve the saved manual
membership. Invalid saves show errors and do not partially change the profile;
pending remembered choices/order remain on the form when correcting another
field such as the title. Native field definitions,
visibility/editability settings, and Device `custom_field_data` remain unchanged
when profiles are managed or deleted.

Field ordering requires JavaScript. A loading message stays visible if the
ordering controls fail to initialize; reload the page and check JavaScript is
enabled before changing selected fields or their order. A separate noscript
message provides the same recovery action when JavaScript is disabled.

### Applicability

Device Type, device role, and Device tags are optional searchable multi-selects.
Each populated selector accepts **any** selected value (OR); populated selectors
must **all** match (AND). The tag rule accepts any selected tag on the Device.
Empty selectors impose no restriction. When all are empty, the edit page shows
**Applies to all Devices**, with no extra unrestricted-save confirmation.
An always-present polite status region announces unrestricted or restricted
scope when these selectors change; actual assistive-technology behavior remains
part of the pending browser checks below.

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

## View Device Parameters

Open a Device's native detail page and choose **Parameters**. The tab appears when
at least one enabled profile matches, including a matching profile that currently
has no fields. Each profile is an expanded full-width card; duplicate titles are
retained. Sections use the same deterministic profile order described above;
Selected fields use saved membership order and All uses current native order.

Users need native Device viewing access, including any object constraints. They
do not need profile or custom-field definition administration permissions. Matching
never grants access. Direct tab URLs enforce the same Device boundary. An
authorized direct visit with no match says **No parameter profiles apply to this
device.** A matching section without fields says **No fields are available in this
profile.** Parameters exposes no profile administration metadata. Authorized Device
editors see **Edit Parameters** when at least one matching field can be edited.

Every relevant field appears, including fields set to native **Hidden** or **If
Set** presentation on the normal detail page. Those native settings remain
unchanged. Missing/null values, empty text and empty multi-value collections show
muted **Not set**. False and numeric zero are values. JSON `{}`, `[]`, `false`, `0`
and empty string remain JSON values. Labels fall back to the exact internal field
name; descriptions use secondary native help tooltips with escaped text.

Values use native type formatting, choice labels/colors and sanitized Markdown.
URLs retain their complete visible text; links obey NetBox's configured URL scheme
policy. Long text retains complete content and line breaks; JSON uses native
preformatted output with local horizontal overflow. Actual desktop/narrow wrapping,
tooltip usability and keyboard behavior still require browser acceptance.

Related object values resolve only through the viewer's native restricted queryset.
A missing/denied scalar or entirely unavailable collection shows **Unavailable**,
without stored IDs, labels or links. Mixed collections show only accessible members,
without a hidden-member count. Native Device access does not grant related-object
access.

Repeated fields show the same native value in every matching section. Values are
read from Device `custom_field_data` on each ordinary request: native script/API
writes appear on the next GET without importing or synchronizing anything. Changing
profile selection, filters or enable state changes relevance while retaining native
stored values. GETs and unsupported POSTs leave native definitions, settings,
choices, applicability, values and every profile aggregate table unchanged.

## Edit Device Parameters

On a matching Device’s Parameters tab, choose **Edit Parameters**. The single form
follows first-occurrence section/field order and offers each native field once,
including fields repeated across profiles. Native Device change permission and
object constraints apply to both the action and direct GET/POST requests; profile
administration permission is not required. The route is
`/dcim/devices/<id>/parameters/edit/`. Save and Cancel return to Parameters.

Only active, applicable fields in currently matching enabled profiles whose native
UI editability is Yes are offered. Native Hidden and noneditable fields retain
their stored values. A field containing inaccessible saved references is omitted
as a whole, preserving its complete value without exposing denied IDs or labels.
New reference choices use native restricted querysets. If no editable fields
remain, the page explains this and has no Save action.

Native widgets, required/type/range/regex/choice/uniqueness validation and change
logging are reused. Invalid submissions display errors and save nothing. Changes
to the available fields or native definitions while the form is open require a
reload. Native stale-Device protection is retained. POST re-resolves matching
profiles and locks the Device before reading its current values. Fields outside
the edit set, including existing orphaned storage keys, remain unchanged; forged
extra inputs cannot change Device properties, tags, or excluded fields. Native
save behavior, including default population, still applies.

Saved values live in native `custom_field_data`; native APIs/scripts and normal
Device editing see the same values. The next Parameters request reflects the save
in every repeated occurrence. Native field definitions and visibility settings
are unchanged.

## Repeatable checks

Run from the canonical repository root:

```sh
make test-profiles
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_permissions
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_preservation
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameters
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_rendering
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_permissions
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_editing
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

## Browser acceptance status

Phase 2's eight user acceptance checks passed and its two WINDOWS entries are
closed. The sequence below remains useful when rechecking profile administration.
It is not outstanding Phase 2 work.

Phase 3 browser discovery was retried on 2026-11-07 during Plan 03-04 through
`mcp__cua_repl` and returned `Browsers: Error: The browser access host is unavailable`
with no browser targets. No browser fixture was created and no live data was
changed. Every required Parameters visual case remains **pending**, with fixture,
viewport and expected outcomes in `.planning/phases/03-parameters-tab/03-UAT.md`.
Server tests establish response content and permissions; they do not establish
layout, focus, tooltip interaction or actual horizontal scrolling. Phase 3 is not
visually accepted until those cases have observed evidence.

In the dedicated sandbox, using disposable verification profiles:

1. Create a Selected profile with at least three applicable fields. Drag its last
   field before the first. Save, reopen Edit, and verify the exact order survives.
2. Tab to **Move down** or **Move up**, activate with Enter/Space, and verify focus
   and the announced position. Save and reopen to confirm persistence.
3. Before switching to All, reorder fields and add/remove a field. Save/reopen,
   then switch back to Selected. Verify the pending manual selection and order
   were remembered. All mode should disable manual controls without losing them.
4. Submit with an empty title while retaining several selected fields, their
   order, and at least one rule. Verify the required-title error appears and the
   choices/order/rules remain available for correction. Correct and save.
   Repeat after changing manual fields/order and switching to All before the
   invalid save; switch back to Selected and verify those pending changes remain.
5. Through native tag administration, create an unused tag compatible with
   Devices. Search for it in Device tags on the profile form, select/save/reopen,
   and verify it is retained. Do the same with an unrestricted unused tag.
6. Clear all three rule selectors and verify **Applies to all Devices** appears
   immediately. Add a rule and verify it hides; clear the rule and verify it
   returns. Verify the polite status announcement for both scope changes with
   assistive technology. Save without an extra unrestricted-profile confirmation.
7. With JavaScript disabled, verify the actionable ordering explanation. With
   the ordering asset blocked, verify the loading/reload explanation remains.
   Restore JavaScript/the asset and reload before modifying selected field order.
8. Record the browser/version, profile IDs, exact observed outcomes and redacted
   screenshot paths. No native field settings or values need changing for these
   tests.

On 2026-11-10 the user explicitly deferred all remaining browser UAT to final
manual acceptance. Phase 3’s 15 cases remain pending, and Phase 4 editing cases
are in `.planning/phases/04-edit-parameters/04-UAT.md`. This no longer blocks
development or automated release checks. It does not establish visual acceptance.
