"""Real-response contracts for all native custom-field types and empty values."""
import re
from html.parser import HTMLParser
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType
from django.template import Context, Template
from django.test import TestCase
from dcim.models import Device, Site
from extras.choices import CustomFieldTypeChoices, CustomFieldUIVisibleChoices
from extras.models import CustomField, CustomFieldChoiceSet
from utilities.templatetags.builtins.tags import url_scheme_is_allowed

from . import test_parameters, test_tracer


class ParametersHTML(HTMLParser):
    """Inspect executable markup and visible text only inside Parameters."""
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.elements = []
        self.links = []
        self.text = []
        self.anchor = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div' and (self.depth or attrs.get('id') == 'device-parameters'):
            self.depth += 1
        if self.depth:
            self.elements.append((tag, attrs))
            if tag == 'a':
                self.anchor = [attrs.get('href'), '']
                self.links.append(self.anchor)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.anchor = None
        if tag == 'div' and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)
            if self.anchor is not None:
                self.anchor[1] += data


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
        self.assertIn('<button', rows[0])
        self.assertIn('type="button"', rows[0])
        self.assertIn('data-bs-trigger="hover focus"', rows[0])
        self.assertIn('aria-label="&lt;script&gt;help&lt;/script&gt; &quot;quoted&quot;"', rows[0])
        self.assertIn('&lt;b&gt;Native label&lt;/b&gt;', rows[1])
        self.assertNotIn('<script>', ''.join(rows))

    def test_full_url_text_and_runtime_configured_scheme_policy(self):
        field = self.field('full_url', 'url')
        self.create_profile('Full URLs', [field])
        long_url = 'https://example.test/' + 'long-segment/' * 16 + '?a=1&b="quoted"'
        values = (long_url, 'custom-safe:resource?x=1&y=2', '/relative/path?a=1&b=2',
                  'javascript:alert(1)', 'data:text/html,<script>alert(1)</script>',
                  'vbscript:msgbox(1)', 'https://example.test/blocked-by-config')
        for value in values:
            # Model validation would reject unsafe legacy/script-written data.
            Device.objects.filter(pk=self.device.pk).update(custom_field_data={field.name: value})
            schemes = ['custom-safe'] if value.endswith('blocked-by-config') else ['https', 'custom-safe']
            with self.subTest(value=value), patch(
                    url_scheme_is_allowed.__module__ + '.get_config',
                    return_value=SimpleNamespace(ALLOWED_URL_SCHEMES=schemes)):
                permitted = url_scheme_is_allowed(value)
                response = self.parameter_response()
                parsed = ParametersHTML(response.content.decode())
                if permitted:
                    self.assertIn([value, value], parsed.links)
                else:
                    self.assertFalse(parsed.links)
                    self.assertIn(value, ''.join(parsed.text))

    def test_full_multiline_markdown_and_json_have_scoped_readable_containers(self):
        longtext = self.field('full_multiline', 'longtext')
        json_field = self.field('full_nested_json', 'json')
        self.create_profile('Long values', [longtext, json_field])
        self.create_profile('Repeated long values', [longtext, json_field])
        text = '**Start of text**\nsingle line break\n' + 'unbroken-word' * 160 + '\nFinal line'
        payload = {'nested': {'items': ['wide-value' * 140, {'unsafe': '<script>json()</script>'}]}}
        self.save_values({longtext.name: text, json_field.name: payload})
        response = self.parameter_response()
        rows = self.rows(response)
        self.assertEqual(rows[:2], rows[2:])
        self.assertIn('<strong>Start of text</strong>\nsingle line break\n', rows[0])
        self.assertIn('unbroken-word' * 160, rows[0])
        self.assertIn('Final line', rows[0])
        self.assertIn('wide-value' * 140, rows[1])
        self.assertIn('&lt;script&gt;json()&lt;/script&gt;', rows[1])
        html = response.content.decode()
        for rule in ('#device-parameters .rendered-markdown', 'white-space: pre-wrap',
                     '#device-parameters pre', 'overflow-x: auto',
                     'table-layout: fixed', 'overflow-wrap: anywhere'):
            self.assertTrue(rule in html, 'Missing Parameters layout rule: ' + rule)

    def test_hostile_stored_metadata_and_values_cannot_create_executable_dom(self):
        payload = '<script>storedAttack()</script><img src=x onerror="storedAttack()">'
        fields = [self.field('hostile_' + kind, kind, label='<img src=x onerror=alert(1)>',
                             description='\" onmouseover=\"storedAttack() ' + payload)
                  for kind in ('text', 'longtext', 'json', 'url')]
        self.create_profile(payload, fields)
        Device.objects.filter(pk=self.device.pk).update(custom_field_data={
            fields[0].name: payload,
            fields[1].name: payload + '\n[unsafe](javascript:storedAttack())\n**Safe emphasis**',
            fields[2].name: {'attack': payload},
            fields[3].name: 'javascript:storedAttack()\" onmouseover=\"storedAttack()',
        })
        response = self.parameter_response()
        parsed = ParametersHTML(response.content.decode())
        self.assertTrue(parsed.elements)
        self.assertIn(payload, ''.join(parsed.text))  # safely escaped text remains readable
        self.assertIn('Safe emphasis', ''.join(parsed.text))
        for tag, attrs in parsed.elements:
            self.assertNotIn(tag, ('script', 'iframe', 'object', 'embed', 'svg'))
            self.assertFalse(any(name.lower().startswith('on') for name in attrs), (tag, attrs))
            self.assertNotIn('srcdoc', attrs)
            for name in ('href', 'src'):
                if name in attrs:
                    self.assertNotRegex(attrs[name].lower().lstrip(), r'^(javascript|data|vbscript):')
