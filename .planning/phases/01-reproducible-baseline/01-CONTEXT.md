# Phase 1: Reproducible baseline - Context

**Gathered:** 2026-11-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix repository usability first, then deliver a dedicated Docker NetBox sandbox
with the renamed plugin installed and registered. Provide repeatable Makefile
setup and startup checks. Profile functionality is not required to work in this
phase. Do not implement profile administration, matching, the Parameters tab, or
value editing here.
</domain>

<decisions>
## Implementation Decisions

### Compatibility
- **D-01:** NetBox 4.7.x is the minimum supported release line. Research and pin a
  suitable exact 4.7 patch/container combination for the baseline; do not infer
  verified compatibility with all later releases.

### Source and Git workflow
- **D-02:** Fix current Git issues before sandbox implementation.
- **D-03:** Use the normal project checkout and one branch per milestone. Do not
  use worktrees or create a branch per phase as the default workflow.
- **D-04:** Reconcile existing implementation and rename changes into the usable
  checkout before retiring stale worktree metadata. The user's statement that
  nothing needs preservation concerns application installations/data, not a
  request to discard source code or the requirements/planning history.

### Sandbox isolation and data
- **D-05:** Create a new sandbox dedicated to this project. Leave the NetBox
  already running on the workstation untouched.
- **D-06:** Use a separate Compose project, network, and volumes with a
  configurable localhost-bound host port to avoid conflicts.
- **D-07:** This plugin is completely new and not deployed. No existing plugin
  configuration or application data needs an upgrade/migration path. A clean
  sandbox database and generated dummy data are acceptable. Still verify clean
  schema creation and migrations for the renamed plugin.
- **D-08:** Normal stop/start preserves sandbox data and generated credentials.
  An explicit reset can recreate dummy data in this project's sandbox only.

### Orchestration and configuration
- **D-09:** Docker is the standard environment for running and testing NetBox.
- **D-10:** Provide a Makefile to orchestrate installation and the sandbox
  lifecycle, including repeatable setup, startup, shutdown, testing, and explicit
  reset. Reuse existing commands where appropriate.
- **D-11:** Automatically generate required passwords, tokens, and application
  secrets. Store sandbox configuration and generated secrets in a local `.env`
  file excluded from Git; avoid regenerating credentials on ordinary restart.
  A tracked example/configuration guide must not contain actual generated secrets.
- **D-12:** Use native NetBox plugin parameters for plugin behavior. The user
  delegated the exact split between environment settings and plugin parameters.

### Completion and test baseline
- **D-13:** Phase 1 is complete when NetBox boots, migrations apply, the renamed
  plugin installs/registers successfully, and admin login works in the sandbox.
- **D-14:** Plugin feature behavior may remain unfinished. Run/document existing
  tests and establish repeatable startup/install checks; feature failures may be
  explicitly documented and deferred to their implementation phases. Do not
  require the legacy feature suite to be entirely green to finish this phase.
- **D-15:** Never treat a failure that prevents startup, migration, plugin
  registration, or admin login as an acceptable deferred feature failure.

### Agent's Discretion
- Exact 4.7 patch and compatible Docker image selection after official-source research.
- Compose project name, available default port, service names, and Make target names.
- Secure generation mechanism, local .env structure, and plugin-setting mapping.
- Small useful dummy dataset and repeatable seed/reset implementation.
- Concrete safe Git consolidation sequence and milestone branch name.
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Product and phase scope
- `docs/REQUIREMENTS.md` — authoritative product requirements.
- `.planning/PROJECT.md` — agreed project boundaries and identity.
- `.planning/REQUIREMENTS.md` — BASE-01 through BASE-04; interpret baseline
  verification using D-13 through D-15 above.
- `.planning/ROADMAP.md` — Phase 1 goal/dependencies; no feature execution here.

### Existing implementation and environment
- `.planning/codebase/STACK.md` — declared versions and Docker stack.
- `.planning/codebase/STRUCTURE.md` — source/worktree layout and caveats.
- `.planning/codebase/CONCERNS.md` — Git, migration, and testing concerns.
- `.worktrees/feature/implement-plugin/Makefile` — existing lifecycle commands.
- `.worktrees/feature/implement-plugin/docker-compose.yml` — existing dev stack.
- `.worktrees/feature/implement-plugin/docker/Dockerfile` — old image/install setup.
- `.worktrees/feature/implement-plugin/docker/configuration.py` — existing settings.
- `.worktrees/feature/implement-plugin/netbox_custom_field_profiles/migrations/0001_initial.py`
  — handwritten migration requiring verification/replacement on the clean sandbox.

No external version documentation was chosen during discussion; verify official
NetBox and netbox-docker documentation during research.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Existing Docker Compose stack provides NetBox, worker, PostgreSQL, and Redis.
- Existing Makefile has build/up/down/migrate/shell/log commands.
- Renamed package metadata, plugin entry point, tests, and migrations exist.

### Established Patterns
- Plugin is loaded through NetBox configuration and editable package installation.
- Current Docker config uses development literals that must move to .env inputs.
- Existing SQLite test settings are not a proven NetBox runtime test baseline.

### Integration Points
- Source is currently in an ignored worktree with stale .git links; consolidate
  into the normal checkout before further implementation.
- Keep GSD planning and product requirements available after consolidation.
- Update plugin registration, packaging, schema, and environment together so the
  renamed plugin can boot without implementing the new profile features.
</code_context>

<specifics>
## Specific Ideas

The user requested: “Netbox should be up & running with the plugin installed
(not working).” This sets the baseline acceptance boundary, not permission to
ship startup failures. Dummy data belongs exclusively to this project's sandbox.
</specifics>

<deferred>
## Deferred Ideas

- Profile model, administration, selection modes, and filters: Phase 2.
- Parameters tab and native field presentation: Phase 3.
- Native custom field value editing: Phase 4.
- Full functional acceptance and release verification: Phase 5.
- No new capabilities were added outside the existing roadmap.
</deferred>

---
*Phase: 01-reproducible-baseline*
*Context gathered: 2026-11-06*
