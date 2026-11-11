# Architecture and integration boundaries

## Native data remains authoritative

`CustomFieldProfile` stores section title, order, enable state, one Device content
type, field-selection mode and fixed Device Type/role/tag relations. `ProfileField`
stores an ordered reference to an existing native custom field. Neither model
stores field values or creates native field definitions.

`matching.py` resolves enabled profiles using AND across populated criteria and OR
within selected values, with tag-any matching. Profile order is
`display_order`, `title`, `created`, `pk`; Selected follows saved membership order,
and All follows native active-field order. A fresh applicability/status guard
excludes stale or inactive definitions.

## Display and edit flow

`PluginConfig.ready()` registers lifecycle signals and imports decorated Device
views before native URL assembly. `DeviceParametersView` uses native Device view
constraints, then `presentation.build_sections()` prepares current native values.
Repeated rows are reused only within that request. Related objects are resolved
through native restricted querysets before rendering. `parameter_tags.py` uses
native field formatting with the plugin's prepared reference/URL handling.

`DeviceParametersEditView` inherits native `ObjectEditView`; it retains Device
change constraints, native form restrictions, validation, change logging and
post-save permission checks. An outer transaction locks the Device before POST
reads. `DeviceParametersForm` unions current matching fields in first-occurrence
order, honors native UI editability and preserves unrelated stored values. A
signed scope rejects changed field membership/definitions. Inaccessible existing
reference sets are omitted intact. No Device add/clone flow is exposed here.

Profile administration uses native generic CRUD plus an aggregate form. It locks
native field IDs before the profile to coordinate with lifecycle cleanup. Saved
rules referencing inaccessible objects reject edits instead of becoming empty and
broadening scope. JavaScript synchronizes Selected/All remembered state and order.

## Lifecycle and migration history

Native deletion/applicability signals clean up only plugin configuration. Filter
reference deletion disables affected profiles; losing the last selected field
also disables a Selected profile. Direct SQL/bulk relation writes bypass those
signals; current field resolution still checks applicability/status defensively.

Migrations retain the initial configuration schema, add profiles in `0002`, and
retire the three obsolete plugin configuration models in `0003`. Clean installation
is supported; there is no legacy-install data mapping. The retired runtime API,
injected panel, templates and tag module are inactive/removed. An internal profile
serializer remains for native event payloads; there is no public profile REST API.

## System plugin metadata

`metadata.py` defines the plain Summary, rich Description, project/license identity
and current docs URLs. `PluginConfig.description` is deliberately the short
Summary so a list entry does not contain Markdown documentation links.

NetBox 4.7's local catalog maps that one config string into both summary and
Description, and does not copy local URL/license values. The registered
`PluginMetadataMiddleware` adapts only the native plugin list and this plugin's
own native detail view. Its mixin copies the catalog dictionary and this one entry
before filling separate fields. Other entries, cached catalog records, native
superuser checks, core templates, certification and release history are retained.
No global function patch, URL registration outside the plugin namespace, or core
file/template replacement is performed.

Middleware registration uses NetBox's plugin middleware extension. The adapter's
subclassing of `core.views.PluginListView`/`PluginView` and `get_cached_plugins` is a
specific compatibility dependency on the exercised NetBox 4.7.4 implementation,
not a claim that those catalog internals are a stable public plugin API. Recheck
this seam when adding support for another NetBox version. Tests cover the native
list/detail rendering, separate fields, unrelated/catalog-object isolation and
denied users. The adapter does not make the plugin catalog-listed or certified.

## Packaging and verification

`pyproject.toml` declares author, MIT license and current docs/project URLs. The
Dockerfile installs the package, then publishes plugin static assets into the
pinned image's static root. Source bind mounts do not refresh collected assets.
The live smoke checks the actual editor's JavaScript reference and served bytes.
The release check verifies wheel assets/license/metadata and installed import
provenance, then exercises native migrations/tests on a fresh isolated database.

[Maintainer index](README.md) · [Testing](testing.md)
