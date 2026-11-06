# Development sandbox

Use the normal repository checkout on `milestone/custom-field-profiles`.
Source recovery retained the renamed snapshot and feature history in `4dba67e`;
the original directory remains ignored at `.recovery/implement-plugin`.

## Requirements and compatibility

Docker Engine with Compose, Python 3 standard library, and Make are required.
The tested official image is `netboxcommunity/netbox:v4.7.4-5.1.1` (ARM64 here;
AMD64 manifest also exists). Plugin minimum is 4.7.0; later releases are not
claimed tested. PostgreSQL 18 and Valkey 9.1 follow that image's upstream stack.

## Start and authenticate

Run `make setup` to generate configuration once, build/install the local package,
start services, apply checked-in native migrations, verify registration/schema,
and seed dummy data. Open http://127.0.0.1:18047 and use SUPERUSER_NAME and
SUPERUSER_PASSWORD from your local `.env`, viewed in a local editor. Never copy
that file into tracked documentation. Generated v2 API credentials and pepper
remain local too. Repeated setup preserves credentials and existing database.

To select another localhost port on first setup, use `NETBOX_PORT=18048 make setup`.
For an existing environment, edit only NETBOX_PORT in `.env` and rerun setup.
The file is mode 0600 and ignored. Invalid/incomplete files are rejected without
rotating existing credentials. `.env.example` lists empty placeholders; it is
not a replacement for your generated `.env`.

Infrastructure/authentication settings come from `.env`; native PLUGINS and
PLUGINS_CONFIG in `docker/plugins.py` control plugin behavior. Upstream DB/cache
configuration, launcher and worker remain in use. The one-time initial schema
recovery already ran before bootstrap; future setup uses the generated migration.
Do not run prepare-schema on an initialized database.

## Commands

| Target | Purpose |
| --- | --- |
| `make env` | Generate or validate persistent local configuration |
| `make setup` | Build, start, native checks and idempotent seed |
| `make build` | Rebuild local editable plugin image |
| `make up` | Start existing sandbox, preserve data |
| `make down` | Stop/remove project containers, preserve volumes and .env |
| `make logs` | Tail project logs |
| `make shell` | Interactive project container shell |
| `make migrate` | Native migrations in the project container |
| `make makemigrations` | Native plugin migration generation, developer mode |
| `make check` | Fast helper/configuration checks |
| `make smoke` | Native version/schema/registry plus real session and API auth |
| `make seed` | Add/update owned CMTS/CPE demonstration data |
| `make seed-check` | Prove seed identities/values stable across reruns |
| `make test` | Blocking helper, configuration, live smoke and seed checks |
| `make test-legacy` | Run optional legacy pytest suite and preserve its true exit |
| `make lifecycle-check` | Repeated setup, down/up persistence, explicit reset, smoke |
| `make reset` | Deliberately recreate only project-owned volumes; seed/smoke |

`lifecycle-check` and `reset` destroy this project's disposable sandbox data;
normal down/up does not. Reset validates rendered nonexternal volumes/network
and actual volume ownership labels, retains `.env`, and never runs global prune.
Credentials remain stable on reset. The project name is fixed to netbox-custom-field-profiles. Only the web port is
published, bound to 127.0.0.1; DB/cache ports remain internal.

## Data and legacy tests

The seed creates CFP Sandbox manufacturer/site/tag, two device types/roles/devices
(CMTS and CPE), and two native custom fields. Native values are not duplicated
into plugin storage. Seed does not create profiles or implement matching.

The baseline suite uses stdlib, requiring no pytest installation. The optional
legacy suite currently reports runner-unavailable and is unexecuted. To inspect
those old tests, explicitly install the already declared extras inside this
sandbox image environment, then rerun make test-legacy:

```sh
python3 scripts/sandbox.py compose exec -T -u root netbox uv pip install --python /opt/netbox/venv/bin/python --editable '/opt/netbox-custom-field-profiles[test]'
make test-legacy
```

These extras are the upstream [pytest](https://pypi.org/project/pytest/) and
[pytest-django](https://pypi.org/project/pytest-django/) distributions. This optional
command is not run by setup. Record resolved versions if used. Old SQLite test
settings may need later adaptation; no successful feature suite is claimed.
The sanitized report is local `.sandbox/legacy-tests.json` and the target returns
its actual nonzero outcome. Feature acceptance belongs to later roadmap phases.

Lifecycle isolation compares original running unrelated container IDs with the final inventory; new unrelated containers are allowed. Missing/replaced original IDs fail, with local diagnostic IDs under `.sandbox/`. No unrelated resource is mutated. All Docker subprocesses use the same environment builder, ignoring ambient DOCKER_/COMPOSE_ overrides.
