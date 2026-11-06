# Project guidance

Read `docs/REQUIREMENTS.md` first for the agreed milestone scope. Read AGENTS.md,
README.md and `.planning/STATE.md` for source/workflow/environment constraints.
The canonical source is the root checkout on milestone/custom-field-profiles.
Do not create worktrees or edit the preserved ignored `.recovery` source.

## Implemented through Phase 2

NetBox Custom Field Profiles (`netbox_custom_field_profiles`) stores presentation
configuration referencing native Device custom fields. Phase 2 implementation is
complete; final phase verification/live browser acceptance remain pending.
Parameters tab and native-value editing are later phases and are not implemented.

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
  switching, scope feedback and editor recovery guidance. Actual browser
  acceptance remains recorded in `.planning/WINDOWS.md`.
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

## Historical design

The original panel-based spec and implementation plan in `docs/superpowers/`
remain background only. Agreed requirements and locked phase context supersede
their conflicting assumptions about one configuration per type, groups, extra
object types and injected panels.
