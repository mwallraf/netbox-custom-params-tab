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

    def test_constrained_reference_matrix_and_request_local_authority(self):
        allowed = Site.objects.create(name='Allowed reference alpha', slug='allowed-reference-alpha')
        second = Site.objects.create(name='Allowed reference beta', slug='allowed-reference-beta')
        denied = Site.objects.create(pk=930001, name='Denied reference unique secret', slug='denied-reference-secret')
        missing_id = 930099
        fields = {}
        for name, kind in (
            ('allowed_scalar', 'object'), ('denied_scalar', 'object'),
            ('missing_scalar', 'object'), ('empty_scalar', 'object'),
            ('mixed_collection', 'multiobject'), ('denied_collection', 'multiobject'),
            ('missing_collection', 'multiobject'), ('empty_collection', 'multiobject')):
            field = CustomField.objects.create(
                name=name, type=kind, related_object_type=ContentType.objects.get_for_model(Site))
            field.object_types.add(self.device_ct)
            ProfileField.objects.create(profile=self.profile, field=field, position=len(fields) + 1)
            fields[name] = field
        repeated = CustomFieldProfile.objects.create(
            title='Repeated references', content_type=self.device_ct, enabled=True, field_mode='selected')
        for position, field in enumerate(fields.values()):
            ProfileField.objects.create(profile=repeated, field=field, position=position)
        values = {
            'tracer_value': 'external value',
            'allowed_scalar': allowed.pk, 'denied_scalar': denied.pk, 'missing_scalar': missing_id,
            'empty_scalar': None, 'mixed_collection': [second.pk, denied.pk, missing_id, allowed.pk],
            'denied_collection': [denied.pk], 'missing_collection': [missing_id], 'empty_collection': [],
        }
        Device.objects.filter(pk=self.device.pk).update(custom_field_data=values)
        limited = self.user('constrained-related-viewer', ['view'])
        self.grant(limited, ['view'], model=Site, constraints={'pk__in': [allowed.pk, second.pk]})
        original = CustomField.deserialize

        def guarded(field, value):
            self.assertNotIn(field.type, ('object', 'multiobject'))
            return original(field, value)

        # Alternate viewers twice: no cross-request authorized-instance cache may survive.
        for viewer in (self.admin, limited, self.admin, limited):
            with self.subTest(viewer=viewer.username):
                self.client.force_login(viewer)
                with patch.object(CustomField, 'deserialize', guarded):
                    response = self.client.get(self.parameter_url())
                self.assertEqual(response.status_code, 200)
                content = self.parameter_content(response)
                sections = response.context['sections']
                records = {row.field.name: row for row in sections[0].rows}
                for name in fields:
                    repeated_row = next(row for row in sections[1].rows if row.field.name == name)
                    self.assertIs(records[name], repeated_row)
                self.assertEqual(records['allowed_scalar'].value, allowed)
                self.assertTrue(records['missing_scalar'].unavailable)
                self.assertIsNone(records['missing_scalar'].value)
                self.assertTrue(records['missing_collection'].unavailable)
                self.assertEqual(records['missing_collection'].value, ())
                for name in ('empty_scalar', 'empty_collection'):
                    self.assertTrue(records[name].is_unset)
                    self.assertFalse(records[name].unavailable)
                self.assertEqual(content.count('Not set'), 4)
                if viewer == limited:
                    for secret in (denied.name, str(denied.pk), denied.get_absolute_url(), str(missing_id)):
                        self.assertNotIn(secret, content)
                        self.assertNotIn(secret, repr([row.value for row in records.values()]))
                    self.assertTrue(records['denied_scalar'].unavailable)
                    self.assertIsNone(records['denied_scalar'].value)
                    self.assertTrue(records['denied_collection'].unavailable)
                    self.assertEqual(records['denied_collection'].value, ())
                    self.assertEqual(records['mixed_collection'].value, tuple(
                        Site.objects.filter(pk__in=[allowed.pk, second.pk])))
                    self.assertEqual(content.count('Unavailable'), 8)
                else:
                    self.assertIn(denied.name, content)
                    self.assertEqual(records['denied_scalar'].value, denied)
                    self.assertEqual(content.count('Unavailable'), 4)
                self.assertEqual(Device.objects.get(pk=self.device.pk).custom_field_data, values)

    def test_viewer_without_related_permissions_sees_one_neutral_collection_placeholder(self):
        field = CustomField.objects.create(
            name='fully_denied_references', type='multiobject',
            related_object_type=ContentType.objects.get_for_model(Site))
        field.object_types.add(self.device_ct)
        ProfileField.objects.create(profile=self.profile, field=field, position=1)
        Device.objects.filter(pk=self.device.pk).update(custom_field_data={field.name: [self.device.site_id, 930099]})
        self.client.force_login(self.user('no-related-grant', ['view']))
        response = self.client.get(self.parameter_url())
        content = self.parameter_content(response)
        self.assertEqual(content.count('Unavailable'), 1)
        self.assertNotIn(self.device.site.name, content)
        self.assertNotIn(self.device.site.get_absolute_url(), content)
        row = response.context['sections'][0].rows[1]
        self.assertEqual(row.value, ())
        self.assertFalse(row.is_unset)
