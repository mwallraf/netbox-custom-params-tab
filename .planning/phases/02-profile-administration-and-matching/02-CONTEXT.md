# Phase 2: Profile administration and matching - Context

**Gathered:** 2026-11-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Provide administration of reusable Device profiles and determine which enabled
profiles match a Device. Cover PROF-01 through PROF-06, MATCH-01 through MATCH-03,
and DATA-01. Profiles reference native NetBox custom fields and store presentation
configuration only. The Parameters tab is Phase 3; editing native values is Phase 4;
full feature/release acceptance is Phase 5. This discussion authorizes context
capture, not feature execution.
</domain>

<decisions>
## Implementation Decisions

### Profile administration
- **D-01:** Manage profiles through standard NetBox plugin pages: list, add, edit,
  delete, accessible under Custom Field Profiles. Django-admin-only or dual
  administration was not selected.
- **D-02:** One title identifies the profile in administration and supplies its
  eventual section heading; no separate internal name or override title.
- **D-03:** Duplicate titles are allowed, including profiles with different filters.
- **D-04:** The list shows title, enabled state, display order, field-selection mode,
  and a readable applicability-filter summary.

### Field selection and ordering
- **D-05:** Selected fields are arranged by drag-to-reorder.
- **D-06:** All applicable fields dynamically follows native NetBox custom-field
  ordering, including newly applicable fields; do not replace with alphabetical
  label/internal-name ordering.
- **D-07:** Switching to All applicable fields remembers the manual selection and
  its order. Ignore that selection in All mode and restore it on switching back.
- **D-08:** Selected mode requires at least one applicable field when an
  administrator saves a configuration. Loss of fields through external changes
  follows D-14; do not block native deletion merely to maintain this form invariant.

### Filter configuration
- **D-09:** Provide three optional searchable multi-selects: Device Type, device
  role, and tag, rather than a repeatable rule-row editor. Empty selectors impose
  no restriction. AND across populated criteria; OR within each criterion, including
  any selected tag, remains locked by the agreed requirements.
- **D-10:** With all selectors empty, show an inline “Applies to all Devices” notice.
  Do not require an extra unrestricted-profile save confirmation.
- **D-11:** New profiles start disabled. An administrator enables them explicitly
  after configuring them.
- **D-12:** The tag selector includes all tags available for Devices, including tags
  not currently assigned to a Device; do not restrict choices to used tags.

### Changes and deletion
- **D-13:** Deleting any referenced Device Type, role, or tag disables every affected
  profile for review. Do not silently broaden matching and do not block native
  deletion instead. Profiles stay disabled until explicitly re-enabled (D-16).
- **D-14:** If a selected custom field is deleted or loses Device applicability,
  remove its invalid selected membership. Keep profiles with valid remaining
  selected fields usable; disable a Selected-mode profile if none remain. Native
  field settings and stored values are never modified as a side effect.
- **D-15:** Equal profile display-order numbers sort alphabetically by title, then
  by creation order (oldest first) when titles also match. Duplicate titles must
  still produce deterministic ordering.
- **D-16:** Correcting an automatically disabled profile does not re-enable it.
  Require an explicit administrator action to enable it again.

### Implementation discretion and inherited constraints
- No specific “you decide” answer was given; the 16 choices above are locked.
  Research/planning chooses internal model structure, native framework integration,
  validation, accessible reorder mechanics, and technical ordering tie-breaks
  consistent with those choices. Do not turn these into additional product scope.
- Devices only, a single object type per profile, existing native fields only,
  Selected/All modes, multiple profiles and duplicate field occurrences across
  profiles remain inherited requirements. Filters affect relevance, not authority.
- Phase 1 established the normal root checkout on milestone/custom-field-profiles,
  NetBox 4.7.4 / Docker packaging 5.1.1, native generated migrations and the dedicated
  sandbox. No worktrees or per-phase branches. The plugin is undeployed; no legacy
  installation upgrade is required. Preserve native values when replacing old
  configuration structures.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Product and workflow authority
- `docs/REQUIREMENTS.md` — agreed native-field/profile scope; overrides historical panel design.
- `.planning/REQUIREMENTS.md` — PROF-01..06, MATCH-01..03, DATA-01 traceability.
- `.planning/ROADMAP.md` — fixed Phase 2 boundary and later tab/edit/release phases.
- `.planning/PROJECT.md` — project constraints, baseline and validated decisions.
- `.planning/phases/01-reproducible-baseline/01-CONTEXT.md` — inherited sandbox,
  source workflow, clean-database and native-validation constraints.
- `docs/development/sandbox.md` — current runnable environment and actual Make commands.
- `docs/development/baseline-status.md` — successful baseline and unexecuted optional legacy tests.

### Current source integration
- `netbox_custom_field_profiles/models.py` — retained one-config-per-type/weighted membership model to replace.
- `netbox_custom_field_profiles/forms.py` — native form/formset patterns; current unscoped choices are not the new requirements.
- `netbox_custom_field_profiles/views.py` — configuration administration and atomic save patterns.
- `netbox_custom_field_profiles/navigation.py` — plugin menu integration.
- `netbox_custom_field_profiles/urls.py` — plugin page routing.
- `netbox_custom_field_profiles/migrations/0001_initial.py` — actual generated baseline schema.

No external specification was selected during this discussion. Version-specific
NetBox integration remains research work; do not infer support from old code.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Existing configuration list/edit/delete pages, tables, navigation and routes
  provide a starting point for standard NetBox plugin administration.
- Existing explicit field memberships use a through model with numeric weights;
  that storage pattern may support persisted drag ordering without exposing
  numeric ordering as the chosen interaction.
- Native NetBoxModel/NetBoxModelForm and atomic form/formset saves are present.
- Phase 1 sandbox offers native ORM seed devices/fields and repeatable runtime,
  authentication, schema and lifecycle checks.

### Established Patterns
- Plugin configuration references native CustomField objects; values remain on
  native objects. Multiple profiles must replace the old ContentType OneToOne
  restriction; old nested groups do not belong in the new profile design.
- Existing forms offer fields beyond the selected type; the new administration
  must constrain Device field choices and validate them beyond the UI.
- Codebase maps predate Phase 1 recovery; their nested source paths and handwritten
  migration notes are historical. Current source is at root.

### Integration Points
- New profile administration connects model/form/table/view/URL/navigation layers.
- Profile matching and ordered field resolution must be reusable by later tab
  display and deduplicated editing, without implementing those phases now.
- Native reference deletion/applicability changes must honor D-13/D-14 without
  unexpectedly broadening matching or modifying native values/settings.
</code_context>

<specifics>
## Specific Ideas

A CMTS-specific profile, a CPE-specific profile and an unrestricted shared profile
remain the agreed examples. Repeated headings such as “Service Details” may be
used for profiles with different filters. “Applies to all Devices” is the chosen
inline unrestricted-profile message. All 16 concrete discussion questions were
answered with their first presented option; no alternatives were delegated.
</specifics>

<deferred>
## Deferred Ideas

No new scope was introduced. Parameters tab/no-match/empty-value presentation
belongs to Phase 3; native editing to Phase 4; full acceptance/release to Phase 5.
Other object types, arbitrary filter expressions and nested grouping remain out
of this milestone as already agreed.
</deferred>

---
*Phase: 02-profile-administration-and-matching*
*Context gathered: 2026-11-06*
