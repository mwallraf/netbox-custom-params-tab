# Project guidance

Read `docs/REQUIREMENTS.md` first for the agreed milestone scope. Read AGENTS.md,
README.md and `.planning/STATE.md` for source/workflow/environment constraints.
The canonical source is the root checkout on milestone/custom-field-profiles.
Do not create worktrees or edit the preserved ignored `.recovery` source.

## Implemented through Phase 4 (final manual acceptance pending)

NetBox Custom Field Profiles (`netbox_custom_field_profiles`) stores presentation
configuration referencing native Device custom fields. Phase 2 is verified complete.
Phase 3 implements the read-only Parameters tab; actual desktop/narrow browser
acceptance remains pending and is deferred to final user-run UAT. Phase 4 adds
native value editing through DeviceParametersForm/DeviceParametersEditView.

- `models.py`: CustomFieldProfile (nonunique title, display order, disabled by
  default, Device content type, Selected/All mode, fixed reference sets) and
  ProfileField (ordered explicit membership, unique within one profile).
- `forms.py`: native NetBoxModelForm, scoped reference validation and atomic
  aggregate membership persistence. Explicit remembered selection/order survives
  All-mode saves; omitted remembered input preserves saved state.
- `views.py`, `urls.py`, `tables.py`, `navigation.py`: native generic plugin CRUD
  with action/constrained-object permissions. Matching conveys no access rights.
- `matching.py`: enabled profiles in display_order/title/created/pk order; AND
  across Device Type/role/tag sets, OR within each, tag-any, no rules matches all.
  All mode follows native active-field ordering; Selected follows saved order.
- `signals.py`: plugin-only cleanup for native reference deletion/applicability
  changes. Deleted filter targets disable affected profiles. Invalid selected
  memberships are removed; losing the last selected field disables the profile.
  Cleanup never re-enables automatically. Direct SQL bypass is documented.
- `static/.../profile_fields.js` and profile templates: reorder controls, mode
  switching, scope feedback and editor recovery guidance. Phase 2 browser
  acceptance passed; its ledger entries are closed.
- `views.py`: registered native Device Parameters view, constrained Device lookup
  before resolution/method rejection, matching-controlled tab visibility and normal
  direct no-match state. Viewing requires Device access, not profile administration.
- `presentation.py`, `templatetags/parameter_tags.py`, Parameters templates:
  request-local ordered sections/rows, native type formatting, restricted references,
  escaped native labels/help, full URLs, sanitized multiline Markdown and local JSON
  overflow. Hidden/If Set presentation does not remove relevant rows; unset uses
  Not set, while false, zero and empty JSON remain values. Denied/missing references
  expose no stored IDs; all-denied references show Unavailable. Device editors see
  Edit Parameters when matching editable fields exist.
- `tests/test_parameter*.py`: native tab/navigation, order/type, permission,
  freshness and complete native/plugin preservation regressions. Phase 3 visual
  cases and the browser-host failure are recorded in `03-UAT.md` under its phase.
- `api/serializers.py`: internal profile serializer required by native events;
  no profile REST endpoint is exposed. The obsolete API/panel is retired.
- `migrations/0001_initial.py` and `0002_profiles.py` retain schema history;
  `0003_retire_legacy_configuration.py` removes only approved obsolete plugin
  configuration structures. There is no legacy installation upgrade mapping.

## Development and verification

The pinned sandbox is NetBox 4.7.4 / Docker packaging 5.1.1 at
http://127.0.0.1:18047. Credentials are generated in ignored `.env`; never print
secrets. `make setup` starts the dedicated project. `make test` runs the required
helper/runtime/authentication/seed baseline; `make test-profiles` runs isolated
native Django/PostgreSQL tests and rejects zero tests. Focus a module using
`python3 scripts/test_profiles.py --label <module>`. Do not use historical SQLite
settings or claim the optional legacy pytest suite passes. Restart services before,
never during, a test run. `make down` preserves data; `make reset` deliberately
recreates only the dedicated sandbox. Native generated migrations and schema
checks use the container interpreter, not host Django.

See `docs/development/profiles.md`, `sandbox.md` and `baseline-status.md`.
All values stay in native custom_field_data. Profile management must never alter
native field settings, applicability, visibility or values. Native operations own
their own effects; plugin cleanup writes only plugin configuration tables.
The Parameters view reads native values on every request; external native writes
need no synchronization. Do not claim browser layout acceptance from server HTML.

## Historical design

The original panel-based spec and implementation plan in `docs/superpowers/`
remain background only. Agreed requirements and locked phase context supersede
their conflicting assumptions about one configuration per type, groups, extra
object types and injected panels.

## Verification direction (user instruction 2026-11-10)

Defer all remaining browser UAT to the end, to be performed manually by the user.
Do not attempt browser access or block Phase 4/5 on browser availability. Keep
unobserved cases pending and maintain the final manual checklist. Native tests
and required baseline checks remain mandatory.

The edit form deduplicates current matching fields and honors native UI editability.
It restricts reference choices, omits inaccessible saved references, preserves all
untouched stored values through native validation, and signs the current field
scope to reject stale membership/definition changes. The native edit view handles
change permissions, constrained querysets, validation, change logging and post-save
authority checks. An outer transaction locks the Device before POST reads. No
plugin schema or native field settings are changed.

## Acceptance status — 2026-11-11

Final manual UAT passed by the user’s overall sign-off (“ok, pass UAT”). Earlier
deferral/pending descriptions are historical. No agent browser run or screenshots
are claimed. All five phases are accepted; milestone audit/archival is next.
