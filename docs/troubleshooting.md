# Troubleshooting

## Custom Fields tab is missing

The tab appears only when an enabled profile matches the Device. Check:

- The profile uses Devices as its object type and is enabled.
- Every populated rule matches: Device Type AND role AND tags; selected values
  within one rule match with OR, and a tag rule accepts any selected tag.
- The user has native Device viewing permission, including object constraints.

A matching profile can have no available fields and still show the tab. Profile
administration permission is not required to view Device parameters. An authorized
direct visit without a match displays “No parameter profiles apply to this device.”

## Profile creation fails with a remembered-fields error

“Remembered fields must contain each selected field exactly once” means the
submitted field selection and hidden editor state disagree. JavaScript maintains
that state when fields or modes change. Do not work around it by disabling server
validation.

1. Reload the editor, preferably with a hard refresh after a plugin update.
2. Check that JavaScript is enabled and the “Field ordering controls are loading”
   message disappears.
3. In browser developer tools, confirm the request for
   `/static/netbox_custom_field_profiles/profile_fields.js` succeeds rather than
   returning 404. A query parameter on that URL is expected.
4. Refresh the deployment's plugin static files. For the repository sandbox, run
   `make build` then `make up`; `make smoke` verifies the actual served script
   matches the current source. For another deployment, recollect static files or
   rebuild its custom image using its normal installation process.

This deployment defect was fixed in commit `81067eb` and confirmed by the user.
If the current script loads but the error persists, report the mode, field count,
steps, browser and console/network errors in the [issue tracker](https://github.com/mwallraf/netbox-custom-params-tab/issues).

## Edit Custom Fields is missing or a field cannot be edited

The action requires native Device change permission and at least one matching
editable field. Only active, applicable fields with native **UI editable** set to
Yes are offered. A field containing references the editor cannot view is omitted
as a whole, preserving its complete stored value.

**UI visibility → Hidden** removes a field from normal detail display; it does not
make the field noneditable. Check UI editability separately. Profile matching
never grants access to a Device or reference target.

## A save asks for a reload

The available fields or their native definitions changed while the editor was
open, or the Device changed after the form was rendered. Reload the page, review
the current values and submit again. Validation errors save nothing.

## A profile was disabled after deleting an object

Deleting a referenced Device Type, role or tag disables affected profiles to avoid
accidentally broadening their match. Removing the last valid selected field also
disables a Selected profile. Review its remaining rules/fields and explicitly
re-enable it. See [lifecycle behavior](administration.md#native-changes-and-review).

## URL, license or description looks outdated

The System plugin page uses the plugin's installed code. After upgrading package
metadata or its middleware, restart the NetBox web and worker processes. The
Summary should be one plain sentence, URL should point to the GitHub repository,
License should be MIT, and Description should hold the explanatory text and docs
links. Catalog certification/version history is separate from this local metadata.

[Documentation index](README.md)
