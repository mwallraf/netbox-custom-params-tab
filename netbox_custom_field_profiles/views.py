from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView
from .models import CustomFieldProfile, CustomTabConfig
from .tables import CustomFieldProfileTable, CustomTabConfigTable
from .forms import (
    CustomTabConfigForm,
    CustomTabConfigGroupFormSet,
    CustomTabConfigFieldFormSet,
    GROUP_FORMSET_PREFIX,
    FIELD_FORMSET_PREFIX,
    CustomFieldProfileForm,
)


class CustomFieldProfileListView(ObjectListView):
    queryset = CustomFieldProfile.objects.select_related('content_type')
    table = CustomFieldProfileTable
    template_name = 'generic/object_list.html'


class CustomFieldProfileView(ObjectView):
    queryset = CustomFieldProfile.objects.select_related('content_type')
    template_name = 'generic/object.html'


class CustomFieldProfileEditView(ObjectEditView):
    queryset = CustomFieldProfile.objects.all()
    form = CustomFieldProfileForm
    template_name = 'generic/object_edit.html'
    default_return_url = 'plugins:netbox_custom_field_profiles:customfieldprofile_list'


class CustomFieldProfileDeleteView(ObjectDeleteView):
    queryset = CustomFieldProfile.objects.all()
    template_name = 'generic/object_delete.html'
    default_return_url = 'plugins:netbox_custom_field_profiles:customfieldprofile_list'


class CustomTabConfigListView(ObjectListView):
    queryset = CustomTabConfig.objects.prefetch_related('config_groups', 'config_fields')
    table = CustomTabConfigTable


class CustomTabConfigView(ObjectView):
    queryset = CustomTabConfig.objects.all()


class CustomTabConfigEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'netbox_custom_field_profiles.add_customtabconfig',
        'netbox_custom_field_profiles.change_customtabconfig',
    )
    template_name = 'netbox_custom_field_profiles/customtabconfig_edit.html'

    def _build_forms(self, instance=None, data=None):
        form = CustomTabConfigForm(data=data, instance=instance)
        group_formset = CustomTabConfigGroupFormSet(
            data=data, instance=instance, prefix=GROUP_FORMSET_PREFIX
        )
        field_formset = CustomTabConfigFieldFormSet(
            data=data, instance=instance, prefix=FIELD_FORMSET_PREFIX
        )
        return form, group_formset, field_formset

    def get(self, request, pk=None):
        instance = get_object_or_404(CustomTabConfig, pk=pk) if pk else CustomTabConfig()
        form, group_formset, field_formset = self._build_forms(instance=instance)
        return render(request, self.template_name, {
            'form': form,
            'group_formset': group_formset,
            'field_formset': field_formset,
            'object': instance,
        })

    def post(self, request, pk=None):
        instance = get_object_or_404(CustomTabConfig, pk=pk) if pk else CustomTabConfig()
        form, group_formset, field_formset = self._build_forms(instance=instance, data=request.POST)
        if form.is_valid() and group_formset.is_valid() and field_formset.is_valid():
            with transaction.atomic():
                config = form.save()
                group_formset.instance = config
                group_formset.save()
                field_formset.instance = config
                field_formset.save()
            messages.success(request, f'Saved config for {config.content_type}.')
            return redirect(reverse('plugins:netbox_custom_field_profiles:customtabconfig_list'))
        return render(request, self.template_name, {
            'form': form,
            'group_formset': group_formset,
            'field_formset': field_formset,
            'object': instance,
        })


class CustomTabConfigDeleteView(ObjectDeleteView):
    queryset = CustomTabConfig.objects.all()
    default_return_url = 'plugins:netbox_custom_field_profiles:customtabconfig_list'
