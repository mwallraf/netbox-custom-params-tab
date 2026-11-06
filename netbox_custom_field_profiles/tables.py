import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import CustomFieldProfile
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
