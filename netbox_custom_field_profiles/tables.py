import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import CustomFieldProfile, CustomTabConfig
from .matching import get_profile_filter_summary


class CustomFieldProfileTable(NetBoxTable):
    title = tables.Column(linkify=True)
    enabled = columns.BooleanColumn()
    applicability = tables.Column(empty_values=(), orderable=False, verbose_name='Applicability')
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = CustomFieldProfile
        fields = ('pk', 'title', 'enabled', 'display_order', 'field_mode', 'applicability', 'actions')
        default_columns = ('title', 'enabled', 'display_order', 'field_mode', 'applicability', 'actions')

    def render_applicability(self, record):
        return get_profile_filter_summary(record)


class CustomTabConfigTable(NetBoxTable):
    content_type = tables.Column(verbose_name='Object Type', linkify=True)
    tab_label = tables.Column(verbose_name='Tab Label')
    enabled = columns.BooleanColumn(verbose_name='Enabled')
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = CustomTabConfig
        fields = ('pk', 'content_type', 'tab_label', 'enabled', 'actions')
        default_columns = ('content_type', 'tab_label', 'enabled', 'actions')
