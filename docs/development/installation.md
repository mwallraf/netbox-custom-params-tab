# Installation and supported runtime

The exercised runtime is NetBox 4.7.4 with Docker packaging 5.1.1. The plugin
declares NetBox 4.7.0 as its minimum, but other versions have not been verified.
This milestone supports a new installation; it does not provide an upgrade/data
mapping from the retired `netbox_custom_params_tab` installation.

## Repository sandbox

From this repository, run `make setup` and open <http://127.0.0.1:18047>. The
Dockerfile installs `netbox-custom-field-profiles` into NetBox's virtual environment.
`docker/plugins.py` registers `netbox_custom_field_profiles` in `PLUGINS`.
Generated administrator credentials are in the ignored `.env`. `make up` starts
the existing sandbox; `make down` preserves its database and credentials.

Source code is bind-mounted for development. Restart the sandbox NetBox and worker
processes after changing registered views. Rebuild the image when changing package
metadata/dependencies; that metadata is baked into the image rather than mounted.
Never restart services during an isolated test run.

## Package installation in a matching NetBox runtime

Build the repository with a PEP 517 frontend such as `uv build`. Install the
resulting `netbox_custom_field_profiles-0.1.0-py3-none-any.whl` into NetBox's own
virtual environment. In the exercised Docker image, the interpreter is
`/opt/netbox/venv/bin/python` and the installer is `uv pip install --python
/opt/netbox/venv/bin/python /path/to/the.whl`. Use a custom image so installation
survives container replacement; the repository Dockerfile demonstrates this.

Add `'netbox_custom_field_profiles'` to the existing NetBox `PLUGINS` list. No
plugin-specific configuration is required for Device profiles. Using NetBox's
virtual-environment interpreter, run `manage.py migrate` and `manage.py collectstatic
--no-input`, then restart NetBox and its workers. Preserve the deployment's existing
configuration and other plugins. Assign native profile administration permissions
and Device view/change permissions to the intended users. Create and enable
profiles through Plugins → Custom Field Profiles.

## Checks and acceptance

Run `make test-profiles`, `make test` and `make release-check` in the dedicated
repository sandbox. The release check builds the current source and metadata,
checks packaged assets, installs into a temporary target, verifies import
provenance and exercises migrations/native tests on a fresh temporary database.
It does not replace the sandbox's editable installation or install into another
deployment. Registry access is needed for uncached build dependencies.

Browser acceptance is deferred to the user at project end. Follow
[final-uat.md](final-uat.md). Automated results do not establish browser layout,
keyboard or widget interaction. Optional historical pytest and unsupported NetBox
versions are not included in the passing baseline.
