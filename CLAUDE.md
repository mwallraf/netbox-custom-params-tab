# Project guidance

Read `docs/REQUIREMENTS.md` for agreed scope, `AGENTS.md` for checkout constraints,
README.md for the public overview, and `.planning/STATE.md` for workflow state.
Canonical source is the root checkout on `milestone/custom-field-profiles`.
Do not create worktrees/per-phase branches or edit/prune ignored `.recovery`.

## Current implementation

- Native CustomFieldProfile/ProfileField configuration, Device-only Selected/All
  resolution, fixed Device Type/role/tag AND/OR/tag-any matching and safe cleanup.
- A dedicated Device Custom Fields tab with ordered sections and native formatting.
  Values remain in native custom_field_data; references use restricted querysets.
- One native partial editor with deduplicated editable fields, constrained Device
  authority, validation, transaction/change logging and preservation of other data.
- Native System plugin metadata with a short Summary, rich Description, URL and
  MIT License via a narrowly scoped compatibility middleware. Keep other plugins,
  cached catalog objects, core templates and superuser checks unchanged.
- No public profile REST API, independent field definitions/value storage,
  automatic native visibility changes or additional object types.

The Device milestone and final manual UAT were accepted by the user on 2026-11-11.
The later missing-static-asset profile-create bug was fixed and user-confirmed.
Do not reopen historical browser deferrals as current blockers. Accepted audit
metadata/Nyquist debt remains documented in `.planning/`.

## Documentation and verification

Start at `docs/README.md` for users and `docs/development/README.md` for maintainers.
`docs/development/architecture.md` explains current integration details.
`docs/history/` and the recovery manifest preserve superseded evidence; do not
execute the old panel implementation plan or use it as current scope.

The exercised sandbox is NetBox 4.7.4 / Docker 5.1.1 at http://127.0.0.1:18047.
Credentials live in ignored `.env`; never print secrets. Use `make test`,
`make test-profiles` and `make release-check`. Native tests use isolated PostgreSQL
and compare live snapshots. The old top-level panel pytest suite is not a passing
baseline. Do not restart services during tests.

After middleware/view registration changes, reload web/workers before verification.
After metadata/JavaScript changes, `make build` then `make up`; source mounts do not
refresh collected static assets. Live smoke checks current JavaScript delivery.
`make down` preserves data; `make reset` destroys only this disposable sandbox.

No migrations or native data/settings changes belong to documentation work.
