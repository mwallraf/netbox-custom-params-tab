# Phase 1: Reproducible baseline - Pattern Map

**Mapped:** 2026-11-06
**Scope:** baseline only; no profile features.
**Files classified:** 12 file groups; 7 have useful tracked-source analogs.

## Provenance and Tracked-Source Gate

HEAD currently tracks documentation and planning, not the plugin source. Existing
implementation analogs below are verified tracked objects on
`feature/implement-plugin` (`42ad9c2`), using `git ls-tree -r --name-only` and
`git show feature/implement-plugin:<path>`. They are **not** instructions to edit
an ignored runtime/source mirror. Output paths are the intended root paths after
the source-consolidation task. The orphaned working snapshot has newer rename,
API, form, and Docker edits; inventory/overlay those before changing the canonical
source. Never restore the branch tree wholesale over current root docs/planning.

## File Classification

| Planned root file/group | Role | Data flow | Closest tracked analog | Quality |
|---|---|---|---|---|
| `Makefile` | utility/config | batch | `feature/implement-plugin:Makefile` | exact role |
| `docker-compose.yml` | config | service lifecycle | `feature/implement-plugin:docker-compose.yml` | exact role |
| `docker/Dockerfile` | config | build/install | `feature/implement-plugin:docker/Dockerfile` | exact role |
| `docker/configuration.py` or plugin-only replacement | config | startup transform | `feature/implement-plugin:docker/configuration.py` | partial; replace hard-coded infrastructure |
| `netbox_custom_field_profiles/__init__.py` | provider | startup registration | `feature/implement-plugin:netbox_custom_params_tab/__init__.py` | renamed analog; working snapshot newer |
| `pyproject.toml` | config | package install | `feature/implement-plugin:pyproject.toml` | renamed analog |
| `netbox_custom_field_profiles/migrations/0001_initial.py` | migration | schema batch | existing model/schema, regenerate in pinned runtime | no trustworthy migration template |
| `.env.example`, env-generation helper | config/utility | file I/O | HEAD `.gitignore` exclusion only | no helper analog |
| source-inventory/consolidation helper or recorded procedure | utility | file I/O | HEAD `README.md`, `AGENTS.md` constraints | no executable analog |
| smoke/auth helper and infrastructure tests | utility/test | request-response | `feature/implement-plugin:tests/conftest.py` | partial; no real HTTP smoke |
| sandbox seed helper | utility | CRUD batch | existing pytest fixture style | partial; no seed analog |
| `README.md`, baseline/deferred-failure report | documentation | transform | HEAD `README.md` | exact documentation role |

Names of new helper/test files are planner-owned; classify them as new tracked
source. Existing `testing/settings.py` is a legacy SQLite approximation, not a
reusable real-NetBox test configuration. Inspect it for legacy-suite reporting,
but do not build baseline acceptance on it.

## Pattern Assignments

### Make lifecycle and container execution

**Analog:** `feature/implement-plugin:Makefile`, lines 9–16 and 27–31:

```make
build:  ## Build (or rebuild) the dev Docker image
	docker compose build
up:  ## Start the full stack in the background
	docker compose up -d
down:  ## Stop and remove containers (data volumes are preserved)
	docker compose down
nbshell:  ## Open NetBox's Django shell_plus inside the netbox container
	docker compose exec netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py shell_plus
```

Retain thin, documented Make targets and explicit container interpreter paths.
Replace bare Compose invocations with one fixed project/file/env wrapper shared
by every target. Use noninteractive execution for automation. Keep `down`
non-destructive; replace broad old `clean --rmi local` with explicitly project-
scoped reset. Never print resolved Compose configuration or credentials.

### Plugin registration and package identity

**Analog:** `feature/implement-plugin:netbox_custom_params_tab/__init__.py`,
lines 1–5 and 27; `feature/implement-plugin:pyproject.toml`, lines 1–3:

```python
from netbox.plugins import PluginConfig

class CustomParamsTabConfig(PluginConfig):
    name = 'netbox_custom_params_tab'
# ...
config = CustomParamsTabConfig
```

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```

Retain PluginConfig entry-point shape and setuptools packaging, using the
**already renamed working snapshot** as canonical source input. Set the minimum
to 4.7.0 and verify imports/resources in the pinned image. Historical fully
qualified resource paths are obsolete; research confirms package-relative
`template_content.template_extensions` and `navigation.menu_items` are correct.
The old pip/user/image details in the Dockerfile are not copyable 4.7 patterns;
use the pinned upstream image's existing uv and native launcher instead.

### Native fixture and authentication boundaries

**Analog:** `feature/implement-plugin:tests/conftest.py`, lines 6–19:

```python
@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        password='password',
        email='admin@example.com',
    )

@pytest.fixture
def client_logged_in(client, admin_user):
    client.force_login(admin_user)
    return client
```

Reuse native models/managers for dummy records, not raw SQL or a parallel value
store. Do **not** copy literal fixture credentials into sandbox configuration.
`force_login` is useful for unit views but cannot prove real admin login: smoke
must exercise actual CSRF-aware authentication and authenticated follow-up.

## Shared Patterns and Gaps

- Credentials: no existing generator; follow research's stdlib `secrets`, stable
  gitignored `.env`, restrictive file permissions, no shell-sourcing or logging.
- Configuration: use upstream DB/cache/superuser/token bootstrap; add only native
  plugin configuration rather than carrying the old full settings file forward.
- Migrations: no deployable-data compatibility obligation. Generate/verify schema
  in the actual sandbox with native developer mode, not the existing bypass helper.
- Isolation: existing dependency health checks and named-volume structure are
  reusable; old public `8000:8080`, globally shared image naming, and fixed secrets
  are not. Bind a configurable localhost port and isolate project resources.
- Verification: distinguish blocking boot/migrate/register/admin/API checks from
  separately reported legacy feature failures; no existing test proves this chain.
- Seed/reset: no close analog. Use idempotent native ORM operations and restrict
  reset to this project's named resources; preserve `.env` across normal lifecycle.
- Source consolidation: preserve current source edits, track the reconciled root
  tree, verify its manifest, then retire stale metadata/snapshot. No Git mutation
  or runtime action was performed by this pattern map.

**Authoritative inputs:** `01-CONTEXT.md`, `01-RESEARCH.md`, and
`docs/REQUIREMENTS.md`. Analogs explain reuse; they do not override user decisions.
