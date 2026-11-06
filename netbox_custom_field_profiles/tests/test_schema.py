from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.migrations.recorder import MigrationRecorder
from django.test import TestCase
from django.test import SimpleTestCase
from unittest import TestSuite
from unittest.mock import patch

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from extras.models import CustomField

from netbox_custom_field_profiles.matching import get_matching_profiles, get_profile_fields
from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from netbox_custom_field_profiles.tests.runner import ProfileTestRunner


class ProfileRunnerTests(SimpleTestCase):
    def test_empty_suite_rejected_before_database_setup(self):
        with patch('django.test.runner.DiscoverRunner.build_suite', return_value=TestSuite()):
            with self.assertRaisesRegex(RuntimeError, 'PROFILE_TESTS_EMPTY'):
                ProfileTestRunner().build_suite([])


class ProfileSchemaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.device_type = ContentType.objects.get_for_model(Device)
        manufacturer = Manufacturer.objects.create(name='Profile manufacturer', slug='profile-manufacturer')
        hardware = DeviceType.objects.create(manufacturer=manufacturer, model='Profile hardware', slug='profile-hardware')
        role = DeviceRole.objects.create(name='Profile role', slug='profile-role')
        site = Site.objects.create(name='Profile site', slug='profile-site')
        cls.device = Device.objects.create(name='Profile device', device_type=hardware, role=role, site=site)

    def profile(self, **kwargs):
        return CustomFieldProfile.objects.create(content_type=self.device_type, title='Service Details', **kwargs)

    def field(self, name, **kwargs):
        field = CustomField.objects.create(name=name, type='text', **kwargs)
        field.object_types.add(self.device_type)
        return field

    def test_duplicate_titles_default_disabled_and_total_order(self):
        first = self.profile(display_order=10)
        second = self.profile(display_order=10)
        alphabetic = CustomFieldProfile.objects.create(content_type=self.device_type, title='Alpha', display_order=10)
        self.assertFalse(first.enabled)
        self.assertEqual(list(CustomFieldProfile.objects.all()), [alphabetic, first, second])
        self.assertEqual(get_matching_profiles(self.device), [])

    def test_device_only_validation(self):
        profile = self.profile()
        profile.content_type = ContentType.objects.get_for_model(Site)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_membership_unique_per_profile_not_per_native_field(self):
        field = self.field('shared')
        first, second = self.profile(), self.profile()
        ProfileField.objects.create(profile=first, field=field, position=0)
        ProfileField.objects.create(profile=second, field=field, position=0)
        with self.assertRaises(IntegrityError), transaction.atomic():
            ProfileField.objects.create(profile=first, field=field, position=1)

    def test_native_all_resolution_enabled_only_and_dynamic_order(self):
        z = self.field('z_field', group_name='A', weight=10)
        a = self.field('a_field', group_name='B', weight=1)
        profile = self.profile(enabled=True, field_mode='all')
        self.assertEqual(get_matching_profiles(self.device), [profile])
        self.assertEqual(get_profile_fields(profile), [z, a])
        new = self.field('new_field', group_name='A', weight=1)
        self.assertEqual(get_profile_fields(profile), [new, z, a])
        self.assertEqual([f.pk for f in get_profile_fields(profile)],
                         [f.pk for f in CustomField.objects.get_for_model(Device)])

    def test_profile_operations_preserve_native_data(self):
        field = self.field('native_sentinel')
        Device.objects.filter(pk=self.device.pk).update(custom_field_data={'native_sentinel': 'external'})
        before_field = CustomField.objects.filter(pk=field.pk).values().get()
        before_device = Device.objects.filter(pk=self.device.pk).values('custom_field_data').get()
        profile = self.profile(enabled=True, field_mode='all')
        ProfileField.objects.create(profile=profile, field=field, position=0)
        get_profile_fields(profile)
        profile.delete()
        self.assertEqual(CustomField.objects.filter(pk=field.pk).values().get(), before_field)
        self.assertEqual(Device.objects.filter(pk=self.device.pk).values('custom_field_data').get(), before_device)

    def test_schema_matches_applied_retirement_state(self):
        retired = MigrationRecorder.Migration.objects.filter(
            app='netbox_custom_field_profiles', name='0003_retire_legacy_configuration').exists()
        tables = connection.introspection.table_names()
        for name in ('customtabconfig', 'customtabconfigfield', 'customtabconfiggroup'):
            self.assertEqual('netbox_custom_field_profiles_' + name in tables, not retired)
        self.assertIn(CustomFieldProfile._meta.db_table, tables)
        self.assertIn(ProfileField._meta.db_table, tables)
