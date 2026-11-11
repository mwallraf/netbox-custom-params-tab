"""Native System plugin metadata, isolation and access-control contracts."""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from core.plugins import Plugin
from netbox_custom_field_profiles.metadata import DOCS_URL, INSTALLATION_URL, PROJECT_URL, SUMMARY


@override_settings(ISOLATED_DEPLOYMENT=True)
class PluginDocumentationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            'documentation-admin', password='test-only')

    def detail_url(self, name='netbox_custom_field_profiles'):
        return reverse('core:plugin', args=[name])

    @patch('core.views.get_catalog_plugins', return_value={})
    def test_native_plugin_page_separates_summary_description_url_and_license(self, catalog):
        self.client.force_login(self.admin)
        response = self.client.get(self.detail_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/plugin.html')
        plugin = response.context['plugin']
        self.assertEqual(plugin.title_long, 'NetBox Custom Field Profiles')
        self.assertEqual(plugin.tag_line, SUMMARY)
        self.assertNotIn('http', plugin.tag_line)
        self.assertNotIn('[', plugin.tag_line)
        self.assertEqual(plugin.homepage_url, PROJECT_URL)
        self.assertEqual(plugin.license_type, 'MIT')
        self.assertContains(response, '<td>MIT</td>', html=True)
        self.assertContains(response, 'Maarten Wallraf')
        self.assertContains(response, 'creates no field definitions or separate value storage')
        self.assertContains(response, 'viewing and editing use native NetBox fields')
        self.assertContains(response, 'UI visibility to Hidden')
        self.assertContains(response, 'native editability still applies')
        for target in (PROJECT_URL, DOCS_URL, INSTALLATION_URL,
                       PROJECT_URL + '/blob/HEAD/docs/user-guide.md'):
            self.assertContains(response, f'href="{target}"')

    def test_other_plugin_entry_and_cached_objects_are_unchanged(self):
        own = Plugin(config_name='netbox_custom_field_profiles', title_long='Catalog title',
                     tag_line='Catalog summary', description_short='Catalog text')
        other = Plugin(config_name='other_plugin', title_long='Other plugin',
                       tag_line='Other summary', description_short='Other description',
                       homepage_url='https://example.com/other', license_type='BSD')
        catalog = {'netbox_custom_field_profiles': own, 'other_plugin': other}
        self.client.force_login(self.admin)
        with patch('core.views.get_catalog_plugins', return_value=catalog):
            response = self.client.get(self.detail_url())
            self.assertEqual(response.context['plugin'].license_type, 'MIT')
            self.assertEqual(own.tag_line, 'Catalog summary')
            self.assertEqual(own.description_short, 'Catalog text')
            self.assertEqual(own.homepage_url, '')
            self.assertEqual(own.license_type, '')
            response = self.client.get(self.detail_url('other_plugin'))
            self.assertEqual(response.status_code, 200)
            self.assertIs(response.context['plugin'], other)
            self.assertContains(response, 'Other description')
            self.assertContains(response, '<td>BSD</td>', html=True)

    @patch('core.views.get_catalog_plugins', return_value={})
    def test_plugin_overview_uses_native_template_and_short_metadata(self, catalog):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('core:plugin_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/plugin_list.html')
        self.assertContains(response, 'NetBox Custom Field Profiles')
        own = next(item for item in response.context['table'].data
                   if item.config_name == 'netbox_custom_field_profiles')
        self.assertEqual(own.tag_line, SUMMARY)
        self.assertEqual(own.homepage_url, PROJECT_URL)
        self.assertEqual(own.license_type, 'MIT')

    def test_native_superuser_boundary_is_preserved(self):
        ordinary = get_user_model().objects.create_user('documentation-viewer', password='test-only')
        for user in (None, ordinary):
            self.client.logout()
            if user:
                self.client.force_login(user)
            for url in (reverse('core:plugin_list'), self.detail_url()):
                response = self.client.get(url)
                self.assertIn(response.status_code, (302, 403))
                self.assertNotContains(response, 'UI visibility to Hidden', status_code=response.status_code)
