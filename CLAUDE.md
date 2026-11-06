# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current direction

The project is now **NetBox Custom Field Profiles** (`netbox-custom-field-profiles`).
Read `docs/REQUIREMENTS.md` first for the agreed requirements. Profiles initially
target Devices, with optional Device Type, role, and tag filters (AND between
rules, OR within a rule). Matching profiles become sections in a dedicated
Parameters tab, with one Edit Parameters page. These requirements supersede the
earlier design and implementation plan. The implementation below still describes
the earlier panel-based model; the new features have not yet been implemented.

## What this project currently implements

A NetBox 4.x plugin (`netbox_custom_field_profiles`) that moves selected custom fields and/or custom field groups into a dedicated panel section on any supported object's detail page. It is **purely presentational**: all field values live in NetBox's native `custom_field_data` — the plugin only stores display configuration.

Design spec: `docs/superpowers/specs/2026-05-04-netbox-custom-field-profiles-design.md`  
Implementation plan: `docs/superpowers/plans/2026-05-04-netbox-custom-field-profiles.md`

## Current development commands

Use `make setup` then http://127.0.0.1:18047. Generated credentials are in local
ignored `.env`; there are no fixed/default passwords. `make test` runs the
blocking stdlib and real runtime/session/API/seed baseline. `make test-legacy`
reports the optional old pytest suite honestly; its runner is currently absent.
Use `make down` to retain data, or explicit `make reset` for project-only reset.
See [sandbox guide](docs/development/sandbox.md) for all supported targets and
[baseline status](docs/development/baseline-status.md) for measured evidence.
Migrations use the native container interpreter with developer mode, not old
SQLite settings. NetBox 4.7.4 / Docker packaging 5.1.1 is exercised; plugin minimum
is 4.7.0. The architecture below describes retained legacy feature code, not a
verified profile implementation.

## Architecture

### Plugin registration (`netbox_custom_field_profiles/__init__.py`)

`CustomFieldProfilesConfig(PluginConfig)` is the entry point. Its `ready()` method reads `PLUGINS_CONFIG['netbox_custom_field_profiles']['extra_models']` and rebuilds `template_content.template_extensions` so dynamically configured models are registered at startup. The `template_extensions` and `menu_items` attributes are string paths resolved by NetBox at load time.

### Data model

Three models store display config only — no field values:

- `CustomTabConfig` — one row per object type (`OneToOneField` → `ContentType`). Inherits from `NetBoxModel` to get `get_absolute_url()` and standard NetBox view compatibility.
- `CustomTabConfigGroup` / `CustomTabConfigField` — through models with a `weight` field controlling display order. Both cascade-delete when their parent config, or the referenced `CustomFieldGroup`/`CustomField`, is deleted.

### Tab rendering (`template_content.py`)

`_make_extension(model_path)` is a factory that returns a `PluginTemplateExtension` subclass for one model. It is called at module load to populate `template_extensions` (NetBox reads this list when rendering pages). `full_width_page()` on each extension:

1. Looks up `CustomTabConfig` for the current content type
2. Returns `''` if no config or `enabled=False`
3. Merges group entries and field entries into one list, sorts by `(weight, name)`
4. Calls `self.render('netbox_custom_field_profiles/tab_panel.html', ...)`

Field values are read directly from `object.custom_field_data` — no extra DB query.

### Forms and views

`CustomTabConfigEditView` is a plain Django `View` (not `ObjectEditView`) because it must handle two inline formsets (`CustomTabConfigGroupFormSet`, `CustomTabConfigFieldFormSet`) alongside the main form. All three are validated and saved atomically in a single `transaction.atomic()` block.

The `content_type` dropdown in `CustomTabConfigForm` is restricted to supported model content types. On create, already-configured types are excluded. On edit, the current type stays selectable.

### Template tag

`netbox_custom_field_profiles/templatetags/customtab_tags.py` provides the `|dict_value` filter used in `tab_panel.html` to look up raw custom field values from `object.custom_field_data` by field name.

## Key constraints

- **No data duplication.** Never store custom field values in plugin models — always read from `object.custom_field_data`.
- **`enabled=False` must be silent.** When a config is disabled, the tab must simply not appear — no error, no empty panel.
- **Weight + alpha ordering.** Groups and standalone fields share one weight space. Equal-weight items sort alphabetically by name.
- **Cascade safety.** Deleting a `CustomField`, `CustomFieldGroup`, or `ContentType` from NetBox removes the corresponding through-model rows but leaves the rest of the config intact.
- **Supported types are extensible.** `BUILTIN_MODELS` in `template_content.py` is the fixed list; `extra_models` from `PLUGINS_CONFIG` is appended in `ready()`. Never hardcode the full list outside `template_content.py`.

## Canonical source

Use the normal repository root on milestone/custom-field-profiles; no worktrees.
Consult README and tracked development documentation for current setup.
