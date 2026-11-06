# Phase 2: Profile administration and matching — Pattern Map

**Mapped:** 2026-11-06
**Scope:** Current canonical repository root; Phase 2 only.
**Status:** Planning guidance, not implementation evidence.

All repository analogs below were verified present in `git ls-files`. Old codebase maps and `.recovery` are not analog sources. Neither `.agents/skills` nor `.codex/skills` exists in this project. Read `docs/REQUIREMENTS.md` and `02-CONTEXT.md` before applying excerpts: retained source expresses the superseded panel design in several places.

## File Classification

Paths for new modules/templates/tests are proposals; the planner may choose consistent names.

| New/modified file | Role | Data flow | Closest tracked analog | Match quality |
|---|---|---|---|---|
| `netbox_custom_field_profiles/models.py` | model | CRUD | same file, lines 8–32 and 52–67 | role match; replace singular semantics |
| `netbox_custom_field_profiles/forms.py` | model/form | request-response, CRUD | same file, lines 34–55 | role match; replace choices and aggregate save |
| `netbox_custom_field_profiles/views.py` | controller | request-response, CRUD | same file, lines 19–25 and 75–77 | exact generic list/detail/delete pattern; edit has no safe local analog |
| `netbox_custom_field_profiles/tables.py` | component | transform | same file, lines 1–15 | exact table integration |
| `netbox_custom_field_profiles/urls.py` | route | request-response | same file, lines 1–10 | exact route convention |
| `netbox_custom_field_profiles/navigation.py` | config | request-response | same file, lines 4–19 | exact menu/permission convention |
| `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html` | component | request-response | existing `customtabconfig_edit.html`, lines 1–14 | native edit shell only |
| Profile detail/delete templates | component | request-response | existing `customtabconfig_delete.html`; generic views in `views.py` | partial; verify native required template context |
| `netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js` | component | event-driven | no close tracked analog | new drag/keyboard implementation |
| `netbox_custom_field_profiles/services.py` (or matching module) | service | transform | no close tracked analog | new fixed matching/resolution boundary |
| `netbox_custom_field_profiles/signals.py` | hook | event-driven | no close tracked analog | use researched native lifecycle contracts |
| `netbox_custom_field_profiles/__init__.py` | config/hook | event-driven | same file, lines 17–24 | ready hook shape only |
| `netbox_custom_field_profiles/migrations/0002_*.py` | migration | batch/CRUD | generated `migrations/0001_initial.py`, lines 10–19 | exact native-generated history convention |
| Existing `api/serializers.py`, `api/views.py`, `api/urls.py`, `template_content.py` | controller/config | request-response | current tracked files | retirement/import audit only; old model consumers must boot after replacement |
| `netbox_custom_field_profiles/tests/__init__.py`, feature tests and fixtures | test | CRUD, request-response, event-driven | native fixture construction in `scripts/seed_sandbox.py` | partial; native Django TestCase infrastructure is new |
| `scripts/test_profiles.py` (if helper needed), `scripts/sandbox.py` | utility | subprocess/file-I/O | `scripts/legacy_tests.py`, lines 38–63; `scripts/sandbox.py`, lines 105–142 | role match; use Django instead of optional pytest |
| `Makefile` | config | batch | same file, lines 25–48 | exact command integration |
| `tests/sandbox/test_profiles_runner.py` (if helper added) | test | subprocess | `tests/sandbox/test_smoke.py`, lines 7–8, 21–25, 46–50 | role match |
| `pyproject.toml` | config | build/file-I/O | same file, lines 18–22 | packaging integration; verify added static/templates are included |
| `docs/development/sandbox.md`, `docs/development/baseline-status.md`, README | documentation | file-I/O | current Make targets and measured baseline | update actual behavior without claiming later tab/edit implementation |

## Pattern Assignments

### Profile model and ordered memberships

**Analog:** `netbox_custom_field_profiles/models.py:1–5,52–67`.

```python
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from netbox.models import NetBoxModel
from extras.models import CustomField

class CustomTabConfigField(models.Model):
    tab_config = models.ForeignKey(
        to=CustomTabConfig,
        on_delete=models.CASCADE,
        related_name='config_fields',
    )
    field = models.ForeignKey(
        to=CustomField,
        on_delete=models.CASCADE,
        related_name='+',
    )
    weight = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['weight', 'field__name']
        unique_together = [('tab_config', 'field')]
```

Copy the native-reference/through-row shape, not the old ordering rule or names. New profile identity is plural per Device type, titles are nonunique, default enabled is false, and memberships have explicit positions. A profile/field uniqueness constraint permits the same field in different profiles. Do not copy the existing ContentType `OneToOneField` or group model. Order profiles by display order/title/creation order with a final stable tie-break. Remember inherited NetBoxModel metadata tags: applicability tags require a distinct relation name.

### Forms, server validation and native views

**Analog:** `netbox_custom_field_profiles/forms.py:34–55` shows `NetBoxModelForm`, a runtime-scoped choice queryset, `Meta.model`, and `Meta.fields`.

```python
class CustomTabConfigForm(NetBoxModelForm):
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.none(),
        label='Object Type',
        help_text='NetBox object type for this tab configuration.',
    )

    class Meta:
        model = CustomTabConfig
        fields = ('content_type', 'tab_label', 'enabled')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

Use Device-only queryset construction and scoped applicable field choices; omit the old exclusion of already-configured types. The existing `CustomTabConfigFieldForm` uses a global alphabetically ordered field queryset and must not be copied as the new applicability or All-mode resolver.

**Analog:** `netbox_custom_field_profiles/views.py:19–25,75–77`.

```python
class CustomTabConfigListView(ObjectListView):
    queryset = CustomTabConfig.objects.prefetch_related('config_groups', 'config_fields')
    table = CustomTabConfigTable

class CustomTabConfigView(ObjectView):
    queryset = CustomTabConfig.objects.all()

class CustomTabConfigDeleteView(ObjectDeleteView):
    queryset = CustomTabConfig.objects.all()
    default_return_url = 'plugins:netbox_custom_field_profiles:customtabconfig_list'
```

These are strong local integration patterns. The existing custom edit `View` is **not** a permission analog: it requires add and change together and does not provide native constrained-object integration. Use native `ObjectEditView` with aggregate form validation/save. `02-RESEARCH.md` verified native `ObjectEditView` action selection, restricted queryset, form restrictions and transactional save. During execution recheck its `commit=False`/`save_m2m` flow before implementing ordered memberships. Invalid ordered-ID payloads must fail atomically, and All mode must preserve remembered memberships.

### Tables, URLs and permission-aware navigation

**Analog:** `netbox_custom_field_profiles/tables.py:1–15`.

```python
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns

class CustomTabConfigTable(NetBoxTable):
    content_type = tables.Column(verbose_name='Object Type', linkify=True)
    tab_label = tables.Column(verbose_name='Tab Label')
    enabled = columns.BooleanColumn(verbose_name='Enabled')
    actions = columns.ActionsColumn(actions=('edit', 'delete'))

    class Meta(NetBoxTable.Meta):
        model = CustomTabConfig
        fields = ('pk', 'content_type', 'tab_label', 'enabled', 'actions')
        default_columns = ('content_type', 'tab_label', 'enabled', 'actions')
```

Replace columns with title, enabled, display order, selection mode, readable filter summary and actions (D-04). Keep escaping in templates and use native table rendering rather than constructing unsafe title/filter HTML.

`urls.py:4–9` pairs list/add/detail/edit/delete names with `as_view()` and `<int:pk>` routes. `navigation.py:5–16` supplies a permission on both the menu entry and add button:

```python
PluginMenuItem(
    link='plugins:netbox_custom_field_profiles:customtabconfig_list',
    link_text='Custom Field Profiles',
    permissions=['netbox_custom_field_profiles.view_customtabconfig'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_custom_field_profiles:customtabconfig_add',
            title='Add',
            icon_class='mdi mdi-plus-thick',
            color=ButtonColorChoices.GREEN,
            permissions=['netbox_custom_field_profiles.add_customtabconfig'],
        ),
    ),
)
```

Update all model permission codenames and reverse targets together. Menu visibility alone does not authorize direct GET/POST.

### Template shell and new ordering interaction

**Analog:** `templates/netbox_custom_field_profiles/customtabconfig_edit.html:1–14`.

```django
{% extends 'generic/object_edit.html' %}
{% load form_helpers %}

{% block form %}
<div class="row mb-3">
  <div class="col-md-6">
    <div class="card">
      <h5 class="card-header">Configuration</h5>
      <div class="card-body">
        {% render_form form %}
```

Reuse native edit scaffolding and form helpers. Existing numeric-weight tables, inline onclick handlers and debugging logs are not the selected drag interaction. No repository drag-ordering or static-JS analog exists. Implement drag ordering plus keyboard move controls, serialize unambiguous ordered field IDs and render validation errors without dropping input. Keep DOM text insertion safe. Verify persisted order through an actual browser and ensure packaged/collected static assets load.

### Native runner and fixture patterns

**Analog:** `scripts/sandbox.py:105–110,129–142` centralizes fixed project identity and redacted subprocess failure handling:

```python
return ['docker', 'compose', '--project-directory', str(ROOT), '-p', PROJECT,
        '-f', str(ROOT / 'docker-compose.yml'), '--env-file', str(ROOT / '.env'), *args]
```

```python
process = subprocess.run(compose_argv(args), cwd=ROOT, env=env, text=True,
                         input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
if process.returncode:
    if process.stdout:
        print(redact(process.stdout[-6000:]), file=sys.stderr)
    if process.stderr:
        print(redact(process.stderr[-6000:]), file=sys.stderr)
    raise RuntimeError('project Compose command failed: ' + args[0])
```

Use the pinned native interpreter `/opt/netbox/venv/bin/python` and `/opt/netbox/netbox/manage.py` through this helper, explicit plugin-owned Django test labels, isolated PostgreSQL test database and nonzero failure on zero tests. `scripts/legacy_tests.py:38–63` is an analog for capturing/reporting a subprocess and refusing unverifiable zero exit, **not** the chosen pytest command. Do not route new tests through historical root pytest modules/SQLite settings.

**Analog:** `scripts/seed_sandbox.py:19–34,38–53` proves native model names and relationships:

```python
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from dcim.models import Site, Manufacturer, DeviceType, DeviceRole, Device
from extras.models import CustomField, Tag

content_type = ContentType.objects.get_for_model(Device)
field.object_types.add(content_type)
```

Copy fixture shape into isolated TestCase setup, not the persistent seed function itself. Device creation uses `site`, `device_type`, `role`, `status`; applicability uses `CustomField.object_types`. Snapshot native definitions and `custom_field_data` around profile CRUD; do not copy the seed's native value writes into profile code.

`tests/sandbox/test_smoke.py:7–8` imports script helpers with an explicit scripts path; lines 21–25 and 46–50 show `unittest.mock.patch.object`, `assertRaises` and assertions that failure prevents later actions. Apply to a new helper runner's argument, failure and isolation tests. Native permission/matching/lifecycle tests need real Django fixtures rather than mocks of the behavior under test.

## Shared Patterns

- **Imports/model integration:** Native Django/NetBox imports then relative plugin modules, as in `models.py`, `forms.py`, `views.py`.
- **Transactions:** The retained edit view saves all aggregate pieces within one `transaction.atomic()` (`views.py:58–64`). Preserve atomicity through native ObjectEditView/form save rather than copying the custom view.
- **Read-only native references:** Existing membership FK shape stores configuration only. DATA-01 applies to every profile write path and cleanup service.
- **Native generic authorization:** Reuse framework behavior, validate direct requests with action-specific and constrained users, and scope reference choice querysets on the server.
- **Migration history:** `migrations/0001_initial.py:1,10–19` is native-generated and already applied. Generate a forward migration in the pinned runtime; do not rewrite history. Include the execution decision checkpoint before irreversible old-config removal.
- **Ready registration:** `__init__.py:17–24` calls `super().ready()` before plugin registration. Use that hook for once-only receiver import with dispatch UIDs; retire old extension imports when dropping old model consumers.
- **Runtime identity/secrets:** Keep `sandbox.compose_argv`, `docker_environment` and `redact`; no new Compose project override, credentials in artifacts or environment reset.

## No Analog Found

| Proposed capability | Role/data flow | Why no close tracked analog | Use instead |
|---|---|---|---|
| Fixed Device matching/ordered field service | service/transform | Current template extension resolves a single old config and groups | Research's AND/OR/any-tag semantics and native field resolver |
| Native target-deletion/applicability safety | hook/event-driven | No plugin signal receivers exist | Research's pre_delete and forward/reverse remove/clear/set contracts, including deferred deletion |
| Safe native ObjectEditView aggregate form save | controller/form CRUD | Current edit class is a custom View | Verified native interfaces in research; test real permission/transaction behavior |
| Drag and keyboard order UI | component/event-driven | Existing formsets expose numeric weights only | Small plugin-owned JS with validated payload and browser proof |
| Isolated native Django feature suite | test/CRUD | Baseline host unittest checks helpers; root feature tests depend on optional legacy pytest | New plugin test package and native PostgreSQL runner in first tracer |

## Metadata

**Analog search scope:** tracked plugin root, scripts, Makefile, pyproject, baseline test helpers. Five principal analog families: model/through rows; forms/generic views; table/route/menu; native template shell; sandbox runner/native fixture helpers. Search stopped after these strong matches. Native installed source cited by research is external integration evidence, not a git-tracked project analog; no runtime mirror paths are proposed for editing. All 16 decisions remain authoritative; Parameters tab and native value editing remain later phases.
