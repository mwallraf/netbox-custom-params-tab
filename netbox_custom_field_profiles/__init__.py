from netbox.plugins import PluginConfig


class CustomFieldProfilesConfig(PluginConfig):
    name = 'netbox_custom_field_profiles'
    verbose_name = 'Custom Field Profiles'
    version = '0.1.0'
    description = 'Moves selected custom fields into a dedicated section on object detail pages'
    min_version = '4.7.0'
    base_url = 'custom-field-profiles'
    template_extensions = 'template_content.template_extensions'
    menu_items = 'navigation.menu_items'
    default_settings = {
        'extra_models': [],
    }

    def ready(self):
        super().ready()
        from django.conf import settings as django_settings
        plugin_cfg = django_settings.PLUGINS_CONFIG.get('netbox_custom_field_profiles', {})
        extra = plugin_cfg.get('extra_models', [])
        if extra:
            import netbox_custom_field_profiles.template_content as tc
            tc.template_extensions = tc.build_template_extensions(extra)


config = CustomFieldProfilesConfig
