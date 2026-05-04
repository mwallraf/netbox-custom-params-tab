from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory
from netbox.forms import NetBoxModelForm
from .models import CustomTabConfig, CustomTabConfigGroup, CustomTabConfigField
from .template_content import BUILTIN_MODELS


def _supported_content_type_pks():
    pks = []
    for model_path in BUILTIN_MODELS:
        app_label, model_name = model_path.split('.')
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
            pks.append(ct.pk)
        except ContentType.DoesNotExist:
            pass
    return pks


class CustomTabConfigForm(NetBoxModelForm):
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.none(),
        label='Object Type',
        help_text='NetBox object type for this tab configuration.',
    )

    class Meta:
        model = CustomTabConfig
        fields = ('content_type', 'tab_label', 'enabled')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        supported_pks = _supported_content_type_pks()
        if self.instance.pk:
            allowed_pks = supported_pks
        else:
            existing_pks = list(
                CustomTabConfig.objects.values_list('content_type_id', flat=True)
            )
            allowed_pks = [pk for pk in supported_pks if pk not in existing_pks]
        self.fields['content_type'].queryset = ContentType.objects.filter(pk__in=allowed_pks)


CustomTabConfigGroupFormSet = inlineformset_factory(
    CustomTabConfig,
    CustomTabConfigGroup,
    fields=['group', 'weight'],
    extra=1,
    can_delete=True,
    fk_name='tab_config',
)

CustomTabConfigFieldFormSet = inlineformset_factory(
    CustomTabConfig,
    CustomTabConfigField,
    fields=['field', 'weight'],
    extra=1,
    can_delete=True,
    fk_name='tab_config',
)
