---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# Codebase Structure

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## Directory Layout
- Repository root: README.md, AGENTS.md, CLAUDE.md, docs/.
- `.planning/`: GSD onboarding and subsequent workflow state.
- `.worktrees/feature/implement-plugin/`: actual implementation.
## Directory Purposes
- `netbox_custom_field_profiles/`: renamed plugin package.
- `netbox_custom_field_profiles/templates/`: plugin HTML.
- `netbox_custom_field_profiles/migrations/`: initial handwritten schema.
- `netbox_custom_field_profiles/api/`: REST scaffold.
- `netbox_custom_field_profiles/management/`: migration-generation helper.
- `tests/`: five test modules and shared fixtures.
- `testing/`: standalone Django test settings.
- `docker/`: development image and NetBox configuration.
## Key File Locations
- Repository `docs/REQUIREMENTS.md`: authoritative product decisions.
- Repository `docs/superpowers/`: historical design and implementation plan.
- `pyproject.toml`: build metadata and plugin entry point.
- `docker-compose.yml`: local integration stack.
## Naming Conventions
- Distribution: netbox-custom-field-profiles.
- Python import: netbox_custom_field_profiles.
- Existing internal model names still use CustomTabConfig.
## Where to Add New Code
- First establish a canonical source location during baseline phase.
- Do not create a second independent plugin implementation at repository root.
- Keep authoritative planning at repository root until source consolidation.
## Special Directories
- `.worktrees` is ignored by the root Git checkout.
- Nested worktree .git points to the old repository location.
- Do not prune the worktree; uncommitted source must be preserved.
- Old egg-info and bytecode are generated artifacts, not renamed source.
