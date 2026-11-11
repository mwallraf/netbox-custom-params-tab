from netbox.plugins import PluginConfig
from .metadata import SUMMARY


class CustomFieldProfilesConfig(PluginConfig):
    name = 'netbox_custom_field_profiles'
    verbose_name = 'NetBox Custom Field Profiles'
    version = '0.1.0'
    author = 'Maarten Wallraf'
    description = SUMMARY
    min_version = '4.7.0'
    base_url = 'custom-field-profiles'
    menu_items = 'navigation.menu_items'
    middleware = ['netbox_custom_field_profiles.middleware.PluginMetadataMiddleware']

    def ready(self):
        super().ready()
        from . import signals
        signals.register()
        # Core Device URLs are assembled before plugin URL modules are loaded.
        from . import views  # noqa: F401


config = CustomFieldProfilesConfig
