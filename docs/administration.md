# Profile administration

This guide covers configuration and permissions for the implemented Device
workflow. For a short walkthrough, start with the [user guide](user-guide.md).

## Manage profiles

Open **Plugins → Custom Field Profiles** in your NetBox installation. Use the
[installation guide](installation.md) if the plugin is not enabled yet.

Users need the native profile `view`, `add`, `change`, or `delete` permissions
for the corresponding operation. NetBox object constraints apply to list results
and direct URLs. Relevance filters grant no authority. Native permissions also
restrict referenced choices; an editor cannot silently clear a saved rule whose
reference they cannot access. Such a profile needs review by an authorized
administrator.

Choose **Add** to create a profile. Devices are the only supported Object Type.
The title identifies the profile and supplies its Custom Fields section heading;
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
message provides the same recovery action when JavaScript is disabled. See
[troubleshooting](troubleshooting.md) if the script is missing or stale.

### Applicability

Device Type, device role, and Device tags are optional searchable multi-selects.
Each populated selector accepts **any** selected value (OR); populated selectors
must **all** match (AND). The tag rule accepts any selected tag on the Device.
Empty selectors impose no restriction. When all are empty, the edit page shows
**Applies to all Devices**, with no extra unrestricted-save confirmation.
An always-present polite status region announces unrestricted or restricted
scope when these selectors change.

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

## View Device Custom Fields

The tab uses `/dcim/devices/<id>/plugin-custom-field-profiles/`. Update any bookmarks
using the former `/parameters/` path; the plugin no longer registers that path.

Open a Device's native detail page and choose **Custom Fields**. The tab appears when
at least one enabled profile matches, including a matching profile that currently
has no fields. Each profile is an expanded full-width card; duplicate titles are
retained. Sections use the same deterministic profile order described above;
Selected fields use saved membership order and All uses current native order.

Users need native Device viewing access, including any object constraints. They
do not need profile or custom-field definition administration permissions. Matching
never grants access. Direct tab URLs enforce the same Device boundary. An
authorized direct visit with no match says **No parameter profiles apply to this
device.** A matching section without fields says **No fields are available in this
profile.** Custom Fields exposes no profile administration metadata. Authorized Device
editors see **Edit Custom Fields** when at least one matching field can be edited.

Every relevant field appears, including fields set to native **Hidden** or **If
Set** presentation on the normal detail page. Those native settings remain
unchanged. Missing/null values, empty text and empty multi-value collections show
muted **Not set**. False and numeric zero are values. JSON `{}`, `[]`, `false`, `0`
and empty string remain JSON values. Labels fall back to the exact internal field
name; descriptions use secondary native help tooltips with escaped text.

Values use native type formatting, choice labels/colors and sanitized Markdown.
URLs retain their complete visible text; links obey NetBox's configured URL scheme
policy. Long text retains complete content and line breaks; JSON uses native
preformatted output with local horizontal overflow.

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

## Edit Device Custom Fields

On a matching Device’s Custom Fields tab, choose **Edit Custom Fields**. The single form
follows first-occurrence section/field order and offers each native field once,
including fields repeated across profiles. Native Device change permission and
object constraints apply to both the action and direct GET/POST requests; profile
administration permission is not required. The route is
`/dcim/devices/<id>/plugin-custom-field-profiles/edit/`. Save and Cancel return
to Custom Fields.

Only active, applicable fields in currently matching enabled profiles whose native
UI editability is Yes are offered. Fields with **UI editable** set to No or Hidden retain
their stored values and are not offered by the editor. This is separate from
**UI visibility**, which controls main-detail display. A field containing inaccessible saved references is omitted
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
Device editing see the same values. The next Custom Fields request reflects the save
in every repeated occurrence. Native field definitions and visibility settings
are unchanged.


[Documentation index](README.md) · [Troubleshooting](troubleshooting.md)
