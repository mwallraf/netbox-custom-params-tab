import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import CustomTabConfig


class CustomTabConfigTable(NetBoxTable):
    content_type = tables.Column(verbose_name='Object Type', linkify=True)
    tab_label = tables.Column(verbose_name='Tab Label')
    enabled = columns.BooleanColumn(verbose_name='Enabled')
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = CustomTabConfig
        fields = ('pk', 'content_type', 'tab_label', 'enabled', 'actions')
        default_columns = ('content_type', 'tab_label', 'enabled', 'actions')
