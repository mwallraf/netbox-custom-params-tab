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
