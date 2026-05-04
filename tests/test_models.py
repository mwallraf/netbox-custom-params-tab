import pytest
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField, CustomFieldGroup, CustomFieldTypeChoices
from netbox_custom_params_tab.models import (
    CustomTabConfig,
    CustomTabConfigGroup,
    CustomTabConfigField,
)


@pytest.mark.django_db
class TestCustomTabConfig:
    def test_create(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type,
            tab_label='Parameters',
            enabled=True,
        )
        assert config.pk is not None
        assert str(config) == f'{device_content_type} — Parameters'

    def test_enabled_default_is_true(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        assert config.enabled is True

    def test_tab_label_default_is_parameters(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        assert config.tab_label == 'Parameters'

    def test_content_type_is_unique(self, device_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type)
        with pytest.raises(Exception):
            CustomTabConfig.objects.create(content_type=device_content_type)

    def test_get_absolute_url_resolves(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = config.get_absolute_url()
        assert str(config.pk) in url


@pytest.mark.django_db
class TestCustomTabConfigGroup:
    def test_create(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Network')
        entry = CustomTabConfigGroup.objects.create(tab_config=config, group=group, weight=100)
        assert entry.pk is not None

    def test_weight_default_is_100(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Network')
        entry = CustomTabConfigGroup.objects.create(tab_config=config, group=group)
        assert entry.weight == 100

    def test_ordering_ascending_by_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group_a = CustomFieldGroup.objects.create(name='Alpha')
        group_b = CustomFieldGroup.objects.create(name='Beta')
        CustomTabConfigGroup.objects.create(tab_config=config, group=group_b, weight=200)
        CustomTabConfigGroup.objects.create(tab_config=config, group=group_a, weight=100)
        names = list(
            config.config_groups.order_by('weight', 'group__name')
            .values_list('group__name', flat=True)
        )
        assert names == ['Alpha', 'Beta']

    def test_cascade_delete_when_tab_config_deleted(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Cascade Test')
        CustomTabConfigGroup.objects.create(tab_config=config, group=group)
        config.delete()
        assert CustomTabConfigGroup.objects.count() == 0

    def test_cascade_delete_when_group_deleted(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Doomed Group')
        CustomTabConfigGroup.objects.create(tab_config=config, group=group)
        group.delete()
        assert CustomTabConfigGroup.objects.count() == 0


@pytest.mark.django_db
class TestCustomTabConfigField:
    def test_create(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        cf = CustomField.objects.create(name='rack_role', type=CustomFieldTypeChoices.TYPE_TEXT)
        entry = CustomTabConfigField.objects.create(tab_config=config, field=cf, weight=100)
        assert entry.pk is not None

    def test_ordering_ascending_by_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        field_a = CustomField.objects.create(name='alpha', type=CustomFieldTypeChoices.TYPE_TEXT)
        field_b = CustomField.objects.create(name='beta', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigField.objects.create(tab_config=config, field=field_b, weight=200)
        CustomTabConfigField.objects.create(tab_config=config, field=field_a, weight=100)
        names = list(
            config.config_fields.order_by('weight', 'field__name')
            .values_list('field__name', flat=True)
        )
        assert names == ['alpha', 'beta']

    def test_cascade_delete_when_custom_field_deleted(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        cf = CustomField.objects.create(name='doomed_field', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigField.objects.create(tab_config=config, field=cf)
        cf.delete()
        assert CustomTabConfigField.objects.count() == 0
