import pytest
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField, CustomFieldGroup, CustomFieldTypeChoices
from netbox_custom_params_tab.models import CustomTabConfig
from netbox_custom_params_tab.forms import (
    CustomTabConfigForm,
    CustomTabConfigGroupFormSet,
    CustomTabConfigFieldFormSet,
    GROUP_FORMSET_PREFIX,
    FIELD_FORMSET_PREFIX,
)


@pytest.mark.django_db
class TestCustomTabConfigForm:
    def test_valid_form(self, device_content_type):
        form = CustomTabConfigForm(data={
            'content_type': device_content_type.pk,
            'tab_label': 'Parameters',
            'enabled': True,
        })
        assert form.is_valid(), form.errors

    def test_missing_content_type_is_invalid(self, device_content_type):
        form = CustomTabConfigForm(data={
            'tab_label': 'Parameters',
            'enabled': True,
        })
        assert not form.is_valid()
        assert 'content_type' in form.errors

    def test_tab_label_field_exists(self):
        form = CustomTabConfigForm()
        assert 'tab_label' in form.fields

    def test_content_type_choices_include_device(self, device_content_type):
        form = CustomTabConfigForm()
        pks = list(form.fields['content_type'].queryset.values_list('pk', flat=True))
        assert device_content_type.pk in pks

    def test_already_configured_type_excluded_on_create(self, device_content_type, site_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type)
        form = CustomTabConfigForm()
        pks = list(form.fields['content_type'].queryset.values_list('pk', flat=True))
        assert device_content_type.pk not in pks
        assert site_content_type.pk in pks

    def test_current_type_kept_on_edit(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        form = CustomTabConfigForm(instance=config)
        pks = list(form.fields['content_type'].queryset.values_list('pk', flat=True))
        assert device_content_type.pk in pks


@pytest.mark.django_db
class TestCustomTabConfigGroupFormSet:
    def test_empty_formset_is_valid(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        formset = CustomTabConfigGroupFormSet(
            instance=config,
            data={
                f'{GROUP_FORMSET_PREFIX}-TOTAL_FORMS': '0',
                f'{GROUP_FORMSET_PREFIX}-INITIAL_FORMS': '0',
                f'{GROUP_FORMSET_PREFIX}-MIN_NUM_FORMS': '0',
                f'{GROUP_FORMSET_PREFIX}-MAX_NUM_FORMS': '1000',
            },
            prefix=GROUP_FORMSET_PREFIX,
        )
        assert formset.is_valid(), formset.errors

    def test_add_group_entry(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Network')
        formset = CustomTabConfigGroupFormSet(
            instance=config,
            data={
                f'{GROUP_FORMSET_PREFIX}-TOTAL_FORMS': '1',
                f'{GROUP_FORMSET_PREFIX}-INITIAL_FORMS': '0',
                f'{GROUP_FORMSET_PREFIX}-MIN_NUM_FORMS': '0',
                f'{GROUP_FORMSET_PREFIX}-MAX_NUM_FORMS': '1000',
                f'{GROUP_FORMSET_PREFIX}-0-group': str(group.pk),
                f'{GROUP_FORMSET_PREFIX}-0-weight': '100',
            },
            prefix=GROUP_FORMSET_PREFIX,
        )
        assert formset.is_valid(), formset.errors
        formset.save()
        assert config.config_groups.count() == 1


@pytest.mark.django_db
class TestCustomTabConfigFieldFormSet:
    def test_add_field_entry(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        cf = CustomField.objects.create(name='rack_role', type=CustomFieldTypeChoices.TYPE_TEXT)
        formset = CustomTabConfigFieldFormSet(
            instance=config,
            data={
                f'{FIELD_FORMSET_PREFIX}-TOTAL_FORMS': '1',
                f'{FIELD_FORMSET_PREFIX}-INITIAL_FORMS': '0',
                f'{FIELD_FORMSET_PREFIX}-MIN_NUM_FORMS': '0',
                f'{FIELD_FORMSET_PREFIX}-MAX_NUM_FORMS': '1000',
                f'{FIELD_FORMSET_PREFIX}-0-field': str(cf.pk),
                f'{FIELD_FORMSET_PREFIX}-0-weight': '150',
            },
            prefix=FIELD_FORMSET_PREFIX,
        )
        assert formset.is_valid(), formset.errors
        formset.save()
        assert config.config_fields.count() == 1
