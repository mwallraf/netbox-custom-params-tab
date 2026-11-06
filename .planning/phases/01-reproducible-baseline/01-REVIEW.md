---
phase: 01-reproducible-baseline
reviewed: 2026-11-06T17:13:16Z
depth: standard
files_reviewed: 18
files_reviewed_list:
  - scripts/source_snapshot.py
  - scripts/sandbox.py
  - scripts/smoke_sandbox.py
  - scripts/seed_sandbox.py
  - scripts/legacy_tests.py
  - scripts/lifecycle_sandbox.py
  - tests/sandbox/test_config.py
  - tests/sandbox/test_smoke.py
  - tests/sandbox/test_legacy_report.py
  - tests/sandbox/test_lifecycle.py
  - Makefile
  - docker-compose.yml
  - docker/Dockerfile
  - docker/plugins.py
  - .dockerignore
  - .env.example
  - netbox_custom_field_profiles/__init__.py
  - netbox_custom_field_profiles/migrations/0001_initial.py
findings:
  critical: 2
  warning: 1
  info: 0
  total: 3
status: issues_found
---

# Phase 1: Code Review Report

**Depth:** standard. Review covers the recovered baseline orchestration and its tests, not deferred profile functionality or unchanged legacy UI.

## Narrative Findings (AI reviewer)

The live successful baseline does not exercise alternate Docker environment selection, unsafe rendered bind mounts, or loss of a persistence sentinel. Three concrete gaps remain in those safeguards.

## Critical Issues

### CR-01: Reset inspects a different Docker environment from the one it mutates

**Classification:** BLOCKER

**File:** `/Users/mwallraf/Developer/netbox-custom-params-tab/scripts/lifecycle_sandbox.py:9-10`; related `scripts/sandbox.py:122-127`.

**Issue:** `docker_json()` inherits the process environment, whereas every Compose invocation removes all `DOCKER_*` variables. With `DOCKER_HOST`, `DOCKER_CONTEXT`, or `DOCKER_CONFIG` set, volume ownership checks and unrelated-container snapshots can therefore inspect a different daemon/context from `down --volumes` and setup. If the inspected daemon lacks the named volumes, reset skips their label verification entirely and proceeds to delete same-named volumes on the other daemon. The final unrelated-ID comparison also observes the wrong daemon. A mock-only reproduction confirmed the Compose subprocess has an explicit environment without DOCKER_HOST, while metadata subprocesses have no explicit environment and inherit it.

**Fix:** Use one shared Docker environment/context builder for Compose, metadata inspection, and legacy execution. Pass that exact environment to every Docker subprocess, and add a regression using nondefault DOCKER_HOST/DOCKER_CONTEXT proving metadata and mutation use identical selection. Either consistently support an explicit selected daemon or consistently reject/strip overrides; do not mix the two.

### CR-02: Resource validation never checks actual service volume bindings

**Classification:** BLOCKER

**File:** `/Users/mwallraf/Developer/netbox-custom-params-tab/scripts/sandbox.py:152-170`.

**Issue:** The validator checks top-level named-volume declarations but never `services[*].volumes`. Replacing the postgres service mount with a bind such as an existing workstation database directory leaves all declared volume checks passing. Setup then starts PostgreSQL against that shared directory, and reset can report success while restarting/reseeding the same external data. This violates the planned unsafe-path refusal and the guarantee that the existing workstation installation is untouched. An arbitrary host bind is valid Compose configuration, so Compose's own parser does not close this gap.

**Fix:** Validate rendered service mounts against an explicit map: postgres/redis/cache/media must use their exact project-scoped named volumes and expected destinations; permit only the known repository-local source/config/test bind mounts, checking resolved paths, destinations, and required read-only modes. Reject unknown service/mount combinations and host paths escaping the canonical checkout before any mutation. Add tests for an absolute foreign database bind and a symlinked bind source, not just top-level external volume declarations.

## Warnings

### WR-01: Persistence verification silently recreates the record it is meant to verify

**Classification:** WARNING

**File:** `/Users/mwallraf/Developer/netbox-custom-params-tab/scripts/lifecycle_sandbox.py:45-60`.

**Issue:** Every persistence assertion calls `sentinel()`, which uses `get_or_create`, and compares only the primary key. A lost/recreated database followed by deterministic seeding can recreate this sentinel with the same PK and pass PERSISTENCE_OK. The check also never snapshots the native values it claims to preserve. A verification read should not repair the state under verification.

**Fix:** Create a sentinel once with an unpredictable marker stored in a native field, then use read-only `.get()` plus marker and PK comparisons after each setup/restart. Snapshot the owned seed identities/native values read-only too. Missing or changed records must fail without inserting/reseeding them. Add a regression showing a missing sentinel or recreated database cannot be made green by the verification helper.

---

Reviewed with no Docker calls, package installation, source edits, or commits. Existing successful live results were treated as execution evidence, not as proof that untested guard branches are correct.
