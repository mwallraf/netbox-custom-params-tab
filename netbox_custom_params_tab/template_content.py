from dataclasses import dataclass
from typing import List

from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField
from netbox.plugins import PluginTemplateExtension

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


@dataclass
class GroupItem:
    name: str
    custom_fields: List


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
                ('group', GroupItem(
                    name=cg.group_name,
                    custom_fields=list(CustomField.objects.filter(group_name=cg.group_name)),
                ), cg.weight)
                for cg in config.config_groups.all()
            ]
            field_entries = [
                ('field', cf.field, cf.weight)
                for cf in config.config_fields.select_related('field').all()
            ]
            items = sorted(
                group_entries + field_entries,
                key=lambda x: (x[2], x[1].name),
            )

            return self.render('netbox_custom_params_tab/tab_panel.html', {
                'config': config,
                'object': self.context['object'],
                'items': items,
            })

    _TabExtension.__name__ = f'CustomParamsTab_{model_path.replace(".", "_").title()}'
    _TabExtension.__qualname__ = _TabExtension.__name__
    return _TabExtension


def build_template_extensions(extra_models=None):
    model_list = list(BUILTIN_MODELS)
    if extra_models:
        model_list.extend(extra_models)
    return [_make_extension(m) for m in model_list]


template_extensions = build_template_extensions()
