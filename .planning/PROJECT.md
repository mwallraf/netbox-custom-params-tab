# NetBox Custom Field Profiles

## What This Is

A NetBox plugin that organizes existing custom fields into reusable profiles.
Matching profiles appear as sections in a dedicated Parameters tab, with one
Edit Parameters page. The initial milestone supports Devices; native field
storage, definitions, validation, and permissions remain authoritative.

## Core Value

Each Device shows and edits the native custom fields relevant through its matching profiles, without cluttering its main detail page.

## Requirements

### Validated

- ✓ Reproducible source, Docker runtime, schema, authentication and lifecycle baseline — Phase 1.

Legacy feature behavior remains unverified; this is not a working profile release.

### Active

- [ ] Multiple Device profiles with scoped field selection and dynamic all-fields mode.
- [ ] Device Type, role, and tag matching; AND between rules, OR within values.
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
Existing code supports one config per model and an inline panel, not profiles.
See `.planning/codebase/` and `.planning/intel/` for evidence and source synthesis.
A service-provider CMTS/CPE example motivates relevance; it is not hard-coded logic.

## Constraints

- **Data:** Never duplicate native custom field values or erase unrelated values.
- **Permissions:** Match native viewing/editing rules; filters confer no access.
- **Compatibility:** Minimum 4.7.0; actually exercised NetBox 4.7.4 / Docker packaging 5.1.1.
- **Delivery:** Onboarding is planning only; no execution is authorized by this file.
- **Identity:** Distribution `netbox-custom-field-profiles`; module/plugin
  `netbox_custom_field_profiles`. New undeployed plugin uses a disposable sandbox; no legacy upgrade is required.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Native custom fields only | Preserve validation, scripts, API, and storage | Agreed; unverified |
| Devices first | Bound the milestone; extend object types later | Agreed; unimplemented |
| Multiple profiles per object type | Reuse relevant sections across many device types | Agreed; unimplemented |
| Fixed Device Type, role, tag filters | Simple automatic relevance | Agreed; unimplemented |
| AND rules, OR values | Predictable matching, including any selected tag | Agreed; unimplemented |
| Selected or dynamically all fields | Explicit control or automatic inclusion | Agreed; unimplemented |
| Dedicated tab; profile equals section | Reduce main-page clutter | Agreed; unimplemented |
| One edit page, one input per field | Avoid conflicting duplicate edits | Agreed; unimplemented |
| Native visibility settings untouched | Preserve administrator choices | Agreed; unverified |
| Normal root checkout and milestone branch | Retain source/history without stale worktrees | Verified Phase 1 |
| Dedicated pinned Docker sandbox | Leave existing workstation NetBox untouched | Verified Phase 1 |
| Clean new-plugin schema, no legacy upgrade | Plugin is new/undeployed; native generated migration | Verified Phase 1 |
| Stable generated credentials; project-only reset | Repeatable setup and isolated disposable data | Verified Phase 1 |

## Evolution

Update active/validated scope and decisions after verified phase completion.
Keep `docs/REQUIREMENTS.md` as product authority; resolve changes explicitly.

---
*Last updated: 2026-11-06 after Phase 1 completion.*
