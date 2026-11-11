---
phase: "02"
slug: "profile-administration-and-matching"
status: verified
threats_open: 0
asvs_level: 1
register_authored_at_plan_time: true
created: "2026-11-06"
---

# Phase 2 — Security

All 18 authored threats were verified CLOSED by the independent gsd-security-auditor. Blocking threshold: high. Existing native framework controls were traced in the pinned installed source; no new threat scope or accepted risk was invented.

## Trust Boundaries

| Boundary | Data crossing |
|---|---|
| Administrator request → native generic views | Action and constrained-object authority |
| Form/widget → profile aggregate | Untrusted reference IDs and ordered selection |
| Native lifecycle → plugin receivers | Reference deletion/applicability events |
| Migration/test runner → PostgreSQL | Approved schema and isolated test execution |

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation evidence | Status |
|---|---|---|---|---|---|---|
| T-02-01 | Elevation | Profile CRUD | high | mitigate | views.py; tests/test_permissions.py | closed |
| T-02-02 | Tampering | Profile save | high | mitigate | forms.py; models.py; tests/test_permissions.py | closed |
| T-02-03 | Tampering | Schema and test runner | high | mitigate | migrations/0002_profiles.py; tests/runner.py; scripts/test_profiles.py | closed |
| T-02-04 | Tampering | Ordered ID payload | high | mitigate | forms.py; tests/test_selection.py | closed |
| T-02-05 | Tampering | Mode switch | high | mitigate | forms.py; tests/test_selection.py | closed |
| T-02-06 | Elevation | Field choice reference | high | mitigate | forms.py; native restrict_form_fields; tests/test_selection.py | closed |
| T-02-07 | Information | Search selectors | high | mitigate | forms.py; tests/test_matching.py | closed |
| T-02-08 | Tampering | Matching | high | mitigate | matching.py; models.py; tests/test_matching.py | closed |
| T-02-09 | Tampering | HTML summary | medium | mitigate | matching.py; templates; profile_fields.js textContent; tests/test_matching.py | closed |
| T-02-10 | Tampering | Target deletion | high | mitigate | signals.py pre_delete; tests/test_lifecycle.py | closed |
| T-02-11 | Tampering | Field cleanup | high | mitigate | signals.py transaction and bidirectional m2m handling; tests/test_lifecycle.py | closed |
| T-02-12 | Tampering | Native data | high | mitigate | signals.py plugin-only writes; tests/test_lifecycle.py; tests/test_preservation.py | closed |
| T-02-13 | Elevation | Direct requests | high | mitigate | views.py native generic views; tests/test_permissions.py | closed |
| T-02-14 | Tampering | Request integrity | high | mitigate | native CSRF middleware; forms.py atomic save; tests/test_permissions.py | closed |
| T-02-15 | Tampering | Native definitions and values | high | mitigate | tests/test_preservation.py complete native snapshots | closed |
| T-02-16 | Tampering | Schema retirement | high | mitigate | 02-08-DECISION.md commit 1ca2e53; migrations/0003_retire_legacy_configuration.py; tests/test_schema.py | closed |
| T-02-17 | Denial | Runtime consumers | high | mitigate | api/urls.py empty; internal serializer retained; template_content.py empty extensions; tests/test_preservation.py | closed |
| T-02-SC | Tampering | Package installation | high | mitigate | pyproject.toml diff changes package-data only; no new dependencies | closed |

Paths are relative to netbox_custom_field_profiles unless prefixed scripts or planning. Native view dispatch, restricted querysets/form references, transaction/post-save constraint enforcement, and CSRF middleware were inspected in the installed NetBox source.

## Accepted Risks Log

No accepted risks. All authored mitigations exist. Browser acceptance remains pending in WINDOWS entries 1/2; these security closures do not claim live UI acceptance.

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|---|---|---|---|---|
| 2026-11-06 | 18 | 18 | 0 | Independent gsd-security-auditor |

Recent 49 native tests and 35-helper baseline evidence reused; no redundant test execution in this audit.

## Sign-Off

- [x] All authored threats have a disposition and source/test evidence.
- [x] Accepted risks log checked; none.
- [x] threats_open: 0 at high blocking threshold.
- [x] status: verified.

## Corrective review follow-up

Independent general code review found and reproduced two lifecycle correctness defects after the initial threat audit. They were fixed in 1f97946 and 07a223c and independently re-reviewed clean. Persistence now revalidates under coordinated native-field/profile locking; native request abort preserves cleanup results. Fields pending native deletion are rejected, while provisioning memberships remain. These strengthen T-02-04/05/06/10/11/12/14 mitigations. The complete 63-test native suite is green, including concurrency/rollback/restricted-choice cases. No open finding or accepted risk remains; browser acceptance is still unverified.
