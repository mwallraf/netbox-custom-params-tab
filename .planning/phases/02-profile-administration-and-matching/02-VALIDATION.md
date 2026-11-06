---
phase: "02"
slug: "profile-administration-and-matching"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-06"
---

# Phase 2 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Native Django TestCase on pinned NetBox 4.7.4 PostgreSQL |
| Config file | Native NetBox settings; bounded preparation establishes isolated test database |
| Quick run command | `make test-profiles` (created by first plan) |
| Full suite command | `make test-profiles` followed by `make test` |
| Estimated runtime | Unmeasured; record during preparation and tracer |

## Sampling Rate

- After every task commit: focused native profile tests, once runner exists.
- After each wave: profile suite and existing baseline.
- Before verification: full suite and native migration checks must pass.
- Feedback latency target: 120 seconds for focused reruns; measure rather than claim.

## Per-Task Verification Map

All commands execute from repository root. Bounded preparation 02-01 creates the additive native schema/resolver and isolated runner. The first meaningful end-to-end user tracer is 02-02 and must pass before feature expansions 03–08.

| Task ID | Plan | Wave | Requirements | Threat Ref | Secure behavior | Test type | Automated command | File exists | Status |
|---------|------|------|--------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | PROF-02/03/05, MATCH-03, DATA-01 | T-02-03 | Additive schema, native snapshots | Native ORM | Native manage.py test netbox_custom_field_profiles.tests.test_schema --noinput | Created by task | pending |
| 02-01-02 | 01 | 1 | DATA-01 | T-02-03 | Separate test DB; zero tests reject | Runner/baseline | make test-profiles; make test | Created by task | pending |
| 02-02-01 | 02 | 2 | PROF-01/02/03/05, MATCH-03, DATA-01 | T-02-01/02 | Native CRUD/form/resolution tracer | Native client/ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_tracer | Created by task | pending |
| 02-02-02 | 02 | 2 | PROF-01 | T-02-01 | Permission-aware native navigation | Native client | make test-profiles; make test | Runner from 01 | pending |
| 02-03-01 | 03 | 3 | PROF-02/04/05/06, DATA-01 | T-02-04/05/06 | Exact ordered-ID validation and rollback | Native form/ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_selection | Created by task | pending |
| 02-03-02 | 03 | 3 | PROF-04/05 | T-02-04 | Packaged browser order and templates | Native plus browser | make test-profiles | Runner from 01 | pending |
| 02-04-01 | 04 | 4 | MATCH-01/02/03, DATA-01 | T-02-07/08 | Restricted references and fixed matching | Native form/ORM | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_matching | Created by task | pending |
| 02-04-02 | 04 | 4 | PROF-01/03, MATCH-01/03 | T-02-09 | Escaped summaries/native widget | Native client/browser | make test-profiles | Runner from 01 | pending |
| 02-05-01 | 05 | 5 | MATCH-01/03, DATA-01 | T-02-10 | Disable before cascade; rollback | Native transaction | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_lifecycle | Created by task | pending |
| 02-05-02 | 05 | 5 | PROF-04/05, DATA-01 | T-02-11/12 | Idempotent plugin-only cleanup | Native transaction | make test-profiles | Runner from 01 | pending |
| 02-06-01 | 06 | 6 | PROF-01/02, DATA-01 | T-02-13/14 | Action/constraint/CSRF enforcement | Native client | python3 scripts/test_profiles.py --label netbox_custom_field_profiles.tests.test_permissions | Created by task | pending |
| 02-06-02 | 06 | 6 | All Phase 2 IDs | T-02-15 | Native snapshots unchanged | Native integration/browser | make test-profiles; make test | Created by task | pending |
| 02-07-01 | 07 | 7 | PROF-01, DATA-01 | T-02-17 | Retire obsolete runtime consumers | Native integration | make test-profiles; make check | Existing by wave 7 | pending |
| 02-07-02 | 07 | 7 | PROF-01, DATA-01 | T-02-17 | Durable native/new-profile preservation; one-time old-row evidence in summary | Native integration | make test-profiles; make test | Existing by task | pending |
| 02-08-01 | 08 | 8 | DATA-01 | T-02-16 | Explicit one-way deletion decision | Human plus baseline | make check | Existing | pending |
| 02-08-02 | 08 | 8 | PROF-01/02, DATA-01 | T-02-16 | Legacy-only migration, final absence introspection/schema tests, native/new-profile snapshots | Native schema | Native makemigrations --check --dry-run; make test-profiles; make test | Existing by task | pending |

## Wave 0 Requirements

- Preparation 02-01 creates plugin-owned native schema tests, isolated runner and make test-profiles.
- Runner proves isolated native PostgreSQL use and rejects zero discovered tests.
- Tracer 02-02 proves real administration CRUD/navigation and reusable matching before expansion.
- No optional historical pytest or SQLite settings dependency.

## Manual-Only Verifications

| Behavior | Requirement | Why manual | Test instructions |
|----------|-------------|------------|-------------------|
| Drag order and accessible alternative persist | PROF-04 / D-05 | Server tests cannot prove browser interaction | Drag three fields, save/reload; repeat using keyboard controls |
| Search unused Device-compatible tag | MATCH-01 / D-12 | Native widget integration | Search a compatible unused tag, select/save/reload |
| Error and mode-switch interaction | PROF-02, PROF-04, PROF-05 | Browser state and errors | Invalid submission retains choices; Selected → All → Selected restores order |

## Validation Sign-Off

- [ ] Every task has automated verification or explicit first-tracer dependencies.
- [ ] No three consecutive tasks lack automated checks.
- [ ] Missing references are created before use.
- [ ] No watch-mode commands; zero-test false greens rejected.
- [ ] Focused runtime measured.
- [ ] Native values/settings remain unchanged by plugin management.

Approval: pending execution evidence. Planning review checks coverage, not implementation success.
