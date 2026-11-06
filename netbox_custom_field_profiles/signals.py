"""Maintain plugin configuration when native references change.

Receivers write only profile tables. Native NetBox handlers retain ownership of
custom-field definitions and object values. Relation-manager operations emit the
signals used here; direct SQL/bulk through-table writes do not. Resolution also
checks live applicability, but such bypasses do not synchronously clean rows.
"""
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models.signals import m2m_changed, pre_delete

from dcim.models import DeviceRole, DeviceType
from extras.models import CustomField, Tag

from .models import CustomFieldProfile, ProfileField


def disable_target_profiles(sender, instance, using, **kwargs):
    """Disable before cascades erase references, in the deletion transaction."""
    relation = {DeviceType: 'device_types', DeviceRole: 'device_roles',
                Tag: 'applicability_tags'}[sender]
    CustomFieldProfile.objects.using(using).filter(
        **{relation: instance.pk}, enabled=True,
    ).update(enabled=False)


def lock_profile_fields(field_ids, using):
    """Serialize native field changes and profile saves before any profile lock."""
    return list(CustomField.objects.using(using).select_for_update().filter(
        pk__in=field_ids,
    ).order_by('pk').values_list('pk', flat=True))


def remove_field_memberships(field_ids, using):
    """Remove invalid references and disable only newly empty Selected profiles."""
    with transaction.atomic(using=using):
        lock_profile_fields(field_ids, using)
        memberships = ProfileField.objects.using(using).filter(field_id__in=field_ids)
        affected_ids = list(memberships.values_list('profile_id', flat=True).distinct())
        if not affected_ids:
            return
        # Field locks precede aggregate locks, including when no membership existed
        # when cleanup began: a concurrent form cannot insert behind this scan.
        list(CustomFieldProfile.objects.using(using).select_for_update().filter(
            pk__in=affected_ids,
        ).order_by('pk').values_list('pk', flat=True))
        memberships.delete()
        CustomFieldProfile.objects.using(using).filter(
            pk__in=affected_ids, field_mode=CustomFieldProfile.FIELD_MODE_SELECTED,
            profile_fields__isnull=True, enabled=True,
        ).update(enabled=False)


def field_deleted(sender, instance, using, **kwargs):
    # A native deferred deletion sends pre_delete while retaining the field row.
    # A queryset collector sends one signal per row. Lock its entire field set
    # before the first aggregate, so multi-field deletion keeps the same order.
    origin = kwargs.get('origin')
    if getattr(origin, 'model', None) is CustomField:
        lock_profile_fields(origin.using(using).values_list('pk', flat=True), using)
    remove_field_memberships([instance.pk], using)


def field_object_types_changed(sender, instance, action, reverse, pk_set, using, **kwargs):
    """Clean actual Device-applicability loss, in either relation direction."""
    if action not in ('pre_clear', 'pre_remove', 'post_clear', 'post_remove'):
        return
    if action == 'pre_remove':
        lock_profile_fields(list(pk_set or ()) if reverse else [instance.pk], using)
        return
    if action == 'pre_clear':
        field_ids = (list(CustomField.objects.using(using).filter(
            object_types=instance.pk,
        ).values_list('pk', flat=True)) if reverse else [instance.pk])
        lock_profile_fields(field_ids, using)
        # clear() has no pk_set. Keep state on this operation's instance, not global
        # process state: concurrent requests/databases must not share a capture.
        captures = getattr(instance, '_profile_field_clear_ids', {})
        captures[using] = field_ids
        instance._profile_field_clear_ids = captures
        return
    if action == 'post_clear':
        field_ids = getattr(instance, '_profile_field_clear_ids', {}).pop(using, [])
    else:
        field_ids = list(pk_set or ()) if reverse else [instance.pk]
    device_type_id = ContentType.objects.using(using).filter(
        app_label='dcim', model='device',
    ).values_list('pk', flat=True).first()
    invalid_ids = list(CustomField.objects.using(using).filter(
        pk__in=field_ids,
    ).exclude(object_types=device_type_id).values_list('pk', flat=True))
    remove_field_memberships(invalid_ids, using)


def register():
    """Stable IDs make repeated ready()/registration calls harmless."""
    for sender, suffix in ((DeviceType, 'device_type'), (DeviceRole, 'device_role'), (Tag, 'tag')):
        pre_delete.connect(disable_target_profiles, sender=sender,
                           dispatch_uid=f'custom_field_profiles.disable_deleted_{suffix}')
    pre_delete.connect(field_deleted, sender=CustomField,
                       dispatch_uid='custom_field_profiles.remove_deleted_field')
    m2m_changed.connect(field_object_types_changed, sender=CustomField.object_types.through,
                        dispatch_uid='custom_field_profiles.field_applicability')
