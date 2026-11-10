from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView
from dcim.models import Device
from utilities.views import ViewTab, register_model_view
from .models import CustomFieldProfile
from .tables import CustomFieldProfileTable
from .forms import CustomFieldProfileForm
from .matching import get_matching_profiles
from .presentation import build_sections
from .forms import DeviceParametersForm
from django.db import transaction
from django.urls import reverse


@register_model_view(Device, name='custom_field_profiles', path='parameters')
class DeviceParametersView(ObjectView):
    queryset = Device.objects.all()
    template_name = 'netbox_custom_field_profiles/device_parameters.html'
    actions = ()
    tab = ViewTab(
        label='Parameters', permission='dcim.view_device',
        visible=lambda device: bool(get_matching_profiles(device)),
    )

    def get_extra_context(self, request, instance):
        # ObjectView has already applied native Device view constraints.
        form = DeviceParametersForm(instance=instance, user=request.user)
        return {
            'sections': build_sections(instance, request.user),
            'can_edit_parameters': bool(form.custom_fields) and Device.objects.restrict(
                request.user, 'change').filter(pk=instance.pk).exists(),
        }

    def http_method_not_allowed(self, request, *args, **kwargs):
        # Native dispatch checks the action grant first. Apply the constrained
        # object lookup too before reporting this read-only destination's methods.
        self.get_object(**kwargs)
        return super().http_method_not_allowed(request, *args, **kwargs)


@register_model_view(Device, name='edit_parameters', path='parameters/edit')
class DeviceParametersEditView(ObjectEditView):
    queryset = Device.objects.all()
    template_name = 'netbox_custom_field_profiles/device_parameters_edit.html'
    http_method_names = ['get', 'post', 'head', 'options']

    def dispatch(self, request, *args, **kwargs):
        # This is only a partial edit of an existing Device. Native quick-add
        # and clone redirects are inappropriate and can include unrelated data.
        request.GET = request.GET.copy()
        request.GET.pop('_quickadd', None)
        if request.method == 'POST':
            request.POST = request.POST.copy()
            request.POST.pop('_addanother', None)
        return super().dispatch(request, *args, **kwargs)

    def form(self, *args, **kwargs):
        return DeviceParametersForm(*args, user=self.request.user, **kwargs)

    def get_object(self, **kwargs):
        if self.request.method == 'POST':
            self.queryset = self.queryset.select_for_update()
        return super().get_object(**kwargs)

    def post(self, request, *args, **kwargs):
        # Lock before loading values so saves merge with the latest unrelated
        # native values, including writes made after the edit page was opened.
        with transaction.atomic():
            return super().post(request, *args, **kwargs)

    def get_return_url(self, request, obj=None):
        return reverse('dcim:device_custom_field_profiles', args=[obj.pk])


class CustomFieldProfileListView(ObjectListView):
    queryset = CustomFieldProfile.objects.select_related('content_type')
    table = CustomFieldProfileTable
    template_name = 'generic/object_list.html'


class CustomFieldProfileView(ObjectView):
    queryset = CustomFieldProfile.objects.select_related('content_type')
    template_name = 'netbox_custom_field_profiles/customfieldprofile.html'


class CustomFieldProfileEditView(ObjectEditView):
    queryset = CustomFieldProfile.objects.all()
    form = CustomFieldProfileForm
    template_name = 'netbox_custom_field_profiles/customfieldprofile_edit.html'
    default_return_url = 'plugins:netbox_custom_field_profiles:customfieldprofile_list'


class CustomFieldProfileDeleteView(ObjectDeleteView):
    queryset = CustomFieldProfile.objects.all()
    template_name = 'generic/object_delete.html'
    default_return_url = 'plugins:netbox_custom_field_profiles:customfieldprofile_list'
