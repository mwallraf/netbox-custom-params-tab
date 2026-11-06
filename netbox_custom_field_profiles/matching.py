"""Read-only native field resolution and reusable Device profile matching."""
from dcim.models import Device
from extras.choices import CustomFieldStatusChoices
from extras.models import CustomField

from .models import CustomFieldProfile


def get_matching_profiles(device):
    """AND between configured criteria, OR within each, in profile order."""
    if not isinstance(device, Device):
        return []
    candidates = CustomFieldProfile.objects.filter(
        enabled=True, content_type__app_label='dcim', content_type__model='device',
    ).prefetch_related('device_types', 'device_roles', 'applicability_tags')
    device_tags = set(device.tags.values_list('pk', flat=True))
    result = []
    for profile in candidates:
        types = {item.pk for item in profile.device_types.all()}
        roles = {item.pk for item in profile.device_roles.all()}
        tags = {item.pk for item in profile.applicability_tags.all()}
        if ((not types or device.device_type_id in types)
                and (not roles or device.role_id in roles)
                and (not tags or tags.intersection(device_tags))):
            result.append(profile)
    return result


def get_profile_filter_summary(profile):
    """Return plain text for native escaping by tables/templates."""
    criteria = []
    for label, name in (('Device Type', 'device_types'), ('Role', 'device_roles'),
                        ('Tag', 'applicability_tags')):
        values = [str(item) for item in getattr(profile, name).all()]
        if values:
            criteria.append(f'{label}: (' + ' OR '.join(values) + ')')
    return ' AND '.join(criteria) or 'Applies to all Devices'


def get_profile_fields(profile):
    """Resolve current active native fields without writing native definitions."""
    if (profile.content_type.app_label, profile.content_type.model) != ('dcim', 'device'):
        return []
    # Native resolution owns ordering, while a fresh applicability/status guard
    # excludes stale cached entries even after direct through-table/status writes.
    database = profile._state.db or 'default'
    live_ids = set(CustomField.objects.using(database).filter(
        object_types__app_label='dcim', object_types__model='device',
        status=CustomFieldStatusChoices.STATUS_ACTIVE,
    ).values_list('pk', flat=True))
    native = [field for field in CustomField.objects.db_manager(database).get_for_model(Device)
              if field.pk in live_ids]
    if profile.field_mode == CustomFieldProfile.FIELD_MODE_ALL:
        return native
    active = {field.pk: field for field in native}
    return [active[entry.field_id] for entry in profile.profile_fields.all() if entry.field_id in active]
