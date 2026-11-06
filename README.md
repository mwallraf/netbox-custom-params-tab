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

These are the agreed direction, not a statement of implemented functionality.
The existing implementation still uses one configuration per object model and
renders a panel. GSD onboarding is complete; the five development phases are in
[the roadmap](.planning/ROADMAP.md), with current progress in
[the project state](.planning/STATE.md). No feature implementation has started.

## Source location

The implementation is tracked in this repository root on `milestone/custom-field-profiles`.
The renamed snapshot and feature history were retained in commit `4dba67e`.
The obsolete nested directory is preserved locally in ignored `.recovery/implement-plugin`.
See [source recovery](docs/development/source-recovery.md) for the inventory.

## Rename status

The project was renamed from NetBox Custom Params Tab. Source imports, plugin
configuration, URL namespaces, templates, tests, and Docker paths now use the new
name. Internal `CustomTabConfig` model names remain until the profile model is
designed.

The Django app identifier and URL prefix changed. Existing installations using
the previous name need a migration strategy before using this version against
their database. This rename does not migrate an existing database or regenerate
local editable-install metadata. Rebuild the development image before running it.

## Earlier documents

- [Original design](docs/superpowers/specs/2026-05-04-netbox-custom-field-profiles-design.md)
- [Original implementation plan](docs/superpowers/plans/2026-05-04-netbox-custom-field-profiles.md)

These describe the earlier panel-based design and are retained as background.
The milestone direction above supersedes their conflicting product assumptions.
