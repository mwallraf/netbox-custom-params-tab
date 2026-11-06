---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# Coding Conventions

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## Naming Patterns
- Python snake_case functions and modules; PascalCase Django classes.
- Template names follow lowercase model names and operation suffixes.
- Uppercase formset-prefix constants prevent repeated literals.
## Code Style
- Four-space indentation and predominantly single-quoted Python strings.
- Django Meta classes declare ordering and uniqueness constraints.
- No formatter or linter configuration was found.
## Import Organization
- Django/NetBox imports precede relative plugin imports.
- Existing files are not entirely uniform in import grouping.
## Error Handling
- Forms perform Django model validation before saving.
- `transaction.atomic()` wraps configuration and membership saves.
- `get_object_or_404` handles absent configuration records.
## Logging
- Edit template contains debug console.log calls in deletion JavaScript.
- Rendering does not implement the historical spec's logged-error fallback.
## Comments
- Migration file explicitly documents handwritten-schema shortcomings.
- Tests explain bypassing template-extension construction with __new__.
## Function Design
- `_build_forms` shares create/edit setup.
- `_make_extension` creates one class per model path.
- Helper functions collect supported ContentTypes and group names.
## Module Design
- Models, forms, tables, views, routes, and templates are separate modules.
- Preserve native custom field ownership while replacing display configuration.
- Avoid extrapolating current one-config uniqueness into the new profile design.
