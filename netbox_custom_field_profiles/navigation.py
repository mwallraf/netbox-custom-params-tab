from netbox.plugins.navigation import PluginMenuItem, PluginMenuButton
from netbox.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_custom_field_profiles:customfieldprofile_list',
        link_text='Custom Field Profiles',
        permissions=['netbox_custom_field_profiles.view_customfieldprofile'],
        buttons=(
            PluginMenuButton(
                link='plugins:netbox_custom_field_profiles:customfieldprofile_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['netbox_custom_field_profiles.add_customfieldprofile'],
            ),
        ),
    ),
)
