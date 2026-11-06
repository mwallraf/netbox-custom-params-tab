# Design: netbox-custom-field-profiles

**Date:** 2026-05-04  
**Status:** Approved  
**Target:** NetBox 4.x

## Overview

A NetBox plugin that moves selected custom fields and/or custom field groups into a dedicated tab on any supported object's detail page. The goal is to reduce clutter on the main object page without losing NetBox's native custom field infrastructure (API, validation, type system).

The plugin is purely presentational: it stores display configuration and injects a tab at render time. All field values remain in NetBox's standard `custom_field_data` — no data duplication.

---

## Data Model

### `CustomTabConfig`

One record per object type. Stores the tab configuration for that type.

| Field | Type | Notes |
|---|---|---|
| `content_type` | FK → ContentType (unique) | Which object type this config applies to |
| `tab_label` | CharField (default: `"Parameters"`) | Label shown on the tab |
| `enabled` | BooleanField | Toggle tab on/off without deleting config |
| `groups` | M2M → CustomFieldGroup (through `CustomTabConfigGroup`) | Groups to display |
| `fields` | M2M → CustomField (through `CustomTabConfigField`) | Standalone fields to display |

### `CustomTabConfigGroup` (through model)

| Field | Type | Notes |
|---|---|---|
| `tab_config` | FK → CustomTabConfig | |
| `group` | FK → CustomFieldGroup | |
| `weight` | PositiveIntegerField (default: 100) | Display order |

### `CustomTabConfigField` (through model)

| Field | Type | Notes |
|---|---|---|
| `tab_config` | FK → CustomTabConfig | |
| `field` | FK → CustomField | |
| `weight` | PositiveIntegerField (default: 100) | Display order |

---

## Tab Rendering

Each supported object type has a `PluginTemplateExtension` subclass registered at plugin startup. When the object detail page renders:

1. The extension queries `CustomTabConfig` for the current content type.
2. If no config exists or `enabled=False`, the extension returns nothing — the tab does not appear.
3. If configured, the extension renders a tab (`full_width_page()`) containing:
   - Groups and standalone fields share a single weight space and are interleaved in ascending `weight` order. A group renders as a labeled section containing all its fields; a standalone field renders as a single row. Items with equal weight are sorted alphabetically as a tiebreaker.
4. Field values are read directly from the object's `custom_field_data` — no separate data fetch needed.

**Visibility on main page:** NetBox's native custom field visibility settings are left untouched. Admins who want a field to appear only in the tab can hide it from the main page using NetBox's own "UI visibility" setting on the custom field.

---

## Admin UI

A section labeled **"Custom Field Profiles"** is added under **Customization** in NetBox's main navigation.

### Views

| View | URL | Purpose |
|---|---|---|
| List | `/plugins/custom-field-profiles/` | All configured object types, with enabled status, group/field counts |
| Create | `/plugins/custom-field-profiles/add/` | New config for an object type |
| Edit | `/plugins/custom-field-profiles/<id>/edit/` | Modify existing config |
| Delete | `/plugins/custom-field-profiles/<id>/delete/` | Confirmation + delete |

### Create/Edit Form

- **Object type** — dropdown restricted to supported types (types with a registered extension); disables already-configured types on the create form
- **Tab label** — text input, default `"Parameters"`
- **Enabled** — checkbox
- **Groups** — filterable multi-select of `CustomFieldGroup` objects, with weight input per entry
- **Standalone fields** — filterable multi-select of `CustomField` objects (filtered to the selected object type), with weight input per entry

All form widgets use NetBox's standard widget styles for a native look and feel.

---

## Supported Object Types

The plugin pre-registers `PluginTemplateExtension` subclasses for the following types at startup:

| App | Models |
|---|---|
| `dcim` | Device, DeviceType, Rack, Site, Location, Cable |
| `virtualization` | VirtualMachine, VMInterface |
| `ipam` | Prefix, IPAddress, VLAN |
| `circuits` | Circuit |

### Extending the Supported List

Admins can add extra types via `PLUGINS_CONFIG` in `configuration.py`:

```python
PLUGINS_CONFIG = {
    "netbox_custom_field_profiles": {
        "extra_models": ["tenancy.Tenant", "dcim.PowerFeed"]
    }
}
```

Extra model extensions are registered dynamically at plugin ready time alongside the built-in list.

---

## Error Handling

- If a `CustomField` or `CustomFieldGroup` referenced in a config is deleted from NetBox, the corresponding through-model row is deleted via `on_delete=CASCADE` on its FK. The tab continues to render with remaining entries.
- If the content type referenced by a `CustomTabConfig` is deleted, the config record is also deleted via cascade.
- If `enabled=False`, the tab is silently omitted — no errors shown to end users.
- Rendering errors (unexpected field data) are caught and logged; the tab renders an error notice rather than crashing the page.

---

## Testing

- **Unit tests:** Model creation, through-model ordering, cascade deletes, `enabled=False` suppression.
- **View tests:** List/create/edit/delete views return correct status codes and context; form validation (duplicate object type, unsupported type).
- **Template extension tests:** Tab appears when config exists and enabled; tab absent when disabled or no config; correct fields/groups rendered.
- **Integration:** Uses NetBox's test fixtures; no mocking of the database.

---

## Plugin Package Structure

```
netbox_custom_field_profiles/
    __init__.py
    models.py          # CustomTabConfig, through models
    views.py           # List, Create, Edit, Delete
    forms.py           # Config form
    tables.py          # List view table
    urls.py            # Plugin URL patterns
    navigation.py      # Customization nav menu entry
    template_content.py  # PluginTemplateExtension subclasses
    templates/
        netbox_custom_field_profiles/
            customtabconfig_list.html
            customtabconfig_edit.html
            customtabconfig_delete.html
            tab_panel.html             # The rendered tab content
    migrations/
setup.cfg / pyproject.toml
```
