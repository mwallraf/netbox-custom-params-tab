"""Real-response contracts for all native custom-field types and empty values."""
import re
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template
from django.test import TestCase
from dcim.models import Device, Site
from extras.choices import CustomFieldTypeChoices, CustomFieldUIVisibleChoices
from extras.models import CustomField, CustomFieldChoiceSet

from . import test_parameters, test_tracer


class ParameterRenderingTests(TestCase):
    setUpTestData = classmethod(test_tracer.ProfileTracerTests.setUpTestData.__func__)
    parameter_url = test_parameters.ParametersTabTests.parameter_url
    parameter_response = test_parameters.ParametersTabTests.parameter_response
    create_profile = test_parameters.ParametersTabTests.create_profile

    def setUp(self):
        self.client.force_login(self.admin)

    def field(self, name, field_type, **kwargs):
        if field_type in ('object', 'multiobject'):
            kwargs['related_object_type'] = ContentType.objects.get_for_model(Site)
        if field_type in ('select', 'multiselect'):
            kwargs['choice_set'], _ = CustomFieldChoiceSet.objects.get_or_create(
                name='Rendering choices', defaults={
                    'extra_choices': [['stored-a', 'Friendly alpha'], ['stored-b', 'Friendly beta']],
                    'choice_colors': {'stored-a': 'blue'}})
        field = CustomField.objects.create(name=name, type=field_type, **kwargs)
        field.object_types.add(self.device_ct)
        return field

    def save_values(self, values):
        self.device.custom_field_data = values
        self.device.full_clean()
        self.device.save()

    def rows(self, response):
        content = response.content.decode().split('<div id="device-parameters">', 1)[1]
        return re.findall(r'<tr>\s*<th.*?</tr>', content, re.S)

    def native_snapshot(self):
        return (list(CustomField.objects.order_by('pk').values()),
                list(CustomField.object_types.through.objects.order_by('pk').values()),
                list(Device.objects.order_by('pk').values('pk', 'custom_field_data')))

    def test_all_thirteen_types_preserve_native_formatting_and_repeat_identically(self):
        cases = [
            ('text', 'plain text', 'plain text'),
            ('longtext', '**Full Markdown**', '<strong>Full Markdown</strong>'),
            ('integer', 0, '0'), ('decimal', 0.0, '0.0'),
            ('boolean', False, 'False'), ('date', '2026-11-07', '2026-11-07'),
            ('datetime', '2026-11-07T14:30:00+00:00', '2026-11-07'),
            ('url', 'https://example.test/native', 'href="https://example.test/native"'),
            ('json', {'answer': 0}, '&quot;answer&quot;'),
            ('select', 'stored-a', 'Friendly alpha'),
            ('multiselect', ['stored-a', 'stored-b'], 'Friendly beta'),
            ('object', self.device.site_id, self.device.site.get_absolute_url()),
            ('multiobject', [self.device.site_id], self.device.site.get_absolute_url()),
        ]
        self.assertEqual({c[0] for c in cases}, set(CustomFieldTypeChoices.values()))
        fields = [self.field('matrix_' + kind, kind) for kind, _, _ in cases]
        self.create_profile('First matrix', fields)
        self.create_profile('Second matrix', fields)
        self.save_values({field.name: value for field, (_, value, _) in zip(fields, cases)})
        before = self.native_snapshot()
        # Any attempt to deserialize raw reference IDs must fail this request.
        original = CustomField.deserialize
        def guarded(field, value):
            self.assertNotIn(field.type, ('object', 'multiobject'))
            return original(field, value)
        with patch.object(CustomField, 'deserialize', guarded):
            response = self.parameter_response()
        rows = self.rows(response)
        self.assertEqual(len(rows), 26)
        sections = response.context['sections']
        for index, (field, (_, _, expected)) in enumerate(zip(fields, cases)):
            with self.subTest(field_type=field.type):
                self.assertIn(expected, rows[index])
                self.assertNotIn('Not set', rows[index])
                self.assertEqual(rows[index], rows[index + 13])
                # Compare against the actual installed native formatting contract.
                native = Template('{% customfield_value field value %}').render(Context({
                    'field': field, 'value': sections[0].rows[index].value}))
                self.assertIn(native.strip(), rows[index])
        self.assertEqual(self.native_snapshot(), before)

    def test_type_specific_unset_and_meaningful_json_false_like_values(self):
        cases = [('text', ''), ('longtext', ''), ('url', ''), ('select', ''),
                 ('multiselect', []), ('multiobject', [])]
        fields = [self.field('empty_' + kind, kind) for kind, _ in cases]
        missing = self.field('missing_key', 'text')
        null = self.field('null_value', 'integer')
        self.create_profile('Unset fields', fields + [missing, null])
        self.save_values({**{f.name: value for f, (_, value) in zip(fields, cases)}, null.name: None})
        self.assertContains(self.parameter_response(), '<span class="text-muted">Not set</span>', count=8)
        for value in ({}, [], False, 0, ''):
            with self.subTest(json=value):
                json_field, _ = CustomField.objects.get_or_create(name='json_false_like', defaults={'type': 'json'})
                json_field.object_types.add(self.device_ct)
                if not json_field.field_profiles.exists():
                    self.create_profile('JSON value', [json_field])
                self.save_values({'json_false_like': value})
                response = self.parameter_response()
                json_row = next(row for row in self.rows(response) if 'json_false_like' in row)
                self.assertIn('<pre>', json_row)
                self.assertNotIn('Not set', json_row)
                self.assertFalse(response.context['sections'][0].rows[0].is_unset)

    def test_missing_and_null_are_unset_for_every_native_type(self):
        fields = [self.field('nullable_' + kind, kind) for kind in CustomFieldTypeChoices.values()]
        self.create_profile('Missing and null', fields)
        for values in ({}, {field.name: None for field in fields}):
            with self.subTest(values=values):
                self.save_values(values)
                before = self.native_snapshot()
                response = self.parameter_response()
                self.assertEqual(len(self.rows(response)), 13)
                self.assertContains(response, '<span class="text-muted">Not set</span>', count=13)
                self.assertEqual(self.native_snapshot(), before)

    def test_all_visibility_modes_keep_relevant_unset_rows_and_native_settings(self):
        fields = [self.field('visibility_' + str(mode), 'text', ui_visible=mode)
                  for mode in CustomFieldUIVisibleChoices.values()]
        self.create_profile('Every presentation mode', fields)
        for values in ({}, {field.name: 'Visible native value' for field in fields}):
            with self.subTest(values=values):
                self.save_values(values)
                before = self.native_snapshot()
                response = self.parameter_response()
                self.assertEqual(len(self.rows(response)), len(fields))
                self.assertContains(response, 'Visible native value' if values else 'Not set', count=len(fields))
                self.assertEqual(self.native_snapshot(), before)

    def test_exact_name_fallback_escaped_label_and_secondary_native_help(self):
        raw = self.field('raw_internal_name', 'text', description='<script>help</script> "quoted"')
        labeled = self.field('labeled_field', 'text', label='<b>Native label</b>')
        self.create_profile('Metadata', [raw, labeled])
        response = self.parameter_response()
        rows = self.rows(response)
        self.assertIn('raw_internal_name', rows[0])
        self.assertNotIn('Raw internal name', rows[0])
        self.assertIn('title="&lt;script&gt;help&lt;/script&gt; &quot;quoted&quot;"', rows[0])
        self.assertIn('data-bs-toggle="tooltip"', rows[0])
        self.assertIn('&lt;b&gt;Native label&lt;/b&gt;', rows[1])
        self.assertNotIn('<script>', ''.join(rows))
