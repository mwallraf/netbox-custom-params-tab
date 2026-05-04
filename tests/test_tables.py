import pytest
from netbox_custom_params_tab.models import CustomTabConfig
from netbox_custom_params_tab.tables import CustomTabConfigTable


@pytest.mark.django_db
class TestCustomTabConfigTable:
    def test_renders_with_queryset(self, device_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type, tab_label='Params')
        table = CustomTabConfigTable(CustomTabConfig.objects.all())
        assert table.rows.data.count() == 1

    def test_empty_queryset_renders(self):
        table = CustomTabConfigTable(CustomTabConfig.objects.none())
        assert table.rows.data.count() == 0

    def test_required_columns_present(self):
        table = CustomTabConfigTable(CustomTabConfig.objects.none())
        col_names = [c.name for c in table.columns]
        for required in ('content_type', 'tab_label', 'enabled', 'actions'):
            assert required in col_names, f'Column {required!r} missing from table'
