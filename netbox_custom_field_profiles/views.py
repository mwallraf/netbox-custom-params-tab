from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView
from .models import CustomFieldProfile
from .tables import CustomFieldProfileTable
from .forms import CustomFieldProfileForm


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
