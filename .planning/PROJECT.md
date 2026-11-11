# NetBox Custom Field Profiles

## What This Is

A NetBox plugin that organizes existing custom fields into reusable profiles.
Device profiles match automatically and present native values on the Custom Fields
tab, with one Edit Custom Fields page for authorized users.
Native field storage, definitions, validation, and permissions remain authoritative.

## Core Value

Each Device shows and edits the native custom fields relevant through its matching profiles, without cluttering its main detail page.

## Current State

v0.1.0 Device Profiles completed locally on 2026-11-11: five phases, 18 plans and
26 accepted requirements. The current wheel passes 109 native tests; the baseline
has 37 helper tests. User final manual UAT is accepted. This is local milestone
completion and tagging, not a remote publication or production deployment.

## Next Milestone Goals

Not yet defined. Additional object types, multi-object-type profiles and more
criteria are possible future scope; gather user requirements before authorizing
implementation. Use `$gsd-new-milestone`.

## Requirements

### Validated

- ✓ Reproducible source, Docker runtime, schema, authentication and lifecycle baseline — Phase 1.

- ✓ Multiple Device profiles, scoped ordered selections and dynamic All mode — Phase 2.
- ✓ Fixed Device Type/role/tag matching, AND across criteria and OR within values — Phase 2.
- ✓ Native permission parity, data preservation and safe lifecycle cleanup — Phase 2.
- ✓ Profile browser acceptance: eight user-confirmed checks, zero issues — Phase 2.

- ✓ Custom Fields Device tab with ordered native sections and all 13 field types — v0.1.0.
- ✓ One native editor with deduplicated inputs, permissions, validation and preservation — v0.1.0.
- ✓ CMTS/CPE/shared interoperability, installed-wheel verification and user UAT — v0.1.0.
- ✓ Public installation/admin/user documentation, current screenshots and System metadata — v0.1.0.

### Active

None. The next milestone is not scoped.

Detailed completed IDs: [v0.1.0 requirements](milestones/v0.1.0-REQUIREMENTS.md).

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
The current native suite has 109 tests. The installed wheel and baseline pass;
manual acceptance was reported by the user. The current screenshot was supplied
by the user. No automated browser observations are claimed.

Known debt: historical summary/schema/status inconsistencies, missing Phase 4/5
Nyquist records and explicitly overridden stale Phase 1–3 verification digests.
The System metadata adapter depends on tested NetBox 4.7.4 core catalog views;
review it when expanding version support. See the archived audit and MILESTONES.md.
See `.planning/codebase/` and `.planning/intel/` for evidence and source synthesis.
A service-provider CMTS/CPE example motivates relevance; it is not hard-coded logic.

## Constraints

- **Data:** Never duplicate native custom field values or erase unrelated values.
- **Permissions:** Match native viewing/editing rules; filters confer no access.
- **Compatibility:** Minimum 4.7.0; actually exercised NetBox 4.7.4 / Docker packaging 5.1.1.
- **Delivery:** v0.1.0 is complete with accepted debt/overrides. A new milestone requires new scope.
- **Identity:** Distribution `netbox-custom-field-profiles`; module/plugin
  `netbox_custom_field_profiles`. New undeployed plugin uses a disposable sandbox; no legacy upgrade is required.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Native custom fields only | Preserve validation, scripts, API, and storage | ✓ Good — v0.1.0 |
| Devices first | Bound the milestone; extend object types later | ✓ Good — v0.1.0 |
| Multiple profiles per object type | Reuse relevant sections across many device types | ✓ Good — v0.1.0 |
| Fixed Device Type, role, tag filters | Simple automatic relevance | ✓ Good — v0.1.0 |
| AND rules, OR values | Predictable matching, including any selected tag | ✓ Good — v0.1.0 |
| Selected or dynamically all fields | Explicit control or automatic inclusion | ✓ Good — v0.1.0 |
| Dedicated tab; profile equals section | Reduce main-page clutter | ✓ Good — delivered v0.1.0 |
| One edit page, one input per field | Avoid conflicting duplicate edits | ✓ Good — delivered v0.1.0 |
| Native visibility settings untouched | Preserve administrator choices | ✓ Good — v0.1.0 |
| Normal root checkout and milestone branch | Retain source/history without stale worktrees | ✓ Good — baseline retained |
| Dedicated pinned Docker sandbox | Leave existing workstation NetBox untouched | ✓ Good — baseline retained |
| Clean new-plugin schema, no legacy upgrade | Plugin is new/undeployed; native generated migration | ✓ Good — baseline retained |
| Stable generated credentials; project-only reset | Repeatable setup and isolated disposable data | ✓ Good — baseline retained |

Additional decisions: Custom Fields / Edit Custom Fields labels and plugin-specific
Device route paths were selected by the user. Native visibility settings stay
under administrator control. The plugin creates no native field definitions or
separate value storage. MIT license, author Maarten Wallraf, project GitHub URL.

## Implementation Decisions

- Native generic CRUD owns action/object permissions; reference choices are independently validated on the server.
- Manual selections, including pending edits, persist through All saves; All resolution follows native active-field ordering.
- Deleting filter targets disables profiles; invalid field memberships are removed, and empty Selected profiles are disabled until explicitly re-enabled.
- Native-field then profile locking and current-state validation prevent stale saves from undoing cleanup. Form-owned split saves require a shared caller transaction.
- Native unused-tag discovery uses for_object_type_id. Native values/settings remain outside profile write paths.

## Evolution

Update active/validated scope and decisions after verified phase completion.
Keep `docs/REQUIREMENTS.md` as product authority; resolve changes explicitly.

---
*Last updated: 2026-11-11 after v0.1.0 milestone completion.*
