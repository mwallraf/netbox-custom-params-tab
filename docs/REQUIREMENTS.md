# NetBox Custom Field Profiles — agreed requirements

Product scope agreed: 2026-11-06. The Device-profile milestone is implemented;
manual UAT was accepted by the user on 2026-11-11. This document remains the scope
contract and supersedes the archived panel-based design where they conflict.

For current usage and installation, start with the [documentation index](README.md).
Implementation evidence and workflow status are maintained in
[the project state](../.planning/STATE.md) and phase records. Requirements for later
object types or capabilities are not implementation authorization by themselves.

## Identity and purpose

- Product name: **NetBox Custom Field Profiles**.
- Distribution/package name: `netbox-custom-field-profiles`.
- Python module and NetBox plugin identifier: `netbox_custom_field_profiles`.
- Organize native NetBox custom fields into relevant sections for each object.
- Use case: a service provider has CMTS devices needing 20–30 custom fields and
  CPE devices needing only two. There may be more than 20 device types; the
  solution must use reusable profiles rather than hard-coded device categories.

## Native custom fields remain authoritative

- Use existing NetBox custom fields only; no independent custom parameter system.
- Store field values in NetBox's native custom field data, without duplication.
- Leave NetBox's custom field definition/settings pages and native visibility
  settings unchanged. Administrators may hide fields on the normal detail page
  using native settings while presenting them in the Parameters tab.
- Values may be populated or updated by external scripts using native NetBox
  facilities. The plugin must remain generic and not depend on those scripts.
- Viewing and editing must follow the same permissions, validation, and field
  behavior as native NetBox custom fields. Profile visibility is presentation,
  not a separate authorization system.

## Milestone scope and object types

- Initially support **Devices** (`dcim.device`).
- Profile administration includes an object-type selector. The available custom
  fields must be restricted to fields applicable to the selected object type.
- Multiple object types per profile and support for other object types are
  deferred to later milestones. Do not implement Devices/Virtual Machines combined
  profiles in the initial scope.
- Keep the design extensible for additional object types and filter criteria,
  including tenancy and IPAM use cases, without building a general-purpose
  filter expression system in this milestone.

## Profiles and administration

- Provide a separate administration interface for creating and managing profiles.
- Allow any number of profiles for the same supported object type.
- Each profile has a section title, display order, and enabled/disabled state.
- Each matching enabled profile renders as one section in the Parameters tab.
- A profile contains an ordered list of fields; no nested grouping initially.
- A custom field may appear in multiple profiles. Every occurrence represents
  the same underlying native value.
- Support two explicit field-selection modes:
  - **Selected fields:** an explicit selection of applicable existing fields.
  - **All applicable fields:** dynamically include all fields applicable to the
    object type, including matching fields created after profile configuration.

## Profile applicability filters

- A profile can have zero, one, or multiple filter rules.
- Initially provide fixed filters for **Device Type**, **device role**, and **tag**.
- A profile with no rules applies to all Devices.
- Combine rules with **AND**; combine selected values within one rule with **OR**.
- For a tag rule containing several tags, having any selected tag satisfies that
  rule.
- Example: Device Type is A or B, AND role is Access, AND the device has any tag
  selected in the tag rule.
- Display only profiles whose filters match the current object. Matching is
  automatic; no manual per-object profile assignment is required initially.
- Filters should remain simple for administrators. Additional criteria can be
  added later; arbitrary object-attribute traversal is not an initial requirement.

## Parameters tab

- Provide a dedicated **Parameters** tab, replacing the earlier panel approach.
- Show applicable enabled profiles as ordered sections, with their selected or
  dynamically applicable custom fields.
- Relevant empty fields are distinct from fields excluded by profile selection
  or filtering; the exact empty-value presentation remains a planning detail.
- Profile changes must not erase stored field values.

## Editing

- Provide one **Edit Parameters** page covering the applicable sections.
- When a field occurs in multiple profiles, edit it once to avoid conflicting
  inputs; show its saved value consistently wherever it appears.
- Save through NetBox's native custom field validation and permission rules.
- Do not change NetBox's existing custom field editing screens.

## Acceptance examples

1. A CMTS Device matches a CMTS profile and shows its 20–30 configured fields.
   A CPE Device does not show that section unless it also satisfies its rules.
2. A CPE Device matches a CPE profile and shows its two configured fields.
3. A shared profile without filters appears on both devices.
4. Several profiles can match one device and appear as separate ordered sections.
5. A field repeated across sections displays one native value and has one edit
   input on Edit Parameters.
6. Creating an applicable native custom field adds it automatically to profiles
   using All applicable fields, but not to Selected fields profiles.
7. Native field visibility settings remain unchanged when profiles are managed.
8. Script-written native values appear in the tab without copying or importing
   them into plugin-specific value storage.

## Resolved implementation details

- Exercised runtime: NetBox 4.7.4 / Docker packaging 5.1.1; declared minimum 4.7.0.
- Source: canonical repository root; original recovery snapshot retained locally.
- Installation: clean plugin migrations; no legacy-installation data mapping.
- No-match behavior: Parameters navigation is absent without an enabled match;
  an authorized direct visit displays the documented no-profile message.
- Profile order: display order, title, creation time, primary key. All follows
  native active-field order; Selected follows saved membership order.
- Unset values are shown as Not set; false/zero and empty JSON remain values.
- Deleted filter targets disable affected profiles rather than broadening matches;
  invalid selected membership is removed and empty Selected profiles are disabled.

See [administration](administration.md) for exact behavior and
[architecture](development/architecture.md) for native integration boundaries.
