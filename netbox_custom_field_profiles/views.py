from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView
from dcim.models import Device
from utilities.views import ViewTab, register_model_view
from .models import CustomFieldProfile
from .tables import CustomFieldProfileTable
from .forms import CustomFieldProfileForm
from .matching import get_matching_profiles
from .presentation import build_sections


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
        return {'sections': build_sections(instance, request.user)}


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
