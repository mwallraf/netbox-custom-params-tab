# Installation and updates

## Compatibility

Tested with **NetBox 4.7.4 / NetBox Docker 5.1.1**. The declared minimum is NetBox
4.7.0; other versions have not been verified. Devices are the only supported
object type. Install the plugin in the same Python environment as NetBox.

This is a new-install plugin. There is no data-upgrade mapping from the retired
`netbox_custom_params_tab` plugin. Existing Custom Field Profiles installations
retain their native values and profile configuration during normal updates.

## Standard NetBox installation

The examples assume a conventional `/opt/netbox` deployment with systemd services.
Adjust paths and service names for your installation.

1. Add this requirement to `/opt/netbox/local_requirements.txt`:

   ```text
   netbox-custom-field-profiles @ git+https://github.com/mwallraf/netbox-custom-params-tab.git
   ```

   This installs the repository's default branch. For a controlled deployment,
   append `@<commit-sha>` to the Git URL to select a reviewed commit. No version tag
   or PyPI publication is required by these instructions.

2. Add the plugin to the existing `PLUGINS` list in `configuration.py`:

   ```python
   PLUGINS = [
       # Keep your other plugins here.
       'netbox_custom_field_profiles',
   ]
   ```

   No plugin-specific `PLUGINS_CONFIG` settings are required. Do not copy the
   development sandbox's credentials, configuration or `DEVELOPER` setting into
   another deployment.

3. Run the standard NetBox upgrade/install sequence, then restart its services:

   ```sh
   sudo /opt/netbox/upgrade.sh
   sudo systemctl restart netbox netbox-rq
   ```

   The upgrade script installs local requirements, applies migrations and collects
   static files. If installing manually instead, install the package with NetBox's
   virtual-environment interpreter, run `manage.py migrate` and
   `manage.py collectstatic --no-input`, then restart the web and worker services.

See the [NetBox plugin installation guide](https://netboxlabs.com/docs/netbox/plugins/installation/)
for permissions and deployment-specific alternatives.

## Docker deployment

Install the package into a custom image so it survives container replacement.
The repository's [Dockerfile](../docker/Dockerfile) demonstrates the pinned base
image, installation into `/opt/netbox/venv/bin/python`, and copying plugin assets
into `/opt/netbox/netbox/static` after installation. For a different image layout,
use its supported static-file collection procedure instead of assuming that path.

Enable the plugin through your deployment's NetBox configuration, apply migrations
using its normal startup/upgrade process, and recreate its web and worker services
with the rebuilt image. A source bind mount alone does not update the files served
from a collected static directory. Rebuild/recollect after JavaScript changes.

To try the included disposable development stack, use the separate
[sandbox guide](development/sandbox.md). It is not a production deployment recipe.

## Wheel installation

From a checkout, `uv build` produces a wheel in `dist/`. Install that wheel into
NetBox's environment. In the exercised image:

```sh
uv pip install --python /opt/netbox/venv/bin/python /path/to/netbox_custom_field_profiles-0.1.0-py3-none-any.whl
```

Enable the plugin, apply migrations, collect its static files and restart as above.
Building requires the declared setuptools dependency; registry access is needed if
it is not cached.

## Verify and start using it

1. Open **System → Plugins → NetBox Custom Field Profiles** as a superuser. Check
   the author, project URL, MIT license, short Summary and documentation links in
   Description.
2. Assign the appropriate native profile administration and Device permissions.
3. Follow the [user guide](user-guide.md) to create and enable a profile.
4. If ordering controls remain “loading” or creation fails with a remembered-field
   error, check [JavaScript delivery](troubleshooting.md#profile-creation-fails-with-a-remembered-fields-error).

## Update an existing installation

Back up the deployment using your normal NetBox procedure. Install the selected
new revision or rebuild the image, retain the plugin in `PLUGINS`, apply migrations,
refresh static files and restart web/workers. Hard-refresh an already-open editor
before making further changes. Do not reset a database to update the plugin.

[Documentation index](README.md) · [Profile administration](administration.md)
