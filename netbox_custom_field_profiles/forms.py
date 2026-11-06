import json

from django import forms
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.forms import inlineformset_factory
from netbox.forms import NetBoxModelForm
from extras.models import CustomField
from .models import CustomFieldProfile, ProfileField, CustomTabConfig, CustomTabConfigGroup, CustomTabConfigField
from .template_content import BUILTIN_MODELS

GROUP_FORMSET_PREFIX = 'config_groups'
FIELD_FORMSET_PREFIX = 'config_fields'


class CustomFieldProfileForm(NetBoxModelForm):
    selected_fields = forms.ModelMultipleChoiceField(
        queryset=CustomField.objects.none(), required=False,
        help_text='Choose applicable fields, then arrange their display order below.',
    )
    field_order = forms.CharField(required=False, widget=forms.HiddenInput)
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(app_label='dcim', model='device'),
        label='Object Type',
    )

    class Meta:
        model = CustomFieldProfile
        fields = ('title', 'content_type', 'display_order', 'enabled', 'field_mode',
                  'selected_fields', 'field_order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_fields'].queryset = CustomField.objects.filter(
            object_types__app_label='dcim', object_types__model='device').distinct()
        self.fields['selected_fields'].widget.attrs['class'] = 'form-select'
        if not self.instance.pk:
            self.initial.setdefault('content_type', self.fields['content_type'].queryset.first())
            self.initial.setdefault('field_mode', CustomFieldProfile.FIELD_MODE_ALL)
        else:
            ordered = list(self.instance.profile_fields.values_list('field_id', flat=True))
            self.initial.setdefault('selected_fields', ordered)
            self.initial.setdefault('field_order', json.dumps(ordered))

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        self.ordered_field_ids = None
        if cleaned.get('field_mode') != CustomFieldProfile.FIELD_MODE_SELECTED:
            return cleaned
        selected = cleaned.get('selected_fields')
        if selected is None:
            return cleaned
        if not selected:
            self.add_error('selected_fields', 'Select at least one applicable field.')
        raw_selection = (self.data.getlist('selected_fields') if hasattr(self.data, 'getlist')
                         else self.data.get('selected_fields', []))
        if len(raw_selection) != len(set(raw_selection)):
            self.add_error('selected_fields', 'Select each field only once.')
        try:
            ordered = json.loads(cleaned.get('field_order') or '[]')
            if (not isinstance(ordered, list) or any(type(pk) is not int or pk <= 0 for pk in ordered)
                    or len(ordered) != len(set(ordered))
                    or set(ordered) != {field.pk for field in selected}):
                raise ValueError
        except (ValueError, TypeError):
            self.add_error('field_order', 'Field order must contain each selected field exactly once.')
        else:
            self.ordered_field_ids = ordered
        return cleaned

    @transaction.atomic
    def _save_m2m(self):
        super()._save_m2m()
        if self.instance.field_mode == CustomFieldProfile.FIELD_MODE_SELECTED:
            # Lock the aggregate while replacing positions; never write native fields.
            CustomFieldProfile.objects.select_for_update().get(pk=self.instance.pk)
            self.instance.profile_fields.all().delete()
            ProfileField.objects.bulk_create([
                ProfileField(profile=self.instance, field_id=pk, position=position)
                for position, pk in enumerate(self.ordered_field_ids)
            ])

    def save(self, commit=True):
        if not commit:
            return super().save(commit=False)
        with transaction.atomic():
            return super().save(commit=True)


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
