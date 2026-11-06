"""Exercise native action/object authority through actual profile requests."""
import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.test import Client, TestCase
from dcim.models import DeviceRole, DeviceType, Site
from extras.models import CustomField, Tag
from users.models import ObjectPermission

from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from . import test_tracer


class ProfilePermissionTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    data = test_tracer.ProfileTracerTests.data
    url = test_tracer.ProfileTracerTests.url

    def setUp(self):
        self.profile = CustomFieldProfile.objects.create(
            title='Permitted', content_type=self.device_ct, field_mode='selected', enabled=True)
        ProfileField.objects.create(profile=self.profile, field=self.native_field, position=0)

    def grant(self, user, actions, model=CustomFieldProfile, constraints=None):
        permission = ObjectPermission.objects.create(
            name=f'{user.username}-{model._meta.model_name}-{actions}',
            actions=actions, constraints=constraints)
        permission.object_types.add(ContentType.objects.get_for_model(model))
        permission.users.add(user)

    def user(self, name, actions=(), constraints=None, references=False):
        user = get_user_model().objects.create_user(name, password='test-only')
        if actions:
            self.grant(user, list(actions), constraints=constraints)
        if references:
            for model in (CustomField, DeviceType, DeviceRole, Tag):
                self.grant(user, ['view'], model=model)
        return user

    def aggregate(self):
        return (list(CustomFieldProfile.objects.values().order_by('pk')),
                list(ProfileField.objects.values().order_by('pk')),
                *[list(getattr(CustomFieldProfile, name).through.objects.values().order_by('id'))
                  for name in ('device_types', 'device_roles', 'applicability_tags')])

    def selected_data(self, **extra):
        return self.data(field_mode='selected', selected_fields=[self.native_field.pk],
                         field_order=json.dumps([self.native_field.pk]), **extra)

    def test_each_native_action_controls_get_post_and_navigation(self):
        routes = (('_list', None, 'view'), ('', self.profile, 'view'),
                  ('_add', None, 'add'), ('_edit', self.profile, 'change'),
                  ('_delete', self.profile, 'delete'))
        for action in ('view', 'add', 'change', 'delete'):
            with self.subTest(action=action):
                user = self.user('only-' + action, [action], references=True)
                self.client.force_login(user)
                before = self.aggregate()
                for route, obj, required in routes:
                    response = self.client.get(self.url(route, obj))
                    self.assertEqual(response.status_code, 200 if action == required else 403,
                                     (action, route))
                self.assertEqual(self.aggregate(), before, 'GET must not mutate any aggregate')
                for route, obj, required in routes[2:]:
                    if action != required:
                        self.assertEqual(self.client.post(self.url(route, obj), self.data()).status_code, 403)
                        self.assertEqual(self.aggregate(), before)
                if action == 'add':
                    response = self.client.post(self.url('_add'), self.data(title='Add-only result'))
                    self.assertEqual(response.status_code, 302)
                    CustomFieldProfile.objects.get(title='Add-only result').delete()
                elif action == 'change':
                    response = self.client.post(self.url('_edit', self.profile), self.selected_data(title='Changed'))
                    self.assertEqual(response.status_code, 302)
                    self.profile.refresh_from_db()
                    self.assertEqual(self.profile.title, 'Changed')
                elif action == 'delete':
                    doomed = CustomFieldProfile.objects.create(title='Delete-only', content_type=self.device_ct)
                    response = self.client.post(self.url('_delete', doomed), {'confirm': True})
                    self.assertEqual(response.status_code, 302)
                    self.assertFalse(CustomFieldProfile.objects.filter(pk=doomed.pk).exists())
                if action == 'view':
                    response = self.client.get(self.url('_list'))
                    self.assertNotContains(response, 'href="' + self.url('_add') + '"')
                    self.assertNotContains(response, 'href="' + self.url('_edit', self.profile) + '"')

    def test_anonymous_and_no_permission_cannot_read_or_mutate(self):
        for user in (None, self.user('no-permissions')):
            self.client.logout()
            if user:
                self.client.force_login(user)
            before = self.aggregate()
            for action, obj in (('_list', None), ('', self.profile), ('_add', None),
                                ('_edit', self.profile), ('_delete', self.profile)):
                response = self.client.get(self.url(action, obj))
                self.assertIn(response.status_code, (302, 403))
            for action, obj in (('_add', None), ('_edit', self.profile), ('_delete', self.profile)):
                self.assertIn(self.client.post(self.url(action, obj), self.data()).status_code, (302, 403))
            self.assertEqual(self.aggregate(), before)

    def test_constrained_lists_direct_urls_and_post_save_rollback(self):
        excluded = CustomFieldProfile.objects.create(title='Excluded', content_type=self.device_ct)
        user = self.user('constrained', ['view', 'add', 'change', 'delete'],
                         constraints={'title': 'Permitted'}, references=True)
        self.client.force_login(user)
        response = self.client.get(self.url('_list'))
        self.assertContains(response, 'Permitted')
        self.assertNotContains(response, '>Excluded<')
        self.assertEqual(list(response.context['table'].data), [self.profile])
        before = self.aggregate()
        for action in ('', '_edit', '_delete'):
            self.assertEqual(self.client.get(self.url(action, excluded)).status_code, 404)
        for action in ('_edit', '_delete'):
            self.assertEqual(self.client.post(self.url(action, excluded), self.data()).status_code, 404)
        # Native ObjectEditView checks constraints again after aggregate persistence.
        for action, obj in (('_add', None), ('_edit', self.profile)):
            response = self.client.post(self.url(action, obj), self.selected_data(
                title='Outside constraint', enabled=False, device_roles=[self.device.role_id]))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].non_field_errors())
            self.assertEqual(self.aggregate(), before)

    def test_forged_aggregate_payloads_preserve_every_component(self):
        self.client.force_login(self.admin)
        tag = Tag.objects.create(name='Saved tag', slug='saved-tag')
        self.profile.device_types.add(self.device.device_type)
        self.profile.device_roles.add(self.device.role)
        self.profile.applicability_tags.add(tag)
        foreign = CustomField.objects.create(name='site_field', type='text')
        foreign.object_types.add(ContentType.objects.get_for_model(Site))
        cases = ({'content_type': ContentType.objects.get_for_model(Site).pk},
                 {'selected_fields': [foreign.pk], 'field_order': json.dumps([foreign.pk])},
                 {'selected_fields': [2147483647]}, {'device_types': [2147483647]},
                 {'device_roles': [2147483647]}, {'applicability_tags': [2147483647]},
                 {'field_order': '[true]'}, {'field_mode': 'forged-mode'})
        before = self.aggregate()
        for forged in cases:
            with self.subTest(payload=forged):
                payload = {**self.selected_data(title='Must not save', enabled=False), **forged}
                response = self.client.post(self.url('_edit', self.profile), payload)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertEqual(self.aggregate(), before)

    def test_membership_write_error_rolls_back_native_view_aggregate(self):
        self.client.force_login(self.admin)
        before = self.aggregate()
        with patch('netbox_custom_field_profiles.forms.ProfileField.objects.bulk_create',
                   side_effect=IntegrityError('injected membership error')):
            with self.assertRaises(IntegrityError):
                self.client.post(self.url('_edit', self.profile), self.selected_data(
                    title='Must roll back', enabled=False, device_roles=[self.device.role_id]))
        self.assertEqual(self.aggregate(), before)

    def test_csrf_required_for_every_mutation_and_get_is_read_only(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        before = self.aggregate()
        for action, obj in (('_add', None), ('_edit', self.profile), ('_delete', self.profile)):
            self.assertEqual(client.post(self.url(action, obj), self.selected_data()).status_code, 403)
            self.assertEqual(client.get(self.url(action, obj)).status_code, 200)
            self.assertEqual(self.aggregate(), before)
