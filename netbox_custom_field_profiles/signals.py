"""Maintain plugin configuration when native references change.

Receivers write only profile tables. Native NetBox handlers retain ownership of
custom-field definitions and object values. Relation-manager operations emit the
signals used here; direct SQL/bulk through-table writes do not. Resolution also
checks live applicability, but such bypasses do not synchronously clean rows.
"""
from django.db.models.signals import pre_delete

from dcim.models import DeviceRole, DeviceType
from extras.models import Tag

from .models import CustomFieldProfile


def disable_target_profiles(sender, instance, using, **kwargs):
    """Disable before cascades erase references, in the deletion transaction."""
    relation = {DeviceType: 'device_types', DeviceRole: 'device_roles',
                Tag: 'applicability_tags'}[sender]
    CustomFieldProfile.objects.using(using).filter(
        **{relation: instance.pk}, enabled=True,
    ).update(enabled=False)


def register():
    """Stable IDs make repeated ready()/registration calls harmless."""
    for sender, suffix in ((DeviceType, 'device_type'), (DeviceRole, 'device_role'), (Tag, 'tag')):
        pre_delete.connect(disable_target_profiles, sender=sender,
                           dispatch_uid=f'custom_field_profiles.disable_deleted_{suffix}')
