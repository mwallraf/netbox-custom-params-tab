---
status: complete
quick_id: 261111-cwr
commit: fc571e4
---

# Plugin identity, license and System documentation

Author Maarten Wallraf; MIT license with 2026 copyright; origin configured as
https://github.com/mwallraf/netbox-custom-params-tab.git. No fetch/push/publication.
Added PEP 621 author, README, license and Homepage/Repository/Documentation/
Installation/Issues links; native PluginConfig author and Markdown explanation.
The short user guide explains existing native fields, profiles/Device matching,
shared storage/editing, native validation/permissions and Hidden UI visibility
versus editability. Profile administration UI remains focused on configuration.

Pinned NetBox 4.7 only maps local author/description. URL/license rows and the
Install tab are catalog-owned; project, MIT, guide and installation links are
provided in the supported Description area, without patching core views/templates
or fabricating catalog registration. System > Plugins is native superuser UI.
Links use GitHub HEAD so they follow the repository default branch when published.

Updated Docker build inputs and isolated release-copy inputs for README/LICENSE,
verified wheel metadata and packaged license. No schema or value change.

## Observed checks

- Focused native System page regression: 1 test pass, 5.13 seconds end to end;
  renders native core/plugin.html, author/explanation/visibility guidance and all
  four links; live data unchanged.
- All 35 sandbox helper tests passed.
- Docker image build passed; native services recreated successfully/healthy.
- Runtime/schema/admin-session/API-authentication smoke passed after reload.
- Live local authenticated HTTP GET to /core/plugins/netbox_custom_field_profiles/
  returned author, explanation, user-guide/installation and MIT links:
  LIVE_SYSTEM_PLUGIN_DOCUMENTATION_OK. No browser screenshot is claimed.
- Installed wheel/fresh database suite: 105 tests; metadata/license/assets/import
  provenance/migration checks pass. RELEASE_PROJECT_METADATA_LICENSE_OK,
  RELEASE_RETIRED_UI_ABSENT, RELEASE_LIVE_UNCHANGED and RELEASE_CHECK_OK observed;
  elapsed 123.09 seconds.
- git diff --check passed. Pre-existing Phase 3 COVERAGE.md edit left untouched.

User-confirmed discussion decisions are in 261111-cwr-CONTEXT.md. The quick task
ran inline under the Codex single-agent fallback, on the canonical root branch.
No ROADMAP edit, worktree, branch change, migration, remote push or UAT reopening.
