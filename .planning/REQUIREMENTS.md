# Requirements: NetBox Custom Field Profiles

**Defined:** 2026-11-06
**Core Value:** Each Device shows and edits the native custom fields relevant through its matching profiles, without cluttering its main detail page.

Source: `docs/REQUIREMENTS.md`; synthesis: `.planning/intel/SYNTHESIS.md`.
BASE requirements are verified complete. Phase 2 is implemented with native test evidence; final browser acceptance remains pending. Later feature/release requirements remain planned. BASE and REL items make the agreed scope reproducible
and verifiable; they do not add new product functionality.

## v1 Requirements

### Reproducible baseline

- [x] **BASE-01**: Establish one usable source checkout while preserving all existing work.
- [x] **BASE-02**: Select/document a supported NetBox version and reproducible dev/test stack.
- [x] **BASE-03**: Install and register the renamed plugin and verify its schema/migrations; define a safe legacy-app/configuration migration policy before applying changes.
- [x] **BASE-04**: Establish a repeatable test baseline with known failures documented and required baseline checks passing before profile development proceeds.

### Profile administration and matching

- [x] **PROF-01**: Administrators can list, create, edit, and delete multiple Device profiles.
- [x] **PROF-02**: Profile object-type selection initially offers Device only; field choices are restricted to native fields applicable to the selected type.
- [ ] **PROF-03**: Each profile has a section title, order, and enabled/disabled state.
- [ ] **PROF-04**: Selected-fields mode stores an ordered explicit field selection.
- [ ] **PROF-05**: All-applicable-fields mode includes new matching fields dynamically.
- [ ] **PROF-06**: The same native field can belong to several profiles.
- [ ] **MATCH-01**: Configure zero or more Device Type, role, and tag rules.
- [ ] **MATCH-02**: Require AND between rules and OR between selected values; tags match any.
- [ ] **MATCH-03**: No rules matches all Devices; only matching enabled profiles apply.
- [x] **DATA-01**: Profile management changes neither native definitions/visibility nor stored field values.

### Parameters tab

- [ ] **TAB-01**: Provide a dedicated Parameters tab on Device detail pages.
- [ ] **TAB-02**: Render matching enabled profiles as ordered sections with ordered fields.
- [ ] **TAB-03**: Display native values consistently, including duplicates across sections, with field-type-appropriate formatting and relevant empty fields handled clearly.
- [ ] **AUTH-01**: Tab and direct view URLs enforce native object/field viewing rules; matching filters do not confer access.

### Edit Parameters

- [ ] **EDIT-01**: One Edit Parameters page covers the currently applicable sections.
- [ ] **EDIT-02**: Repeated fields have one edit input and save one native value.
- [ ] **EDIT-03**: Native custom field validation/types apply and errors are shown clearly.
- [ ] **EDIT-04**: Save to native custom_field_data while preserving unrelated field values.
- [ ] **AUTH-02**: Editing and direct POSTs enforce native object/field editing permissions.

### Release verification

- [ ] **REL-01**: Verify CMTS/CPE/shared profiles, AND/OR matching, dynamic field inclusion, duplicate display/editing, and preservation of values and native settings.
- [ ] **REL-02**: Verify script-written native values display and plugin-written values remain available through native NetBox facilities.
- [ ] **REL-03**: Verify clean package install, migration behavior, and end-to-end UI flow on the supported version; document installation, configuration, and limitations. nested grouping, manual per-object profile assignment, automatic native visibility changes, and a separate authorization system.

## v2 Requirements

- **EXT-01**: Support additional object types, including tenancy/IPAM and VMs.
- **EXT-02**: Allow multiple object types within one profile.
- **EXT-03**: Add further fixed applicability criteria.

## Out of Scope

- Independent parameter storage or a separate authorization system.
- Changes to native custom field settings, visibility, or existing editing screens.
- Arbitrary attribute expressions, nested grouping, and manual per-object assignment.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 1 | Complete |
| BASE-02 | Phase 1 | Complete |
| BASE-03 | Phase 1 | Complete |
| BASE-04 | Phase 1 | Complete |
| PROF-01 | Phase 2 | Complete |
| PROF-02 | Phase 2 | Complete |
| PROF-03 | Phase 2 | Pending |
| PROF-04 | Phase 2 | Pending |
| PROF-05 | Phase 2 | Pending |
| PROF-06 | Phase 2 | Pending |
| MATCH-01 | Phase 2 | Pending |
| MATCH-02 | Phase 2 | Pending |
| MATCH-03 | Phase 2 | Pending |
| DATA-01 | Phase 2 | Complete |
| TAB-01 | Phase 3 | Pending |
| TAB-02 | Phase 3 | Pending |
| TAB-03 | Phase 3 | Pending |
| AUTH-01 | Phase 3 | Pending |
| EDIT-01 | Phase 4 | Pending |
| EDIT-02 | Phase 4 | Pending |
| EDIT-03 | Phase 4 | Pending |
| EDIT-04 | Phase 4 | Pending |
| AUTH-02 | Phase 4 | Pending |
| REL-01 | Phase 5 | Pending |
| REL-02 | Phase 5 | Pending |
| REL-03 | Phase 5 | Pending |

**Coverage:** 26 v1 requirements; 26 mapped; 0 unmapped.

*Last updated: 2026-11-06 after Phase 1 verification.*
