"""Native custom-field ownership remains unchanged by profile administration."""
import json

from django.test import TestCase
from django.apps import apps
from django.urls import Resolver404, resolve, reverse
from dcim.models import Device, DeviceRole, DeviceType
from extras.models import CustomField, Tag

from netbox_custom_field_profiles.matching import get_matching_profiles, get_profile_fields
from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from . import test_tracer


class ProfilePreservationTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    setUp = test_tracer.ProfileTracerTests.setUp
    data = test_tracer.ProfileTracerTests.data
    url = test_tracer.ProfileTracerTests.url

    def snapshot(self):
        return (list(CustomField.objects.values().order_by('pk')),
                list(CustomField.object_types.through.objects.values().order_by('id')),
                list(Device.objects.values('pk', 'custom_field_data').order_by('pk')))

    def selected(self, fields, **extra):
        return self.data(field_mode='selected', enabled=True,
                         selected_fields=[field.pk for field in fields],
                         field_order=json.dumps([field.pk for field in fields]), **extra)

    def post_unchanged(self, url, payload):
        before = self.snapshot()
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.snapshot(), before)
        return response

    def test_all_management_operations_preserve_full_native_snapshots(self):
        second_field = CustomField.objects.create(
            name='second_native', type='text', label='Native label', group_name='Native group',
            weight=7, ui_visible='hidden', ui_editable='hidden')
        second_field.object_types.add(self.device_ct)
        other_type = DeviceType.objects.create(manufacturer=self.device.device_type.manufacturer,
                                              model='CPE hardware', slug='cpe-hardware')
        other_role = DeviceRole.objects.create(name='CPE role', slug='cpe-role')
        cpe = Device.objects.create(name='CPE sentinel', device_type=other_type,
                                    role=other_role, site=self.device.site,
                                    custom_field_data={'tracer_value': 'CPE value', 'second_native': 'keep CPE'})
        Device.objects.filter(pk=self.device.pk).update(
            custom_field_data={'tracer_value': 'CMTS value', 'second_native': 'keep CMTS'})
        tag = Tag.objects.create(name='Matching tag', slug='matching-tag')
        self.device.tags.add(tag)
        before = self.snapshot()
        for title, types in (('CMTS', [self.device.device_type_id]), ('CPE', [other_type.pk]), ('Shared', [])):
            self.post_unchanged(self.url('_add'), self.selected(
                [second_field, self.native_field], title=title, device_types=types))
        cmts, cpe_profile, shared = [CustomFieldProfile.objects.get(title=title) for title in ('CMTS', 'CPE', 'Shared')]
        self.assertEqual(get_matching_profiles(self.device), [cmts, shared])
        self.assertEqual(get_matching_profiles(cpe), [cpe_profile, shared])
        self.assertEqual(ProfileField.objects.filter(field=self.native_field).count(), 3)
        for profile in (cmts, cpe_profile, shared):
            fields = get_profile_fields(profile)
            self.assertEqual(fields, [second_field, self.native_field])
            self.assertTrue(all(isinstance(field, CustomField) for field in fields))
        # Reorder, title/order change, every fixed criterion, disable and enable.
        payload = self.selected([self.native_field, second_field], title='Reordered', display_order=1,
                                device_types=[self.device.device_type_id, other_type.pk],
                                device_roles=[self.device.role_id, other_role.pk], applicability_tags=[tag.pk])
        self.post_unchanged(self.url('_edit', cmts), payload)
        self.assertEqual(get_profile_fields(cmts), [self.native_field, second_field])
        self.post_unchanged(self.url('_edit', cmts), {**payload, 'enabled': False})
        self.post_unchanged(self.url('_edit', cmts), payload)
        self.post_unchanged(self.url('_edit', cmts), self.data(field_mode='all', enabled=True))
        cmts.refresh_from_db()
        self.assertEqual(list(cmts.profile_fields.values_list('field_id', flat=True)),
                         [self.native_field.pk, second_field.pk])
        self.post_unchanged(self.url('_edit', cmts), self.selected([self.native_field, second_field]))
        for profile in (cmts, cpe_profile, shared):
            self.post_unchanged(self.url('_delete', profile), {'confirm': True})
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(CustomFieldProfile.objects.count(), 0)

    def test_external_native_changes_are_resolved_without_copying_values(self):
        self.post_unchanged(self.url('_add'), self.selected([self.native_field], title='Selected'))
        selected = CustomFieldProfile.objects.get(title='Selected')
        self.post_unchanged(self.url('_add'), self.data(title='All', field_mode='all', enabled=True))
        all_fields = CustomFieldProfile.objects.get(title='All')
        # This deliberately simulates an external native script, not a profile write.
        Device.objects.filter(pk=self.device.pk).update(custom_field_data={'tracer_value': 'script updated'})
        new = CustomField.objects.create(name='new_native', type='text', group_name='Z', weight=3)
        new.object_types.add(self.device_ct)
        before = self.snapshot()
        self.assertEqual(get_profile_fields(selected), [self.native_field])
        self.assertIn(new, get_profile_fields(all_fields))
        self.assertEqual(get_profile_fields(all_fields), list(CustomField.objects.get_for_model(Device)))
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(any('value' in field.name or 'data' in field.name
                             for field in ProfileField._meta.fields))

    def test_native_lifecycle_preserves_unrelated_definitions_and_values(self):
        unrelated = CustomField.objects.create(name='untouched', type='text', label='Untouched label')
        unrelated.object_types.add(self.device_ct)
        Device.objects.filter(pk=self.device.pk).update(
            custom_field_data={'tracer_value': 'native target', 'untouched': 'unrelated value'})
        tag = Tag.objects.create(name='Lifecycle target', slug='lifecycle-target')
        self.post_unchanged(self.url('_add'), self.selected(
            [self.native_field, unrelated], applicability_tags=[tag.pk]))
        profile = CustomFieldProfile.objects.get()
        before = self.snapshot()
        tag.delete()
        profile.refresh_from_db()
        self.assertFalse(profile.enabled)
        self.assertEqual(self.snapshot(), before)
        field_before = CustomField.objects.filter(pk=unrelated.pk).values().get()
        # NetBox owns cleanup for the deliberately removed field; assert only unrelated state.
        self.native_field.object_types.remove(self.device_ct)
        self.assertEqual(CustomField.objects.filter(pk=unrelated.pk).values().get(), field_before)
        self.device.refresh_from_db()
        self.assertEqual(self.device.custom_field_data['untouched'], 'unrelated value')
        self.assertEqual(list(profile.profile_fields.values_list('field_id', flat=True)), [unrelated.pk])
        self.assertFalse(CustomFieldProfile.objects.get(pk=profile.pk).enabled)

    def test_retired_runtime_has_no_legacy_api_or_panel_registration(self):
        from netbox.registry import registry
        from netbox_custom_field_profiles import template_content
        from netbox_custom_field_profiles.api import serializers, views

        config = apps.get_app_config('netbox_custom_field_profiles')
        self.assertNotIn('extra_models', config.default_settings)
        self.assertEqual(template_content.template_extensions, [])
        self.assertFalse(hasattr(views, 'CustomTabConfigViewSet'))
        self.assertFalse(hasattr(serializers, 'CustomTabConfigSerializer'))
        for extensions in registry['plugins']['template_extensions'].values():
            self.assertFalse(any(extension.__module__ == template_content.__name__
                                 for extension in extensions))
        with self.assertRaises(Resolver404):
            resolve('/api/plugins/custom-field-profiles/custom-tab-configs/')

    def test_profile_runtime_and_event_serialization_survive_retirement(self):
        from netbox_custom_field_profiles.api.serializers import CustomFieldProfileSerializer

        before = self.snapshot()
        self.post_unchanged(self.url('_add'), self.data(title='Runtime sentinel', field_mode='all'))
        profile = CustomFieldProfile.objects.get()
        self.assertEqual(self.client.get(self.url('_list')).status_code, 200)
        self.assertEqual(self.client.get(profile.get_absolute_url()).status_code, 200)
        self.assertEqual(CustomFieldProfileSerializer(profile).data['title'], 'Runtime sentinel')
        self.post_unchanged(self.url('_delete', profile), {'confirm': True})
        self.assertEqual(self.snapshot(), before)

    def test_native_device_page_does_not_render_retired_plugin_panel(self):
        before = self.snapshot()
        response = self.client.get(reverse('dcim:device', args=[self.device.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'netbox_custom_field_profiles/tab_panel.html')
        self.assertEqual(self.snapshot(), before)
