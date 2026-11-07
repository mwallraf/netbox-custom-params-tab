"""Real Device navigation and cold-start native registration contracts."""
import re

from django.test import TestCase
from django.urls import NoReverseMatch, resolve, reverse

from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from . import test_tracer


class ParametersTabTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)

    def setUp(self):
        self.client.force_login(self.admin)
        self.profile = CustomFieldProfile.objects.create(
            title='Service parameters', content_type=self.device_ct,
            enabled=True, field_mode='selected')
        ProfileField.objects.create(profile=self.profile, field=self.native_field, position=0)

    def parameter_url(self, device=None):
        return reverse('dcim:device_custom_field_profiles', args=[(device or self.device).pk])

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
