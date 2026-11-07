"""Real Device navigation and cold-start native registration contracts."""
import re
from datetime import timedelta

from django.test import TestCase
from django.urls import NoReverseMatch, resolve, reverse
from django.utils import timezone

from dcim.models import Device, DeviceRole, DeviceType, Site
from extras.models import CustomField, Tag

from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from netbox_custom_field_profiles.matching import get_profile_fields
from . import test_tracer


class ParametersTabTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)

    def setUp(self):
        self.client.force_login(self.admin)
        self.profile = CustomFieldProfile.objects.create(
            title='Service parameters', content_type=self.device_ct,
            enabled=True, field_mode='selected', display_order=10)
        ProfileField.objects.create(profile=self.profile, field=self.native_field, position=0)

    def parameter_url(self, device=None):
        return reverse('dcim:device_custom_field_profiles', args=[(device or self.device).pk])

    def parameter_response(self, device=None):
        response = self.client.get(self.parameter_url(device))
        self.assertEqual(response.status_code, 200)
        return response

    def create_profile(self, title, fields=(), **kwargs):
        kwargs.setdefault('display_order', 0)
        profile = CustomFieldProfile.objects.create(
            title=title, content_type=self.device_ct, enabled=True,
            field_mode='selected', **kwargs)
        for position, field in enumerate(fields):
            ProfileField.objects.create(profile=profile, field=field, position=position)
        return profile

    def assert_sections(self, response, profiles):
        sections = response.context['sections']
        self.assertEqual([section.profile.pk for section in sections], [p.pk for p in profiles])
        for section, profile in zip(sections, profiles):
            self.assertEqual([row.field.pk for row in section.rows],
                             [field.pk for field in get_profile_fields(profile)])
        content = response.content.decode().split('<div id="device-parameters">', 1)[1]
        self.assertEqual(re.findall(r'<h2 class="card-header">(.*?)</h2>', content),
                         [p.title for p in profiles])
        for forbidden in ('data-bs-toggle="collapse"', 'Applies to all Devices',
                          'Selected fields', 'Display order', 'Edit Parameters'):
            self.assertNotIn(forbidden, content)

    def test_matching_device_classes_shared_and_combined_rules(self):
        cpe_type = DeviceType.objects.create(manufacturer=self.device.device_type.manufacturer,
                                            model='CPE', slug='cpe')
        cpe_role = DeviceRole.objects.create(name='CPE', slug='cpe')
        cpe = Device.objects.create(name='CPE device', site=self.device.site,
                                   device_type=cpe_type, role=cpe_role)
        wanted = Tag.objects.create(name='Wanted', slug='wanted')
        other = Tag.objects.create(name='Other', slug='other')
        self.device.tags.add(wanted)
        cmts = self.create_profile('CMTS only', [self.native_field], display_order=0)
        cmts.device_types.add(self.device.device_type, cpe_type)
        cmts.device_roles.add(self.device.role)
        cmts.applicability_tags.add(wanted, other)
        cpe_profile = self.create_profile('CPE only', [self.native_field], display_order=1)
        cpe_profile.device_types.add(cpe_type)
        disabled = self.create_profile('Disabled', [self.native_field])
        disabled.enabled = False
        disabled.save()
        self.assert_sections(self.parameter_response(), [cmts, self.profile])
        self.assert_sections(self.parameter_response(cpe), [cpe_profile, self.profile])
        self.device.tags.clear()
        self.assert_sections(self.parameter_response(), [self.profile])

    def test_duplicate_titles_complete_tie_breaks_and_selected_order(self):
        alpha = CustomField.objects.create(name='alpha', type='text', weight=1)
        alpha.object_types.add(self.device_ct)
        first = self.create_profile('Duplicate', [self.native_field, alpha], display_order=1)
        second = self.create_profile('Duplicate', [alpha, self.native_field], display_order=1)
        third = self.create_profile('Duplicate', [alpha], display_order=1)
        now = timezone.now()
        CustomFieldProfile.objects.filter(pk=first.pk).update(created=now + timedelta(seconds=1))
        CustomFieldProfile.objects.filter(pk__in=[second.pk, third.pk]).update(created=now)
        response = self.parameter_response()
        self.assert_sections(response, [second, third, first, self.profile])
        content = response.content.decode().split('<div id="device-parameters">', 1)[1]
        self.assertEqual(content.count('external value'), 3)

    def test_dynamic_all_membership_and_live_status_applicability(self):
        all_profile = self.create_profile('All fields')
        all_profile.field_mode = 'all'
        all_profile.save()
        added = CustomField.objects.create(name='added_later', type='text', weight=1)
        added.object_types.add(self.device_ct)
        hidden = CustomField.objects.create(name='inactive_field', type='text')
        hidden.object_types.add(self.device_ct)
        deleting = CustomField.objects.create(name='deleting_field', type='text')
        deleting.object_types.add(self.device_ct)
        CustomField.objects.filter(pk=hidden.pk).update(status='provisioning')
        CustomField.objects.filter(pk=deleting.pk).update(status='deleting')
        foreign = CustomField.objects.create(name='site_only', type='text')
        from django.contrib.contenttypes.models import ContentType
        foreign.object_types.add(ContentType.objects.get_for_model(Site))
        response = self.parameter_response()
        self.assert_sections(response, [all_profile, self.profile])
        self.assertEqual([r.field.name for r in response.context['sections'][0].rows],
                         ['added_later', 'tracer_value'])
        self.assertEqual([r.field.name for r in response.context['sections'][1].rows], ['tracer_value'])
        added.object_types.clear()
        self.assert_sections(self.parameter_response(), [all_profile, self.profile])
        self.native_field.delete()
        added.delete()
        response = self.parameter_response()
        self.assert_sections(response, [all_profile])
        self.assertContains(response, 'No fields are available in this profile.')

    def test_native_writes_refresh_every_repeated_occurrence_and_selection_retains_data(self):
        repeated = self.create_profile('Repeated', [self.native_field])
        for value in ('updated through native Device', None):
            self.device.custom_field_data = {'tracer_value': value}
            self.device.full_clean()
            self.device.save()
            response = self.parameter_response()
            self.assert_sections(response, [repeated, self.profile])
            sections = response.context['sections']
            self.assertIs(sections[0].rows[0], sections[1].rows[0])
            self.assertEqual([s.rows[0].raw_value for s in sections], [value, value])
            self.assertContains(response, value or 'Not set', count=2)
        self.device.custom_field_data = {'tracer_value': 'retained native value'}
        self.device.save()
        self.profile.profile_fields.all().delete()
        repeated.enabled = False
        repeated.save()
        self.parameter_response()
        self.device.refresh_from_db()
        self.assertEqual(self.device.custom_field_data['tracer_value'], 'retained native value')

    def test_cold_start_registered_device_navigation_and_real_value(self):
        # No import of plugin views: only normal application startup may register it.
        try:
            url = self.parameter_url()
        except NoReverseMatch:
            self.fail('Application startup must register the native Device Parameters route')
        self.assertEqual(resolve(url).func.view_class.__name__, 'DeviceParametersView')
        detail = self.client.get(reverse('dcim:device', args=[self.device.pk]))
        self.assertContains(detail, f'href="{url}"')
        self.assertTemplateNotUsed(detail, 'netbox_custom_field_profiles/tab_panel.html')
        response = self.client.get(url)
        self.assertContains(response, 'Service parameters')
        self.assertContains(response, 'external value')
        self.assertTemplateUsed(response, 'dcim/device/base.html')
        self.assertRegex(response.content.decode(),
                         rf'<a(?=[^>]*class="[^"]*active[^"]*")(?=[^>]*href="{re.escape(url)}")[^>]*>')

    def test_disabled_or_nonmatching_profiles_hide_navigation_and_direct_empty_state(self):
        for state in ('disabled', 'nonmatching'):
            with self.subTest(state=state):
                self.profile.enabled = state != 'disabled'
                self.profile.save()
                if state == 'nonmatching':
                    from dcim.models import DeviceRole
                    role = DeviceRole.objects.create(name='Other role', slug='other-role')
                    self.profile.device_roles.add(role)
                detail = self.client.get(reverse('dcim:device', args=[self.device.pk]))
                self.assertNotContains(detail, f'href="{self.parameter_url()}"')
                response = self.client.get(self.parameter_url())
                self.assertContains(response, 'No parameter profiles apply to this device.', count=1)
                self.assertTemplateUsed(response, 'dcim/device/base.html')
                self.assertNotContains(response, 'No fields are available in this profile.')

    def test_zero_fields_keeps_matching_navigation_and_section(self):
        # All mode is allowed to have no fields and stays enabled.
        self.profile.field_mode = 'all'
        self.profile.save()
        self.native_field.object_types.clear()
        detail = self.client.get(reverse('dcim:device', args=[self.device.pk]))
        self.assertContains(detail, f'href="{self.parameter_url()}"')
        response = self.client.get(self.parameter_url())
        self.assertContains(response, 'Service parameters')
        self.assertContains(response, 'No fields are available in this profile.', count=1)
        self.assertNotContains(response, 'No parameter profiles apply to this device.')
