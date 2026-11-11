# Selected-fields profile creation failure

Reported 2026-11-11: enabled Device profile with a title, order and one selected
field, no rules, fails with “Remembered fields must contain each selected field
exactly once.”

## Evidence and cause

- Source JavaScript updates field_order and remembered_fields on selection changes
  and form submission. Server validation checks consistency before saving.
- Live GET /static/netbox_custom_field_profiles/profile_fields.js returned HTTP 404.
- Pinned image STATIC_ROOT is /opt/netbox/netbox/static. Upstream image collected
  its own assets before installing this plugin; no plugin directory existed in
  STATIC_ROOT. The Dockerfile installed the package but did not publish its assets.
- A new live profile-asset smoke check failed before the Docker fix with
  “profile ordering JavaScript missing or stale; rebuild the sandbox image”.

## Fix

Copy the installed plugin's static directory into the pinned image's native static
root during the build. Add a version query to invalidate older cached script
responses. Keep strict server validation intact. The baseline smoke now fetches
the actual authenticated editor, follows its local script reference and compares
the served script to source, rejecting 404/stale assets. Add guards for missing/
stale assets plus the exact one-field enabled/no-rules native create payload.

Rebuild/recreate only the dedicated sandbox, preserving its DB and credentials.
Do not modify unrelated input screenshots or the pre-existing COVERAGE.md edit.

## Verification and resolution

Resolved 2026-11-11. Docker build and sandbox service recreation passed.
Before the image fix, both direct HTTP asset GET (404) and the new live smoke
check failed. After the fix, make test passed all 37 helper regressions and
CONFIG_OK / RUNTIME_OK / PROFILE_ASSETS_HTTP_OK / BASELINE_SMOKE_OK /
SEED_IDEMPOTENT_OK. The actual editor references ?v=2 and its served JavaScript
exactly matches the source with selection/order/remembered synchronization.

make test-profiles passed 106 native tests in 20.074s (24.53s end to end), including
the new enabled/Selected/one-field/no-rules create regression and existing
Selected/All/remembered-state round trips. PROFILE_TESTS_ISOLATED and
PROFILE_LIVE_UNCHANGED observed. No native field definitions or user profile data
were changed by verification; no browser interaction was claimed.

Hard-refresh the profile creation page after deployment. No validation relaxation,
new migration or remote push. For other deployments, publish/collect plugin static
assets as documented during installation; the image fix applies to this repository
sandbox.

## User confirmation — 2026-11-11

User retried the workflow and confirmed: “it works, confirmed”. The reported
one-field Selected-profile creation bug is closed with automated and manual
confirmation.
