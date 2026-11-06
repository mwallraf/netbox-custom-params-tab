---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# Architecture

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## System Overview
- Current system is a presentational NetBox plugin.
- Current data model supports one configuration per ContentType.
- New multi-profile requirements are not implemented.
## Component Responsibilities
- `models.py`: configuration plus weighted groups and field membership.
- `forms.py`: main form and inline group/field formsets.
- `views.py`: list/detail/create/edit/delete configuration views.
- `template_content.py`: per-model template-extension factory.
- `api/`: basic configuration REST scaffold.
## Pattern Overview
- Django models/forms/templates with NetBox integration.
- Plugin registration occurs in `__init__.py`.
## Layers
- Database configuration is separated from native field value storage.
- Views validate forms and save related configuration atomically.
## Data Flow
- Object page invokes `full_width_page()`.
- Extension resolves ContentType and enabled configuration.
- Group-name lookups and explicit memberships are combined by weight/name.
- Template reads raw values from the object's custom_field_data.
## Key Abstractions
- CustomTabConfig: one-to-one ContentType configuration.
- CustomTabConfigGroup: group_name string, not group foreign key.
- CustomTabConfigField: foreign key to native CustomField.
## Architectural Constraints
- No independent field-value storage.
- Profile filtering and the dedicated tab will replace current panel behavior.
## Error Handling
- Missing ContentType or enabled config returns an empty extension.
- Unexpected rendering failures are not caught by the extension.
## Cross-Cutting Concerns
- Native object permission and validation reuse must be researched before editing.
- Model-name and app-label migration require explicit treatment.
