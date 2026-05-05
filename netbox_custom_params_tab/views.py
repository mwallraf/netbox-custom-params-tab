from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from netbox.views.generic import ObjectListView, ObjectView, ObjectDeleteView
from .models import CustomTabConfig
from .tables import CustomTabConfigTable
from .forms import (
    CustomTabConfigForm,
    CustomTabConfigGroupFormSet,
    CustomTabConfigFieldFormSet,
    GROUP_FORMSET_PREFIX,
    FIELD_FORMSET_PREFIX,
)


class CustomTabConfigListView(ObjectListView):
    queryset = CustomTabConfig.objects.prefetch_related('groups', 'fields')
    table = CustomTabConfigTable


class CustomTabConfigView(ObjectView):
    queryset = CustomTabConfig.objects.all()


class CustomTabConfigEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = (
        'netbox_custom_params_tab.add_customtabconfig',
        'netbox_custom_params_tab.change_customtabconfig',
    )
    template_name = 'netbox_custom_params_tab/customtabconfig_edit.html'

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
        instance = get_object_or_404(CustomTabConfig, pk=pk) if pk else None
        form, group_formset, field_formset = self._build_forms(instance=instance)
        return render(request, self.template_name, {
            'form': form,
            'group_formset': group_formset,
            'field_formset': field_formset,
            'object': instance,
        })

    def post(self, request, pk=None):
        instance = get_object_or_404(CustomTabConfig, pk=pk) if pk else None
        form, group_formset, field_formset = self._build_forms(instance=instance, data=request.POST)
        if form.is_valid() and group_formset.is_valid() and field_formset.is_valid():
            with transaction.atomic():
                config = form.save()
                group_formset.instance = config
                group_formset.save()
                field_formset.instance = config
                field_formset.save()
            messages.success(request, f'Saved config for {config.content_type}.')
            return redirect(reverse('plugins:netbox_custom_params_tab:customtabconfig_list'))
        return render(request, self.template_name, {
            'form': form,
            'group_formset': group_formset,
            'field_formset': field_formset,
            'object': instance,
        })


class CustomTabConfigDeleteView(ObjectDeleteView):
    queryset = CustomTabConfig.objects.all()
    default_return_url = 'plugins:netbox_custom_params_tab:customtabconfig_list'
