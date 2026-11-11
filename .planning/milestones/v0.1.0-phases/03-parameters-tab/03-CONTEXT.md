# Phase 3: Parameters tab - Context

**Gathered:** 2026-11-07
**Status:** Ready for planning

<domain>
## Phase Boundary

Provide a dedicated, read-only Parameters tab on Device detail pages, rendering
matching enabled profiles as ordered sections with native custom-field values.
Cover TAB-01, TAB-02, TAB-03 and AUTH-01. Native value editing is Phase 4;
release-wide acceptance is Phase 5. This discussion captures planning decisions
and does not authorize implementation.
</domain>

<decisions>
## Implementation Decisions

### Tab visibility and empty states
- **D-01:** Show the Parameters tab when at least one enabled profile matches the
  Device, subject to native Device viewing access. Hide it when none match, keeping
  unrelated Devices uncluttered.
- **D-02:** An authorized direct visit with no matching profiles displays a normal
  empty state: “No parameter profiles apply to this device.” Apply authorization
  before evaluating or disclosing the empty state; do not redirect or grant access.
- **D-03:** A matching profile with no currently available fields remains a section
  with “No fields are available in this profile.” Matching controls tab visibility;
  populated values and field count do not. This avoids silently losing a section
  when an All-mode profile temporarily has no active fields.
- **D-04:** No profile-management permission is required just to view a Device's
  Parameters tab. Do not expose profile administration actions or links without
  their own native permissions. Matching is presentation, never authorization.

### Relevant empty values
- **D-05:** Show every resolved relevant field, including unset values. Use a muted
  “Not set” placeholder so missing data is distinct from an excluded field.
- **D-06:** Do not use truthiness to detect missing values: false and numeric zero
  are real values. Use native field-type semantics for null, empty text and empty
  multi-value collections; preserve meaningful JSON values, including empty JSON
  structures, rather than treating all false-like objects as unset.
- **D-07:** Profile selection determines presentation in Parameters, independently
  of native main-detail `ui_visible` presentation settings. Hidden and If Set fields
  may therefore appear here, including unset fields, as explicitly required by
  docs/REQUIREMENTS.md. Do not change those native settings. This is not permission
  to bypass actual native object/field authorization or related-object restrictions.

### Section and field presentation
- **D-08:** Render one full-width section per matching profile in a vertical stack,
  expanded by default. Reuse NetBox's native card and label/value table styling,
  with responsive wrapping. Do not add nested groups, collapse controls or saved
  per-user layout state in this phase.
- **D-09:** Use the profile title as its heading, preserving duplicate titles and
  the established display_order/title/created/pk order. Within each section use
  Selected membership order or All native active-field order from Phase 2.
- **D-10:** Display the native field label, falling back to its internal name.
  Reuse native field-description/help presentation where available, keeping help
  secondary to values. Do not add filter summaries, mode labels or administrative
  metadata to Device sections.
- **D-11:** Repeat a shared field in each applicable section with identical native
  value and formatting. Read directly from Device native custom-field data; do not
  introduce copied values, plugin value storage or import/synchronization steps.

### Native and complex values
- **D-12:** Prefer the supported NetBox runtime's native custom-field rendering
  utilities for all applicable field types. Preserve native choice labels,
  booleans, dates, numeric formatting, URLs, object references and multi-values.
  Research the exact 4.7.4 integration rather than inventing a parallel formatter.
- **D-13:** Preserve full long text and line breaks, with safe wrapping. Render
  JSON readably through native formatting and contain horizontal overflow locally
  when necessary. Do not silently truncate values or require a new modal to read
  them. Preserve native sanitization, safe link handling and permission behavior.
- **D-14:** Enforce native constrained Device access on navigation and direct URLs;
  handle inaccessible related objects according to native rendering behavior.
  Profile matching and profile administration access confer no additional rights.
- **D-15:** Keep this phase read-only, without an inactive Edit Parameters button.
  Phase 4 supplies the authorized edit action and deduplicated native form.

### Agent's Discretion
The user explicitly delegated all four proposed discussion areas: “You can make
the decisions based on best practices and your own recommendations.” The defaults
above are agent recommendations adopted under that delegation, not individually
selected user answers. Exact markup, native integration points, spacing and help
presentation remain implementation discretion within these behaviors. Native
permission semantics must be investigated against the pinned runtime; escalate a
real conflict with product requirements rather than silently weakening access.
</decisions>

<canonical_refs>
## Canonical References

Downstream agents MUST read these before planning or implementing.

- `docs/REQUIREMENTS.md` — product authority, including independent Parameters
  presentation while native main-detail visibility settings remain unchanged.
- `.planning/REQUIREMENTS.md` — TAB-01, TAB-02, TAB-03 and AUTH-01 traceability.
- `.planning/ROADMAP.md` — Phase 3 boundary and success criteria; editing in Phase 4.
- `.planning/PROJECT.md` — milestone decisions and validated foundation.
- `.planning/phases/02-profile-administration-and-matching/02-CONTEXT.md` — locked
  profile ordering, field modes, matching, duplicate fields and lifecycle decisions.
- `README.md` and `docs/development/sandbox.md` — canonical root source and pinned
  NetBox 4.7.4 / Docker 5.1.1 runtime.
- `docs/development/profiles.md` — existing profile administration and resolver behavior.

External research reference: https://netbox.readthedocs.io/en/stable/customization/custom-fields/
documents native field types and UI visibility as presentation distinct from API
availability. Stable docs may evolve; verify implementation against pinned 4.7.4
source and its plugin view APIs. Product requirements govern intended presentation.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `netbox_custom_field_profiles/matching.py`: get_matching_profiles(device) and
  get_profile_fields(profile) already resolve deterministic matching and active,
  applicable fields. Reuse rather than duplicating filters or lifecycle logic.
- `netbox_custom_field_profiles/models.py`: CustomFieldProfile and ProfileField
  store presentation configuration only; values remain in Device.custom_field_data.
- `netbox_custom_field_profiles/tests/`: native Django/PostgreSQL suite and
  established permission/lifecycle testing patterns.

### Established Patterns
- Native NetBox generic views, constrained querysets and plugin templates.
- Field resolution rechecks current native applicability and provisioning state.
- Existing codebase maps predate root source consolidation and Phase 2: their old
  worktree paths, models and runtime assertions are historical, not current authority.

### Integration Points
- `netbox_custom_field_profiles/views.py` and `urls.py`: currently profile CRUD;
  research native Device model-view/tab registration for the new read-only view.
- `netbox_custom_field_profiles/__init__.py`: plugin initialization/registration.
- `netbox_custom_field_profiles/template_content.py`: intentionally inert after
  old panel retirement. Do not restore an injected main-detail panel.
- `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/`: native
  plugin templates; add the dedicated Device tab using the supported framework.
</code_context>

<specifics>
## Specific Ideas

CMTS Devices with 20–30 fields should remain easy to scan: ordered expanded
sections, consistent label/value rows and visible missing values. CPE Devices
receive only their matching sections. Native script updates must appear on the
next normal page request without copying or synchronizing values.
</specifics>

<deferred>
## Deferred Ideas

No new scope was proposed. Native value editing and a deduplicated Edit Parameters
page remain Phase 4; full workflow/release verification remains Phase 5.
</deferred>

---
*Phase: 03-parameters-tab*
*Context gathered: 2026-11-07*
