"""Edit Parameters through real native GET/POST routes and isolated storage."""
import time
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse
from dcim.models import Device, Site
from extras.models import CustomField, CustomFieldChoiceSet, Tag
from netbox_custom_field_profiles.models import CustomFieldProfile, ProfileField
from . import test_tracer, test_permissions


class ParameterEditingTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    grant = test_permissions.ProfilePermissionTests.grant
    aggregate = test_permissions.ProfilePermissionTests.aggregate

    def setUp(self):
        self.client.force_login(self.admin)
        self.profile = CustomFieldProfile.objects.create(
            title='Editable', content_type=self.device_ct, enabled=True, field_mode='selected')
        ProfileField.objects.create(profile=self.profile, field=self.native_field, position=0)
        self.url = reverse('dcim:device_edit_parameters', args=[self.device.pk])
        self.tab_url = reverse('dcim:device_custom_field_profiles', args=[self.device.pk])

    def field(self, name, kind='text', **kwargs):
        field = CustomField.objects.create(name=name, type=kind, **kwargs)
        field.object_types.add(self.device_ct)
        ProfileField.objects.create(profile=self.profile, field=field,
                                    position=self.profile.profile_fields.count())
        return field

    def payload(self, **values):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        return {'_parameter_scope': response.context['form']['_parameter_scope'].value(),
                'cf_tracer_value': 'edited native value', **values}

    def values(self):
        self.device.refresh_from_db()
        return self.device.custom_field_data

    def test_native_save_deduplicates_and_preserves_all_unrelated_state(self):
        repeated = CustomFieldProfile.objects.create(
            title='Repeated', content_type=self.device_ct, enabled=True, field_mode='selected')
        ProfileField.objects.create(profile=repeated, field=self.native_field, position=0)
        excluded = CustomField.objects.create(name='excluded', type='text')
        excluded.object_types.add(self.device_ct)
        self.device.custom_field_data.update(excluded='keep', unknown={'nested': [False, 0]})
        self.device.save()
        tag = Tag.objects.create(name='Retain', slug='retain')
        self.device.tags.add(tag)
        config = self.aggregate()
        definitions = list(CustomField.objects.values().order_by('pk'))
        response = self.client.get(self.url)
        self.assertContains(response, 'name="cf_tracer_value"', count=1)
        self.assertNotIn('tags', response.context['form'].fields)
        response = self.client.post(self.url, self.payload(
            cf_excluded='forged', name='forged', tags=[], custom_field_data='{}',
            return_url='https://example.com/'))
        self.assertRedirects(response, self.tab_url, fetch_redirect_response=False)
        self.assertEqual(self.values(), {'tracer_value': 'edited native value',
                                       'excluded': 'keep', 'unknown': {'nested': [False, 0]}})
        self.assertEqual(self.device.name, 'Tracer device')
        self.assertEqual(list(self.device.tags.all()), [tag])
        self.assertEqual(self.aggregate(), config)
        self.assertEqual(list(CustomField.objects.values().order_by('pk')), definitions)
        self.assertContains(self.client.get(self.tab_url), 'edited native value', count=2)
        from core.models import ObjectChange
        self.assertTrue(ObjectChange.objects.filter(changed_object_id=self.device.pk,
            changed_object_type=self.device_ct, action='update').exists())

    def test_invalid_required_integer_regex_choice_and_json_do_not_save(self):
        self.field('required_text', required=True)
        self.field('number', 'integer', validation_minimum=2, validation_maximum=9)
        self.field('pattern', validation_regex='^ok$')
        choices = CustomFieldChoiceSet.objects.create(name='Edit choices', extra_choices=[['a', 'Alpha']])
        self.field('choice', 'select', choice_set=choices)
        self.field('json_data', 'json')
        valid = dict(cf_required_text='set', cf_number='3', cf_pattern='ok', cf_choice='a', cf_json_data='{}')
        before = self.values().copy()
        for name, bad in [('cf_required_text', ''), ('cf_number', 'bad'), ('cf_number', '10'),
                          ('cf_pattern', 'wrong'), ('cf_choice', 'forged'), ('cf_json_data', '{broken')]:
            with self.subTest(name=name, bad=bad):
                response = self.client.post(self.url, self.payload(**{**valid, name: bad}))
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertEqual(self.values(), before)

    def test_native_types_serialize_and_clear(self):
        choices = CustomFieldChoiceSet.objects.create(name='Typed choices',
            extra_choices=[['a', 'Alpha'], ['b', 'Beta']])
        for name, kind, extra in [('number', 'integer', {}), ('decimal', 'decimal', {}),
                ('flag', 'boolean', {}), ('day', 'date', {}), ('when', 'datetime', {}),
                ('url', 'url', {}), ('notes', 'longtext', {}), ('json_data', 'json', {}),
                ('choice', 'select', {'choice_set': choices}),
                ('choices', 'multiselect', {'choice_set': choices}),
                ('site', 'object', {'related_object_type': ContentType.objects.get_for_model(Site)}),
                ('sites', 'multiobject', {'related_object_type': ContentType.objects.get_for_model(Site)})]:
            self.field(name, kind, **extra)
        response = self.client.post(self.url, self.payload(cf_number='0', cf_decimal='1.2500',
            cf_flag='False', cf_day='2026-11-10', cf_when='2026-11-10 12:30:00',
            cf_url='https://example.com/a', cf_notes='first\nsecond', cf_json_data='{"a":[false,0]}',
            cf_choice='a', cf_choices=['a', 'b'], cf_site=self.device.site_id, cf_sites=[self.device.site_id]))
        self.assertEqual(response.status_code, 302, getattr(response, 'context', None) and response.context['form'].errors)
        values = self.values()
        self.assertEqual(values['number'], 0)
        self.assertEqual(values['flag'], False)
        self.assertEqual(values['json_data'], {'a': [False, 0]})
        self.assertEqual(values['choices'], ['a', 'b'])
        self.assertEqual(values['site'], self.device.site_id)
        self.assertEqual(values['sites'], [self.device.site_id])
        response = self.client.post(self.url, self.payload(cf_tracer_value=''))
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(self.values()['tracer_value'])

    def test_hidden_and_readonly_fields_preserve_values_against_forged_inputs(self):
        self.field('hidden', ui_editable='hidden')
        self.field('readonly', ui_editable='no')
        self.device.custom_field_data.update(hidden='private', readonly='retained')
        self.device.save()
        response = self.client.get(self.url)
        self.assertNotContains(response, 'name="cf_hidden"')
        self.assertNotContains(response, 'name="cf_readonly"')
        self.assertEqual(self.client.post(self.url, self.payload(cf_hidden='forged', cf_readonly='forged')).status_code, 302)
        self.assertEqual(self.values()['hidden'], 'private')
        self.assertEqual(self.values()['readonly'], 'retained')

    def test_changed_membership_rejects_stale_form_and_dynamic_all_refreshes(self):
        data = self.payload()
        self.field('added')
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'available parameters changed')
        self.assertEqual(self.values()['tracer_value'], 'external value')
        self.profile.field_mode = 'all'
        self.profile.save()
        new = CustomField.objects.create(name='new_dynamic', type='text')
        new.object_types.add(self.device_ct)
        self.assertContains(self.client.get(self.url), 'name="cf_new_dynamic"')

    def test_changed_native_definition_and_tampered_scope_reject(self):
        for change in ('definition', 'signature'):
            data = self.payload()
            if change == 'definition':
                self.native_field.description = 'changed'
                self.native_field.save()
            else:
                data['_parameter_scope'] += 'tampered'
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
            self.assertEqual(self.values()['tracer_value'], 'external value')

    def test_no_match_or_no_editable_fields_has_no_save_and_post_preserves(self):
        data = self.payload()
        for mode in ('disabled', 'hidden'):
            self.profile.enabled = mode != 'disabled'
            self.profile.save()
            if mode == 'hidden':
                self.native_field.ui_editable = 'hidden'
                self.native_field.save()
            self.assertNotContains(self.client.get(self.tab_url), 'Edit Parameters')
            response = self.client.get(self.url)
            self.assertContains(response, 'No editable parameters are available')
            self.assertNotContains(response, 'name="_update"')
            self.assertEqual(self.client.post(self.url, data).status_code, 200)
            self.assertEqual(self.values()['tracer_value'], 'external value')

    def test_native_stale_timestamp_blocks_save_and_fresh_post_preserves_external_values(self):
        data = self.payload(_init_time=str(time.time() - 3600))
        self.device.custom_field_data['external_key'] = 'fresh external write'
        self.device.save()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertEqual(self.values()['tracer_value'], 'external value')
        self.assertEqual(self.client.post(self.url, self.payload()).status_code, 302)
        self.assertEqual(self.values()['external_key'], 'fresh external write')

    def test_native_permissions_constrain_get_post_and_action_without_profile_grants(self):
        data = self.payload()
        for name, actions, constraints, status in [
                ('viewer', ['view'], None, 403), ('denied', [], None, 403),
                ('constrained', ['view', 'change'], {'pk': 2147483647}, 404),
                ('editor', ['view', 'change'], None, 200)]:
            user = get_user_model().objects.create_user(name, password='test-only')
            if actions:
                self.grant(user, actions, model=Device, constraints=constraints)
            self.client.force_login(user)
            before = self.values().copy()
            self.assertEqual(self.client.get(self.url).status_code, status)
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, 302 if status == 200 else status)
            if status != 200:
                self.assertEqual(self.values(), before)
            if status != 404 and 'view' in actions:
                tab = self.client.get(self.tab_url)
                self.assertEqual('Edit Parameters' in tab.content.decode(), status == 200)

    def test_reference_choices_reject_denied_targets_and_preserve_inaccessible_current_values(self):
        self.field('reference', 'object', related_object_type=ContentType.objects.get_for_model(Site))
        user = get_user_model().objects.create_user('reference-editor', password='test-only')
        self.grant(user, ['view', 'change'], model=Device)
        self.client.force_login(user)
        response = self.client.post(self.url, self.payload(cf_reference=self.device.site_id))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cf_reference', response.context['form'].errors)
        self.assertNotIn('reference', self.values())
        self.device.custom_field_data['reference'] = self.device.site_id
        self.device.save()
        response = self.client.get(self.url)
        self.assertNotContains(response, 'name="cf_reference"')
        self.assertEqual(self.client.post(self.url, self.payload(cf_reference='')).status_code, 302)
        self.assertEqual(self.values()['reference'], self.device.site_id)

    def test_csrf_and_anonymous_posts_do_not_save(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        self.assertEqual(client.post(self.url, self.payload()).status_code, 403)
        self.client.logout()
        self.assertIn(self.client.post(self.url, {}).status_code, (302, 403))
        self.assertEqual(self.values()['tracer_value'], 'external value')

    def test_post_save_permission_constraint_rolls_back_native_values(self):
        user = get_user_model().objects.create_user('value-constrained', password='test-only')
        self.grant(user, ['view', 'change'], model=Device,
                   constraints={'custom_field_data__tracer_value': 'external value'})
        self.client.force_login(user)
        response = self.client.post(self.url, self.payload())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertEqual(self.values()['tracer_value'], 'external value')

    def test_unique_native_value_rejects_duplicate(self):
        self.native_field.unique = True
        self.native_field.save()
        Device.objects.create(name='Other device', device_type=self.device.device_type,
            site=self.device.site, role=self.device.role, custom_field_data={'tracer_value': 'taken'})
        response = self.client.post(self.url, self.payload(cf_tracer_value='taken'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(self.values()['tracer_value'], 'external value')

    def test_quickadd_and_clone_flags_cannot_expose_unrelated_values(self):
        response = self.client.get(self.url + '?_quickadd=1')
        self.assertContains(response, 'Edit Parameters:')
        response = self.client.post(self.url + '?_quickadd=1', self.payload(_addanother='1'))
        self.assertRedirects(response, self.tab_url, fetch_redirect_response=False)

    def test_multiobject_reference_constraints_reject_or_preserve_complete_saved_set(self):
        self.field('references', 'multiobject', related_object_type=ContentType.objects.get_for_model(Site))
        denied = Site.objects.create(name='Denied site', slug='denied-site')
        user = get_user_model().objects.create_user('multi-editor', password='test-only')
        self.grant(user, ['view', 'change'], model=Device)
        self.grant(user, ['view'], model=Site, constraints={'pk': self.device.site_id})
        self.client.force_login(user)
        response = self.client.post(self.url, self.payload(cf_references=[self.device.site_id, denied.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('cf_references', response.context['form'].errors)
        self.device.custom_field_data['references'] = [self.device.site_id, denied.pk]
        self.device.save()
        response = self.client.get(self.url)
        self.assertNotContains(response, 'name="cf_references"')
        self.assertNotContains(response, denied.name)
        self.assertEqual(self.client.post(self.url, self.payload(cf_references=[])).status_code, 302)
        self.assertEqual(self.values()['references'], [self.device.site_id, denied.pk])
