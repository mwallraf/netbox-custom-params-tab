---
phase: 02-profile-administration-and-matching
plan: "07"
subsystem: integration
tags: [netbox, runtime, retirement, preservation]
requires:
  - phase: 02-06
    provides: Verified profile administration and native preservation matrix
provides:
  - Retired legacy configuration API and injected main-page panel
  - Preserved native event serialization and lifecycle signal registration
  - Verified legacy row inventory for the separate schema deletion decision
affects: [02-08, phase-verification]
tech-stack:
  added: []
  patterns: [inert discovery modules, one-time legacy inventory, durable retirement regression]
key-files:
  created:
    - .planning/tmp/02-07-red.json
  modified:
    - netbox_custom_field_profiles/api/views.py
    - netbox_custom_field_profiles/api/serializers.py
    - netbox_custom_field_profiles/api/urls.py
    - netbox_custom_field_profiles/__init__.py
    - netbox_custom_field_profiles/template_content.py
    - netbox_custom_field_profiles/tests/test_preservation.py
key-decisions:
  - Keep the internal CustomFieldProfileSerializer for native event payloads without a public profile API.
  - Retain only an inert BUILTIN_MODELS import constant until legacy form classes are removed in 02-08.
requirements-completed: [PROF-01, DATA-01]
actuals:
  tokens: 3134
  tasks: 2
  commits: 3
plan_head_before: a5f732697ac401b632b96c74cd1696ed9c7335e7
plan_head_after: 44d851336035e689c6bcc4ba727bf3985a4a6e09
coverage:
  - id: runtime-retirement
    description: No obsolete API or injected panel registration; profile routes and event payloads work
    requirement: PROF-01
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles/tests/test_preservation.py
        status: pass
    human_judgment: false
  - id: pre-retirement-inventory
    description: Legacy configuration rows, new profiles and native definitions/Device values unchanged
    requirement: DATA-01
    verification:
      - kind: integration
        ref: 02-07-SUMMARY.md#live-inventory-before-and-after
        status: pass
    human_judgment: false
duration: 13min
completed: 2026-11-06
status: complete
---

# Phase 2 Plan 7: Legacy Runtime Retirement Summary

**Legacy API/panel consumers are unregistered while native profile pages, event serialization, lifecycle signals and every existing configuration row remain intact.**

## Task Commits

1. **Retire obsolete runtime consumers and inventory configuration scheduled for removal** — `85ad633`; supporting failing contract/evidence commit `f16ce61`.
2. **Prove the runtime retirement boundary before schema deletion** — `44d8513`.

Commit actuals are measured from the persisted plan ledger before this metadata commit. No schema migration was generated or applied.

## Verification

- `make test-profiles`: **49 native tests pass**, native **6.366 s**, runner **10.86 s**; isolated PostgreSQL and `PROFILE_LIVE_UNCHANGED` confirmed after dedicated web/worker restart.
- Focused preservation suite: **5 tests pass**, runner **5.64 s**, before the additional native Device-page assertion. That assertion passes in the final 49-test suite.
- `make check`: **35 helper tests pass**, configuration/bootstrap guard checks pass.
- `make test`: **35 helper tests pass**, native NetBox 4.7.4/Docker 5.1.1 runtime/schema/registration, real administrator session, native token and negative authentication controls, and seed idempotence pass.
- Real HTTP authenticated profile list and add pages return **200**; `/api/plugins/custom-field-profiles/custom-tab-configs/` returns **404**.
- Native Device detail rendering is **200** and does not use `netbox_custom_field_profiles/tab_panel.html`.
- `git diff --check` passes. No new packages, schema operations or native data write paths.

## Live Inventory Before and After

Read-only native connection introspection and `SELECT * ... ORDER BY id` captured all Device rows, native custom-field tables and plugin tables before changes and after service reload, suites and baseline seed checks. All table counts and the entire data hash match exactly:

`2ca44fe941993eb135d159952ca56812021a9fb9a63617f1c424c4636c17861e`

| Table / model | Before | After |
|---|---:|---:|
| `netbox_custom_field_profiles_customtabconfig` / CustomTabConfig | 1 | 1 |
| `netbox_custom_field_profiles_customtabconfiggroup` / CustomTabConfigGroup | 1 | 1 |
| `netbox_custom_field_profiles_customtabconfigfield` / CustomTabConfigField | 1 | 1 |
| `netbox_custom_field_profiles_customfieldprofile` | 0 | 0 |
| New profile device-type/role/applicability-tag through tables | 0 each | 0 each |
| `netbox_custom_field_profiles_profilefield` | 0 | 0 |
| `dcim_device` | 2 | 2 |
| `extras_customfield` | 2 | 2 |
| `extras_customfield_object_types` | 2 | 2 |
| `extras_customfieldchoiceset` | 0 | 0 |

This is one-time pre-retirement execution evidence. Durable tests neither import the old models nor require their tables or rows to remain after 0003.

## Exact Following Decision Scope

Plan 02-08 proposes deletion of **CustomTabConfigGroup**, **CustomTabConfigField** and **CustomTabConfig** only: one row in each table at this checkpoint. Reverse schema migration would not restore these three configuration rows. Native CustomField definitions/settings, native Device values and all new profile tables are outside this removal. No deletion is authorized by this summary; the explicit `retire` / `preserve` decision remains pending.

## Runtime Integration

The API URL module stays importable with an empty `urlpatterns`; old viewset and serializer/model imports are removed. The internal **CustomFieldProfileSerializer** remains for native create/update/delete event serialization. No replacement profile REST endpoint is exposed.

The plugin no longer registers the old template extension or `extra_models` startup behavior. An inert template-content resource returns no extensions because inspected pinned PluginConfig falls back to its conventional resource path even without an explicit setting. `ready()` still calls native setup and registers profile lifecycle signals.

## Deviations and TDD Evidence

- **[Rule 3 — import compatibility]** Retiring the old template factory initially revealed that still-imported legacy form classes import `BUILTIN_MODELS`. Preserve that constant as inert import compatibility until 02-08 removes the old classes; it builds/registers no extension and imports no legacy model. No active old administration route exists.
- Regression contracts were written before runtime retirement, ahead of their nominal second task, so the retirement has real RED→GREEN evidence. The named target failed on the intended `extra_models` registration assertion: 5 tests, 1 assertion failure, no fixture/import fault. `.planning/tmp/02-07-red.json` records the unchanged report, exit status and semantic assessment; classifier returned **RED_EVIDENCE_OK**. The later missing `reverse` import in the new Device-page test was a test-authoring error corrected before its final green run; it is not claimed as RED evidence.
- No baseline smoke change was required: it authenticates against native user endpoints and continues to pass.

## Outstanding Acceptance and Scope

Existing browser acceptance debt remains open in WINDOWS entries 1/2. This plan did not retry or claim browser interaction acceptance. Runtime HTTP and native rendering tests are not evidence of drag/keyboard/search-widget interaction. Phase 3 Parameters tab and Phase 4 native-value editing remain unimplemented. Optional legacy pytest was not run or claimed as passing.

## Known Stubs and Threat Surface

The empty API URL list and empty template-extension list intentionally retire obsolete integration; they are not incomplete profile features. The inert BUILTIN_MODELS constant is bounded migration compatibility until 02-08. No new endpoint, authentication path, dependency or schema trust boundary was added. T-02-17 has startup, route, serialization and preservation evidence.

## Self-Check: PASSED

All six planned task files and the RED evidence exist; all three task/evidence commits are reachable from HEAD. Final native and baseline checks pass; captured old/native counts/hash are identical. No generated/destructive migration exists for this plan.

## Next Plan Readiness

Ready for 02-08's blocking-human decision: **1 legacy config, 1 legacy group, 1 legacy field-membership row**, with all native/new-profile state preserved. Retain the internal event serializer. Do not remove browser acceptance debt or mark Phase 2 fully accepted from these automated checks.
