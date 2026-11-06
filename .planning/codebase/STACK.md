---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# Technology Stack

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## Languages
- Python >=3.10 declared in `pyproject.toml`.
- Django templates and inline JavaScript in `templates/`.
- YAML for Compose; Make for development commands.
## Runtime
- Runs inside NetBox, not as an independent Django service.
- `netbox_custom_field_profiles/__init__.py` declares NetBox minimum 4.0.0.
- `docker/Dockerfile` references `netboxcommunity/netbox:v4.6-5.0.1`.
- The image tag is source evidence, not verified runtime compatibility.
## Frameworks
- Django ORM, forms, inline formsets, and transactions.
- NetBox PluginConfig, NetBoxModel, generic views, tables, REST infrastructure.
- pytest and pytest-django are optional test dependencies.
## Key Dependencies
- NetBox provides Django and its supporting libraries.
- `pyproject.toml` has no runtime dependency pins.
- Setuptools build backend and netbox.plugins entry point.
## Configuration
- `docker/configuration.py` enables the renamed plugin.
- `testing/settings.py` supplies simplified test settings.
- `pytest.ini` points to testing.settings.
## Platform Requirements
- Development stack has NetBox, worker, PostgreSQL, and two Redis services.
- Test settings currently use in-memory SQLite, unlike the development stack.
- Reproducible supported-version baseline remains to be established.
