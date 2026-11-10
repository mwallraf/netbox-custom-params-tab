---
phase: 05-release-verification
status: human_needed
automated_status: passed
manual_status: deferred_by_user
---

# Release verification

| Requirement | Automated evidence | Remaining |
|---|---|---|
| REL-01 | Native CMTS/CPE/shared matching/rendering, dynamic fields, duplicate editing and preservation tests | Final manual workflow observations |
| REL-02 | Native-write freshness tests; plugin saves native Device values/change logs | Final manual native/Parameters round trip |
| REL-03 | Current wheel asset/import checks; fresh installed-wheel native test DB, 104 tests and migration drift checks; baseline/runtime/authentication pass | Final manual UI and acceptance sign-off |

All automated release gates passed. See 05-01-SUMMARY.md for observed markers and
timing. No visual evidence is claimed. User explicitly deferred all remaining
browser checks to final manual testing; no development task is blocked on browser
availability. Do not mark the milestone accepted or archive it until manual
results are recorded.
