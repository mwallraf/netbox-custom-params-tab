"""Public identity and documentation used by the System plugin pages."""

PLUGIN_NAME = 'netbox_custom_field_profiles'
PROJECT_URL = 'https://github.com/mwallraf/netbox-custom-params-tab'
DOCS_URL = PROJECT_URL + '/blob/HEAD/docs/README.md'
INSTALLATION_URL = PROJECT_URL + '/blob/HEAD/docs/installation.md'
LICENSE = 'MIT'
SUMMARY = 'Organizes existing Device custom fields into reusable profiles on a Parameters tab.'
DESCRIPTION = (
    'Organizes existing NetBox custom fields into reusable profiles on each matching '
    'Device’s Parameters tab. It creates no field definitions or separate value storage; '
    'viewing and editing use native NetBox fields, permissions and validation.\n\n'
    'To reduce clutter, set a custom field’s UI visibility to Hidden and include it in '
    'a profile. The field remains available in Parameters; native editability still applies.\n\n'
    f'[Documentation]({DOCS_URL}) · '
    f'[User guide]({PROJECT_URL}/blob/HEAD/docs/user-guide.md) · '
    f'[Installation]({INSTALLATION_URL})'
)
