from netbox.plugins import PluginTemplateExtension  # noqa: F401

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
