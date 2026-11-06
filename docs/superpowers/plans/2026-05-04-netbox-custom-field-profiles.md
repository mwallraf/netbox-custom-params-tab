# netbox-custom-field-profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a NetBox 4.x plugin that moves selected custom fields and/or custom field groups into a dedicated section on any supported object's detail page, storing only display configuration and reading all field values from the object's existing `custom_field_data`.

**Architecture:** Three models (`CustomTabConfig`, `CustomTabConfigGroup`, `CustomTabConfigField`) store per-object-type display config. At render time, `PluginTemplateExtension` subclasses query the config and call `full_width_page()` to inject a panel section. A CRUD admin UI lives under Customization > Custom Field Profiles. All custom field data stays in NetBox's native infrastructure.

**Tech Stack:** Python 3.10+, Django 4.x, NetBox 4.x plugin API (`PluginConfig`, `PluginTemplateExtension`, `NetBoxModel`, `ObjectListView`, `ObjectDeleteView`), Django inline formsets for through-model editing, pytest + pytest-django with SQLite in-memory for tests.

---

## File Map

| File | Role |
|---|---|
| `pyproject.toml` | Package metadata and build config |
| `pytest.ini` | Pytest + Django settings pointer |
| `testing/__init__.py` | Makes testing a package |
| `testing/settings.py` | Minimal Django/NetBox settings for test runs |
| `tests/__init__.py` | Makes tests a package |
| `tests/conftest.py` | Shared fixtures (admin user, content types) |
| `netbox_custom_field_profiles/__init__.py` | `PluginConfig`; wires `template_extensions`, `menu_items`, and `ready()` for extra models |
| `netbox_custom_field_profiles/models.py` | `CustomTabConfig`, `CustomTabConfigGroup`, `CustomTabConfigField` |
| `netbox_custom_field_profiles/migrations/0001_initial.py` | DB schema |
| `netbox_custom_field_profiles/tables.py` | `CustomTabConfigTable` for the list view |
| `netbox_custom_field_profiles/forms.py` | `CustomTabConfigForm`, `CustomTabConfigGroupFormSet`, `CustomTabConfigFieldFormSet` |
| `netbox_custom_field_profiles/views.py` | `CustomTabConfigListView`, `CustomTabConfigEditView`, `CustomTabConfigDeleteView` |
| `netbox_custom_field_profiles/urls.py` | URL patterns under `plugins:netbox_custom_field_profiles:` |
| `netbox_custom_field_profiles/navigation.py` | `menu_items` tuple |
| `netbox_custom_field_profiles/template_content.py` | `PluginTemplateExtension` factory + `BUILTIN_MODELS` list |
| `netbox_custom_field_profiles/templatetags/__init__.py` | Makes templatetags a package |
| `netbox_custom_field_profiles/templatetags/customtab_tags.py` | `\|dict_value` filter for template use |
| `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_edit.html` | Create/edit form with inline formsets |
| `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_delete.html` | Delete confirmation |
| `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/tab_panel.html` | Rendered tab content injected on object detail pages |
| `tests/test_models.py` | Model unit + cascade tests |
| `tests/test_tables.py` | Table rendering tests |
| `tests/test_forms.py` | Form and formset validation tests |
| `tests/test_views.py` | View HTTP status + data persistence tests |
| `tests/test_template_content.py` | Extension render logic tests |
| `docker/Dockerfile` | Extends official NetBox image, installs plugin from source |
| `docker/configuration.py` | NetBox `configuration.py` for the dev stack (DB, Redis, plugin enabled) |
| `docker-compose.yml` | Dev stack: netbox, netbox-worker, postgres, redis, redis-cache |
| `Makefile` | Developer shortcuts: `up`, `down`, `build`, `logs`, `shell`, `migrate`, `superuser`, `clean` |

---

### Task 1: Package Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `pytest.ini`
- Create: `testing/__init__.py`
- Create: `testing/settings.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `netbox_custom_field_profiles/__init__.py`

- [ ] **Step 1: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "netbox-custom-field-profiles"
version = "0.1.0"
description = "NetBox plugin: move custom fields into a dedicated section on object detail pages"
requires-python = ">=3.10"
dependencies = []

[project.entry-points."netbox.plugins"]
netbox_custom_field_profiles = "netbox_custom_field_profiles:config"

[tool.setuptools.packages.find]
include = ["netbox_custom_field_profiles*"]
```

- [ ] **Step 2: Create `pytest.ini`**

```ini
[pytest]
DJANGO_SETTINGS_MODULE = testing.settings
python_files = tests/test_*.py
python_classes = Test*
python_functions = test_*
```

- [ ] **Step 3: Create `testing/__init__.py`**

Empty file.

- [ ] **Step 4: Create `testing/settings.py`**

```python
SECRET_KEY = 'netbox-custom-field-profiles-test-only-not-for-production'
ALLOWED_HOSTS = ['*']
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party deps required by NetBox
    'django_tables2',
    'mptt',
    'taggit',
    # NetBox core apps (adjust list to match your installed NetBox version)
    'netbox',
    'extras',
    'dcim',
    'ipam',
    'virtualization',
    'circuits',
    'tenancy',
    'users',
    'utilities',
    # Plugin under test
    'netbox_custom_field_profiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'netbox.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PLUGINS = ['netbox_custom_field_profiles']
PLUGINS_CONFIG = {
    'netbox_custom_field_profiles': {},
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/netbox_media_test/'
```

> **Note:** NetBox must be installed in the Python environment (`pip install netbox` or from source). The `INSTALLED_APPS` list may need adjustment to match your exact NetBox 4.x version's required apps.

- [ ] **Step 5: Create `tests/__init__.py`**

Empty file.

- [ ] **Step 6: Create `tests/conftest.py`**

```python
import pytest
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        password='password',
        email='admin@example.com',
    )


@pytest.fixture
def client_logged_in(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def device_content_type(db):
    return ContentType.objects.get(app_label='dcim', model='device')


@pytest.fixture
def site_content_type(db):
    return ContentType.objects.get(app_label='dcim', model='site')
```

- [ ] **Step 7: Create `netbox_custom_field_profiles/__init__.py`**

```python
from netbox.plugins import PluginConfig


class CustomFieldProfilesConfig(PluginConfig):
    name = 'netbox_custom_field_profiles'
    verbose_name = 'Custom Field Profiles'
    version = '0.1.0'
    description = 'Moves selected custom fields into a dedicated section on object detail pages'
    min_version = '4.0.0'
    base_url = 'custom-field-profiles'
    template_extensions = 'netbox_custom_field_profiles.template_content.template_extensions'
    menu_items = 'netbox_custom_field_profiles.navigation.menu_items'
    default_settings = {
        'extra_models': [],
    }

    def ready(self):
        super().ready()
        from django.conf import settings as django_settings
        import netbox_custom_field_profiles.template_content as tc
        plugin_cfg = django_settings.PLUGINS_CONFIG.get('netbox_custom_field_profiles', {})
        extra = plugin_cfg.get('extra_models', [])
        if extra:
            tc.template_extensions = tc.build_template_extensions(extra)


config = CustomFieldProfilesConfig
```

- [ ] **Step 8: Install in dev mode**

```bash
pip install -e .
```

Expected output contains: `Successfully installed netbox-custom-field-profiles-0.1.0`

- [ ] **Step 9: Verify the plugin config imports**

```bash
python -c "from netbox_custom_field_profiles import config; print(config.name)"
```

Expected: `netbox_custom_field_profiles`

- [ ] **Step 10: Commit**

```bash
git add pyproject.toml pytest.ini testing/ tests/__init__.py tests/conftest.py netbox_custom_field_profiles/__init__.py
git commit -m "feat: add package scaffold, test infrastructure, and PluginConfig"
```

---

### Task 2: Models

**Files:**
- Create: `netbox_custom_field_profiles/models.py`
- Create: `netbox_custom_field_profiles/migrations/__init__.py`
- Create: `tests/test_models.py`

- [ ] **Step 1: Write failing tests in `tests/test_models.py`**

```python
import pytest
from django.db import IntegrityError
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField, CustomFieldGroup, CustomFieldTypeChoices
from netbox_custom_field_profiles.models import (
    CustomTabConfig,
    CustomTabConfigGroup,
    CustomTabConfigField,
)


@pytest.mark.django_db
class TestCustomTabConfig:
    def test_create(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type,
            tab_label='Parameters',
            enabled=True,
        )
        assert config.pk is not None
        assert str(config) == f'{device_content_type} — Parameters'

    def test_enabled_default_is_true(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        assert config.enabled is True

    def test_tab_label_default_is_parameters(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        assert config.tab_label == 'Parameters'

    def test_content_type_is_unique(self, device_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type)
        with pytest.raises(Exception):
            CustomTabConfig.objects.create(content_type=device_content_type)

    def test_get_absolute_url_resolves(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = config.get_absolute_url()
        assert str(config.pk) in url


@pytest.mark.django_db
class TestCustomTabConfigGroup:
    def test_create(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Network')
        entry = CustomTabConfigGroup.objects.create(tab_config=config, group=group, weight=100)
        assert entry.pk is not None

    def test_weight_default_is_100(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Network')
        entry = CustomTabConfigGroup.objects.create(tab_config=config, group=group)
        assert entry.weight == 100

    def test_ordering_ascending_by_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group_a = CustomFieldGroup.objects.create(name='Alpha')
        group_b = CustomFieldGroup.objects.create(name='Beta')
        CustomTabConfigGroup.objects.create(tab_config=config, group=group_b, weight=200)
        CustomTabConfigGroup.objects.create(tab_config=config, group=group_a, weight=100)
        names = list(
            config.config_groups.order_by('weight', 'group__name')
            .values_list('group__name', flat=True)
        )
        assert names == ['Alpha', 'Beta']

    def test_cascade_delete_when_tab_config_deleted(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Cascade Test')
        CustomTabConfigGroup.objects.create(tab_config=config, group=group)
        config.delete()
        assert CustomTabConfigGroup.objects.count() == 0

    def test_cascade_delete_when_group_deleted(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Doomed Group')
        CustomTabConfigGroup.objects.create(tab_config=config, group=group)
        group.delete()
        assert CustomTabConfigGroup.objects.count() == 0


@pytest.mark.django_db
class TestCustomTabConfigField:
    def test_create(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        cf = CustomField.objects.create(name='rack_role', type=CustomFieldTypeChoices.TYPE_TEXT)
        entry = CustomTabConfigField.objects.create(tab_config=config, field=cf, weight=100)
        assert entry.pk is not None

    def test_ordering_ascending_by_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        field_a = CustomField.objects.create(name='alpha', type=CustomFieldTypeChoices.TYPE_TEXT)
        field_b = CustomField.objects.create(name='beta', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigField.objects.create(tab_config=config, field=field_b, weight=200)
        CustomTabConfigField.objects.create(tab_config=config, field=field_a, weight=100)
        names = list(
            config.config_fields.order_by('weight', 'field__name')
            .values_list('field__name', flat=True)
        )
        assert names == ['alpha', 'beta']

    def test_cascade_delete_when_custom_field_deleted(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        cf = CustomField.objects.create(name='doomed_field', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigField.objects.create(tab_config=config, field=cf)
        cf.delete()
        assert CustomTabConfigField.objects.count() == 0
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/test_models.py -v
```

Expected: `ModuleNotFoundError: No module named 'netbox_custom_field_profiles.models'`

- [ ] **Step 3: Create `netbox_custom_field_profiles/models.py`**

```python
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from netbox.models import NetBoxModel
from extras.models import CustomField, CustomFieldGroup


class CustomTabConfig(NetBoxModel):
    content_type = models.OneToOneField(
        to=ContentType,
        on_delete=models.CASCADE,
        related_name='custom_tab_config',
    )
    tab_label = models.CharField(max_length=100, default='Parameters')
    enabled = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        to=CustomFieldGroup,
        through='CustomTabConfigGroup',
        blank=True,
        related_name='custom_tab_configs',
    )
    fields = models.ManyToManyField(
        to=CustomField,
        through='CustomTabConfigField',
        blank=True,
        related_name='custom_tab_configs',
    )

    class Meta:
        ordering = ['content_type__app_label', 'content_type__model']
        verbose_name = 'Custom Tab Config'
        verbose_name_plural = 'Custom Tab Configs'

    def __str__(self):
        return f'{self.content_type} — {self.tab_label}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_custom_field_profiles:customtabconfig', args=[self.pk])


class CustomTabConfigGroup(models.Model):
    tab_config = models.ForeignKey(
        to=CustomTabConfig,
        on_delete=models.CASCADE,
        related_name='config_groups',
    )
    group = models.ForeignKey(
        to=CustomFieldGroup,
        on_delete=models.CASCADE,
        related_name='+',
    )
    weight = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['weight', 'group__name']
        unique_together = [('tab_config', 'group')]

    def __str__(self):
        return f'{self.tab_config} / {self.group.name} (weight={self.weight})'


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

    def __str__(self):
        return f'{self.tab_config} / {self.field.name} (weight={self.weight})'
```

- [ ] **Step 4: Create `netbox_custom_field_profiles/migrations/__init__.py`**

Empty file.

- [ ] **Step 5: Generate initial migration**

```bash
python -m django makemigrations netbox_custom_field_profiles --settings=testing.settings
```

Expected: `Created migrations/0001_initial.py`

- [ ] **Step 6: Apply migrations**

```bash
python -m django migrate --settings=testing.settings
```

Expected: `Applying netbox_custom_field_profiles.0001_initial... OK`

- [ ] **Step 7: Run tests**

```bash
pytest tests/test_models.py -v
```

Expected: All 11 tests PASS

- [ ] **Step 8: Commit**

```bash
git add netbox_custom_field_profiles/models.py netbox_custom_field_profiles/migrations/ tests/test_models.py
git commit -m "feat: add models CustomTabConfig, CustomTabConfigGroup, CustomTabConfigField"
```

---

### Task 3: Tables

**Files:**
- Create: `netbox_custom_field_profiles/tables.py`
- Create: `tests/test_tables.py`

- [ ] **Step 1: Write failing tests in `tests/test_tables.py`**

```python
import pytest
from netbox_custom_field_profiles.models import CustomTabConfig
from netbox_custom_field_profiles.tables import CustomTabConfigTable


@pytest.mark.django_db
class TestCustomTabConfigTable:
    def test_renders_with_queryset(self, device_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type, tab_label='Params')
        table = CustomTabConfigTable(CustomTabConfig.objects.all())
        assert table.rows.data.count() == 1

    def test_empty_queryset_renders(self):
        table = CustomTabConfigTable(CustomTabConfig.objects.none())
        assert table.rows.data.count() == 0

    def test_required_columns_present(self):
        table = CustomTabConfigTable(CustomTabConfig.objects.none())
        col_names = [c.name for c in table.columns]
        for required in ('content_type', 'tab_label', 'enabled', 'actions'):
            assert required in col_names, f'Column {required!r} missing from table'
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
pytest tests/test_tables.py -v
```

Expected: `ModuleNotFoundError: No module named 'netbox_custom_field_profiles.tables'`

- [ ] **Step 3: Create `netbox_custom_field_profiles/tables.py`**

```python
import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import CustomTabConfig


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

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_tables.py -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add netbox_custom_field_profiles/tables.py tests/test_tables.py
git commit -m "feat: add CustomTabConfigTable"
```

---

### Task 4: Template Content Stub + Forms

`forms.py` needs `BUILTIN_MODELS` from `template_content.py`. Create a stub now; Task 8 replaces it with the full implementation.

**Files:**
- Create: `netbox_custom_field_profiles/template_content.py` (stub)
- Create: `netbox_custom_field_profiles/forms.py`
- Create: `tests/test_forms.py`

- [ ] **Step 1: Create stub `netbox_custom_field_profiles/template_content.py`**

```python
from netbox.plugins import PluginTemplateExtension  # noqa: F401 — required by PluginConfig

BUILTIN_MODELS = [
    'dcim.device',
    'dcim.devicetype',
    'dcim.rack',
    'dcim.site',
    'dcim.location',
    'dcim.cable',
    'virtualization.virtualmachine',
    'virtualization.vminterface',
    'ipam.prefix',
    'ipam.ipaddress',
    'ipam.vlan',
    'circuits.circuit',
]


def build_template_extensions(extra_models=None):
    return []


template_extensions = build_template_extensions()
```

- [ ] **Step 2: Write failing tests in `tests/test_forms.py`**

```python
import pytest
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField, CustomFieldGroup, CustomFieldTypeChoices
from netbox_custom_field_profiles.models import CustomTabConfig
from netbox_custom_field_profiles.forms import (
    CustomTabConfigForm,
    CustomTabConfigGroupFormSet,
    CustomTabConfigFieldFormSet,
)


@pytest.mark.django_db
class TestCustomTabConfigForm:
    def test_valid_form(self, device_content_type):
        form = CustomTabConfigForm(data={
            'content_type': device_content_type.pk,
            'tab_label': 'Parameters',
            'enabled': True,
        })
        assert form.is_valid(), form.errors

    def test_missing_content_type_is_invalid(self):
        form = CustomTabConfigForm(data={
            'tab_label': 'Parameters',
            'enabled': True,
        })
        assert not form.is_valid()
        assert 'content_type' in form.errors

    def test_tab_label_field_exists(self, device_content_type):
        form = CustomTabConfigForm()
        assert 'tab_label' in form.fields

    def test_content_type_choices_include_device(self, device_content_type):
        form = CustomTabConfigForm()
        pks = list(form.fields['content_type'].queryset.values_list('pk', flat=True))
        assert device_content_type.pk in pks

    def test_already_configured_type_excluded_on_create(self, device_content_type, site_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type)
        form = CustomTabConfigForm()
        pks = list(form.fields['content_type'].queryset.values_list('pk', flat=True))
        assert device_content_type.pk not in pks
        assert site_content_type.pk in pks

    def test_current_type_kept_on_edit(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        form = CustomTabConfigForm(instance=config)
        pks = list(form.fields['content_type'].queryset.values_list('pk', flat=True))
        assert device_content_type.pk in pks


@pytest.mark.django_db
class TestCustomTabConfigGroupFormSet:
    def test_empty_formset_is_valid(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        formset = CustomTabConfigGroupFormSet(
            instance=config,
            data={
                'config_groups-TOTAL_FORMS': '0',
                'config_groups-INITIAL_FORMS': '0',
                'config_groups-MIN_NUM_FORMS': '0',
                'config_groups-MAX_NUM_FORMS': '1000',
            },
            prefix='config_groups',
        )
        assert formset.is_valid(), formset.errors

    def test_add_group_entry(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        group = CustomFieldGroup.objects.create(name='Network')
        formset = CustomTabConfigGroupFormSet(
            instance=config,
            data={
                'config_groups-TOTAL_FORMS': '1',
                'config_groups-INITIAL_FORMS': '0',
                'config_groups-MIN_NUM_FORMS': '0',
                'config_groups-MAX_NUM_FORMS': '1000',
                'config_groups-0-group': str(group.pk),
                'config_groups-0-weight': '100',
            },
            prefix='config_groups',
        )
        assert formset.is_valid(), formset.errors
        formset.save()
        assert config.config_groups.count() == 1


@pytest.mark.django_db
class TestCustomTabConfigFieldFormSet:
    def test_add_field_entry(self, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        cf = CustomField.objects.create(name='rack_role', type=CustomFieldTypeChoices.TYPE_TEXT)
        formset = CustomTabConfigFieldFormSet(
            instance=config,
            data={
                'config_fields-TOTAL_FORMS': '1',
                'config_fields-INITIAL_FORMS': '0',
                'config_fields-MIN_NUM_FORMS': '0',
                'config_fields-MAX_NUM_FORMS': '1000',
                'config_fields-0-field': str(cf.pk),
                'config_fields-0-weight': '150',
            },
            prefix='config_fields',
        )
        assert formset.is_valid(), formset.errors
        formset.save()
        assert config.config_fields.count() == 1
```

- [ ] **Step 3: Run tests to confirm they fail**

```bash
pytest tests/test_forms.py -v
```

Expected: `ModuleNotFoundError: No module named 'netbox_custom_field_profiles.forms'`

- [ ] **Step 4: Create `netbox_custom_field_profiles/forms.py`**

```python
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory
from netbox.forms import NetBoxModelForm
from .models import CustomTabConfig, CustomTabConfigGroup, CustomTabConfigField
from .template_content import BUILTIN_MODELS


def _supported_content_type_pks():
    pks = []
    for model_path in BUILTIN_MODELS:
        app_label, model_name = model_path.split('.')
        try:
            ct = ContentType.objects.get(app_label=app_label, model=model_name)
            pks.append(ct.pk)
        except ContentType.DoesNotExist:
            pass
    return pks


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
        supported_pks = _supported_content_type_pks()
        if self.instance.pk:
            # Edit: show all supported types (current type stays selectable)
            allowed_pks = supported_pks
        else:
            # Create: exclude content types that already have a config
            existing_pks = list(
                CustomTabConfig.objects.values_list('content_type_id', flat=True)
            )
            allowed_pks = [pk for pk in supported_pks if pk not in existing_pks]
        self.fields['content_type'].queryset = ContentType.objects.filter(pk__in=allowed_pks)


CustomTabConfigGroupFormSet = inlineformset_factory(
    CustomTabConfig,
    CustomTabConfigGroup,
    fields=['group', 'weight'],
    extra=1,
    can_delete=True,
    fk_name='tab_config',
)

CustomTabConfigFieldFormSet = inlineformset_factory(
    CustomTabConfig,
    CustomTabConfigField,
    fields=['field', 'weight'],
    extra=1,
    can_delete=True,
    fk_name='tab_config',
)
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_forms.py -v
```

Expected: All 9 tests PASS

- [ ] **Step 6: Commit**

```bash
git add netbox_custom_field_profiles/template_content.py netbox_custom_field_profiles/forms.py tests/test_forms.py
git commit -m "feat: add forms, inline formsets, and template_content stub"
```

---

### Task 5: Views and URLs

**Files:**
- Create: `netbox_custom_field_profiles/urls.py`
- Create: `netbox_custom_field_profiles/views.py`
- Create: `tests/test_views.py`

- [ ] **Step 1: Create `netbox_custom_field_profiles/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomTabConfigListView.as_view(), name='customtabconfig_list'),
    path('add/', views.CustomTabConfigEditView.as_view(), name='customtabconfig_add'),
    path('<int:pk>/', views.CustomTabConfigView.as_view(), name='customtabconfig'),
    path('<int:pk>/edit/', views.CustomTabConfigEditView.as_view(), name='customtabconfig_edit'),
    path('<int:pk>/delete/', views.CustomTabConfigDeleteView.as_view(), name='customtabconfig_delete'),
]
```

- [ ] **Step 2: Write failing tests in `tests/test_views.py`**

```python
import pytest
from django.urls import reverse
from netbox_custom_field_profiles.models import CustomTabConfig


@pytest.mark.django_db
class TestCustomTabConfigListView:
    def test_returns_200(self, client_logged_in):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_list')
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_unauthenticated_redirects(self, client):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_list')
        response = client.get(url)
        assert response.status_code in (302, 403)


@pytest.mark.django_db
class TestCustomTabConfigEditView:
    def test_get_add_returns_200(self, client_logged_in):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_add')
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_post_creates_config(self, client_logged_in, device_content_type):
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_add')
        response = client_logged_in.post(url, {
            'content_type': device_content_type.pk,
            'tab_label': 'Parameters',
            'enabled': True,
            'config_groups-TOTAL_FORMS': '0',
            'config_groups-INITIAL_FORMS': '0',
            'config_groups-MIN_NUM_FORMS': '0',
            'config_groups-MAX_NUM_FORMS': '1000',
            'config_fields-TOTAL_FORMS': '0',
            'config_fields-INITIAL_FORMS': '0',
            'config_fields-MIN_NUM_FORMS': '0',
            'config_fields-MAX_NUM_FORMS': '1000',
        })
        assert response.status_code in (200, 302)
        assert CustomTabConfig.objects.filter(content_type=device_content_type).exists()

    def test_get_edit_returns_200(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_edit', args=[config.pk])
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_edit_updates_tab_label(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, tab_label='Old Label'
        )
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_edit', args=[config.pk])
        client_logged_in.post(url, {
            'content_type': device_content_type.pk,
            'tab_label': 'New Label',
            'enabled': True,
            'config_groups-TOTAL_FORMS': '0',
            'config_groups-INITIAL_FORMS': '0',
            'config_groups-MIN_NUM_FORMS': '0',
            'config_groups-MAX_NUM_FORMS': '1000',
            'config_fields-TOTAL_FORMS': '0',
            'config_fields-INITIAL_FORMS': '0',
            'config_fields-MIN_NUM_FORMS': '0',
            'config_fields-MAX_NUM_FORMS': '1000',
        })
        config.refresh_from_db()
        assert config.tab_label == 'New Label'


@pytest.mark.django_db
class TestCustomTabConfigDeleteView:
    def test_get_delete_returns_200(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_delete', args=[config.pk])
        response = client_logged_in.get(url)
        assert response.status_code == 200

    def test_post_delete_removes_config(self, client_logged_in, device_content_type):
        config = CustomTabConfig.objects.create(content_type=device_content_type)
        url = reverse('plugins:netbox_custom_field_profiles:customtabconfig_delete', args=[config.pk])
        response = client_logged_in.post(url, {'confirm': True})
        assert response.status_code in (200, 302)
        assert not CustomTabConfig.objects.filter(pk=config.pk).exists()
```

- [ ] **Step 3: Run tests to confirm they fail**

```bash
pytest tests/test_views.py -v
```

Expected: `ModuleNotFoundError: No module named 'netbox_custom_field_profiles.views'`

- [ ] **Step 4: Create `netbox_custom_field_profiles/views.py`**

```python
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from netbox.views.generic import ObjectListView, ObjectView, ObjectDeleteView
from .models import CustomTabConfig
from .tables import CustomTabConfigTable
from .forms import CustomTabConfigForm, CustomTabConfigGroupFormSet, CustomTabConfigFieldFormSet


class CustomTabConfigListView(ObjectListView):
    queryset = CustomTabConfig.objects.prefetch_related('groups', 'fields')
    table = CustomTabConfigTable


class CustomTabConfigView(ObjectView):
    queryset = CustomTabConfig.objects.all()


class CustomTabConfigEditView(View):
    template_name = 'netbox_custom_field_profiles/customtabconfig_edit.html'

    def _build_forms(self, instance=None, data=None):
        form = CustomTabConfigForm(data=data, instance=instance)
        group_formset = CustomTabConfigGroupFormSet(
            data=data, instance=instance, prefix='config_groups'
        )
        field_formset = CustomTabConfigFieldFormSet(
            data=data, instance=instance, prefix='config_fields'
        )
        return form, group_formset, field_formset

    def get(self, request, pk=None):
        instance = get_object_or_404(CustomTabConfig, pk=pk) if pk else None
        form, group_formset, field_formset = self._build_forms(instance=instance)
        return render(request, self.template_name, {
            'form': form,
            'group_formset': group_formset,
            'field_formset': field_formset,
            'object': instance,
        })

    def post(self, request, pk=None):
        instance = get_object_or_404(CustomTabConfig, pk=pk) if pk else None
        form, group_formset, field_formset = self._build_forms(instance=instance, data=request.POST)
        if form.is_valid() and group_formset.is_valid() and field_formset.is_valid():
            with transaction.atomic():
                config = form.save()
                group_formset.instance = config
                group_formset.save()
                field_formset.instance = config
                field_formset.save()
            messages.success(request, f'Saved config for {config.content_type}.')
            return redirect(reverse('plugins:netbox_custom_field_profiles:customtabconfig_list'))
        return render(request, self.template_name, {
            'form': form,
            'group_formset': group_formset,
            'field_formset': field_formset,
            'object': instance,
        })


class CustomTabConfigDeleteView(ObjectDeleteView):
    queryset = CustomTabConfig.objects.all()
    default_return_url = 'plugins:netbox_custom_field_profiles:customtabconfig_list'
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_views.py -v
```

Expected: All 7 tests PASS

- [ ] **Step 6: Commit**

```bash
git add netbox_custom_field_profiles/views.py netbox_custom_field_profiles/urls.py tests/test_views.py
git commit -m "feat: add CRUD views and URL patterns"
```

---

### Task 6: Navigation

**Files:**
- Create: `netbox_custom_field_profiles/navigation.py`

- [ ] **Step 1: Create `netbox_custom_field_profiles/navigation.py`**

```python
from netbox.plugins.navigation import PluginMenuItem, PluginMenuButton
from utilities.choices import ButtonColorChoices

menu_items = (
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
    ),
)
```

- [ ] **Step 2: Verify it imports cleanly**

```bash
python -c "from netbox_custom_field_profiles.navigation import menu_items; print(len(menu_items), 'items')"
```

Expected: `1 items`

- [ ] **Step 3: Commit**

```bash
git add netbox_custom_field_profiles/navigation.py
git commit -m "feat: add navigation menu entry under Customization"
```

---

### Task 7: Templates

**Files:**
- Create: `netbox_custom_field_profiles/templatetags/__init__.py`
- Create: `netbox_custom_field_profiles/templatetags/customtab_tags.py`
- Create: `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_edit.html`
- Create: `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_delete.html`
- Create: `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/tab_panel.html`

- [ ] **Step 1: Create `netbox_custom_field_profiles/templatetags/__init__.py`**

Empty file.

- [ ] **Step 2: Create `netbox_custom_field_profiles/templatetags/customtab_tags.py`**

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

- [ ] **Step 3: Create `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_edit.html`**

```html
{% extends 'generic/object_edit.html' %}
{% load form_helpers %}

{% block form %}
<div class="row mb-3">
  <div class="col-md-6">
    <div class="card">
      <h5 class="card-header">Configuration</h5>
      <div class="card-body">
        {% render_form form %}
      </div>
    </div>
  </div>
</div>

<div class="row mb-3">
  <div class="col-12">
    <div class="card">
      <h5 class="card-header">Custom Field Groups</h5>
      <div class="card-body">
        <p class="text-muted small">Groups rendered in the tab, sorted by ascending weight.</p>
        {{ group_formset.management_form }}
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Group</th>
              <th style="width:120px">Weight</th>
              <th style="width:60px">Delete</th>
            </tr>
          </thead>
          <tbody>
            {% for gform in group_formset %}
              <tr>
                <td>{{ gform.group }}{% for h in gform.hidden_fields %}{{ h }}{% endfor %}</td>
                <td>{{ gform.weight }}</td>
                <td>{{ gform.DELETE }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<div class="row mb-3">
  <div class="col-12">
    <div class="card">
      <h5 class="card-header">Standalone Custom Fields</h5>
      <div class="card-body">
        <p class="text-muted small">Individual fields rendered in the tab, sorted by ascending weight.</p>
        {{ field_formset.management_form }}
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Field</th>
              <th style="width:120px">Weight</th>
              <th style="width:60px">Delete</th>
            </tr>
          </thead>
          <tbody>
            {% for ffield in field_formset %}
              <tr>
                <td>{{ ffield.field }}{% for h in ffield.hidden_fields %}{{ h }}{% endfor %}</td>
                <td>{{ ffield.weight }}</td>
                <td>{{ ffield.DELETE }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

- [ ] **Step 4: Create `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_delete.html`**

```html
{% extends 'generic/object_delete.html' %}
```

- [ ] **Step 5: Create `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/tab_panel.html`**

```html
{% load customtab_tags %}

<div class="card">
  <h5 class="card-header">{{ config.tab_label }}</h5>
  <div class="card-body">
    {% for item_type, item_obj, weight in items %}

      {% if item_type == 'group' %}
        <div class="mb-4">
          <h6 class="border-bottom pb-1 text-muted">{{ item_obj.name }}</h6>
          <table class="table table-hover attr-table">
            <tbody>
              {% for cf in item_obj.customfields.all %}
                {% with raw_value=object.custom_field_data|dict_value:cf.name %}
                <tr>
                  <th scope="row" style="width:30%">{{ cf.label|default:cf.name }}</th>
                  <td>
                    {% if raw_value is not None %}{{ raw_value }}{% else %}<span class="text-muted">&mdash;</span>{% endif %}
                  </td>
                </tr>
                {% endwith %}
              {% empty %}
                <tr><td class="text-muted">No fields in this group.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>

      {% elif item_type == 'field' %}
        {% with raw_value=object.custom_field_data|dict_value:item_obj.name %}
        <table class="table table-hover attr-table mb-2">
          <tbody>
            <tr>
              <th scope="row" style="width:30%">{{ item_obj.label|default:item_obj.name }}</th>
              <td>
                {% if raw_value is not None %}{{ raw_value }}{% else %}<span class="text-muted">&mdash;</span>{% endif %}
              </td>
            </tr>
          </tbody>
        </table>
        {% endwith %}

      {% endif %}

    {% empty %}
      <p class="text-muted">No fields or groups configured for this tab.</p>
    {% endfor %}
  </div>
</div>
```

- [ ] **Step 6: Run view tests to confirm templates load without errors**

```bash
pytest tests/test_views.py -v
```

Expected: All 7 tests PASS

- [ ] **Step 7: Commit**

```bash
git add netbox_custom_field_profiles/templatetags/ netbox_custom_field_profiles/templates/
git commit -m "feat: add HTML templates for edit, delete, and tab panel"
```

---

### Task 8: Full Template Extensions

Replace the stub `template_content.py` with the working implementation.

**Files:**
- Modify: `netbox_custom_field_profiles/template_content.py`
- Create: `tests/test_template_content.py`

- [ ] **Step 1: Write failing tests in `tests/test_template_content.py`**

```python
import pytest
from unittest.mock import patch, MagicMock
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField, CustomFieldGroup, CustomFieldTypeChoices
from netbox_custom_field_profiles.models import (
    CustomTabConfig,
    CustomTabConfigGroup,
    CustomTabConfigField,
)
from netbox_custom_field_profiles.template_content import build_template_extensions, BUILTIN_MODELS


class TestBuildTemplateExtensions:
    def test_returns_one_extension_per_builtin_model(self):
        extensions = build_template_extensions()
        assert len(extensions) == len(BUILTIN_MODELS)

    def test_each_extension_model_attr_matches(self):
        extensions = build_template_extensions()
        for ext, model_path in zip(extensions, BUILTIN_MODELS):
            assert ext.model == model_path

    def test_extra_models_appended(self):
        extensions = build_template_extensions(extra_models=['tenancy.tenant'])
        assert len(extensions) == len(BUILTIN_MODELS) + 1
        assert extensions[-1].model == 'tenancy.tenant'


@pytest.mark.django_db
class TestTabExtensionFullWidthPage:
    def _get_extension_instance(self, model_path, obj):
        extensions = build_template_extensions()
        ext_class = next(e for e in extensions if e.model == model_path)
        instance = ext_class.__new__(ext_class)
        instance.context = {'object': obj}
        return instance

    def test_returns_empty_string_when_no_config_exists(self, device_content_type):
        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)
        with patch.object(type(ext), 'render', return_value='rendered'):
            result = ext.full_width_page()
        assert result == ''

    def test_returns_empty_string_when_config_disabled(self, device_content_type):
        CustomTabConfig.objects.create(content_type=device_content_type, enabled=False)
        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)
        with patch.object(type(ext), 'render', return_value='rendered'):
            result = ext.full_width_page()
        assert result == ''

    def test_calls_render_when_config_is_enabled(self, device_content_type):
        CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True, tab_label='My Params'
        )
        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)
        with patch.object(type(ext), 'render', return_value='<div>ok</div>') as mock_render:
            result = ext.full_width_page()
        assert result == '<div>ok</div>'
        mock_render.assert_called_once()
        template_name = mock_render.call_args[0][0]
        assert template_name == 'netbox_custom_field_profiles/tab_panel.html'

    def test_items_sorted_field_before_group_when_lower_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True
        )
        group = CustomFieldGroup.objects.create(name='Group A')
        field = CustomField.objects.create(name='field_b', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigGroup.objects.create(tab_config=config, group=group, weight=200)
        CustomTabConfigField.objects.create(tab_config=config, field=field, weight=100)

        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)

        captured = {}

        def capture(template_name, context):
            captured.update(context)
            return 'rendered'

        with patch.object(type(ext), 'render', side_effect=capture):
            ext.full_width_page()

        items = captured.get('items', [])
        assert len(items) == 2
        assert items[0][0] == 'field'   # weight=100 comes first
        assert items[1][0] == 'group'   # weight=200 comes second

    def test_items_alphabetical_tiebreak_on_equal_weight(self, device_content_type):
        config = CustomTabConfig.objects.create(
            content_type=device_content_type, enabled=True
        )
        field_z = CustomField.objects.create(name='zzz', type=CustomFieldTypeChoices.TYPE_TEXT)
        field_a = CustomField.objects.create(name='aaa', type=CustomFieldTypeChoices.TYPE_TEXT)
        CustomTabConfigField.objects.create(tab_config=config, field=field_z, weight=100)
        CustomTabConfigField.objects.create(tab_config=config, field=field_a, weight=100)

        mock_obj = MagicMock()
        mock_obj.custom_field_data = {}
        ext = self._get_extension_instance('dcim.device', mock_obj)

        captured = {}

        def capture(template_name, context):
            captured.update(context)
            return 'rendered'

        with patch.object(type(ext), 'render', side_effect=capture):
            ext.full_width_page()

        items = captured.get('items', [])
        assert items[0][1].name == 'aaa'
        assert items[1][1].name == 'zzz'
```

- [ ] **Step 2: Run tests to confirm stub fails new tests**

```bash
pytest tests/test_template_content.py -v
```

Expected: `TestBuildTemplateExtensions` tests fail (stub returns empty list), `TestTabExtensionFullWidthPage` tests error (no `full_width_page` on stub extensions)

- [ ] **Step 3: Replace stub with full `netbox_custom_field_profiles/template_content.py`**

```python
from netbox.plugins import PluginTemplateExtension
from django.contrib.contenttypes.models import ContentType
from .models import CustomTabConfig

BUILTIN_MODELS = [
    'dcim.device',
    'dcim.devicetype',
    'dcim.rack',
    'dcim.site',
    'dcim.location',
    'dcim.cable',
    'virtualization.virtualmachine',
    'virtualization.vminterface',
    'ipam.prefix',
    'ipam.ipaddress',
    'ipam.vlan',
    'circuits.circuit',
]


def _make_extension(model_path):
    class _TabExtension(PluginTemplateExtension):
        model = model_path

        def full_width_page(self):
            app_label, model_name = self.model.split('.')
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
            except ContentType.DoesNotExist:
                return ''

            config = CustomTabConfig.objects.filter(
                content_type=ct, enabled=True
            ).first()
            if not config:
                return ''

            group_entries = [
                ('group', cg.group, cg.weight)
                for cg in config.config_groups.select_related('group').all()
            ]
            field_entries = [
                ('field', cf.field, cf.weight)
                for cf in config.config_fields.select_related('field').all()
            ]
            items = sorted(
                group_entries + field_entries,
                key=lambda x: (x[2], x[1].name),
            )

            return self.render('netbox_custom_field_profiles/tab_panel.html', {
                'config': config,
                'object': self.context['object'],
                'items': items,
            })

    _TabExtension.__name__ = f'CustomFieldProfiles_{model_path.replace(".", "_").title()}'
    _TabExtension.__qualname__ = _TabExtension.__name__
    return _TabExtension


def build_template_extensions(extra_models=None):
    model_list = list(BUILTIN_MODELS)
    if extra_models:
        model_list.extend(extra_models)
    return [_make_extension(m) for m in model_list]


template_extensions = build_template_extensions()
```

- [ ] **Step 4: Run all tests**

```bash
pytest tests/ -v
```

Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add netbox_custom_field_profiles/template_content.py tests/test_template_content.py
git commit -m "feat: implement PluginTemplateExtension for all supported model types"
```

---

### Task 9: Docker Compose Integration Environment

Provides a full NetBox stack for manual end-to-end testing: create configs in the UI, navigate to a Device/IPAddress/etc. detail page, and verify the custom fields panel appears.

**Files:**
- Create: `docker/Dockerfile`
- Create: `docker/configuration.py`
- Create: `docker-compose.yml`
- Create: `Makefile`

- [ ] **Step 1: Create `docker/Dockerfile`**

```dockerfile
FROM ghcr.io/netbox-community/netbox:v4.2-latest

USER root

# Copy plugin source and install as editable so volume-mounted edits are live
COPY . /opt/netbox-custom-field-profiles/
RUN pip install --no-cache-dir -e /opt/netbox-custom-field-profiles/

USER unit
```

> **Note:** Replace `v4.2-latest` with the exact tag you are testing against. Available tags: https://github.com/netbox-community/netbox-docker/pkgs/container/netbox

- [ ] **Step 2: Create `docker/configuration.py`**

```python
ALLOWED_HOSTS = ['*']

DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'netbox',
    'USER': 'netbox',
    'PASSWORD': 'netbox',
    'HOST': 'postgres',
    'PORT': '5432',
    'CONN_MAX_AGE': 300,
}

REDIS = {
    'tasks': {
        'HOST': 'redis',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': 'redis-cache',
        'PORT': 6379,
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    },
}

SECRET_KEY = 'dev-only-insecure-secret-key-do-not-use-in-production'

PLUGINS = ['netbox_custom_field_profiles']

PLUGINS_CONFIG = {
    'netbox_custom_field_profiles': {
        'extra_models': [],
    },
}
```

- [ ] **Step 3: Create `docker-compose.yml`**

```yaml
services:
  netbox:
    build:
      context: .
      dockerfile: docker/Dockerfile
    image: netbox-custom-field-profiles-dev:latest
    ports:
      - '8000:8080'
    environment:
      SUPERUSER_NAME: admin
      SUPERUSER_EMAIL: admin@example.com
      SUPERUSER_PASSWORD: admin
    volumes:
      - .:/opt/netbox-custom-field-profiles
      - ./docker/configuration.py:/etc/netbox/config/configuration.py:ro
      - netbox-media:/opt/netbox/netbox/media
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      redis-cache:
        condition: service_healthy
    restart: unless-stopped

  netbox-worker:
    build:
      context: .
      dockerfile: docker/Dockerfile
    image: netbox-custom-field-profiles-dev:latest
    command: /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py rqworker
    volumes:
      - .:/opt/netbox-custom-field-profiles
      - ./docker/configuration.py:/etc/netbox/config/configuration.py:ro
    depends_on:
      - netbox
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: netbox
      POSTGRES_USER: netbox
      POSTGRES_PASSWORD: netbox
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U netbox']
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 5s
      retries: 5

  redis-cache:
    image: redis:7-alpine
    volumes:
      - redis-cache-data:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  netbox-media:
  postgres-data:
  redis-data:
  redis-cache-data:
```

- [ ] **Step 4: Create `Makefile`**

```makefile
.DEFAULT_GOAL := help

.PHONY: help build up down restart logs shell nbshell migrate superuser clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Build (or rebuild) the dev Docker image
	docker compose build

up:  ## Start the full stack in the background
	docker compose up -d

down:  ## Stop and remove containers (data volumes are preserved)
	docker compose down

restart:  ## Restart all services
	docker compose restart

logs:  ## Tail logs from all services (Ctrl-C to stop)
	docker compose logs -f

shell:  ## Open a bash shell inside the netbox container
	docker compose exec netbox bash

nbshell:  ## Open NetBox's Django shell_plus inside the netbox container
	docker compose exec netbox python /opt/netbox/netbox/manage.py shell_plus

migrate:  ## Run pending database migrations inside the netbox container
	docker compose exec netbox python /opt/netbox/netbox/manage.py migrate

superuser:  ## Interactively create a Django superuser
	docker compose exec netbox python /opt/netbox/netbox/manage.py createsuperuser

clean:  ## Destroy containers, volumes, and the locally-built image
	docker compose down -v --rmi local
```

- [ ] **Step 5: Build the image**

```bash
make build
```

Expected: Build completes without errors; final line: `=> exporting to image`

- [ ] **Step 6: Start the stack**

```bash
make up
```

Expected: All 5 containers reach healthy/running state. Verify with:

```bash
docker compose ps
```

Expected output (all `running` or `healthy`):
```
NAME               STATUS
netbox             running
netbox-worker      running
postgres           healthy
redis              healthy
redis-cache        healthy
```

- [ ] **Step 7: Run migrations inside the container**

```bash
make migrate
```

Expected: `Applying netbox_custom_field_profiles.0001_initial... OK` among the output

- [ ] **Step 8: Verify the plugin is loaded**

```bash
docker compose exec netbox python /opt/netbox/netbox/manage.py shell -c \
  "from netbox_custom_field_profiles.models import CustomTabConfig; print('OK')"
```

Expected: `OK`

- [ ] **Step 9: Open the UI and perform manual smoke test**

Open http://localhost:8000 in a browser. Log in as `admin` / `admin`.

Manual checklist:
- [ ] Navigate to **Customization → Custom Field Profiles** — list page loads
- [ ] Click **Add** — create form opens with Object Type dropdown populated
- [ ] Create a config for **dcim → device**, label `Parameters`, enabled ✓
- [ ] Navigate to any **Device** detail page — custom fields panel section appears with the label `Parameters`
- [ ] Disable the config (edit → uncheck Enabled) — reload the Device page — panel is gone
- [ ] Delete the config — confirm it disappears from the list

- [ ] **Step 10: Stop the stack**

```bash
make down
```

- [ ] **Step 11: Commit**

```bash
git add docker/ docker-compose.yml Makefile
git commit -m "feat: add Docker Compose dev stack and Makefile for integration testing"
```

---

### Task 10: Final Integration Verification

- [ ] **Step 1: Run the full test suite**

```bash
pytest tests/ -v --tb=short
```

Expected: All tests PASS, 0 errors, 0 failures

- [ ] **Step 2: Verify no pending migrations**

```bash
python -m django makemigrations --check --settings=testing.settings
```

Expected: `No changes detected`

- [ ] **Step 3: Verify package is installable from a clean state**

```bash
pip install --dry-run .
```

Expected: No errors

- [ ] **Step 4: Final commit**

```bash
git add .
git commit -m "feat: complete netbox-custom-field-profiles plugin v0.1.0"
```

---

## Spec Coverage Check

| Spec Section | Covered By |
|---|---|
| `CustomTabConfig` model with all fields | Task 2 |
| `CustomTabConfigGroup` through model with weight | Task 2 |
| `CustomTabConfigField` through model with weight | Task 2 |
| Tab rendering via `PluginTemplateExtension.full_width_page()` | Task 8 |
| Groups + fields interleaved by weight, alpha tiebreak | Task 8 |
| Field values from `custom_field_data` | Tasks 7 + 8 |
| `enabled=False` suppresses tab | Task 8 |
| Admin list view with enabled status | Tasks 3 + 5 |
| Admin create/edit/delete views | Tasks 4 + 5 + 7 |
| Create form restricts to supported types, excludes configured | Task 4 |
| Edit form keeps current type selectable | Task 4 |
| Navigation under Customization | Task 6 |
| Built-in supported models (12 types) | Task 8 |
| `extra_models` via `PLUGINS_CONFIG` | Tasks 1 (ready()) + 8 |
| Cascade delete on CustomField/Group/ContentType delete | Task 2 |
| Unit tests, view tests, template extension tests | Tasks 2–5, 8 |
| No database mocking | All test tasks |
| Manual integration test environment (Docker Compose + Makefile) | Task 9 |
