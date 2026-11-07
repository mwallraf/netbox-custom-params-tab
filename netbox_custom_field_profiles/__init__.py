from netbox.plugins import PluginConfig


class CustomFieldProfilesConfig(PluginConfig):
    name = 'netbox_custom_field_profiles'
    verbose_name = 'Custom Field Profiles'
    version = '0.1.0'
    description = 'Reusable native custom field profiles for Devices'
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
