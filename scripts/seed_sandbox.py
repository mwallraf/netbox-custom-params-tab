"""Native ORM dummy data, executed through manage.py shell in the project container.

Integration: exec(open('/opt/netbox-custom-field-profiles/scripts/seed_sandbox.py').read()); seed(check=True)
"""
import os


def require_sandbox():
    if os.environ.get('SANDBOX_PROJECT') != 'netbox-custom-field-profiles':
        raise RuntimeError('refusing seed outside dedicated project context')
    from django.conf import settings
    database = settings.DATABASES['default']
    if database.get('HOST') != 'postgres' or database.get('NAME') != 'netbox':
        raise RuntimeError('refusing seed outside dedicated project database')


def seed_once():
    require_sandbox()
    from django.contrib.contenttypes.models import ContentType
    from django.db import transaction
    from dcim.models import Site, Manufacturer, DeviceType, DeviceRole, Device
    from extras.models import CustomField, Tag
    with transaction.atomic():
        site, _ = Site.objects.get_or_create(slug='cfp-sandbox', defaults={'name': 'CFP Sandbox'})
        manufacturer, _ = Manufacturer.objects.get_or_create(slug='cfp-sandbox', defaults={'name': 'CFP Sandbox'})
        tag, _ = Tag.objects.get_or_create(slug='cfp-sandbox', defaults={'name': 'CFP Sandbox', 'color': '2196f3'})
        content_type = ContentType.objects.get_for_model(Device)
        fields = []
        for name, kind in [('cfp_sandbox_service', 'text'), ('cfp_sandbox_capacity', 'integer')]:
            field, _ = CustomField.objects.get_or_create(name=name, defaults={'type': kind, 'group_name': 'CFP Sandbox'})
            if field.type != kind:
                raise RuntimeError('owned seed field has conflicting type')
            field.object_types.add(content_type)
            fields.append(field)
        devices = []
        types = []
        roles = []
        for kind, capacity in [('cmts', 24), ('cpe', 2)]:
            device_type, _ = DeviceType.objects.get_or_create(manufacturer=manufacturer, model='CFP Sandbox ' + kind.upper(),
                                                             defaults={'slug': 'cfp-sandbox-' + kind})
            role, _ = DeviceRole.objects.get_or_create(name='CFP Sandbox ' + kind.upper(),
                                                       defaults={'slug': 'cfp-sandbox-' + kind, 'color': '2196f3'})
            device, _ = Device.objects.get_or_create(name='cfp-sandbox-' + kind,
                                                      defaults={'site': site, 'device_type': device_type, 'role': role, 'status': 'active'})
            if device.site_id != site.pk or device.device_type_id != device_type.pk or device.role_id != role.pk:
                raise RuntimeError('owned seed identity conflicts with existing device')
            data = dict(device.custom_field_data)
            data.update(cfp_sandbox_service=kind.upper(), cfp_sandbox_capacity=capacity)
            if data != device.custom_field_data:
                device.custom_field_data = data
                device.full_clean()
                device.save()
            device.tags.add(tag)
            devices.append((device.pk, device.name, device.custom_field_data, tuple(device.tags.order_by('pk').values_list('pk', flat=True))))
            types.append(device_type.pk)
            roles.append(role.pk)
        return {'site': site.pk, 'manufacturer': manufacturer.pk, 'tag': tag.pk,
                'fields': [field.pk for field in fields], 'types': types, 'roles': roles, 'devices': devices}


def seed(check=False):
    first = seed_once()
    if check:
        second = seed_once()
        if first != second:
            raise RuntimeError('owned seed identities or values changed on repeat')
        print('SEED_IDEMPOTENT_OK')
    else:
        print('SEED_READY')
    return first


def seed_snapshot():
    """Read-only lifecycle sentinel; missing data is an error, never reseeded."""
    require_sandbox()
    from dcim.models import Device
    devices = list(Device.objects.filter(name__in=['cfp-sandbox-cmts', 'cfp-sandbox-cpe']).order_by('name')
                   .values('id', 'name', 'custom_field_data'))
    if len(devices) != 2:
        raise RuntimeError('owned lifecycle sentinels missing')
    return devices
