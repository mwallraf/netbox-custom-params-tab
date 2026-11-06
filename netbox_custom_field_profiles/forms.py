from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms import inlineformset_factory
from netbox.forms import NetBoxModelForm
from extras.models import CustomField
from .models import CustomTabConfig, CustomTabConfigGroup, CustomTabConfigField
from .template_content import BUILTIN_MODELS

GROUP_FORMSET_PREFIX = 'config_groups'
FIELD_FORMSET_PREFIX = 'config_fields'


def _supported_content_type_pks():
    query = Q()
    for model_path in BUILTIN_MODELS:
        app_label, model_name = model_path.split('.')
        query |= Q(app_label=app_label, model=model_name)
    return list(ContentType.objects.filter(query).values_list('pk', flat=True))


def _group_name_choices():
    names = list(
        CustomField.objects
        .exclude(group_name='')
        .exclude(group_name__isnull=True)
        .values_list('group_name', flat=True)
        .distinct()
        .order_by('group_name')
    )
    return [('', '---------')] + [(n, n) for n in names]


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


class CustomTabConfigGroupForm(forms.ModelForm):
    group_name = forms.ChoiceField(
        choices=[],
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = CustomTabConfigGroup
        fields = ['group_name', 'weight']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = _group_name_choices()
        # Keep saved value even if it no longer appears in NetBox
        if self.instance.pk and self.instance.group_name:
            values = [c[0] for c in choices]
            if self.instance.group_name not in values:
                choices.insert(1, (self.instance.group_name, self.instance.group_name))
        self.fields['group_name'].choices = choices


CustomTabConfigGroupFormSet = inlineformset_factory(
    CustomTabConfig,
    CustomTabConfigGroup,
    form=CustomTabConfigGroupForm,
    fields=['group_name', 'weight'],
    extra=0,
    can_delete=True,
    fk_name='tab_config',
)

class CustomTabConfigFieldForm(forms.ModelForm):
    field = forms.ModelChoiceField(
        queryset=CustomField.objects.order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = CustomTabConfigField
        fields = ['field', 'weight']


CustomTabConfigFieldFormSet = inlineformset_factory(
    CustomTabConfig,
    CustomTabConfigField,
    form=CustomTabConfigFieldForm,
    fields=['field', 'weight'],
    extra=0,
    can_delete=True,
    fk_name='tab_config',
)
