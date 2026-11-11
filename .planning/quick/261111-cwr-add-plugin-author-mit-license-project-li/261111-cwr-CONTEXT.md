# Confirmed user decisions

- Author: Maarten Wallraf.
- Project and origin remote: https://github.com/mwallraf/netbox-custom-params-tab.
- License: MIT; create LICENSE.
- Explain native fields/no separate value storage and native Hidden UI visibility.
- Documentation belongs in System > Plugins, not profile management pages.
- Pinned NetBox 4.7 maps only local author/description into the System page;
  catalog-only URL/license/Install fields cannot be populated by adding config
  attributes. Supply links in the supported Markdown Description and proper
  package metadata; do not patch native views or replace core templates.
- Native editing is supported; describe it accurately, not as display-only.
