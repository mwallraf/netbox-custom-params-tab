from django.db import transaction
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from dcim.models import Device, DeviceRole, DeviceType, Site
from extras.models import Tag
from users.models import ObjectPermission
from utilities.forms.fields import DynamicModelMultipleChoiceField

from netbox_custom_field_profiles.forms import CustomFieldProfileForm
from netbox_custom_field_profiles.matching import get_matching_profiles
from netbox_custom_field_profiles.models import CustomFieldProfile
from . import test_tracer


class ProfileMatchingTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    setUp = test_tracer.ProfileTracerTests.setUp
    data = test_tracer.ProfileTracerTests.data
    url = test_tracer.ProfileTracerTests.url
    snapshot = test_tracer.ProfileTracerTests.snapshot

    def profile(self, title='Profile', **kwargs):
        return CustomFieldProfile.objects.create(title=title, content_type=self.device_ct,
                                                enabled=True, field_mode='all', **kwargs)

    def test_fixed_and_or_any_tag_matrix(self):
        before = self.snapshot()
        other_type = DeviceType.objects.create(manufacturer=self.device.device_type.manufacturer,
                                              model='Other hardware', slug='other-hardware')
        other_role = DeviceRole.objects.create(name='Other role', slug='other-role')
        second = Device.objects.create(name='Second', device_type=other_type, role=other_role,
                                       site=self.device.site)
        red = Tag.objects.create(name='Red', slug='red')
        blue = Tag.objects.create(name='Blue', slug='blue')
        self.device.tags.add(red, blue)
        second.tags.add(blue)
        unrestricted = self.profile('A unrestricted')
        typed = self.profile('B types')
        typed.device_types.set([self.device.device_type, other_type])
        role = self.profile('C role')
        role.device_types.set([self.device.device_type, other_type])
        role.device_roles.add(self.device.role)
        tagged = self.profile('D tags')
        tagged.applicability_tags.set([red, blue])
        combined = self.profile('E combined')
        combined.device_types.add(self.device.device_type)
        combined.device_roles.add(self.device.role)
        combined.applicability_tags.add(red, blue)
        disabled = self.profile('F disabled')
        disabled.enabled = False
        disabled.save()
        self.assertEqual(get_matching_profiles(self.device), [unrestricted, typed, role, tagged, combined])
        self.assertEqual(get_matching_profiles(second), [unrestricted, typed, tagged])
        self.assertEqual(get_matching_profiles(self.device), get_matching_profiles(self.device))
        self.assertEqual(get_matching_profiles(self.device.site), [])
        # Rule changes and resolution never write native definitions/values.
        self.assertEqual(self.snapshot()[0], before[0])
        self.device.refresh_from_db()
        self.assertEqual(self.device.custom_field_data, {'tracer_value': 'external value'})

    def test_empty_disabled_and_deterministic_ties(self):
        self.assertEqual(get_matching_profiles(self.device), [])
        older = self.profile('Same', display_order=7)
        newer = self.profile('Same', display_order=7)
        alphabetic = self.profile('Alpha', display_order=7)
        self.assertEqual(get_matching_profiles(self.device), [alphabetic, older, newer])
        CustomFieldProfile.objects.update(enabled=False)
        self.assertEqual(get_matching_profiles(self.device), [])

    def test_searchable_fields_unused_tags_and_invalid_post_preservation(self):
        unused = Tag.objects.create(name='Unused compatible', slug='unused-compatible')
        unused.object_types.add(self.device_ct)
        unrestricted = Tag.objects.create(name='Unrestricted unused', slug='unrestricted-unused')
        foreign = Tag.objects.create(name='Site only', slug='site-only')
        foreign.object_types.add(ContentType.objects.get_for_model(Site))
        form = CustomFieldProfileForm()
        for name in ('device_types', 'device_roles', 'applicability_tags'):
            self.assertIsInstance(form.fields[name], DynamicModelMultipleChoiceField)
            self.assertFalse(form.fields[name].required)
        self.assertEqual(form.fields['applicability_tags'].query_params,
                         {'for_object_type_id': self.device_ct.pk})
        self.assertIn(unused, form.fields['applicability_tags'].queryset)
        self.assertIn(unrestricted, form.fields['applicability_tags'].queryset)
        self.assertNotIn(foreign, form.fields['applicability_tags'].queryset)
        response = self.client.post(self.url('_add'), self.data(
            enabled=True, device_types=[self.device.device_type_id],
            device_roles=[self.device.role_id], applicability_tags=[unused.pk, unrestricted.pk]))
        self.assertEqual(response.status_code, 302)
        profile = CustomFieldProfile.objects.get()
        before = self.snapshot()
        response = self.client.post(self.url('_edit', profile), self.data(
            title='Rejected', applicability_tags=[foreign.pk]))
        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertEqual(profile.title, 'Service Details')
        self.assertEqual(set(profile.applicability_tags.all()), {unused, unrestricted})
        self.assertEqual(list(profile.device_types.all()), [self.device.device_type])
        self.assertEqual(self.snapshot(), before)
        # Exercise native search discovery, including tags with no TaggedItem rows.
        response = self.client.get('/api/extras/tags/',
                                   {'for_object_type_id': self.device_ct.pk, 'q': 'unused'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({item['id'] for item in response.json()['results']}, {unused.pk, unrestricted.pk})

    def test_restricted_saved_references_cannot_be_silently_cleared(self):
        tag = Tag.objects.create(name='Restricted saved', slug='restricted-saved')
        profile = self.profile()
        profile.applicability_tags.add(tag)
        form = CustomFieldProfileForm(data=self.data(), instance=profile)
        form.fields['applicability_tags'].queryset = Tag.objects.none()
        self.assertFalse(form.is_valid())
        self.assertEqual(list(profile.applicability_tags.all()), [tag])

    def test_failed_transaction_does_not_publish_partial_rules(self):
        profile = self.profile()
        profile.device_roles.add(self.device.role)
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                form = CustomFieldProfileForm(data=self.data(device_types=[self.device.device_type_id]),
                                              instance=profile)
                self.assertTrue(form.is_valid(), form.errors)
                form.save()
                raise RuntimeError('rollback')
        self.assertEqual(list(profile.device_roles.all()), [self.device.role])
        self.assertFalse(profile.device_types.exists())

    def test_native_restricted_reference_post_cannot_broaden_profile(self):
        tag = Tag.objects.create(name='Not visible', slug='not-visible')
        profile = self.profile()
        profile.applicability_tags.add(tag)
        user = get_user_model().objects.create_user('limited-editor', password='test-only')
        permission = ObjectPermission.objects.create(name='Edit profiles', actions=['view', 'change'])
        permission.object_types.add(ContentType.objects.get_for_model(CustomFieldProfile))
        permission.users.add(user)
        self.client.force_login(user)
        response = self.client.post(self.url('_edit', profile), self.data(title='Should not save'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'saved references you cannot access')
        profile.refresh_from_db()
        self.assertEqual(profile.title, 'Profile')
        self.assertEqual(list(profile.applicability_tags.all()), [tag])

    def test_scope_columns_notice_and_escaped_labels(self):
        tag = Tag.objects.create(name='<script>tag()</script>', slug='escaped-tag')
        profile = self.profile('<script>title()</script>')
        response = self.client.get(self.url('_list'))
        for column in ('title', 'enabled', 'display_order', 'field_mode', 'applicability'):
            self.assertIn(column, response.context['table'].columns.names())
        self.assertContains(response, 'All applicable fields')
        self.assertContains(response, 'Applies to all Devices')
        profile.applicability_tags.add(tag)
        response = self.client.get(self.url('_list'))
        self.assertContains(response, '&lt;script&gt;tag()&lt;/script&gt;')
        self.assertNotContains(response, '<script>tag()</script>')
        response = self.client.get(profile.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;title()&lt;/script&gt;')
        self.assertContains(response, '&lt;script&gt;tag()&lt;/script&gt;')
        self.assertNotContains(response, 'Applies to all Devices')
        response = self.client.get(self.url('_edit', profile))
        self.assertContains(response, 'id="profile-unrestricted-notice" hidden')
        profile.applicability_tags.clear()
        response = self.client.get(self.url('_edit', profile))
        self.assertContains(response, 'id="profile-unrestricted-notice">Applies to all Devices')
        self.assertEqual(self.client.post(self.url('_edit', profile), self.data()).status_code, 302)
