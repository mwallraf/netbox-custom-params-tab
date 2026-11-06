# Phase 1: Reproducible baseline - Research

**Researched:** 2026-11-06
**Domain:** NetBox 4.7 Docker sandbox and source consolidation
**Confidence:** MEDIUM — official versioned sources were inspected; no project image was built or application started.

<user_constraints>
## User Constraints (from CONTEXT.md)

The following decisions are copied verbatim from `01-CONTEXT.md`; they are user requirements, not externally verified implementation claims.

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

### Deferred Ideas
- Profile model, administration, selection modes, and filters: Phase 2.
- Parameters tab and native field presentation: Phase 3.
- Native custom field value editing: Phase 4.
- Full functional acceptance and release verification: Phase 5.
- No new capabilities were added outside the existing roadmap.
</user_constraints>

## Project Constraints (from AGENTS.md)

- Read `docs/REQUIREMENTS.md` before planning/implementation; it supersedes conflicting earlier design assumptions. [VERIFIED: AGENTS.md:3-6] Verbatim: `Read docs/REQUIREMENTS.md before planning or implementing changes` (Markdown backticks omitted).
- Read GSD state, roadmap, and traceable requirements; consult README and CLAUDE background. [VERIFIED: AGENTS.md:7-12] Verbatim filenames: `.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `README.md`, `CLAUDE.md`.
- Do not infer feature implementation authorization from requirements; preserve existing uncommitted implementation work and do not prune the stale worktree. [VERIFIED: AGENTS.md:14-20] Verbatim: `Preserve its existing uncommitted changes.`
- No project-local skills were found at the two checked discovery locations; this is an observation, not proof that no skills exist elsewhere. [VERIFIED: research command `ls -d .codex/skills .agents/skills` on 2026-11-06]

## Summary

Use the published image `netboxcommunity/netbox:v4.7.4-5.1.1` as the initial exact baseline, with its native Docker bootstrap/configuration machinery. The versioned image tag is listed on the official Docker Hub repository; NetBox release 4.7.4 was published October 27, 2026, and NetBox Docker 5.1.1 explicitly supports the 4.7 line. [CITED: https://hub.docker.com/r/netboxcommunity/netbox/tags] [CITED: https://github.com/netbox-community/netbox/releases/tag/v4.7.4] [CITED: https://github.com/netbox-community/netbox-docker/releases/tag/5.1.1]

Consolidate source first, then build one thin working path: dedicated Compose services → migrations → registered plugin → generated administrator → successful session login. Preserve startup checks as blocking; record legacy feature-suite failures separately. This decomposition follows the locked D-02 and D-13–D-15 decisions above. [VERIFIED: .planning/phases/01-reproducible-baseline/01-CONTEXT.md:26-34,67-76] Verbatim decision IDs: `D-02`, `D-13`, `D-14`, `D-15`.

**Primary recommendation:** build the isolated, reproducible startup path before expanding lifecycle/reset/seed/test reporting; keep all profile features out of this phase. [ASSUMED: recommended planning decomposition under delegated discretion]

<phase_requirements>
## Phase Requirements

| ID | Behavior | Research support |
|---|---|---|
| BASE-01 | Usable checkout preserving source | Current orphaned-source observation; verified copy plus Git snapshot before retirement |
| BASE-02 | Supported reproducible Docker environment | Published 4.7.4/5.1.1 pair, versioned official Compose, Make orchestration |
| BASE-03 | Renamed plugin registers and migrations work | Native PluginConfig paths, DEVELOPER migration support, clean database policy |
| BASE-04 | Repeatable baseline and known failure report | Startup/auth/schema gate, infrastructure tests, separate legacy feature result |

Requirement identifiers and wording derive from `.planning/REQUIREMENTS.md:16-19`; verbatim IDs: `BASE-01`, `BASE-02`, `BASE-03`, `BASE-04`. [VERIFIED: .planning/REQUIREMENTS.md:16-19]
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary tier | Secondary tier | Rationale |
|---|---|---|---|
| Git/source reconciliation | Developer tooling | Filesystem | Complete before application changes |
| Install/lifecycle/config | Host Make + small helper scripts | Compose | One repeatable entry point, fixed project identity |
| Plugin loading and schema | NetBox/Django backend | PostgreSQL | Use native app registration and migrations |
| Admin/token bootstrap | Native image initialization | NetBox user models | Avoid custom authentication infrastructure |
| Login verification | HTTP client against real sandbox | Native Django session | Page availability alone is insufficient |
| Dummy devices/fields | Native NetBox ORM | Dedicated sandbox DB | Seed idempotently; no production linkage |

This is the recommended responsibility assignment, not implemented architecture. [ASSUMED: planning recommendation]

## Standard Stack

| Component | Baseline | Evidence / instruction |
|---|---|---|
| NetBox | 4.7.4 | Released 2026-10-27 [CITED: https://github.com/netbox-community/netbox/releases/tag/v4.7.4] |
| NetBox Docker | 5.1.1 | Its release declares compatibility with 4.7.x and later [CITED: https://github.com/netbox-community/netbox-docker/releases/tag/5.1.1] |
| Application image | `netboxcommunity/netbox:v4.7.4-5.1.1` | Published tag; pin this exact pair and record pulled digest during execution [CITED: https://hub.docker.com/r/netboxcommunity/netbox/tags] |
| Python | Container interpreter, >=3.12 | NetBox's versioned metadata explicitly declares this floor [CITED: https://raw.githubusercontent.com/netbox-community/netbox/v4.7.4/pyproject.toml] |
| PostgreSQL/cache | Start from versioned upstream Compose | 5.1.1 uses PostgreSQL 18 and Valkey 9.1; follow its matching volume layout [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/docker-compose.yml] |
| Installer | Image's existing uv | No extra latest uv copy needed; the upstream image already includes it [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/Dockerfile] |
| Baseline test harness | Python stdlib + NetBox/Django runtime | Avoid adding packages solely for setup checks [ASSUMED: recommendation] |

Do not advertise every NetBox release >=4.7 as tested. Set the plugin minimum to 4.7.0, pin the sandbox to 4.7.4, and state the actually tested patch. The current minimum is explicitly `min_version = '4.0.0'`. [VERIFIED: .worktrees/feature/implement-plugin/netbox_custom_field_profiles/__init__.py:4-12] NetBox's documented min_version attribute enforces the floor. [CITED: https://netboxlabs.com/docs/netbox/plugins/development/]

### Package Legitimacy Audit

No new runtime Python package is recommended: install the local plugin into the upstream image, whose framework dependencies are already supplied. [ASSUMED: scope recommendation] Existing optional test extras are verbatim `"pytest"`, `"pytest-django"`. [VERIFIED: .worktrees/feature/implement-plugin/pyproject.toml:12-16]

The GSD PyPI legitimacy probe for those existing test extras returned `SUS` solely with null metadata (`exists`, age, downloads, repository) and reasons `unknown-age`, `unknown-downloads`, `no-repository`. This is **an unavailable audit**, not evidence that the projects are malicious. Do not add new dependency installation based on this probe. The planner can use stdlib infrastructure tests and run the legacy suite only after verifying its already-declared extras from their official sources/registry during execution. [VERIFIED: `query package-legitimacy check --ecosystem pypi pytest pytest-django`, 2026-11-06]

## Architecture Patterns

### Git recovery and canonical source

Observed now: `git worktree list --porcelain` lists only the main checkout; the previously recorded linked-worktree administration directory is absent. The source directory remains present with a stale `.git` pointer. The feature branch still resolves to `42ad9c2`. These are read-only observations from this session; older maps describe an earlier metadata state. [VERIFIED: `git worktree list --porcelain`, `git rev-parse --git-common-dir`, `git log feature/implement-plugin -1`, 2026-11-06]

The stale pointer's verbatim value is `gitdir: /Users/mwallraf/Documents/dev/netbox-custom-params-tab/.git/worktrees/implement-plugin`. [VERIFIED: .worktrees/feature/implement-plugin/.git:1]

Recommended sequence: inventory/hash the current source snapshot; create the milestone branch in the normal checkout during execution; integrate the existing implementation history without overwriting root GSD/docs; overlay the renamed/uncommitted source; verify every retained source file; commit the canonical source before removing the orphaned snapshot. A full-tree merge may conflict with the newer documentation; resolve by preserving authoritative root documents. Do not reset to the old feature branch or blindly copy nested README/docs over current files. [ASSUMED: recovery procedure tailored to observations]

Git documents repair for moved linked worktrees, but its description presumes repairable administration links. It does not justify discarding orphaned source. Since current administration metadata is absent, plan verified reconciliation rather than assuming repair alone solves this checkout. [CITED: https://git-scm.com/docs/git-worktree]

### Compose isolation and environment

Use one explicit project identity on every Make target. Compose project names isolate environments; `-p` has higher precedence than ambient project-name configuration. Use project-scoped named volumes/network, no fixed global container names, no external/shared volumes, and expose only the web port on localhost. [CITED: https://docs.docker.com/compose/how-tos/project-name/]

Generate a gitignored `.env` once, with restrictive local permissions and a tracked placeholder-only example. Reuse nonempty existing values. Use explicit environment injection because Compose interpolation and container environments are separate concerns; use `config --quiet` for validation to avoid printing resolved secrets. [CITED: https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/]

Use stdlib `secrets` for cryptographic randomness, with an alphabet safe for dotenv parsing. Do not shell-source untrusted configuration or interpolate secrets into command text. [CITED: https://docs.python.org/3/library/secrets.html] The precise file format/helper path is delegated implementation design. [ASSUMED: recommendation]

### Native image bootstrap and plugin loading

The 5.1.1 image includes uv and the virtual environment, with working directory at the NetBox project. Extend that image and install the local plugin editable into its existing interpreter. Preserve the image's launcher rather than recreate the application server. [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/Dockerfile]

Use a small additional plugin configuration file; upstream's loader reads the main configuration then additional Python configuration files. Retain upstream environment-driven database/cache settings instead of replacing the entire configuration with the repository's old hard-coded file. [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/docker/configuration.docker.py]

Plugin resource paths are relative to the plugin package: versioned PluginConfig loads resources by prefixing its own module. The repository's relative `template_content.template_extensions` and `navigation.menu_items` declarations already follow that convention; do not regress to doubly qualified paths. [CITED: https://raw.githubusercontent.com/netbox-community/netbox/v4.7.4/netbox/netbox/plugins/__init__.py] [VERIFIED: .worktrees/feature/implement-plugin/netbox_custom_field_profiles/__init__.py:10-12] Verbatim: `template_extensions = 'template_content.template_extensions'`, `menu_items = 'navigation.menu_items'`.

### Migrations on the disposable sandbox

Use native developer mode and supported makemigrations. Official docs require `DEVELOPER=True` for migration generation; this avoids the existing custom command that bypasses NetBox safeguards. [CITED: https://netboxlabs.com/docs/netbox/plugins/development/models/]

The existing migration warns verbatim: `This migration was hand-crafted because NetBox was not installed at` and lists missing manager/encoder fidelity. Regenerate or repair it in the actual 4.7 environment before applying to the clean plugin sandbox; verify no drift afterwards. No legacy deployed-data upgrade path is required by D-07. [VERIFIED: .worktrees/feature/implement-plugin/netbox_custom_field_profiles/migrations/0001_initial.py:1-10]

The native image entrypoint waits for database access, applies pending migrations, performs initialization, and creates a configured superuser before launching NetBox. Use this path; a migration failure must block readiness. [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/docker/docker-entrypoint.sh]

### NetBox 4.7 administrator and token bootstrap

Use native SUPERUSER environment bootstrap, including the separate API key/token and pepper inputs. It creates the account only when absent; if the account already exists, it exits without rotating/reconciling its token. Therefore generated credentials must remain stable across restart, and smoke checks should detect mismatch rather than silently reset passwords. [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/docker/super_user.py]

4.7 v2 token authentication uses a bearer credential combining a prefix/key and raw token, not the legacy Token header alone. Source constants specify prefix `nbt_`, key length 12, and default token length 40; generate alphanumeric key/token values accordingly and retain the pepper. [CITED: https://raw.githubusercontent.com/netbox-community/netbox/v4.7.4/netbox/users/constants.py] Token.get_auth_header_prefix supplies the bearer prefix; use that native representation in the smoke helper. [CITED: https://raw.githubusercontent.com/netbox-community/netbox/v4.7.4/netbox/users/models/tokens.py]

### Lifecycle and reset

Normal down preserves named volumes; `down --volumes` removes project-declared volumes. Keep reset separate and restrict it to the pinned project identity. Never run global Docker prune. Reset may recreate dummy data using the same local credentials. [CITED: https://docs.docker.com/reference/cli/docker/compose/down/]

## Don't Hand-Roll

| Problem | Use instead | Reason/evidence |
|---|---|---|
| Application process startup | Native image CMD/entrypoint | Includes migration/bootstrap sequencing [CITED: upstream docker-entrypoint.sh above] |
| Password/token hashing | NetBox bootstrap/models | Matches current 4.7 token/pepper behavior [CITED: super_user.py and tokens.py above] |
| Schema generation | Native Django makemigrations with developer mode | Documented plugin development path [CITED: model docs above] |
| Environment isolation | Compose project namespace | Official isolation mechanism [CITED: Compose project docs above] |
| Random credential generation | Python secrets | OS-backed cryptographic randomness [CITED: Python secrets docs above] |

## Runtime State Inventory

| Category | Observed state | Action |
|---|---|---|
| Stored data | User explicitly says new/not deployed; no plugin data preservation required | Clean project DB; do not connect to existing workstation NetBox |
| Live service config | Existing workstation NetBox is user-reported; not inspected or changed | Separate project/network/volumes/port; no mutations outside project |
| OS registrations | Not audited; no phase requirement to alter them | Do not claim none exist; no global service changes |
| Secrets/env | Root ignore includes `.env`; old Docker configuration has literals | Generate new project-only secrets; do not read/reuse other NetBox credentials |
| Build/installed artifacts | Nested egg-info/bytecode may retain old name; old image reference is in Dockerfile | Exclude generated artifacts, rebuild/reinstall renamed local plugin |

The ignore value `.env` is verbatim in root `.gitignore:9`; container source verbatim `FROM netboxcommunity/netbox:v4.6-5.0.1` appears in `.worktrees/feature/implement-plugin/docker/Dockerfile:1`. [VERIFIED: those files opened this session]

## Common Pitfalls

- **Confusing core version and Docker packaging version:** pin both halves of the published tag. The image README defines their independent meanings. [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/README.md]
- **Copying old configuration wholesale:** loses new upstream settings such as token peppers. Keep the native configuration and add a minimal plugin file. [CITED: https://raw.githubusercontent.com/netbox-community/netbox-docker/5.1.1/configuration/configuration.py]
- **Passing only the old token variable:** native v2 bootstrap also requires API key and pepper configuration. [CITED: super_user.py above]
- **Calling a login GET an auth test:** it proves only page availability. Submit an actual CSRF-aware login and verify an authenticated page/session, then test the generated API credential separately. [ASSUMED: acceptance-test design]
- **Feature tests hiding startup failures:** separate the blocking startup/migration/register/login smoke command from the legacy test report; capture collection/setup failures honestly. [ASSUMED: test design enforcing D-14/D-15]
- **Treating unknown metadata as incompatible:** a failed registry/source fetch cannot prove absence. Current sources do positively establish the proposed baseline image. [CITED: Docker Hub tag listing above]

## Code Examples

These are proposed commands after consolidation, not claims that targets already exist. [ASSUMED: proposed Make contract]

```text
make setup            # generate/reuse env, build, initialize, start
make check            # short static/env checks without emitting secrets
make smoke            # running instance: migrations/register/login/token
make test             # blocking infrastructure tests
make test-legacy      # capture actual feature-suite status separately
make down             # retain data and credentials
make reset            # explicit project-only DB/seed reset
```

Verified native command patterns to use inside the project service: run the container interpreter with manage.py `check`, `migrate --check`, and `makemigrations <plugin> --check --dry-run`; exact Make wrapper/script implementation is planner-owned. [CITED: migration docs and Docker entrypoint above] Do not print full settings, environment, request headers, passwords, or tokens to test output. [ASSUMED: safeguard implementing D-11]

## Environment Availability

| Dependency | Observation this session | Fallback/action |
|---|---|---|
| Git | 2.56.0; read-only connectivity fsck completed without output/errors | Use explicit staging; no reset/prune recovery |
| Docker CLI/daemon | 29.9.2; daemon read succeeded after sandbox escalation | Future Docker actions may require sandbox approval |
| Compose | v5.6.1 | Available; verify target command flags during execution |
| Make | GNU Make 3.81 | Use portable Make syntax |
| Context7 | MCP tool absent; ctx7 CLI not found | Used official versioned web/raw sources |
| Project sandbox/image pull | Not created/pulled in research | Execution verifies real architecture/image availability |

These versions are command observations, not support guarantees. [VERIFIED: `git --version`, `docker --version`, `docker compose version`, `make --version`, escalated `docker info --format '{{.ServerVersion}}'`, 2026-11-06]

## Validation Architecture

### Framework and commands

Use stdlib unittest for helper/config invariants and HTTP integration checks against the real Docker service, plus native Django system/migration checks. No additional dependency is needed for those checks. [ASSUMED: proposed validation design]

| Property | Proposed contract |
|---|---|
| Quick command | `make check` — helper syntax/config/static invariants; aim <30 seconds |
| Blocking baseline suite | `make test` and `make smoke` against running project sandbox |
| Legacy report | `make test-legacy` with exact outcomes and a deferred-failure inventory |
| Cold integration | `make setup`, readiness wait, `make smoke` |
| Lifecycle | setup twice; down/up; assert env digest/data identity stable; explicit project-only reset |

### Requirement → Test Map

| Requirement | Verification | Category |
|---|---|---|
| BASE-01 | Source manifest matches consolidated tracked source; branch usable; no active linked worktrees; planning/docs retained | Git/filesystem acceptance |
| BASE-02 | Pinned runtime version; Compose isolation/localhost only; second setup does not rotate env; other project untouched | Static config + integration |
| BASE-03 | Native check, plugin app registration assertion, applied migrations and zero pending/drift, clean restart | Django/container smoke |
| BASE-04 | CSRF-aware real admin login, generated v2 API auth, baseline suite pass, feature failures separately recorded | HTTP + test report |

All commands above are proposed verification interfaces, not existing files. [ASSUMED: implementation plan input]

### Wave 0 Gaps

- Add helper tests for stable generated configuration, secrets omitted from output, and project-scoped reset safeguards.
- Add the real startup/auth/registration smoke helper and expose it through Make.
- Add a dummy-data seed with idempotence checks; snapshot relevant row counts before/after rerun.
- Add a legacy test result report that preserves actual collection/runtime failure classification.

These gaps follow observed source plus D-08/D-10/D-11/D-13–D-15; file names are intentionally left to the planner. [ASSUMED: proposed work]

### Sampling

Run quick checks after each helper/config task; run blocking real smoke after the first runnable end-to-end slice and each lifecycle change. Cold setup may take minutes and is not a sub-30-second test; do not mislabel it. Phase completion requires actual boot/migrate/register/login evidence, not mocked calls. [ASSUMED: recommended verification schedule]

## Security Domain

Use current ASVS category names/version references rather than assuming older V2/V3/V4 numbering still describes authentication/session/access controls. ASVS 5.0.0 is the current stable standard; the numbering is version-sensitive. [CITED: https://asvs.owasp.org/]

For this local baseline, apply concrete checks: credentials remain local/ignored, web binds localhost, other services are unexposed, Make subprocesses do not expand untrusted shell text, authentication uses native NetBox, and reset operations remain project-scoped. These are phase-specific mitigations, not a claim of ASVS certification. [ASSUMED: proposed threat controls]

## Assumptions Log / Open Questions

1. Proposed Make interfaces, test architecture, recovery sequence, and isolation naming are recommendations under delegated implementation discretion, not externally verified existing behavior.
2. Real build, image manifest/digest resolution, migration fidelity, and actual admin/API login remain execution checks. No startup compatibility has been claimed from source inspection alone.
3. Legacy test extras need authoritative package metadata verification if installed; the GSD audit returned null metadata. Prefer standard-library baseline checks; do not block boot work on the feature suite.
4. Exact image architecture/digest and available host port should be checked immediately before setup. Do not infer host port availability from the user's existing stack.

No user decision is needed to proceed to planning: D-01–D-15 already settle scope, new-data policy, and implementation discretion. [VERIFIED: 01-CONTEXT.md decisions copied above]

## Sources and Confidence

Primary sources were fetched using web tools because Context7 MCP/CLI were unavailable. The GSD research-plan seam selected Context7, then fallback was required; the installed classify-confidence seam reports LOW for generic webfetch and MEDIUM for Context7 even with verified=true. Official-source claims use `[CITED]`; MEDIUM overall is a source-quality assessment, not a successful runtime or registry verification. In-repo `[VERIFIED]` tags identify files opened in this session or literal command observations. The optional global research cache write was sandbox-denied and was not retried because this task owns only the research artifact. [VERIFIED: research-plan/classify-confidence/research-store outputs this session]

- NetBox 4.7.4 release: https://github.com/netbox-community/netbox/releases/tag/v4.7.4
- Docker packaging release: https://github.com/netbox-community/netbox-docker/releases/tag/5.1.1
- Published tags: https://hub.docker.com/r/netboxcommunity/netbox/tags
- Versioned Docker sources: https://github.com/netbox-community/netbox-docker/tree/5.1.1
- Versioned NetBox sources: https://github.com/netbox-community/netbox/tree/v4.7.4
- NetBox plugin/model docs: https://netboxlabs.com/docs/netbox/plugins/development/ and its models page
- Compose docs: https://docs.docker.com/compose/how-tos/project-name/ and environment-variable interpolation
- Git worktree docs: https://git-scm.com/docs/git-worktree
- Python secrets: https://docs.python.org/3/library/secrets.html

**Valid until:** recheck image/tag/patch availability at execution; source recommendations are tied to the pinned versions above.
