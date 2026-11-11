# NetBox Custom Field Profiles

Package: `netbox-custom-field-profiles`  
Python module and NetBox plugin identifier: `netbox_custom_field_profiles`

Organize NetBox's existing custom fields into relevant, grouped views for objects.
Custom field definitions, visibility settings, and values remain managed by NetBox.

## Agreed milestone direction

See [agreed requirements](docs/REQUIREMENTS.md) for the authoritative milestone scope,
filter matching rules, acceptance examples, and remaining planning details.

- Reusable field profiles for Devices, with optional Device Type, role, and tag filters.
- A dedicated Parameters tab; each matching profile is an ordered section.
- Selected fields or dynamically all applicable fields; duplicates across profiles allowed.
- One Edit Parameters page using native custom field values, validation, and permissions.
- A separate profile administration interface; NetBox's custom field settings stay unchanged.
- No independent parameter storage or automatic changes to native field visibility.

Profile administration and matching are implemented: native plugin CRUD,
ordered Selected/All field modes, fixed applicability filters, and safe lifecycle
cleanup. The old panel/API and configuration schema have been retired. Phase 3
adds a read-only Device **Parameters** tab with matching ordered sections,
native typed values, explicit empty states and native viewing permissions.
Native script writes appear on the next request; profile changes preserve values
and native visibility settings. Phase 3 desktop/narrow browser acceptance is
deferred to final manual acceptance by the user. Phase 4 adds **Edit Parameters**,
using native widgets, validation, permissions and change logging with one input per
relevant editable field. See the
[administration guide](docs/development/profiles.md),
[roadmap](.planning/ROADMAP.md), and [project state](.planning/STATE.md).

## Source location

The implementation is tracked in this repository root on `milestone/custom-field-profiles`.
The renamed snapshot and feature history were retained in commit `4dba67e`.
The obsolete nested directory is preserved locally in ignored `.recovery/implement-plugin`.
See [source recovery](docs/development/source-recovery.md) for the inventory.

## Rename status

The project was renamed from NetBox Custom Params Tab. Source imports, plugin
configuration, URL namespaces, templates, tests, and Docker paths now use the new
name. `CustomFieldProfile` and ordered `ProfileField` memberships replace the old
`CustomTabConfig` models; migrations retain the original history and explicitly
retire the obsolete configuration schema.

## Development sandbox

Run `make setup`, then open <http://127.0.0.1:18047>. Administrator credentials
are generated once in the ignored local `.env` file. Run `make test` for native
runtime, migration, real admin/API authentication and dummy-data checks. Run `make test-profiles`
for the isolated native profile suite; see the guide for focused test labels.

The exercised baseline is NetBox **4.7.4**, Docker packaging **5.1.1**; minimum
plugin version is 4.7.0. Other versions have not been verified. The dedicated
Compose project leaves other workstation NetBox installations untouched.
`make down` preserves data; `make reset` deliberately recreates this project's
sandbox database while retaining credentials.

See [installation and supported runtime](docs/development/installation.md),
[sandbox guide](docs/development/sandbox.md) and
[actual baseline status](docs/development/baseline-status.md).
Run `make release-check` for an isolated installed-wheel/fresh-database check.
The [final manual UAT guide](docs/development/final-uat.md) collects the deferred
browser acceptance steps.
This is a new, undeployed plugin using a disposable development database: no
legacy app/data upgrade is needed or supported by this baseline. Profile administration,
matching, the Parameters tab and native value editing are implemented. Browser UAT
is deferred to final manual acceptance; automated checks remain required.

## Earlier documents

- [Original design](docs/superpowers/specs/2026-05-04-netbox-custom-field-profiles-design.md)
- [Original implementation plan](docs/superpowers/plans/2026-05-04-netbox-custom-field-profiles.md)

These describe the earlier panel-based design and are retained as background.
The milestone direction above supersedes their conflicting product assumptions.

## Acceptance status — 2026-11-11

Final manual UAT passed by the user’s overall sign-off (“ok, pass UAT”). Earlier
deferral/pending descriptions are historical. No agent browser run or screenshots
are claimed. All five phases are accepted; milestone audit/archival is next.
