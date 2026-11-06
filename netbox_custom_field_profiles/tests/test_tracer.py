from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from extras.models import CustomField
from users.models import ObjectPermission

from netbox_custom_field_profiles.matching import get_matching_profiles, get_profile_fields
from netbox_custom_field_profiles.models import CustomFieldProfile


class ProfileTracerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser('profile-admin', 'profile@example.test', 'test-only')
        cls.device_ct = ContentType.objects.get_for_model(Device)
        manufacturer = Manufacturer.objects.create(name='Tracer manufacturer', slug='tracer-manufacturer')
        hardware = DeviceType.objects.create(manufacturer=manufacturer, model='Tracer hardware', slug='tracer-hardware')
        role = DeviceRole.objects.create(name='Tracer role', slug='tracer-role')
        site = Site.objects.create(name='Tracer site', slug='tracer-site')
        cls.device = Device.objects.create(name='Tracer device', device_type=hardware, role=role, site=site,
                                          custom_field_data={'tracer_value': 'external value'})
        cls.native_field = CustomField.objects.create(name='tracer_value', type='text')
        cls.native_field.object_types.add(cls.device_ct)

    def setUp(self):
        self.client.force_login(self.admin)

    def url(self, action='', profile=None):
        return reverse('plugins:netbox_custom_field_profiles:customfieldprofile' + action,
                       args=[profile.pk] if profile else None)

    def data(self, **kwargs):
        return {'title': 'Service Details', 'content_type': self.device_ct.pk,
                'display_order': 10, **kwargs}

    def snapshot(self):
        return (list(CustomField.objects.values().order_by('pk')),
                list(Device.objects.values('pk', 'custom_field_data').order_by('pk')))

    def test_real_admin_crud_and_native_resolution(self):
        before = self.snapshot()
        self.assertEqual(self.client.get(self.url('_list')).status_code, 200)
        self.assertEqual(self.client.get(self.url('_add')).status_code, 200)
        self.assertEqual(self.client.post(self.url('_add'), self.data()).status_code, 302)
        first = CustomFieldProfile.objects.get()
        self.assertFalse(first.enabled)
        self.assertEqual(first.field_mode, 'all')
        self.assertEqual(get_matching_profiles(self.device), [])
        self.assertEqual(self.client.post(self.url('_add'), self.data(enabled=True)).status_code, 302)
        second = CustomFieldProfile.objects.exclude(pk=first.pk).get()
        self.assertEqual(first.title, second.title)
        self.assertEqual(get_matching_profiles(self.device), [second])
        self.assertEqual(get_profile_fields(second), [self.native_field])
        self.assertEqual(self.client.get(first.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(self.url('_edit', first)).status_code, 200)
        for _ in range(2):
            self.assertEqual(self.client.post(self.url('_edit', first), self.data(enabled=True)).status_code, 302)
        self.assertEqual(list(CustomFieldProfile.objects.all()), [first, second])
        self.assertEqual(self.client.get(self.url('_delete', first)).status_code, 200)
        self.assertEqual(self.client.post(self.url('_delete', first), {'confirm': True}).status_code, 302)
        self.assertFalse(CustomFieldProfile.objects.filter(pk=first.pk).exists())
        self.assertEqual(self.snapshot(), before)

    def test_invalid_posts_preserve_existing_configuration(self):
        profile = CustomFieldProfile.objects.create(title='Original', content_type=self.device_ct, field_mode='all')
        before = self.snapshot()
        for data in (self.data(title=''), self.data(content_type=ContentType.objects.get_for_model(Site).pk)):
            response = self.client.post(self.url('_edit', profile), data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
            profile.refresh_from_db()
            self.assertEqual(profile.title, 'Original')
            self.assertFalse(profile.enabled)
            self.assertEqual(CustomFieldProfile.objects.count(), 1)
        self.assertEqual(self.snapshot(), before)

    def test_empty_list_and_escaped_titles(self):
        response = self.client.get(self.url('_list'))
        self.assertEqual(response.status_code, 200)
        profile = CustomFieldProfile.objects.create(title='<script>bad()</script>', content_type=self.device_ct)
        self.assertContains(self.client.get(profile.get_absolute_url()), '&lt;script&gt;bad()&lt;/script&gt;')

    def test_unpermitted_user_cannot_read_or_mutate(self):
        user = get_user_model().objects.create_user('profile-denied', password='test-only')
        self.client.force_login(user)
        profile = CustomFieldProfile.objects.create(title='Restricted', content_type=self.device_ct)
        for action, obj in (('_list', None), ('_add', None), ('', profile), ('_edit', profile), ('_delete', profile)):
            self.assertEqual(self.client.get(self.url(action, obj)).status_code, 403)
        for action, obj in (('_add', None), ('_edit', profile), ('_delete', profile)):
            self.assertEqual(self.client.post(self.url(action, obj), self.data(title='Changed')).status_code, 403)
        profile.refresh_from_db()
        self.assertEqual(profile.title, 'Restricted')
        self.assertEqual(CustomFieldProfile.objects.count(), 1)

    def test_navigation_and_view_only_authority(self):
        from netbox_custom_field_profiles.navigation import menu_items

        item = menu_items[0]
        self.assertEqual(str(item.url), self.url('_list'))
        self.assertEqual(item.permissions, ['netbox_custom_field_profiles.view_customfieldprofile'])
        self.assertEqual(str(item.buttons[0].url), self.url('_add'))
        self.assertEqual(item.buttons[0].permissions, ['netbox_custom_field_profiles.add_customfieldprofile'])
        self.assertContains(self.client.get(self.url('_list')), 'href="' + self.url('_add') + '"')

        viewer = get_user_model().objects.create_user('profile-viewer', password='test-only')
        permission = ObjectPermission.objects.create(name='Profile read only', actions=['view'])
        permission.object_types.add(ContentType.objects.get_for_model(CustomFieldProfile))
        permission.users.add(viewer)
        self.client.force_login(viewer)
        response = self.client.get(self.url('_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Custom Field Profiles')
        self.assertNotContains(response, 'href="' + self.url('_add') + '"')
        self.assertEqual(self.client.get(self.url('_add')).status_code, 403)

    def test_native_csrf_rejects_untrusted_mutation(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        self.assertEqual(client.post(self.url('_add'), self.data()).status_code, 403)
        self.assertEqual(CustomFieldProfile.objects.count(), 0)
