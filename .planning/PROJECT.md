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

None yet. Existing panel-based code has not been verified as a working release.

### Active

- [ ] Reproducible development, test, source, and migration baseline.
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
Implementation lives in `.worktrees/feature/implement-plugin/`; its stale Git
metadata and uncommitted changes must be preserved and reconciled in Phase 1.
Existing code supports one config per model and an inline panel, not profiles.
See `.planning/codebase/` and `.planning/intel/` for evidence and source synthesis.
A service-provider CMTS/CPE example motivates relevance; it is not hard-coded logic.

## Constraints

- **Data:** Never duplicate native custom field values or erase unrelated values.
- **Permissions:** Match native viewing/editing rules; filters confer no access.
- **Compatibility:** Select and verify exact supported NetBox runtime in Phase 1.
- **Delivery:** Onboarding is planning only; no execution is authorized by this file.
- **Identity:** Distribution `netbox-custom-field-profiles`; module/plugin
  `netbox_custom_field_profiles`. Renamed app migration policy remains unresolved.

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

## Evolution

Update active/validated scope and decisions after verified phase completion.
Keep `docs/REQUIREMENTS.md` as product authority; resolve changes explicitly.

---
*Last updated: 2026-11-06 after approved GSD onboarding scaffold creation.*
