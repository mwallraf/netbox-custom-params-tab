from netbox.plugins.navigation import PluginMenuItem, PluginMenuButton
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_custom_params_tab:customtabconfig_list',
        link_text='Custom Params Tab',
        permissions=['netbox_custom_params_tab.view_customtabconfig'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_custom_params_tab:customtabconfig_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_custom_params_tab.add_customtabconfig'],
            ),
        ),
    ),
)
