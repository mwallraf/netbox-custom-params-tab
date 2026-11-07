# NetBox Custom Field Profiles

## What This Is

A NetBox plugin that organizes existing custom fields into reusable profiles.
The reproducible baseline and Device-profile administration/matching are verified.
The next deliveries are a dedicated Parameters tab and one Edit Parameters page.
Native field storage, definitions, validation, and permissions remain authoritative.

## Core Value

Each Device shows and edits the native custom fields relevant through its matching profiles, without cluttering its main detail page.

## Requirements

### Validated

- ✓ Reproducible source, Docker runtime, schema, authentication and lifecycle baseline — Phase 1.

- ✓ Multiple Device profiles, scoped ordered selections and dynamic All mode — Phase 2.
- ✓ Fixed Device Type/role/tag matching, AND across criteria and OR within values — Phase 2.
- ✓ Native permission parity, data preservation and safe lifecycle cleanup — Phase 2.
- ✓ Profile browser acceptance: eight user-confirmed checks, zero issues — Phase 2.

The Parameters tab, native value editing and release acceptance remain planned.

### Active

- [ ] Dedicated Parameters tab with ordered profile sections.
- [ ] One native-value editing flow with deduplicated inputs and permission parity.
- [ ] CMTS/CPE/shared-profile acceptance and installable documented release.

Detailed IDs and phase assignments: `.planning/REQUIREMENTS.md`.

### Out of Scope

- Independent parameters/value storage: use native custom fields only.
- Native custom field settings or visibility changes: administrators retain control.
- Other object types, multi-object-type profiles, and additional filters: later milestones.
- Nested grouping and arbitrary filter expressions: keep this milestone simple.
- Manual per-object profile assignments: matching is automatic.

## Context

Product authority: `docs/REQUIREMENTS.md` (agreed 2026-11-06).
The May design and plan are historical and superseded where conflicting.
Implementation is canonical in the repository root on `milestone/custom-field-profiles`.
The renamed snapshot and feature history are retained in `4dba67e`; the original
directory remains ignored in `.recovery/implement-plugin`.
CustomFieldProfile and ordered ProfileField memberships replace the old single-config
panel system. Its runtime API/panel and three legacy models were retired with explicit
user approval; native data was preserved. Code review is clean after lifecycle fixes.
The pinned suite has 63 native profile tests; baseline and browser acceptance pass.
See `.planning/codebase/` and `.planning/intel/` for evidence and source synthesis.
A service-provider CMTS/CPE example motivates relevance; it is not hard-coded logic.

## Constraints

- **Data:** Never duplicate native custom field values or erase unrelated values.
- **Permissions:** Match native viewing/editing rules; filters confer no access.
- **Compatibility:** Minimum 4.7.0; actually exercised NetBox 4.7.4 / Docker packaging 5.1.1.
- **Delivery:** Phases 1–2 are verified complete. This file does not authorize implementation of later phases.
- **Identity:** Distribution `netbox-custom-field-profiles`; module/plugin
  `netbox_custom_field_profiles`. New undeployed plugin uses a disposable sandbox; no legacy upgrade is required.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Native custom fields only | Preserve validation, scripts, API, and storage | Verified Phase 2 |
| Devices first | Bound the milestone; extend object types later | Verified Phase 2 |
| Multiple profiles per object type | Reuse relevant sections across many device types | Verified Phase 2 |
| Fixed Device Type, role, tag filters | Simple automatic relevance | Verified Phase 2 |
| AND rules, OR values | Predictable matching, including any selected tag | Verified Phase 2 |
| Selected or dynamically all fields | Explicit control or automatic inclusion | Verified Phase 2 |
| Dedicated tab; profile equals section | Reduce main-page clutter | Agreed; unimplemented |
| One edit page, one input per field | Avoid conflicting duplicate edits | Agreed; unimplemented |
| Native visibility settings untouched | Preserve administrator choices | Verified Phase 2 |
| Normal root checkout and milestone branch | Retain source/history without stale worktrees | Verified Phase 1 |
| Dedicated pinned Docker sandbox | Leave existing workstation NetBox untouched | Verified Phase 1 |
| Clean new-plugin schema, no legacy upgrade | Plugin is new/undeployed; native generated migration | Verified Phase 1 |
| Stable generated credentials; project-only reset | Repeatable setup and isolated disposable data | Verified Phase 1 |

## Phase 2 Implementation Decisions

- Native generic CRUD owns action/object permissions; reference choices are independently validated on the server.
- Manual selections, including pending edits, persist through All saves; All resolution follows native active-field ordering.
- Deleting filter targets disables profiles; invalid field memberships are removed, and empty Selected profiles are disabled until explicitly re-enabled.
- Native-field then profile locking and current-state validation prevent stale saves from undoing cleanup. Form-owned split saves require a shared caller transaction.
- Native unused-tag discovery uses for_object_type_id. Native values/settings remain outside profile write paths.

## Evolution

Update active/validated scope and decisions after verified phase completion.
Keep `docs/REQUIREMENTS.md` as product authority; resolve changes explicitly.

---
*Last updated: 2026-11-07 after Phase 2 completion and user acceptance.*
