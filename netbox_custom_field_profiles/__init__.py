from netbox.plugins import PluginConfig


class CustomFieldProfilesConfig(PluginConfig):
    name = 'netbox_custom_field_profiles'
    verbose_name = 'NetBox Custom Field Profiles'
    version = '0.1.0'
    author = 'Maarten Wallraf'
    description = (
        'Organizes existing NetBox custom fields into reusable profiles on each matching '
        'Device’s Parameters tab. It creates no field definitions or separate value storage; '
        'viewing and editing use native NetBox fields, permissions and validation.\n\n'
        'To reduce clutter, set a custom field’s UI visibility to Hidden and include it in '
        'a profile. The field remains available in Parameters; native editability still applies.\n\n'
        '[User guide](https://github.com/mwallraf/netbox-custom-params-tab/blob/HEAD/docs/user-guide.md) · '
        '[Installation](https://github.com/mwallraf/netbox-custom-params-tab/blob/HEAD/docs/development/installation.md) · '
        '[Project](https://github.com/mwallraf/netbox-custom-params-tab) · '
        '[MIT license](https://github.com/mwallraf/netbox-custom-params-tab/blob/HEAD/LICENSE)'
    )
    min_version = '4.7.0'
    base_url = 'custom-field-profiles'
    menu_items = 'navigation.menu_items'

    def ready(self):
        super().ready()
        from . import signals
        signals.register()
        # Core Device URLs are assembled before plugin URL modules are loaded.
        from . import views  # noqa: F401


config = CustomFieldProfilesConfig
