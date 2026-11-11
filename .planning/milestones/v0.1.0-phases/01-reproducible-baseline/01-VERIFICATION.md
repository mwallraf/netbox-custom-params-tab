---
phase: 01-reproducible-baseline
verified: 2026-11-06T17:41:17Z
status: passed
score: 24/24 must-haves verified
covered_files: [".dockerignore", ".env.example", ".gitignore", ".planning/phases/01-reproducible-baseline/01-01-PLAN.md", ".planning/phases/01-reproducible-baseline/01-01-SUMMARY.md", ".planning/phases/01-reproducible-baseline/01-02-PLAN.md", ".planning/phases/01-reproducible-baseline/01-02-SUMMARY.md", ".planning/phases/01-reproducible-baseline/01-03-PLAN.md", ".planning/phases/01-reproducible-baseline/01-03-SUMMARY.md", ".planning/phases/01-reproducible-baseline/01-04-PLAN.md", ".planning/phases/01-reproducible-baseline/01-04-SUMMARY.md", "AGENTS.md", "CLAUDE.md", "Makefile", "README.md", "docker-compose.yml", "docker/Dockerfile", "docker/plugins.py", "docs/development/baseline-status.md", "docs/development/sandbox.md", "docs/development/source-recovery.md", "netbox_custom_field_profiles/__init__.py", "netbox_custom_field_profiles/migrations/0001_initial.py", "pyproject.toml", "pytest.ini", "scripts/legacy_tests.py", "scripts/lifecycle_sandbox.py", "scripts/sandbox.py", "scripts/seed_sandbox.py", "scripts/smoke_sandbox.py", "scripts/source_snapshot.py", "tests/sandbox/test_config.py", "tests/sandbox/test_legacy_report.py", "tests/sandbox/test_lifecycle.py", "tests/sandbox/test_smoke.py"]
covered_digest: "v4:sha256:fc3095b5367c435b1b6973998fcfc0e928a1dc098e997501a448e3b0c0529db8"
behavior_unverified: 0
overrides_applied: 0
human_verification: []
decision_coverage:
  honored: 15
  total: 15
  not_honored: []
---

# Phase 1: Reproducible baseline Verification Report

**Phase Goal:** A developer can install, run, and test the renamed plugin from a usable checkout without losing prior work.
**Verified:** 2026-11-06T17:41:17Z
**Status:** passed
**Re-verification:** No — initial verification; no previous VERIFICATION.md existed.

## Goal Achievement

The four roadmap success criteria and additional PLAN truths are satisfied for the agreed developer baseline. This verdict covers installation, native schema/registration, actual authentication, reproducible checks, recovery and isolated lifecycle. It does not certify the imported panel implementation or future profile features.

Evidence comes from actual source inspection, commands run by this verifier, and identified live command results from the parent orchestrator's current tool transcript. SUMMARY claims alone were not used to establish behavior. No Docker mutation was repeated by this verifier; the parent had just completed the live baseline and destructive lifecycle checks.

### Observable Truths

The roadmap wording is retained in rows 1–4. Plan 01's source-retention truth is merged into row 1; Plan 04's final-evidence truth is merged into row 4. Other PLAN truths add detail and remain separately checked. No PLAN declares a prohibitions block or backstop-tier truth.

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Existing source and uncommitted changes are preserved in a documented usable checkout; stale worktree metadata no longer obstructs development. | VERIFIED | Both `verify --commit 4dba67e` and `verify --root .recovery/implement-plugin` returned SOURCE_SNAPSHOT_OK. Manifest hashes cover the original renamed files. Merge 4dba67e has parents a6b9d5f and 42ad9c2; root product/planning documents are unchanged across that merge. SOURCE_LAYOUT_OK; only root checkout registered. |
| 2 | A documented supported NetBox version runs the renamed plugin and its reproducible test stack. | VERIFIED | Dockerfile pins v4.7.4-5.1.1 and installs the local distribution in the native interpreter. Parent live `make test` exited 0 with exact runtime, native registry/schema and authenticated HTTP checks. Guide states prerequisites and tested version. |
| 3 | Schema checks and the chosen legacy-app/config migration policy are verified before applying destructive or incompatible changes. | VERIFIED | D-07 explicitly authorizes a clean disposable database; guide excludes existing-deployment migration. Native generated migration is checked in; setup rejects the handwritten predecessor. Runtime runs `check`, `migrate --check` and plugin `makemigrations --check --dry-run`; live reset/setup/runtime succeeded. |
| 4 | Required baseline checks pass; known residual failures and their scope are explicitly recorded. | VERIFIED | Independent 35-test helper run passed; parent final live `make test` and lifecycle exited 0. Local legacy report actually records runner-unavailable, exit 1, no counts and no collection; baseline-status.md states unexecuted. Future feature scope remains explicit. |
| 5 | D-02: Git/source reconciliation is complete before Docker setup changes begin. | VERIFIED | Git history places recovery merge 4dba67e and retirement 19e26e4 before environment d122e38, image e6596d8 and runtime 4da597b commits. |
| 6 | D-03: Development uses milestone/custom-field-profiles in the normal checkout and creates no worktrees or per-phase branches. | VERIFIED | Actual branch is milestone/custom-field-profiles; worktree inventory has one root record. AGENTS.md and guide prescribe this layout. |
| 7 | Missing source, divergent files, or unexpected local changes stop reconciliation rather than being silently overwritten. | VERIFIED | Inventory rejects incomplete directories and symlinks; manifest capture refuses replacement; verify compares complete inventories/hashes and raises on mismatch. It performs no source-copy/overwrite operation. Original and canonical snapshots both match independently. |
| 8 | D-01: Plugin minimum is 4.7.0 and the sandbox pins published netboxcommunity/netbox:v4.7.4-5.1.1; later versions are not claimed tested. | VERIFIED | Plugin `min_version`, Dockerfile FROM and guide agree. Live runtime asserts exact 4.7.4-Docker-5.1.1. Parent setup transcript observed editable installation and official base digest; digest recorded in baseline-status.md. |
| 9 | D-05/D-06: A dedicated Compose project owns its network/volumes and exposes only a configurable localhost web port, leaving the existing NetBox untouched. | VERIFIED | Fixed project/file/env argv; exact service/mount validation; nonexternal project resources; only 127.0.0.1 web mapping. Foreign mount/symlink/label regressions pass. Live lifecycle passed; independently read diagnostic snapshots show all 35 original running unrelated IDs remain among 50 final IDs. |
| 10 | D-09/D-10: make setup runs the complete Docker installation/startup chain from canonical source. | VERIFIED | Make → sandbox.setup → validated build → healthy dependencies → normal native services → runtime → seed. `test_normal_startup_follows_healthy_dependencies` passed; parent actual lifecycle performed two successful setup runs and another after reset. |
| 11 | D-11: Generated .env secrets are ignored, local, stable on repeat setup, and absent from logs and tracked examples. | VERIFIED | Atomic mode-0600 creation, redacted subprocess failures, silent Make recipes, blank example credentials and build-context exclusions. `.env` is ignored and untracked. Repeat-preservation/redaction tests and actual lifecycle CREDENTIALS_STABLE passed. No real .env contents were read by this verifier. |
| 12 | D-12: Infrastructure uses .env while plugin behavior uses native PLUGINS_CONFIG. | VERIFIED | Compose injects infrastructure/auth variables. Native extra-config mount supplies PLUGINS/PLUGINS_CONFIG without replacing upstream configuration. Plugin ready() reads its native settings. |
| 13 | D-07/D-13/D-15: Clean native migrations and plugin registration must succeed; startup failures are blocking. | VERIFIED | Runtime checks throw on nonzero native commands and assert installed app/applied migration. `test_runtime_failure_blocks_authentication` passed; parent live native checks passed again after clean reset. |
| 14 | Initial migration generation runs directly in the native interpreter before any bootstrap can apply the handwritten plugin schema; normal web/worker startup remains native. | VERIFIED | prepare_schema checks absence through direct one-off Python, removes old migration and runs native makemigrations; no web startup in that path. setup refuses handwritten schema before Docker calls. Direct-interpreter, uncorrected-schema and failure-ordering tests passed. Normal services have no entrypoint override; generated migration and current native no-drift check agree. Historical generation markers are executor narration, not newly observed native evidence; unit-test marker output was not treated as live generation proof. |
| 15 | Interrupted or concurrent configuration initialization cannot replace existing secrets with partial or conflicting values. | VERIFIED | Bounded flock plus fsynced temporary file and nonreplacing hard link publish complete configuration; existing invalid data is rejected. `test_atomic_concurrent_initialization`, `test_partial_config_fails_without_rotation` and preservation test passed. |
| 16 | D-13/D-15: Real CSRF-aware admin login and authenticated follow-up succeed; a login-page GET alone cannot pass smoke. | VERIFIED | Smoke checks CSRF POST, session cookie and separate protected-page follow-up, anonymous control and wrong-password control. False-positive helper regressions passed; actual live parent `make test` emitted BASELINE_SMOKE_OK and exited 0. |
| 17 | Generated native token credentials authenticate successfully without printing tokens, peppers, passwords, cookies or headers. | VERIFIED | Smoke builds native v2 bearer credentials in memory; exact API username/count asserted and invalid token requires 401/403. Exact-user/redaction tests passed; same live smoke exercised successful native token and negative control. |
| 18 | D-07: A repeatable native ORM seed supplies dedicated CMTS/CPE dummy devices and fields without creating profile functionality. | VERIFIED | Transactional native ORM creates deterministic sandbox objects, preserves unrelated native values and compares repeated identities/values. Live parent `make test` emitted SEED_IDEMPOTENT_OK; read-only lifecycle snapshot covers native Device data. No profile model added. |
| 19 | D-14: Baseline checks are blocking; legacy test outcomes and setup/collection failures are reported honestly and separately. | VERIFIED | Make test requires check/smoke/seed-check. Legacy runner classifies unavailable/collection/setup/failure outcomes and preserves nonzero exits; no-tests zero is rejected. Three report tests passed; actual local report confirms pytest unavailable, exit 1, no executed tests. |
| 20 | The Docker sandbox is the environment for runtime checks; mocks only test helper error handling. | VERIFIED | Native checks use the explicit project container interpreter; HTTP smoke uses actual configured localhost endpoint. Mocks test parser, guard, order and failure branches, not a substitute runtime. Parent live tool outputs independently establish actual runtime and HTTP behavior. |
| 21 | D-08: Normal down/up and repeated setup preserve database records and .env credentials; explicit reset recreates only this project's disposable sandbox. | VERIFIED | Real lifecycle creates a random-marker sentinel once; later `.get()` and seed snapshots are read-only. Parent lifecycle exited 0 with PERSISTENCE_OK, PROJECT_RESET_OK, RESET_RECREATED_DATABASE_OK and CREDENTIALS_STABLE. Missing-sentinel regression passed. |
| 22 | D-05/D-06: Lifecycle and reset commands cannot target the existing workstation NetBox or external resources. | VERIFIED | Same Docker environment builder for inspection and mutation; fixed project and strict mount/network/volume guards; reset checks actual volume ownership labels before scoped down --volumes. Guard tests passed; live original-ID preservation passed. |
| 23 | D-10: Documented Make targets orchestrate setup, checks, tests, seeding, stop/start and explicit reset. | VERIFIED | Every target in sandbox.md exists in Makefile and calls the inspected shared CLI/module path. Destructive lifecycle/reset behavior and retained credentials are explicit. |
| 24 | No worktree, global Docker cleanup, secret leak or implementation of deferred profile features is introduced. | VERIFIED | One active root checkout; no prune/global cleanup path. Ignored recovery/env/report inputs excluded from build. Post-recovery plugin diff is limited to version floor, initial schema and removal of migration bypass; models/forms/views/API/templates/navigation are unchanged. |

**Score:** 24/24 truths verified; 0 present, behavior-unverified. No overrides or coincidental-reliance items were needed. The required runtime preconditions are declared prerequisites and established by setup, not hidden test fixtures.

### Required Artifacts

All 14 PLAN artifact declarations passed `query verify.artifacts` (3/3, 5/5, 3/3, 3/3). Manual checks additionally verified substance and actual consumers:

| Artifact | Expected | Status | Substance and wiring |
| --- | --- | --- | --- |
| scripts/source_snapshot.py | Recovery inventory/verification | VERIFIED | Hash inventory, immutable capture and layout checks; used by recovery guide and independently executed. |
| docs/development/source-recovery.md | Provenance | VERIFIED | Original manifest and real merge hash; both retained and canonical bytes verified against it. |
| netbox_custom_field_profiles/__init__.py | Renamed plugin | VERIFIED | Real PluginConfig exported as config; installed by package entry point and enabled by native PLUGINS. |
| scripts/sandbox.py | Safe environment/Compose orchestration | VERIFIED | Full parsing, atomic credentials, validated targeting, setup/runtime/seed/lifecycle dispatch; Make invokes it. |
| docker-compose.yml | Isolated services | VERIFIED | Five configured native services, health dependencies, project volumes, local binds and localhost web port; helper renders/validates it. |
| docker/Dockerfile | Pinned native plugin image | VERIFIED | Official exact base and native-interpreter editable installation; Compose builds it. |
| docker/plugins.py | Native plugin supplement | VERIFIED | PLUGINS/PLUGINS_CONFIG/DEVELOPER only; mounted to native extra-config path. |
| netbox_custom_field_profiles/migrations/0001_initial.py | Native clean schema | VERIFIED | Substantive generated operations/dependencies match current model state; actual migration/no-drift checks passed. |
| scripts/smoke_sandbox.py | Runtime/session/token checks | VERIFIED | Real HTTP controls and native runtime prerequisite; sandbox smoke dispatch calls it. |
| scripts/seed_sandbox.py | Native dummy data | VERIFIED | Transactional ORM seed and read-only snapshot; container shell invokes it from setup/seed-check/lifecycle. |
| scripts/legacy_tests.py | Honest legacy report | VERIFIED | Actual subprocess/status/counts/redaction/report path; make test-legacy invokes it. |
| tests/sandbox/test_lifecycle.py | Lifecycle guard tests | VERIFIED | Twelve active tests cover scoping, daemon consistency, mounts, sentinel and unrelated identities; discovered by make check. Real lifecycle entry point is scripts/lifecycle_sandbox.py via make lifecycle-check. |
| docs/development/sandbox.md | Reproducible guide | VERIFIED | Prerequisites, commands, native setting split, credential handling and reset policy match implementation. |
| docs/development/baseline-status.md | Actual results/residual status | VERIFIED | Agrees with inspected source/report and identified live outputs; explicitly makes no successful legacy-feature claim. |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| source_snapshot.py | source-recovery.md | Default/explicit manifest | WIRED | Manifest parsed and compared; commands passed. |
| pyproject.toml | plugin __init__.py | netbox.plugins entry point | WIRED | `netbox_custom_field_profiles:config` resolves real config export. |
| Makefile | sandbox.py | Explicit CLI recipes | WIRED | Setup/check/lifecycle/reset all use inspected wrapper. |
| docker-compose.yml | docker/plugins.py | Native extra-config bind | WIRED | Read-only supported config destination; runtime app installed. |
| Dockerfile | plugin package | COPY plus uv editable install | WIRED | Directory copy contains __init__.py; native interpreter installation, then PLUGINS activation. |
| Makefile | smoke_sandbox.py | sandbox.py smoke dispatch | WIRED | make test → smoke → shared CLI → smoke() import and call. |
| smoke_sandbox.py | sandbox.py | import plus actual calls | WIRED | ensure_env(), runtime() and redact() consumed. |
| sandbox.py | seed_sandbox.py | Native manage.py shell | WIRED | Executed in same explicit project container. |
| sandbox.md | Makefile | Documented targets | WIRED | All documented target names exist and have implementations. |

`query verify.key-links` recognized 5/10 declared links, including duplicate Make→sandbox declarations. Its five negative results were literal-reference false negatives: package entry points, directory COPY, indirect CLI dispatch, Python module import and target-name documentation. Each was resolved by tracing the concrete consumers above; none was accepted solely because a file existed.

### Data-Flow Trace (Level 4)

No new dynamic UI is in this phase. Runtime evidence paths were traced anyway:

| Artifact | Data | Real source | Status |
| --- | --- | --- | --- |
| smoke_sandbox.py | CSRF/session/protected page/API identity | Actual native HTTP responses, cookie jar and parsed JSON | FLOWING |
| sandbox.py runtime | Version/app/migration state | Native Django settings/apps/MigrationRecorder plus real command exits | FLOWING |
| seed_sandbox.py | Dummy Device/native field values | Transactional native ORM, compared identities and native custom_field_data | FLOWING |
| lifecycle_sandbox.py | Persistence marker/seed snapshot/volume labels | Native DB read, current project resource metadata and exact env-byte comparison | FLOWING |
| legacy_tests.py | Outcome/counts | Actual pytest subprocess exit/output; currently unavailable | FLOWING, explicitly unexecuted tests |

### Behavioral Spot-Checks

| Behavior | Command/evidence | Result | Status |
| --- | --- | --- | --- |
| Helper state/order/error invariants | Verifier: `python3 -m unittest discover -s tests/sandbox -v` | 35 tests, 0.118s, exit 0. Named tests include atomic_concurrent_initialization, partial_config_fails_without_rotation, generation_failure_never_starts_web, normal_startup_follows_healthy_dependencies, runtime_failure_blocks_authentication, missing_sentinel_is_not_recreated and metadata_and_compose_use_same_docker_environment. | PASS |
| Original source retention | Verifier: `python3 scripts/source_snapshot.py verify --commit 4dba67e`; `verify --root .recovery/implement-plugin` | SOURCE_SNAPSHOT_OK for both, exit 0 | PASS |
| Layout/history/whitespace | Verifier: verify-layout, branch/worktree inventory, merge ancestry, `git diff --check b090288` | SOURCE_LAYOUT_OK; root milestone branch only; feature ancestor; clean diff | PASS |
| Full native baseline | Parent live `make test`, session 69910 completion | exit 0; 35 helpers, CONFIG_OK, actual RUNTIME_OK NetBox=4.7.4-Docker-5.1.1, BASELINE_SMOKE_OK and SEED_IDEMPOTENT_OK | PASS |
| Persistent setup/restart and isolated reset | Parent live `python3 -u scripts/sandbox.py lifecycle-check`, session 81886 completion | exit 0; real repeated setup/native checks, PERSISTENCE_OK, PROJECT_RESET_OK, RESET_RECREATED_DATABASE_OK, CREDENTIALS_STABLE and LIFECYCLE_OK | PASS |
| Isolation diagnostic evidence | Verifier read only .sandbox/lifecycle-before.json and after.json | Original 35 running unrelated IDs are a subset of final 50 IDs | PASS |
| Legacy status honesty | Verifier parsed .sandbox/legacy-tests.json | Actual command invokes native pytest; runner version/status 1; classification runner-unavailable; counts empty; output says No module named pytest | PASS reporting; suite unexecuted |

Only the helper suite was run by this verifier, once. No new server, Docker mutation or package installation was performed. Parent live commands are separately identified, rather than represented as this verifier's own commands. Mock tests print PRE_BOOTSTRAP_SCHEMA_ABSENT and SANDBOX_READY; those prints are not native integration evidence. Actual native runtime/auth/seed results above come from the live completion output.

### Probe Execution

No `scripts/**/tests/probe-*.sh` exists and no phase PLAN declares a shell probe. Probe-specific execution is N/A. The real runnable baseline/lifecycle scripts were executed by the parent in their own live processes with the exact outcomes above; SUMMARY pass-marker counts were not substituted for their exit status.

### Requirements Coverage

| Requirement | Source plans | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| BASE-01 | 01, 04 | Usable checkout preserving all work | SATISFIED | Original/canonical hash matches, real merge ancestry, retained recovery directory, authoritative root docs and single canonical checkout. |
| BASE-02 | 02, 04 | Supported reproducible version/dev-test stack | SATISFIED | Exact native runtime/image, explicit Compose isolation, executable Make orchestration, live setup/test/lifecycle, tracked guide. |
| BASE-03 | 02, 03, 04 | Renamed install/registry/schema and safe migration policy | SATISFIED | Real editable install/native app registry, generated migration/current no-drift checks, setup blocks handwritten schema, clean disposable policy and postreset validation. |
| BASE-04 | 03, 04 | Repeatable required baseline and known failures | SATISFIED | Blocking test target, 35 helper passes, live positive/negative auth and seed/lifecycle, exact nonzero unexecuted legacy outcome documented separately. |

All four IDs assigned to Phase 1 appear in PLAN frontmatter. No orphaned Phase 1 requirement was found. Later feature requirements remain pending. The absence of a passing legacy suite is permitted by D-14 and does not mask startup/schema/registration/authentication failures prohibited by D-15.

### Decision Coverage

`query check.decision-coverage-verify` exited 0: all 15 trackable CONTEXT.md decisions are honored by shipped artifacts; honored 15/15, not_honored []. Manual source checks confirmed the important isolation, native-schema, lifecycle and scope decisions rather than relying on the heuristic alone.

### Test Quality Audit

| Test file | Linked requirements | Active | Skipped | Circular | Strongest assertion | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| test_config.py | BASE-02/03 | 11 | 0 | No | Byte/permission preservation, concurrent calls, exact argv and ordered calls, fail-closed guards | PASS |
| test_smoke.py | BASE-03/04 | 9 | 0 | No | Exact API identity, rejected false login evidence, runtime failure prevents auth | PASS with live authentication evidence |
| test_lifecycle.py | BASE-01/02/04 | 12 | 0 | No | Rejection before mutation, identical Docker environment, exact mounts, nonrepairing sentinel, original-ID survival | PASS with live persistence/reset evidence |
| test_legacy_report.py | BASE-04 | 3 | 0 | No | Exact classifications/counts/redacted value | PASS with actual unavailable-run report |

Disabled requirement-linked baseline tests: 0. Circular expected-output generation: 0. Test inputs use independent literal expectations and temporary files, not generated golden outputs. Helper mocks do not prove actual NetBox functionality; the identified live checks supply that evidence.

Disconfirmation limits: the optional legacy suite has no executed feature assertions, so no profile/panel behavior is inferred. `test_no_public_or_external_resources` uses incomplete service fixtures and can reject at the earlier service-set guard; that test alone does not prove the later port branch. The explicit localhost configuration, inspected validator and live rendered CONFIG_OK establish the actual baseline. Interrupted-publish crash injection is not a separate test; atomic publication is implemented by fsync plus nonreplacing link and concurrent/invalid-existing-state tests exercise the reachable preservation paths. These limits do not contradict a baseline must-have.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customtabconfig_edit.html | 134 | Existing console.log diagnostics, also lines 137/139 | INFO | Imported unchanged. Handler also sets DELETE and hides the row; it is not a console-only stub. No new baseline UI is claimed. |

No unreferenced TBD/FIXME/XXX debt markers, empty baseline handlers, disabled helper tests or disconnected baseline data sources were found in the changed implementation inputs. Current source confirms CR-01, CR-02 and WR-01 are corrected: shared daemon environment, exact service mount validation and read-only unpredictable persistence sentinel. Independent helper tests and the parent corrected live rerun cover those fixes. The earlier failed lifecycle run used equality of all unrelated containers; the final check deliberately allows additions while rejecting loss/replacement of original IDs, with regression coverage.

### Human Verification Required

None. This phase establishes developer infrastructure and uses native NetBox authentication; it adds no UI contract. Actual CSRF/session/API behavior is proven by live automation. No behavior-dependent truth is left on presence-only evidence. The UI review correctly records visual review as not applicable; no browser appearance approval or future feature workflow is implied.

### Gaps Summary

No blocking baseline gaps. The milestone roadmap was inspected for deferred scope: profile administration/matching, Parameters tab, edit flow and full release acceptance belong to Phases 2–5. They are not failed Phase 1 truths. The missing optional legacy runner remains an explicit baseline limitation, with a documented opt-in installation command and truthful nonzero reporting; it is neither a passed suite nor an invented feature-failure inventory.

The source and guide are ready for the orchestrator's completion gate. STATE.md and roadmap progress were deliberately left for that gate. No implementation, requirements or workflow-state files were changed, and no commit was created by this verifier.

---

_Verified: 2026-11-06T17:41:17Z_
_Verifier: the agent (gsd-verifier)_
