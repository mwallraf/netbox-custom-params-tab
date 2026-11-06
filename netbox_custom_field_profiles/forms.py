import json

from django import forms
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.forms import NetBoxModelForm
from extras.models import CustomField, Tag
from dcim.models import DeviceType, DeviceRole
from utilities.forms.fields import DynamicModelMultipleChoiceField
from .models import CustomFieldProfile, ProfileField


class CustomFieldProfileForm(NetBoxModelForm):
    rule_fields = ('device_types', 'device_roles', 'applicability_tags')
    device_types = DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(), required=False,
        help_text='Match any selected Device Type. Empty means any type.',
    )
    device_roles = DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(), required=False,
        label='Device roles', help_text='Match any selected role. Empty means any role.',
    )
    applicability_tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.none(), required=False, label='Device tags',
        help_text='Match any selected tag. Empty means no tag restriction.',
    )
    selected_fields = forms.ModelMultipleChoiceField(
        queryset=CustomField.objects.none(), required=False,
        help_text='Choose applicable fields, then arrange their display order below.',
    )
    field_order = forms.CharField(required=False, widget=forms.HiddenInput)
    remembered_fields = forms.CharField(required=False, widget=forms.HiddenInput)
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(app_label='dcim', model='device'),
        label='Object Type',
    )

    class Meta:
        model = CustomFieldProfile
        fields = ('title', 'content_type', 'display_order', 'enabled', 'field_mode',
                  'selected_fields', 'field_order', 'remembered_fields', 'device_types', 'device_roles',
                  'applicability_tags')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (self.is_bound and self.data.get('field_mode') == CustomFieldProfile.FIELD_MODE_ALL
                and 'remembered_fields' in self.data and 'selected_fields' not in self.data):
            try:
                remembered = self._parse_field_ids(self.data.get('remembered_fields'))
            except (ValueError, TypeError):
                pass  # clean() reports malformed remembered state without saving it.
            else:
                # All disables the visible selector. Rebind its explicit remembered
                # values so native field validation/permission restrictions still
                # apply, and a failed form redisplays the pending choices.
                self.data = self.data.copy()
                if hasattr(self.data, 'setlist'):
                    self.data.setlist('selected_fields', [str(pk) for pk in remembered])
                else:
                    self.data['selected_fields'] = remembered
        device_ct = self.fields['content_type'].queryset.first()
        self.fields['applicability_tags'].queryset = Tag.objects.filter(
            Q(object_types=device_ct) | Q(object_types__isnull=True)).distinct()
        self.fields['applicability_tags'].query_params = {'for_object_type_id': device_ct.pk}
        self.fields['selected_fields'].queryset = CustomField.objects.filter(
            object_types__app_label='dcim', object_types__model='device').distinct()
        self.fields['selected_fields'].widget.attrs['class'] = 'form-select'
        ordered = []
        if not self.instance.pk:
            self.initial.setdefault('content_type', self.fields['content_type'].queryset.first())
            self.initial.setdefault('field_mode', CustomFieldProfile.FIELD_MODE_ALL)
        else:
            ordered = list(self.instance.profile_fields.values_list('field_id', flat=True))
        self.initial.setdefault('selected_fields', ordered)
        self.initial.setdefault('field_order', json.dumps(ordered))
        self.initial.setdefault('remembered_fields', json.dumps(ordered))

    @staticmethod
    def _parse_field_ids(raw):
        ids = json.loads(raw)
        if (not isinstance(ids, list) or any(type(pk) is not int or pk <= 0 for pk in ids)
                or len(ids) != len(set(ids))):
            raise ValueError
        return ids

    def full_clean(self):
        # Dynamic fields narrow their queryset to bound values when constructing
        # BoundFields. Capture native permission restrictions before that happens.
        self.rule_authority = {name: self.fields[name].queryset.all() for name in self.rule_fields}
        super().full_clean()

    def clean(self):
        super().clean()
        cleaned = self.cleaned_data
        if self.instance.pk:
            for name in self.rule_fields:
                # Native views restrict these querysets by the editor's authority.
                # A hidden/inaccessible saved reference must not become an empty rule.
                existing = getattr(self.instance, name).values_list('pk', flat=True)
                if set(existing) - set(self.rule_authority[name].values_list('pk', flat=True)):
                    self.add_error(name, 'This profile has saved references you cannot access. '
                                         'Ask an administrator to review its applicability.')
        self.ordered_field_ids = None
        selected_mode = cleaned.get('field_mode') == CustomFieldProfile.FIELD_MODE_SELECTED
        if not selected_mode and 'remembered_fields' not in self.data:
            # Clients without an explicit remembered payload preserve saved state.
            return cleaned
        selected = cleaned.get('selected_fields')
        if selected is None:
            return cleaned
        if selected_mode and not selected:
            self.add_error('selected_fields', 'Select at least one applicable field.')
        selected_ids = {field.pk for field in selected}
        if 'remembered_fields' in self.data:
            try:
                remembered = self._parse_field_ids(cleaned.get('remembered_fields'))
                if set(remembered) != selected_ids:
                    raise ValueError
            except (ValueError, TypeError):
                self.add_error('remembered_fields', 'Remembered fields must contain each selected field exactly once. '
                                                  'Review the selection and try again.')
        raw_selection = (self.data.getlist('selected_fields') if hasattr(self.data, 'getlist')
                         else self.data.get('selected_fields', []))
        if len(raw_selection) != len(set(raw_selection)):
            self.add_error('selected_fields', 'Select each field only once.')
        try:
            ordered = self._parse_field_ids(cleaned.get('field_order') or '[]')
            if set(ordered) != selected_ids:
                raise ValueError
        except (ValueError, TypeError):
            self.add_error('field_order', 'Field order must contain each selected field exactly once.')
        else:
            self.ordered_field_ids = ordered
        return cleaned

    @property
    def applies_to_all_devices(self):
        if self.is_bound:
            return not any(self.data.get(name) for name in self.rule_fields)
        return not any(self.initial.get(name) for name in self.rule_fields)

    @transaction.atomic
    def _save_m2m(self):
        super()._save_m2m()
        if self.ordered_field_ids is not None:
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
