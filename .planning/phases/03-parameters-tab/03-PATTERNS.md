# Phase 03: Parameters tab — Pattern Map

**Mapped:** 2026-11-07  
**Files classified:** 12 proposed create/modify targets  
**Analogs:** 10 role matches, 2 without a close tracked analog; no exact Device-tab implementation exists.

Scope comes from 03-CONTEXT.md D-01–D-15 and 03-RESEARCH.md proposed files. Paths below are relative to the canonical repository root. All named existing analogs were verified in `git ls-files`; no recovery tree, installed runtime mirror, or stale codebase-map path is an edit target. Proposed filenames remain planner discretion.

## File Classification

| New/modified file | Role | Data flow | Closest tracked analog | Match |
|---|---|---|---|---|
| `netbox_custom_field_profiles/views.py` | controller | request-response | same file, CustomFieldProfileView | role-match |
| `netbox_custom_field_profiles/__init__.py` | config | event-driven | same file, ready | role-match |
| `netbox_custom_field_profiles/presentation.py` | service | transform | `netbox_custom_field_profiles/matching.py` | role-match |
| `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/device_parameters.html` | component | transform | `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html` | role-match |
| `netbox_custom_field_profiles/templatetags/parameter_tags.py` | utility | transform | `netbox_custom_field_profiles/templatetags/customtab_tags.py` | role-match |
| `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/parameter_value.html` | component | transform | none; native renderer documented in research | none |
| `netbox_custom_field_profiles/tests/test_parameters.py` | test | request-response | `netbox_custom_field_profiles/tests/test_tracer.py` | role-match |
| `netbox_custom_field_profiles/tests/test_parameter_rendering.py` | test | request-response | `netbox_custom_field_profiles/tests/test_tracer.py` | role-match |
| `netbox_custom_field_profiles/tests/test_parameter_permissions.py` | test | request-response | `netbox_custom_field_profiles/tests/test_permissions.py` | role-match |
| `docs/development/profiles.md` | utility (documentation) | file-I/O | same file | role-match |
| `README.md` | utility (documentation) | file-I/O | `docs/development/profiles.md` | role-match |
| `CLAUDE.md` | config (developer documentation) | file-I/O | none; update current capability boundary directly | none |

`matching.py`, models, signals, `urls.py`, inert `template_content.py`, test runner and packaging are reuse/verification dependencies, not necessary change targets. If a separate CSS file is chosen, add it explicitly to package data; existing template/JS packaging does not include CSS. Prefer existing utilities or scoped template styling for this bounded phase.

## Pattern Assignments

### Native view: `views.py`

**Analog:** `netbox_custom_field_profiles/views.py:1-4,13-15`:

```python
from netbox.views.generic import ObjectListView, ObjectView, ObjectEditView, ObjectDeleteView
from .models import CustomFieldProfile
from .tables import CustomFieldProfileTable
from .forms import CustomFieldProfileForm

class CustomFieldProfileView(ObjectView):
    queryset = CustomFieldProfile.objects.select_related('content_type')
    template_name = 'netbox_custom_field_profiles/customfieldprofile.html'
```

Copy native generic-view inheritance, queryset and namespaced template convention. Use a **Device** queryset for the new view so native action/constraint enforcement derives Device authority. Add `register_model_view`/`ViewTab` using the research Code Examples and runtime evidence; these have no tracked local analog. Build section context only after native object authorization. Tab visibility checks matching enabled profiles, never field count/value truthiness. An authorized direct no-match visit still renders the normal Device shell. Do not require profile-management or CustomField-definition permission. Native generic handling owns permission/404 errors; do not add manual object lookup or exception swallowing. Keep the destination read-only, with unsupported POST and no edit control.

### Early registration: `__init__.py`

**Analog:** `netbox_custom_field_profiles/__init__.py:13-16`:

```python
    def ready(self):
        super().ready()
        from . import signals
        signals.register()
```

Import the decorated view module after this existing initialization. Research establishes that importing solely from plugin URLs is too late for core Device URL materialization. Preserve signal registration. Prove fresh-process reverse/resolve and actual Device navigation after restart; an already-imported test helper does not prove startup timing.

### Presentation service: `presentation.py`

**Analog:** `netbox_custom_field_profiles/matching.py:1-6,9-15,40-56`. Copy the small read-only helper boundary and native imports/local relative imports:

```python
from dcim.models import Device
from extras.choices import CustomFieldStatusChoices
from extras.models import CustomField

from .models import CustomFieldProfile

def get_matching_profiles(device):
    """AND between configured criteria, OR within each, in profile order."""
    if not isinstance(device, Device):
        return []
    candidates = CustomFieldProfile.objects.filter(
        enabled=True, content_type__app_label='dcim', content_type__model='device',
    ).prefetch_related('device_types', 'device_roles', 'applicability_tags')
```

Call the existing helpers rather than copying/reimplementing their matching logic. Field resolution already preserves active/applicable authority and selection order (`matching.py:46-56`):

```python
    database = profile._state.db or 'default'
    live_ids = set(CustomField.objects.using(database).filter(
        object_types__app_label='dcim', object_types__model='device',
        status=CustomFieldStatusChoices.STATUS_ACTIVE,
    ).values_list('pk', flat=True))
    native = [field for field in CustomField.objects.db_manager(database).get_for_model(Device)
              if field.pk in live_ids]
    if profile.field_mode == CustomFieldProfile.FIELD_MODE_ALL:
        return native
    active = {field.pk: field for field in native}
    return [active[entry.field_id] for entry in profile.profile_fields.all() if entry.field_id in active]
```

Read `device.custom_field_data.get(field.name)` afresh per request. Preserve duplicate profile sections and repeated fields; cache resolved duplicate values only within the authorized request. Keep matching empty sections. Do not use native grouped-field selection, which would reapply detail-page visibility. Follow research Type and Empty-Value Contract: false/zero and JSON empty containers are values; absent/null and type-specific empties use `Not set`.

No local analog supplies secure object-reference presentation: use native `.restrict(user, 'view')` before formatting referenced objects. Denied references receive neutral unavailable text without IDs, labels, links or hidden counts. Mixed collections may show permitted references. Do not pass unrestricted deserializer output directly to linkification. Research contains the verified native source/probe evidence; installed runtime paths are not repository analogs or edit targets.

### Device template and value adapter

**Card/escaping analog:** `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html:1-5,17-20`:

```django
{% extends 'generic/object.html' %}
{% block content %}
<div class="card"><h2 class="card-header">Profile configuration</h2><div class="card-body">
  <dl><dt>Title</dt><dd>{{ object.title }}</dd><dt>Field selection</dt><dd>{{ object.get_field_mode_display }}</dd>
```

Copy native card classes and default escaping, but extend the **native Device base** specified by research rather than this profile object's base. Stack full-width cards with label/value rows, preserve duplicate headings and use `field.label|default:field.name`. Use escaped native help tooltip conventions from research. Render distinct no-match and matching-zero-fields messages. No `safe` on stored labels/help/values.

**Tag-module analog:** `netbox_custom_field_profiles/templatetags/customtab_tags.py:1-11`:

```python
from django import template

register = template.Library()

@register.filter
def dict_value(d, key):
    """Look up key in a dict; returns None if missing or d is not a dict."""
    if isinstance(d, dict):
        return d.get(key)
    return None
```

Copy module registration/import conventions only. There is no current secure native value adapter to copy. Delegate ordinary values to native `customfield_value`; retain native choice colors/labels, Markdown sanitation and JSON escaping. The new value partial handles explicit unset/unavailable states and full URL text using native URL scheme safety. Preserve long-text line breaks without bypassing Markdown sanitization. Constrain JSON overflow locally and verify desktop/narrow wrapping in a browser. Use 03-RESEARCH.md Code Examples and runtime findings for these absent local patterns.

### Native integration/rendering tests

**Analog:** `netbox_custom_field_profiles/tests/test_tracer.py:1-26,28-33` supplies imports, native TestCase, Device fixtures, applicable native field and real client login/reverse conventions:

```python
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase
from django.urls import reverse

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from extras.models import CustomField
from users.models import ObjectPermission
```

```python
        cls.device = Device.objects.create(name='Tracer device', device_type=hardware, role=role, site=site,
                                          custom_field_data={'tracer_value': 'external value'})
        cls.native_field = CustomField.objects.create(name='tracer_value', type='text')
        cls.native_field.object_types.add(cls.device_ct)
```

Reuse fixtures without inheriting unrelated test methods. `test_tracer.py:80-84` demonstrates escaped rendered-response assertions:

```python
    def test_empty_list_and_escaped_titles(self):
        response = self.client.get(self.url('_list'))
        self.assertEqual(response.status_code, 200)
        profile = CustomFieldProfile.objects.create(title='<script>bad()</script>', content_type=self.device_ct)
        self.assertContains(self.client.get(profile.get_absolute_url()), '&lt;script&gt;bad()&lt;/script&gt;')
```

For `test_parameters.py`, assert native navigation/active tab, reverse/resolve, ordering, CMTS/CPE/shared matches, disabled/no-match/empty-section states and external writes visible next request. For `test_parameter_rendering.py`, extend real-response assertions to all 13 native types, false/zero/JSON empties, labels/help, duplicates, Markdown/XSS, unsafe and full-length URLs. Server HTML checks supplement actual visual evidence rather than replacing it.

### Permission/preservation tests

**Analog:** `netbox_custom_field_profiles/tests/test_permissions.py:17-32`:

```python
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
```

Set `model=Device` explicitly; the default above is profile administration authority. Test Device-only viewer, profile-admin-without-Device-access, constrained allowed/denied Devices, and constrained related references using authenticated users. Include no-match direct URL authorization and forged POST. Snapshot Device/native definitions and complete plugin aggregate before/after requests; `test_permissions.py:43-47` includes profile memberships and rule through tables in its aggregate. The tracer's `snapshot()` (`test_tracer.py:39-41`) shows the native-value snapshot shape:

```python
    def snapshot(self):
        return (list(CustomField.objects.values().order_by('pk')),
                list(Device.objects.values('pk', 'custom_field_data').order_by('pk')))
```

### Documentation targets

**Analog:** `docs/development/profiles.md:3-6,15-20,100-120` documents runtime version, actual capability boundary, native authority and repeatable isolated commands. Update this guide with tab visibility, both empty states, type-aware unset semantics, native value freshness and Device/reference access. Update README/CLAUDE capability statements consistently; editing remains Phase 4. Existing pending-browser language is stale relative to current STATE; cite actual new evidence and do not copy obsolete status claims. Do not rewrite agreed requirements as implementation status.

## Shared Patterns

- **Native authorization/error handling:** use ObjectView and native constrained querysets; no plugin-specific authorization scheme or profile-permission substitute. Match visibility and authority remain distinct.
- **Read-only resolution:** reuse `matching.py` helpers without writing definitions, values or profile configuration; do not change lifecycle/filter semantics.
- **Escaping:** plain text plus template autoescape; native renderer/sanitizers own typed formatting. Adapter adds the missing reference guard and agreed presentation details only.
- **Isolation:** existing `netbox_custom_field_profiles/tests/runner.py:6-25` rejects empty suites, requires PostgreSQL and verifies a separate test database. Keep it unchanged and run new modules through `python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameters` (or the other new labels), then `make test-profiles` and final `make test`. No live reset for feature tests; coordinate service restart outside test runs.
- **No panel regression:** retain inert `template_content.py`; existing `tests/test_preservation.py:151-156` GETs `dcim:device` and asserts retired `tab_panel.html` was not used. Extend that regression alongside the new tab.

## No Analog Found

| Responsibility | Reason / planner source |
|---|---|
| Native Device registry/ViewTab and cold-start URL registration | Existing root views are profile CRUD only. Use 03-RESEARCH.md Architecture Patterns/Code Examples and verify a fresh process. |
| Secure typed value partial/reference adapter | Existing dict lookup tag is only a module-shape analog. Use research's verified native formatter, restriction, URL safety and unset contract. |
| CLAUDE capability status update | Direct documentation correction; no source-code pattern needed. |

## Metadata

**Search scope:** tracked root plugin, its native tests/templates, scripts and current documentation. Five primary pattern families: ObjectView, ready initialization, read-only resolver, native card/tag structure, native request/permission tests. Supplemental runner/preservation/docs evidence is identified above. No runtime probes or tests were performed during mapping. No production/configuration files were changed. Only this pattern map was written.
