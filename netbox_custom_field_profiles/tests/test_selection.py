import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from dcim.models import Site
from extras.models import CustomField
from users.models import ObjectPermission

from netbox_custom_field_profiles.forms import CustomFieldProfileForm
from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from netbox_custom_field_profiles.matching import get_profile_fields
from . import test_tracer


class ProfileSelectionTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    setUp = test_tracer.ProfileTracerTests.setUp
    data = test_tracer.ProfileTracerTests.data
    url = test_tracer.ProfileTracerTests.url
    snapshot = test_tracer.ProfileTracerTests.snapshot
    def form_data(self, fields, **extra):
        return self.data(field_mode='selected', selected_fields=[f.pk for f in fields],
                         field_order=json.dumps([f.pk for f in fields]), **extra)

    def save_form(self, data, profile=None, commit=True):
        form = CustomFieldProfileForm(data=data, instance=profile)
        self.assertTrue(form.is_valid(), form.errors)
        with transaction.atomic():
            obj = form.save(commit=commit)
            if not commit:
                obj.save()
                form.save_m2m()
        return obj

    def test_selected_order_mode_roundtrip_and_dynamic_all(self):
        other = CustomField.objects.create(name='a_second', type='text', group_name='Z')
        other.object_types.add(self.device_ct)
        before = self.snapshot()
        profile = self.save_form(self.form_data([other, self.native_field]), commit=False)
        self.assertEqual(get_profile_fields(profile), [other, self.native_field])
        self.save_form(self.data(field_mode='all'), profile)
        self.assertEqual(list(profile.profile_fields.values_list('field_id', flat=True)), [other.pk, self.native_field.pk])
        self.assertEqual(get_profile_fields(profile), list(CustomField.objects.get_for_model(self.device)))
        self.save_form(self.form_data([other, self.native_field]), profile)
        self.assertEqual(get_profile_fields(profile), [other, self.native_field])
        second = self.save_form(self.form_data([self.native_field]))
        self.assertEqual(get_profile_fields(second), [self.native_field])
        self.assertEqual(self.snapshot(), before)
        new = CustomField.objects.create(name='new_dynamic', type='text', group_name='A', weight=1)
        new.object_types.add(self.device_ct)
        self.assertNotIn(new, get_profile_fields(profile))
        self.save_form(self.data(field_mode='all'), profile)
        self.assertIn(new, get_profile_fields(profile))

    def test_invalid_selection_payloads_rejected_atomically(self):
        profile = self.save_form(self.form_data([self.native_field]))
        other = CustomField.objects.create(name='foreign_field', type='text')
        other.object_types.add(ContentType.objects.get_for_model(Site))
        cases = [self.form_data([]), self.form_data([other]),
                 {**self.form_data([self.native_field]), 'field_order': '[true]'},
                 {**self.form_data([self.native_field]), 'field_order': '["bad"]'},
                 {**self.form_data([self.native_field]), 'field_order': 'broken'},
                 {**self.form_data([self.native_field]), 'field_order': '[]'},
                 {**self.form_data([self.native_field]), 'field_order': json.dumps([self.native_field.pk]*2)}]
        cases.append({**self.form_data([self.native_field]), 'selected_fields': [self.native_field.pk]*2})
        before = self.snapshot()
        for data in cases:
            form = CustomFieldProfileForm(data=data, instance=profile)
            self.assertFalse(form.is_valid(), data)
            profile.refresh_from_db()
            self.assertEqual(list(profile.profile_fields.values_list('field_id', flat=True)), [self.native_field.pk])
        self.assertEqual(self.snapshot(), before)

    def test_restricted_choices_reject_even_otherwise_applicable_field(self):
        form = CustomFieldProfileForm(data=self.form_data([self.native_field]))
        form.fields['selected_fields'].queryset = CustomField.objects.none()
        self.assertFalse(form.is_valid())

    def test_all_empty_and_temporary_inactive_preserve_membership(self):
        profile = self.save_form(self.form_data([self.native_field]))
        CustomField.objects.filter(pk=self.native_field.pk).update(status='provisioning')
        self.assertEqual(get_profile_fields(profile), [])
        self.assertEqual(profile.profile_fields.count(), 1)
        self.save_form(self.data(field_mode='all'), profile)
        self.assertEqual(get_profile_fields(profile), [])
        self.assertEqual(profile.profile_fields.count(), 1)

    def test_invalid_browser_form_retains_order_and_errors(self):
        response = self.client.post(self.url('_add'), self.form_data([self.native_field], title=''))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertContains(response, 'field_order')

    def test_native_page_saves_selection_and_restores_manual_order(self):
        other = CustomField.objects.create(name='page_second', type='text')
        other.object_types.add(self.device_ct)
        response = self.client.post(self.url('_add'), self.form_data([other, self.native_field]))
        self.assertEqual(response.status_code, 302)
        profile = CustomFieldProfile.objects.get()
        self.assertEqual(get_profile_fields(profile), [other, self.native_field])
        response = self.client.post(self.url('_edit', profile), self.data(field_mode='all'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(self.url('_edit', profile))
        self.assertEqual(response.context['form'].initial['selected_fields'], [other.pk, self.native_field.pk])
        self.assertContains(response, 'profile_fields.js')

    def remembered_data(self, fields, **extra):
        ids = [field.pk for field in fields]
        # The browser disables selected_fields in All mode, so only the explicit
        # remembered state and its ordering are submitted.
        return self.data(field_mode='all', remembered_fields=json.dumps(ids),
                         field_order=json.dumps(ids), **extra)

    def test_pending_manual_changes_survive_native_all_save_and_selected_reopen(self):
        second = CustomField.objects.create(name='pending_second', type='text')
        third = CustomField.objects.create(name='pending_third', type='text')
        for field in (second, third):
            field.object_types.add(self.device_ct)
        before = self.snapshot()
        for fields in ([second, self.native_field], [third, second, self.native_field], [second]):
            with self.subTest(fields=[field.name for field in fields]):
                profile = self.save_form(self.form_data([self.native_field, second]))
                response = self.client.post(self.url('_edit', profile), self.remembered_data(fields))
                self.assertEqual(response.status_code, 302)
                profile.refresh_from_db()
                self.assertEqual(profile.field_mode, 'all')
                self.assertEqual(list(profile.profile_fields.values_list('field_id', flat=True)),
                                 [field.pk for field in fields])
                self.assertEqual(get_profile_fields(profile), list(CustomField.objects.get_for_model(self.device)))
                response = self.client.get(self.url('_edit', profile))
                form = response.context['form']
                self.assertEqual(list(map(int, form['selected_fields'].value())), [field.pk for field in fields])
                self.assertEqual(json.loads(form['field_order'].value()), [field.pk for field in fields])
                self.assertEqual(json.loads(form['remembered_fields'].value()), [field.pk for field in fields])
                self.assertContains(self.client.get(profile.get_absolute_url()), 'Remembered selected fields')
                response = self.client.post(self.url('_edit', profile), self.form_data(fields))
                self.assertEqual(response.status_code, 302)
                profile.refresh_from_db()
                self.assertEqual(get_profile_fields(profile), fields)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_all_form_retains_pending_selection_order_and_recovers(self):
        second = CustomField.objects.create(name='pending_recovery', type='text')
        second.object_types.add(self.device_ct)
        profile = self.save_form(self.form_data([self.native_field]))
        pending = [second, self.native_field]
        response = self.client.post(self.url('_edit', profile), self.remembered_data(pending, title=''))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('title', form.errors)
        self.assertEqual(list(map(int, form['selected_fields'].value())), [field.pk for field in pending])
        self.assertEqual(json.loads(form['field_order'].value()), [field.pk for field in pending])
        self.assertEqual(json.loads(form['remembered_fields'].value()), [field.pk for field in pending])
        profile.refresh_from_db()
        self.assertEqual(profile.field_mode, 'selected')
        self.assertEqual(get_profile_fields(profile), [self.native_field])
        response = self.client.post(self.url('_edit', profile), self.remembered_data(pending))
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(list(profile.profile_fields.values_list('field_id', flat=True)),
                         [field.pk for field in pending])

    def test_invalid_all_remembered_state_rejected_without_aggregate_changes(self):
        second = CustomField.objects.create(name='valid_pending', type='text')
        second.object_types.add(self.device_ct)
        foreign = CustomField.objects.create(name='foreign_pending', type='text')
        foreign.object_types.add(ContentType.objects.get_for_model(Site))
        profile = self.save_form(self.form_data([self.native_field], device_roles=[self.device.role_id]))
        cases = [self.remembered_data([foreign]),
                 self.remembered_data([self.native_field, self.native_field]),
                 {**self.remembered_data([self.native_field]), 'remembered_fields': '[2147483647]'},
                 {**self.remembered_data([self.native_field]), 'remembered_fields': '[true]'},
                 {**self.remembered_data([self.native_field]), 'remembered_fields': '["1"]'},
                 {**self.remembered_data([self.native_field]), 'remembered_fields': '{}'},
                 {**self.remembered_data([self.native_field]), 'remembered_fields': 'broken'},
                 {**self.remembered_data([self.native_field]), 'field_order': '[]'},
                 {**self.remembered_data([self.native_field]), 'field_order': '[true]'},
                 {**self.remembered_data([self.native_field]), 'field_order': json.dumps([self.native_field.pk] * 2)},
                 {**self.remembered_data([self.native_field]), 'selected_fields': [second.pk]}]
        before = (list(CustomFieldProfile.objects.values()), list(ProfileField.objects.values()),
                  list(profile.device_roles.values_list('pk', flat=True)), self.snapshot())
        for data in cases:
            with self.subTest(data=data):
                response = self.client.post(self.url('_edit', profile), {**data, 'title': 'Must not save'})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertEqual((list(CustomFieldProfile.objects.values()), list(ProfileField.objects.values()),
                                  list(profile.device_roles.values_list('pk', flat=True)), self.snapshot()), before)

    def test_all_remembered_choices_use_native_permission_restrictions(self):
        profile = self.save_form(self.form_data([self.native_field]))
        user = get_user_model().objects.create_user('remembered-restricted', password='test-only')
        permission = ObjectPermission.objects.create(name='Remembered profile change', actions=['change'])
        permission.object_types.add(ContentType.objects.get_for_model(CustomFieldProfile))
        permission.users.add(user)
        self.client.force_login(user)
        response = self.client.post(self.url('_edit', profile), self.remembered_data([self.native_field]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('selected_fields', response.context['form'].errors)
        profile.refresh_from_db()
        self.assertEqual(profile.field_mode, 'selected')
        self.assertEqual(get_profile_fields(profile), [self.native_field])

    def test_all_explicit_empty_and_commit_false_membership_persistence(self):
        profile = self.save_form(self.form_data([self.native_field]))
        self.save_form(self.remembered_data([]), profile, commit=False)
        self.assertEqual(profile.profile_fields.count(), 0)
        self.assertEqual(get_profile_fields(profile), [self.native_field])
        second = CustomField.objects.create(name='deferred_pending', type='text')
        second.object_types.add(self.device_ct)
        form = CustomFieldProfileForm(data=self.remembered_data([second, self.native_field]), instance=profile)
        self.assertTrue(form.is_valid(), form.errors)
        obj = form.save(commit=False)
        self.assertEqual(profile.profile_fields.count(), 0)
        with transaction.atomic():
            obj.save()
            form.save_m2m()
        self.assertEqual(list(profile.profile_fields.values_list('field_id', flat=True)),
                         [second.pk, self.native_field.pk])

    def test_all_remembered_membership_write_failure_rolls_back_native_save(self):
        profile = self.save_form(self.form_data([self.native_field]))
        before = (list(CustomFieldProfile.objects.values()), list(ProfileField.objects.values()))
        with patch('netbox_custom_field_profiles.forms.ProfileField.objects.bulk_create',
                   side_effect=IntegrityError('injected remembered membership error')):
            with self.assertRaises(IntegrityError):
                self.client.post(self.url('_edit', profile), self.remembered_data([], title='Must roll back'))
        self.assertEqual((list(CustomFieldProfile.objects.values()), list(ProfileField.objects.values())), before)
