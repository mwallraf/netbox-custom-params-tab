# Requirement inventory for scaffold review

Source: `docs/REQUIREMENTS.md`. All requirements are pending implementation and
verification. BASE and REL items are proposed engineering acceptance requirements
needed to make the agreed product scope installable and verifiable.

## Phase 1 — Reproducible baseline

- BASE-01: Establish one usable source checkout while preserving all existing work.
- BASE-02: Select/document a supported NetBox version and reproducible dev/test stack.
- BASE-03: Install and register the renamed plugin and verify its schema/migrations;
  define a safe legacy-app/configuration migration policy before applying changes.
- BASE-04: Establish a repeatable test baseline with known failures documented and
  required baseline checks passing before profile development proceeds.

## Phase 2 — Profile administration and matching

- PROF-01: Administrators can list, create, edit, and delete multiple Device profiles.
- PROF-02: Profile object-type selection initially offers Device only; field choices
  are restricted to native fields applicable to the selected type.
- PROF-03: Each profile has a section title, order, and enabled/disabled state.
- PROF-04: Selected-fields mode stores an ordered explicit field selection.
- PROF-05: All-applicable-fields mode includes new matching fields dynamically.
- PROF-06: The same native field can belong to several profiles.
- MATCH-01: Configure zero or more Device Type, role, and tag rules.
- MATCH-02: Require AND between rules and OR between selected values; tags match any.
- MATCH-03: No rules matches all Devices; only matching enabled profiles apply.
- DATA-01: Profile management changes neither native definitions/visibility nor
  stored field values.

## Phase 3 — Parameters tab

- TAB-01: Provide a dedicated Parameters tab on Device detail pages.
- TAB-02: Render matching enabled profiles as ordered sections with ordered fields.
- TAB-03: Display native values consistently, including duplicates across sections,
  with field-type-appropriate formatting and relevant empty fields handled clearly.
- AUTH-01: Tab and direct view URLs enforce native object/field viewing rules;
  matching filters do not confer access.

## Phase 4 — Edit Parameters

- EDIT-01: One Edit Parameters page covers the currently applicable sections.
- EDIT-02: Repeated fields have one edit input and save one native value.
- EDIT-03: Native custom field validation/types apply and errors are shown clearly.
- EDIT-04: Save to native custom_field_data while preserving unrelated field values.
- AUTH-02: Editing and direct POSTs enforce native object/field editing permissions.

## Phase 5 — Release verification

- REL-01: Verify CMTS/CPE/shared profiles, AND/OR matching, dynamic field inclusion,
  duplicate display/editing, and preservation of values and native settings.
- REL-02: Verify script-written native values display and plugin-written values
  remain available through native NetBox facilities.
- REL-03: Verify clean package install, migration behavior, and end-to-end UI flow
  on the supported version; document installation, configuration, and limitations.

## Deferred

- Other object types, including tenancy/IPAM and Virtual Machines.
- Multiple object types in one profile.
- Additional fixed filter criteria beyond Device Type, role, and tag.

## Excluded from this milestone

- Independent parameter storage, arbitrary object-attribute expressions,
  nested grouping, manual per-object profile assignment, automatic native
  visibility changes, and a separate authorization system.
