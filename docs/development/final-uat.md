# Final manual acceptance

Browser UAT is owned by the user and deferred to project end by instruction on
2026-11-10. Automated passes do not mark these cases passed.

## Environment

Use the dedicated sandbox at <http://127.0.0.1:18047>. Start it with `make up` if
needed. Administrator credentials are in the local ignored `.env`. Do not include
credentials in evidence. Tests below change sample values: use disposable Devices,
fields and profiles created specifically for acceptance, and remove only those
objects when finished. Do not use `make reset` as a cleanup shortcut.

Create a sample CMTS Device and CPE Device with distinct Device Types/roles and
known tags through native administration. Create Device-applicable native fields
using NetBox Custom Fields, then profile configuration at
<http://127.0.0.1:18047/plugins/custom-field-profiles/>:

- CMTS Selected profile: 20–30 fields, matched to the CMTS Device Type.
- CPE Selected profile: two fields, matched to the CPE Device Type.
- Shared Selected profile: no rules, with a field repeated in CMTS/CPE.
- All profile: active Device fields, matched to one sample Device.

Include representative text/longtext, integer/decimal, boolean, date/datetime,
URL, JSON, select/multiselect, object/multiobject fields. Include unset values,
false/zero, long URLs, multiline Markdown and wide JSON. Create an authorized
Device editor, a Device-only viewer, and a viewer/editor constrained to one sample
Device using native object permissions. Reference-target viewing permissions must
be granted separately. None needs profile administration permission to view/edit
Device parameter values.

## Cases

1. Run the 15 Parameters cases in
   `.planning/phases/03-parameters-tab/03-UAT.md` at 1440×900 and 390×844.
   Phase 3’s historical no-edit-action expectation is superseded by Phase 4:
   only authorized editors with editable matching fields see Edit Parameters.
   The Parameters destination itself remains a read-only GET.
2. Run the eight editing cases in
   `.planning/phases/04-edit-parameters/04-UAT.md`.
3. End to end: CMTS sees CMTS/shared; CPE sees CPE/shared. Test Device Type OR,
   role AND, and tag-any matching. Add an applicable native field: All picks it
   up on reload, Selected stays unchanged. Duplicate fields display repeatedly
   but have one edit input. Save and confirm native values and unrelated values.
4. Change a native field value through ordinary native Device editing or a
   native script/API operation. Reload Parameters: every repeated row updates.
   Change it through Edit Parameters: native Device editing/API reads the same
   value. Check native change logging; no profile save/import is needed.
5. Confirm profile changes and parameter edits leave native visibility/settings,
   field definitions and unrelated Device data unchanged. Restore the sample
   values/remove only acceptance-owned sample objects afterward.

Record pass/fail with actual browser/version, viewport, sample IDs, observations
and redacted screenshots. Report defects with reproduction steps. No case has
been visually observed in this implementation session.

## Automated verification

`make test-profiles` runs the source checkout in native Django/PostgreSQL, using
an isolated test database and checking that live native/plugin data is unchanged.
`make test` checks sandbox guards, native schema/runtime, authentication and seed
idempotence. `make release-check` builds the current package in a temporary source
copy, checks wheel assets, installs to a temporary target, verifies import
provenance and runs the native suite against a fresh temporary test database.
It needs the declared setuptools build dependency (registry access if uncached).
The temporary install does not replace the sandbox's editable installation.

The supported exercised runtime is NetBox 4.7.4 / Docker packaging 5.1.1.
Other versions and the optional historical pytest suite are not verified. No
legacy installation upgrade mapping is supported; this is the agreed new-install
milestone. Final acceptance and milestone archival wait for manual observations.

## Acceptance status — 2026-11-11

Final manual UAT passed by the user’s overall sign-off (“ok, pass UAT”). Earlier
deferral/pending descriptions are historical. No agent browser run or screenshots
are claimed. All five phases are accepted; milestone audit/archival is next.
