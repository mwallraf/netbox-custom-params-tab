---
phase: 02-profile-administration-and-matching
plan: "08"
subsystem: database
tags: [netbox, migrations, retirement, preservation]
requires:
  - phase: 02-07
    provides: Retired legacy runtime and exact pre-deletion inventory
provides:
  - Explicitly authorized legacy configuration schema retirement
  - Sole active CustomFieldProfile administration representation
  - Verified native/new-profile preservation after migration and restart
affects: [phase-verification, phase-3]
actuals:
  tokens: 3873
  tasks: 2
  commits: 2
plan_head_before: d628eb61c48bafc805840d60d1961f37dff8fa13
plan_head_after: 505abbe967a2442f4952a6830f98179a98bc1de6
tech-stack:
  added: []
  patterns: [constraint-first legacy deletion, explicit irreversible decision, native row snapshot]
key-files:
  created:
    - .planning/phases/02-profile-administration-and-matching/02-08-DECISION.md
    - netbox_custom_field_profiles/migrations/0003_retire_legacy_configuration.py
  modified:
    - netbox_custom_field_profiles/models.py
    - netbox_custom_field_profiles/forms.py
    - netbox_custom_field_profiles/views.py
    - netbox_custom_field_profiles/tables.py
    - netbox_custom_field_profiles/template_content.py
key-decisions:
  - User explicitly selected retire without an export for the three inventoried legacy rows.
  - Clear legacy compound constraints before removing their referenced fields in generated 0003.
requirements-completed: [PROF-01, PROF-02, DATA-01]
coverage:
  - id: approved-retirement
    description: Explicit retire decision followed by exact legacy-only forward migration
    requirement: PROF-01
    verification:
      - kind: integration
        ref: 02-08-DECISION.md and 0003_retire_legacy_configuration.py
        status: pass
    human_judgment: false
  - id: final-schema-preservation
    description: Old tables absent, new profile tables usable, native definitions and Device data unchanged
    requirement: DATA-01
    verification:
      - kind: integration
        ref: netbox_custom_field_profiles/tests/test_schema.py#test_schema_matches_applied_retirement_state
        status: pass
      - kind: integration
        ref: 02-08-SUMMARY.md#native-and-new-profile-preservation
        status: pass
    human_judgment: false
duration: 6min
completed: 2026-11-06
status: complete
---

# Phase 2 Plan 8: Approved Legacy Schema Retirement Summary

**The three obsolete configuration models and their rows are removed by an explicitly approved native migration, with native definitions, Device data and new profile state unchanged.**

## Task Commits

1. **Confirm deletion of obsolete plugin configuration** — `1ca2e53`: recorded the user's explicit **retire** response, exact three-model scope and no-export choice.
2. **Generate and apply legacy-only retirement, then verify the live schema** — `505abbe`: removed old model/form/view/table classes and their inert compatibility constant, and applied reviewed 0003.

The measured two commits above exclude this SUMMARY metadata commit. The plan ledger anchors both hashes for reproducible actuals.

## Approval and Removal Scope

Before deletion the live database contained one row in each of `CustomTabConfig`, `CustomTabConfigGroup` and `CustomTabConfigField`. The blocking-human checkpoint explained that reversing DeleteModel cannot recover those rows. The user selected **retire**, authorizing their removal without a configuration export. The committed decision is in `02-08-DECISION.md`.

The migration alters/removes constraints and fields only on those three obsolete models, then deletes them. It depends on `0002_profiles`; 0001 and 0002 are unchanged. Native CustomField definitions/settings, Device custom_field_data and new profile tables are outside its operations. No fake migration, reset or native data cleanup was used.

## Native and New-Profile Preservation

Read-only connection introspection and ordered full-row hashing captured native Device/custom-field tables and every new profile/membership table before and after retirement. Legacy tables were deliberately excluded from the preservation hash because their deletion was the approved operation.

**Identical before/after SHA-256:**

`a9eea3c6e89766d10110e8ad3087930607b5318e4d28ce065350254cab9207f3`

| Data | Before | After |
|---|---:|---:|
| Legacy configuration table | 1 row | table absent |
| Legacy group membership table | 1 row | table absent |
| Legacy field membership table | 1 row | table absent |
| Native Devices | 2 | 2 |
| Native CustomFields | 2 | 2 |
| Native applicability memberships | 2 | 2 |
| Native choice sets | 0 | 0 |
| New profile table | 0 rows | 0 rows, table usable |
| New selected-field/reference tables | 0 rows each | 0 rows each, tables present |

Native tests independently exercise populated profile CRUD, ordered memberships, matching, lifecycle and preservation in isolated PostgreSQL. Live equality does not claim that the empty sandbox profile tables alone prove populated behavior.

## Verification

- Native `migrate`: **0003_retire_legacy_configuration applied OK**.
- Native `showmigrations netbox_custom_field_profiles`: **0001, 0002 and 0003 all [X]**.
- Native `makemigrations netbox_custom_field_profiles --check --dry-run`: **No changes detected**.
- Native `manage.py check`: **no issues (0 silenced)**.
- Dedicated web and worker restarted before final test suites; `make up` confirmed readiness.
- `make test-profiles`: **49 native tests pass**, **7.117 s** native / **12.27 s** runner; isolated PostgreSQL and **PROFILE_LIVE_UNCHANGED** confirmed. This includes the migration-state-aware final legacy-table absence assertion.
- `make test`: **35 helper tests pass**, runtime/schema/registration, real administrator session, native token and negative controls, and seed idempotence all pass.
- Real authenticated HTTP profile list and add pages return **200**; old configuration API returns **404**.
- Native/new-profile snapshot counts and hash remain identical after final checks.
- Source compilation and `git diff --check` pass. No removed-model imports remain in durable feature tests or active plugin code; legacy names remain only in migration history and absence assertions.

## Deviations and Issues

**[Rule 1 — native generated migration ordering]** The pinned Django autodetector emitted `RemoveField(tab_config)` before `AlterUniqueTogether` for constraints that referenced that field. The first native apply raised `FieldDoesNotExist`. PostgreSQL atomic migration rollback was verified: all three legacy rows remained and the native/new-profile hash matched the original. Reordered the two generated constraint-removal operations ahead of field removals, preserving the exact authorized scope; the corrected migration then applied successfully. The durable test database also migrated through this corrected operation sequence.

**[Rule 3 — obsolete compatibility removal]** Removed the inert `BUILTIN_MODELS` constant from template_content.py once its legacy form import was removed. This sixth source file is a bounded cleanup of the temporary compatibility added in 02-07. The conventional empty template-extension resource, internal CustomFieldProfileSerializer and ready() lifecycle registration remain intact.

A model-drift command issued during service restart exited nonzero before the service was ready. It was rerun after `make up` and passed; the interrupted attempt is not counted as verification. The pre-existing LOGIN_REQUIRED deprecation warning remains unchanged. Optional legacy pytest was not run or claimed as passing.

## Scope and Outstanding Acceptance

All eight Phase 2 plans are now implemented; phase completion still requires the orchestrator's review/verifier gates. Existing browser interaction acceptance remains pending in WINDOWS entries 1/2. No drag, keyboard, mode-switch or search-widget browser pass is claimed by this schema plan. No new browser verification debt was introduced.

No new package, endpoint or authentication surface was added. T-02-16 has explicit decision, exact generated-operation review, applied schema/introspection and snapshot evidence. The empty template resource is intentional retirement, not an unfinished profile feature. Parameters tab and native-value editing remain for Phases 3 and 4.

## Self-Check: PASSED

Decision artifact, generated migration and all modified source paths exist. Both task commits are ancestors of HEAD. Migration history 0001/0002 is intact; final native/baseline checks pass and the preservation hash matches. SUMMARY status records plan implementation completion, not completed browser acceptance or completed Phase 2 verification.
