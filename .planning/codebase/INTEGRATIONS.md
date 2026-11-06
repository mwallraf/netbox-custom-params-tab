---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# External Integrations

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## APIs & External Services
- No external business service integration is implemented.
- Native NetBox custom fields are the value source.
- Scripts can continue writing native values without plugin-specific storage.
## Data Storage
- Plugin configuration is stored through the Django ORM.
- `docker-compose.yml` provisions PostgreSQL with persistent storage.
- Redis supports the NetBox worker and caching.
- Native object `custom_field_data` is read by `tab_panel.html`.
## Authentication & Identity
- Uses NetBox/Django authentication and permission facilities.
- `views.py` combines login and model-permission mixins for configuration editing.
- Object-level permission parity for future device editing is not yet verified.
## Monitoring & Observability
- Compose logs are exposed through Makefile shortcuts.
- No separate telemetry or error-reporting service is configured.
## CI/CD & Deployment
- Local Docker image installs the plugin editable using uv.
- No CI workflow was found in the inspected source.
- API scaffold in `api/` exposes configuration metadata, not field memberships.
## Environment Configuration
- `docker/configuration.py` is a development-only setup.
- `extra_models` registers additional template extensions.
- Main repository and implementation worktree have separate working changes.
## Webhooks & Callbacks
- No plugin-specific webhook integration was found.
- No requirement for a separate script-ingestion API exists.
