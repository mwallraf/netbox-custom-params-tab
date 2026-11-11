"""Fill this installed plugin's metadata without replacing NetBox templates.

NetBox 4.7's local catalog maps one config string to both summary and description
and drops local project/license metadata. Keep this compatibility adapter limited
to the native System plugin views; their superuser checks still run normally.
"""
from copy import copy

from django.utils.deprecation import MiddlewareMixin
from core.views import PluginListView, PluginView

from .metadata import DESCRIPTION, LICENSE, PLUGIN_NAME, PROJECT_URL, SUMMARY


class LocalMetadataMixin:
    def get_cached_plugins(self, request):
        plugins = super().get_cached_plugins(request)
        plugin = plugins.get(PLUGIN_NAME)
        if plugin is not None and plugin.is_local:
            # Never mutate a shared cached catalog object or another entry.
            plugins = dict(plugins)
            plugin = copy(plugin)
            plugin.tag_line = SUMMARY
            plugin.description_short = DESCRIPTION
            plugin.homepage_url = PROJECT_URL
            plugin.license_type = LICENSE
            plugins[PLUGIN_NAME] = plugin
        return plugins


class LocalPluginListView(LocalMetadataMixin, PluginListView):
    pass


class LocalPluginView(LocalMetadataMixin, PluginView):
    pass


class PluginMetadataMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        view_class = getattr(view_func, 'view_class', None)
        if view_class is PluginListView:
            return LocalPluginListView.as_view(**view_func.view_initkwargs)(
                request, *view_args, **view_kwargs)
        if view_class is PluginView and view_kwargs.get('name') == PLUGIN_NAME:
            return LocalPluginView.as_view(**view_func.view_initkwargs)(
                request, *view_args, **view_kwargs)
        return None
