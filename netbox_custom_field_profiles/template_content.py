"""No injected main-page panel; the Parameters tab belongs to a later phase."""

# Import compatibility for inert legacy form classes until schema retirement.
# This list no longer creates or registers any template extension.
BUILTIN_MODELS = [
    'dcim.device', 'dcim.devicetype', 'dcim.rack', 'dcim.site',
    'dcim.location', 'dcim.cable', 'virtualization.virtualmachine',
    'virtualization.vminterface', 'ipam.prefix', 'ipam.ipaddress',
    'ipam.vlan', 'circuits.circuit',
]

# NetBox falls back to this resource even without an explicit PluginConfig path.
template_extensions = []
