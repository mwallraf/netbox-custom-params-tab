from netbox.plugins import PluginConfig


class CustomParamsTabConfig(PluginConfig):
    name = 'netbox_custom_params_tab'
    verbose_name = 'Custom Params Tab'
    version = '0.1.0'
    description = 'Moves selected custom fields into a dedicated section on object detail pages'
    min_version = '4.0.0'
    base_url = 'custom-params-tab'
    template_extensions = 'netbox_custom_params_tab.template_content.template_extensions'
    menu_items = 'netbox_custom_params_tab.navigation.menu_items'
    default_settings = {
        'extra_models': [],
    }

    def ready(self):
        super().ready()
        from django.conf import settings as django_settings
        import netbox_custom_params_tab.template_content as tc
        plugin_cfg = django_settings.PLUGINS_CONFIG.get('netbox_custom_params_tab', {})
        extra = plugin_cfg.get('extra_models', [])
        if extra:
            tc.template_extensions = tc.build_template_extensions(extra)


config = CustomParamsTabConfig
