# Testing and verification

## Automated checks

Run from the canonical repository root with the dedicated sandbox running:

```sh
make test
make test-profiles
make release-check
```

| Command | What it establishes |
|---|---|
| `make test` | Helper/configuration guards, native runtime/schema, real session/API authentication, live editor JavaScript delivery and seed idempotence |
| `make test-profiles` | Native plugin behavior in isolated Django/PostgreSQL tests, plus unchanged live native/plugin snapshots |
| `make release-check` | Current wheel assets/license/metadata, installed import provenance, schema drift checks and all native tests on a new temporary test database |

Focus a module while working on a defect:

```sh
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_selection
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_parameter_editing
python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_plugin_documentation
```

The runner rejects an empty suite and requires a test database distinct from the
live database. `PROFILE_LIVE_UNCHANGED`/`RELEASE_LIVE_UNCHANGED` confirm the compared
native/plugin data did not change. A failing command is not a pass even if a marker
appears earlier. Use the actual output for test counts/timing; they change as
regressions are added. Never restart services during a test run.

The installed-wheel check builds in a temporary source copy, installs into a
temporary target, checks the import path and runs with a fresh uniquely named
native test database. Normal test teardown removes that database; temporary files
are removed. It does not replace the running sandbox's editable installation.
Registry access is needed for an uncached setuptools build dependency.

## Manual regression workflow

Use the dedicated sandbox at <http://127.0.0.1:18047> with disposable sample
Devices, fields, profiles and constrained users. Use an isolated fixture or record
a baseline before changing existing sample objects, then restore them afterward.
Do not use `make reset` as a cleanup shortcut. Generated credentials are in the
ignored local `.env`; keep them out of screenshots and logs.

1. Create CMTS and CPE sample Devices with distinct types/roles and known tags.
2. Create a 20–30-field CMTS profile, a two-field CPE profile, a shared profile,
   and an All profile, using native Device-applicable field definitions.
3. Verify AND across populated rules, OR within values, tag-any matching, disabled
   profiles, Selected/All ordering and newly created native-field inclusion.
4. View Custom Fields with unset values, false/zero, all native types, duplicate
   fields, long URLs/text, Markdown and wide JSON. Check desktop/narrow readability,
   help, keyboard focus and local overflow.
5. Edit Custom Fields: one input per native field, native widget/type/required/range/
   regex/choice/uniqueness errors, Save/Cancel, stale-form rejection and identical
   repeated values after save. Confirm unrelated native data/settings remain intact.
6. Check viewer/editor/denied/constrained users on navigation, direct URLs and
   POSTs. Related-object permissions are independent of Device permissions.
7. Change a value through native Device editing or a native script/API operation;
   the next Custom Fields request must show it. Save through Custom Fields and confirm
   native consumers see the same value and native change log.
8. Recheck profile ordering/mode switching through pointer and keyboard controls,
   invalid-form recovery, unused-tag search and no-JavaScript/error guidance.
9. Inspect System → Plugins: short Summary, rich Description/docs links, project
   URL, MIT License, correct name and author. Confirm another plugin is unaffected.

Record steps, actual outcomes, browser/viewport and sample IDs. For detailed
historical case matrices, see the [historical Parameters UAT record](../../.planning/phases/03-parameters-tab/03-UAT.md)
and [editing UAT record](../../.planning/phases/04-edit-parameters/04-UAT.md).
The Phase 3-only “no Edit Parameters action” case was superseded by the authorized
Phase 4 editor; the Custom Fields GET view itself still rejects POST.

## Existing acceptance and known scope

The user reported final manual UAT passed on 2026-11-11. The subsequent single-field
profile-create deployment defect was fixed and separately confirmed by the user.
Those are user-reported results, not invented agent browser runs. The two public
README screenshots were supplied by the user. Earlier deferral notes in historical
planning files do not describe an outstanding UAT block.

Phase 4/5 Nyquist-record gaps and completion-metadata debt were explicitly accepted
by the user. This guide does not create missing validation records or claim they
were audited. Maintainer verification for later changes remains separate from the
accepted milestone's original evidence.

## Historical pytest suite

The top-level `tests/test_*.py` and `testing/` files describe the retired panel
implementation. They are retained historical inputs, not the required current
feature suite and not claimed passing. `make test-legacy` reports its actual
outcome in ignored `.sandbox/legacy-tests.json`; previous baseline runs reported
pytest unavailable. Installing the optional `[test]` extra does not make those
old model/SQLite assumptions valid for current profiles. Port a relevant test to
the native plugin-owned suite instead of treating legacy collection as acceptance.

[Maintainer index](README.md) · [Sandbox](sandbox.md)
