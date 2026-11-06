"""Read-only native field resolution and reusable Device profile matching."""
from dcim.models import Device
from extras.models import CustomField

from .models import CustomFieldProfile


def get_matching_profiles(device):
    """Return enabled, unrestricted Device profiles in deterministic order.

    Fixed-rule matching is added by the applicability plan. Restricting this
    preparation slice to empty criteria fails closed for any configured rules.
    """
    if not isinstance(device, Device):
        return []
    return list(CustomFieldProfile.objects.filter(
        enabled=True, content_type__app_label='dcim', content_type__model='device',
        device_types__isnull=True, device_roles__isnull=True, applicability_tags__isnull=True,
    ))


def get_profile_fields(profile):
    """Resolve current active native fields without writing native definitions."""
    if (profile.content_type.app_label, profile.content_type.model) != ('dcim', 'device'):
        return []
    native = CustomField.objects.get_for_model(Device)
    if profile.field_mode == CustomFieldProfile.FIELD_MODE_ALL:
        return native
    active = {field.pk: field for field in native}
    return [active[entry.field_id] for entry in profile.profile_fields.all() if entry.field_id in active]
