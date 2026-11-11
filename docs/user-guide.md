# Custom Field Profiles: user guide

Custom Field Profiles organizes existing NetBox custom fields into relevant
sections on a Device’s **Parameters** tab. For example, a CMTS can show 20–30
fields while a CPE shows only two, with a shared profile visible on both.

## Your fields and values stay in NetBox

Create field definitions through NetBox’s built-in **Custom Fields** administration.
This plugin stores profile configuration: field selections, order and matching
rules. It creates no field definitions and has no separate field-value storage.
**Edit Parameters** writes the same native values used by normal NetBox editing,
scripts and APIs, with native permissions and validation.

## Configure a profile

1. Open **Plugins → Custom Field Profiles** and add a profile for Devices.
2. Give its section a title and display order.
3. Choose **Selected fields** and arrange them, or **All applicable fields** to
   include new Device-applicable fields automatically.
4. Optionally filter by Device Type, device role or tags. Different rules combine
   with AND; selected values within a rule combine with OR. A tag rule matches any
   selected tag. No rules means all Devices.
5. Enable the profile and save. Each matching enabled profile becomes a section
   on the Device’s Parameters tab.

The same field can appear in several sections. **Edit Parameters** offers one
input for it, and every occurrence displays the same saved native value. Viewing
or editing Device values does not require profile administration permission.

## Reduce clutter on the main Device page

Edit a native custom field and set **UI visibility** to **Hidden** if you want to
remove it from the normal detail display. Include that field in a profile to keep
it visible on the Device’s Parameters tab. The plugin does not change visibility
settings for you, and native visibility settings can affect other applicable
object types too.

Visibility and editability are separate: keep **UI editable** enabled if users
should edit the field through **Edit Parameters**. Native noneditable/hidden edit
settings and object permissions remain authoritative. Profile matching never
grants access to a Device or a referenced object.

## Where to find more information

Open **System → Plugins → Custom Field Profiles** for the author, explanation and
project/documentation links. In NetBox 4.7, the dedicated URL/license rows and
catalog Install tab are populated by catalog entries; a local installation exposes
these links in its native Description area instead.

- [Installation and supported runtime](development/installation.md)
- [Detailed profile administration](development/profiles.md)
- [Project and issue tracker](https://github.com/mwallraf/netbox-custom-params-tab)
- [MIT license](../LICENSE) — Maarten Wallraf
