---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# Testing

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## Test Framework
- pytest plus pytest-django; configured in `pytest.ini`.
- `testing/settings.py` selects in-memory SQLite.
- NetBox modules must be importable for test setup.
## Test File Organization
- `tests/test_models.py`: defaults, uniqueness, ordering, deletion.
- `tests/test_forms.py`: main form and inline membership formsets.
- `tests/test_views.py`: configuration CRUD and authentication.
- `tests/test_tables.py`: table structure and rows.
- `tests/test_template_content.py`: registration and extension behavior.
## Test Structure
- 45 test methods were found in the inspected implementation.
- Database tests use pytest.mark.django_db.
- Class grouping follows model, form, or view responsibilities.
## Mocking
- Template extension tests use MagicMock objects and patched render methods.
- These tests do not prove actual detail-page rendering or tab registration.
## Fixtures and Factories
- `tests/conftest.py` creates admin user, logged-in client, and content types.
- Many native custom fields and configurations are created directly in tests.
## Coverage
- No measured coverage or passing runtime baseline is established.
- Earlier pytest attempts failed during environment initialization.
- Python syntax checks passed after the rename; that is not runtime testing.
## Test Types
- Unit/ORM and Django view tests exist.
- Compose stack supports manual integration checks, not yet verified here.
## Common Patterns
- Redirect assertions check expected destinations.
- Render-call capture verifies weighted item ordering.
- Future tests must cover matching, dynamic fields, deduplicated editing,
  native validation, permission restrictions, and preservation of other values.
