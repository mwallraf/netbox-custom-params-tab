import pytest
from unittest.mock import patch, MagicMock
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField, CustomFieldTypeChoices
from netbox_custom_field_profiles.models import (
    CustomTabConfig,
    CustomTabConfigGroup,
    CustomTabConfigField,
)
from netbox_custom_field_profiles.template_content import build_template_extensions, BUILTIN_MODELS


class TestBuildTemplateExtensions:
    def test_returns_one_extension_per_builtin_model(self):
        extensions = build_template_extensions()
        assert len(extensions) == len(BUILTIN_MODELS)

    def test_each_extension_model_attr_matches(self):
        extensions = build_template_extensions()
        for ext, model_path in zip(extensions, BUILTIN_MODELS):
            assert ext.model == model_path

    def test_extra_models_appended(self):
        extensions = build_template_extensions(extra_models=['tenancy.tenant'])
        assert len(extensions) == len(BUILTIN_MODELS) + 1
        assert extensions[-1].model == 'tenancy.tenant'


@pytest.mark.django_db
class TestTabExtensionFullWidthPage:
    def _get_extension_instance(self, model_path, obj):
        extensions = build_template_extensions()
        ext_class = next(e for e in extensions if e.model == model_path)
        # PluginTemplateExtension.__init__ expects a request context that isn't
        # available in unit tests. We bypass it and inject only the 'object' key
        # that full_width_page() actually reads from self.context.
        instance = ext_class.__new__(ext_class)
        instance.context = {'object': obj}
        return instance

    def test_returns_empty_string_when_no_config_exists(self, device_content_type):
        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)
        with patch.object(type(ext), 'render', return_value='rendered'):
            result = ext.full_width_page()
        assert result == ''

    def test_returns_empty_string_when_config_disabled(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type, enabled=False)
        # Assert the row exists so we know '' comes from the enabled=True filter, not from an empty table
        assert CustomTabConfig.objects.filter(pk=config.pk).exists()
        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)
        with patch.object(type(ext), 'render', return_value='rendered') as mock_render:
            result = ext.full_width_page()
        assert result == ''
        mock_render.assert_not_called()

    def test_calls_render_when_config_is_enabled(self, device_content_type):
        CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True, tab_label='My Params'
        )
        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)
        with patch.object(type(ext), 'render', return_value='<div>ok</div>') as mock_render:
            result = ext.full_width_page()
        assert result == '<div>ok</div>'
        mock_render.assert_called_once()
        assert mock_render.call_args[0][0] == 'netbox_custom_field_profiles/tab_panel.html'

    def test_items_sorted_field_before_group_when_lower_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True
        )
        field = CustomField.objects.create(name='field_b', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigGroup.objects.create(tab_config=config, group_name='Group A', weight=200)
        CustomTabConfigField.objects.create(tab_config=config, field=field, weight=100)

        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)

        captured = {}

        def capture(template_name, context):
            captured.update(context)
            return 'rendered'

        with patch.object(type(ext), 'render', side_effect=capture):
            ext.full_width_page()

        items = captured.get('items', [])
        assert len(items) == 2
        assert items[0][0] == 'field'   # weight=100 comes first
        assert items[1][0] == 'group'   # weight=200 comes second

    def test_group_item_has_name_and_custom_fields(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True
        )
        cf = CustomField.objects.create(
            name='some_field', type=CustomFieldTypeChoices.TYPE_TEXT, group_name='MyGroup'
        )
        CustomTabConfigGroup.objects.create(tab_config=config, group_name='MyGroup', weight=100)

        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)

        captured = {}

        def capture(template_name, context):
            captured.update(context)
            return 'rendered'

        with patch.object(type(ext), 'render', side_effect=capture):
            ext.full_width_page()

        items = captured.get('items', [])
        assert len(items) == 1
        item_type, item_obj, weight = items[0]
        assert item_type == 'group'
        assert item_obj.name == 'MyGroup'
        assert len(item_obj.custom_fields) == 1
        assert item_obj.custom_fields[0].name == 'some_field'

    def test_alphabetical_tiebreak_on_equal_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True
        )
        field_z = CustomField.objects.create(name='zzz', type=CustomFieldTypeChoices.TYPE_TEXT)
        field_a = CustomField.objects.create(name='aaa', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigField.objects.create(tab_config=config, field=field_z, weight=100)
        CustomTabConfigField.objects.create(tab_config=config, field=field_a, weight=100)

        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)

        captured = {}

        def capture(template_name, context):
            captured.update(context)
            return 'rendered'

        with patch.object(type(ext), 'render', side_effect=capture):
            ext.full_width_page()

        items = captured.get('items', [])
        assert items[0][1].name == 'aaa'
        assert items[1][1].name == 'zzz'
