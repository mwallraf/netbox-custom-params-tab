"""Documentation is discoverable through NetBox's own System plugin page."""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse


class PluginDocumentationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            'documentation-admin', password='test-only')

    @override_settings(ISOLATED_DEPLOYMENT=True)
    @patch('core.views.get_catalog_plugins', return_value={})
    def test_native_plugin_page_explains_native_fields_visibility_and_links(self, catalog):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('core:plugin', args=['netbox_custom_field_profiles']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/plugin.html')
        self.assertContains(response, 'Maarten Wallraf')
        self.assertContains(response, 'creates no field definitions or separate value storage')
        self.assertContains(response, 'viewing and editing use native NetBox fields')
        self.assertContains(response, 'UI visibility to Hidden')
        self.assertContains(response, 'native editability still applies')
        for target in ('', '/blob/HEAD/docs/user-guide.md', '/blob/HEAD/LICENSE',
                       '/blob/HEAD/docs/development/installation.md'):
            self.assertContains(response,
                'href="https://github.com/mwallraf/netbox-custom-params-tab' + target + '"')
        # Dedicated catalog metadata is not falsely advertised as supplied locally.
        self.assertEqual(response.context['plugin'].license_type, '')
        self.assertEqual(response.context['plugin'].homepage_url, '')
