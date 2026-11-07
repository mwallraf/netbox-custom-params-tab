"""Native Device authority is required before resolving profile presentation."""
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from dcim.models import Device, Site
from extras.models import CustomField

from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from . import test_parameters, test_permissions, test_tracer


class ParameterPermissionTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    grant = test_permissions.ProfilePermissionTests.grant
    aggregate = test_permissions.ProfilePermissionTests.aggregate
    snapshot = test_tracer.ProfileTracerTests.snapshot
    parameter_url = test_parameters.ParametersTabTests.parameter_url

    def setUp(self):
        self.profile = CustomFieldProfile.objects.create(
            title='Private profile section', content_type=self.device_ct,
            enabled=True, field_mode='selected')
        ProfileField.objects.create(profile=self.profile, field=self.native_field, position=0)

    def user(self, name, actions=(), constraints=None):
        user = get_user_model().objects.create_user(name, password='test-only')
        if actions:
            self.grant(user, list(actions), model=Device, constraints=constraints)
        return user

    def parameter_content(self, response):
        return response.content.decode().split('<div id="device-parameters">', 1)[1]

    def test_device_only_viewer_and_constrained_included_device(self):
        for name, constraints in (('device-viewer', None),
                                  ('included-device', {'pk': self.device.pk})):
            with self.subTest(subject=name):
                user = self.user(name, ['view'], constraints)
                self.client.force_login(user)
                self.assertFalse(user.has_perm('netbox_custom_field_profiles.view_customfieldprofile'))
                self.assertFalse(user.has_perm('extras.view_customfield'))
                detail = self.client.get(reverse('dcim:device', args=[self.device.pk]))
                self.assertContains(detail, f'href="{self.parameter_url()}"')
                response = self.client.get(self.parameter_url())
                self.assertContains(response, 'external value')
                content = self.parameter_content(response)
                self.assertNotIn('Edit Parameters', content)
                self.assertNotIn('/plugins/custom-field-profiles/', content)

    def test_denied_subjects_and_no_match_never_resolve_profiles(self):
        profile_admin = self.user('profile-admin-only')
        self.grant(profile_admin, ['view', 'add', 'change', 'delete'])
        subjects = ((None, (302, 403)), (self.user('no-device-authority'), (403,)),
                    (self.user('change-only', ['change']), (403,)), (profile_admin, (403,)),
                    (self.user('excluded-device', ['view'], {'pk': 2147483647}), (404,)))
        for matching in (True, False):
            self.profile.enabled = matching
            self.profile.save()
            for user, expected in subjects:
                with self.subTest(matching=matching, subject=user):
                    self.client.logout()
                    if user:
                        self.client.force_login(user)
                    with patch('netbox_custom_field_profiles.views.build_sections') as build, \
                            patch('netbox_custom_field_profiles.views.get_matching_profiles') as match:
                        for url in (reverse('dcim:device', args=[self.device.pk]), self.parameter_url()):
                            response = self.client.get(url)
                            self.assertIn(response.status_code, expected)
                            for secret in ('Private profile section', 'Tracer device',
                                           'No parameter profiles apply to this device.'):
                                self.assertNotContains(response, secret, status_code=response.status_code)
                        build.assert_not_called()
                        match.assert_not_called()

    def test_authorized_direct_no_match_uses_normal_shell(self):
        self.profile.enabled = False
        self.profile.save()
        self.client.force_login(self.user('empty-state-viewer', ['view']))
        response = self.client.get(self.parameter_url())
        self.assertContains(response, 'No parameter profiles apply to this device.', count=1)
        self.assertTemplateUsed(response, 'dcim/device/base.html')

    def test_post_is_unsupported_and_preserves_native_and_profile_data(self):
        before = self.snapshot(), self.aggregate()
        self.client.force_login(self.user('post-viewer', ['view']))
        response = self.client.post(self.parameter_url(), {
            'custom_field_data': {'tracer_value': 'forged'}, 'enabled': False})
        self.assertEqual(response.status_code, 405)
        self.assertEqual((self.snapshot(), self.aggregate()), before)
        self.client.force_login(self.user('post-denied'))
        with patch('netbox_custom_field_profiles.views.build_sections') as build:
            self.assertEqual(self.client.post(self.parameter_url(), {}).status_code, 403)
            build.assert_not_called()

    def test_post_on_excluded_device_obeys_native_object_boundary(self):
        self.client.force_login(self.user('excluded-post', ['view'], {'pk': 2147483647}))
        self.assertEqual(self.client.post(self.parameter_url(), {}).status_code, 404)

    def test_initial_reference_guard_never_links_denied_native_object(self):
        field = CustomField.objects.create(
            name='private_reference', type='object',
            related_object_type=ContentType.objects.get_for_model(Site))
        # A Device grant conveys no Site grant.
        field.object_types.add(self.device_ct)
        ProfileField.objects.create(profile=self.profile, field=field, position=1)
        Device.objects.filter(pk=self.device.pk).update(custom_field_data={
            'tracer_value': 'external value', 'private_reference': self.device.site_id})
        self.client.force_login(self.user('restricted-reference-viewer', ['view']))
        content = self.parameter_content(self.client.get(self.parameter_url()))
        self.assertIn('Unavailable', content)
        self.assertNotIn('Tracer site', content)
        self.assertNotIn(self.device.site.get_absolute_url(), content)
