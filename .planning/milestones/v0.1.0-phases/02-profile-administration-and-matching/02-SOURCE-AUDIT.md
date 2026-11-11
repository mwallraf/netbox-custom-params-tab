# Phase 2 source coverage audit

| Source | ID / capability | Plan | Status |
|--------|-----------------|------|--------|
| GOAL | Define reusable Device profiles and determine matches | 01–08 | COVERED |
| REQ | PROF-01 | 02,04,06,07,08 | COVERED |
| REQ | PROF-02 | 01,02,03,06,08 | COVERED |
| REQ | PROF-03 | 01,02,04,06 | COVERED |
| REQ | PROF-04 | 03,05,06 | COVERED |
| REQ | PROF-05 | 01,02,03,05,06 | COVERED |
| REQ | PROF-06 | 03,06 | COVERED |
| REQ | MATCH-01 | 04,05,06 | COVERED |
| REQ | MATCH-02 | 04,06 | COVERED |
| REQ | MATCH-03 | 01,02,04,05,06 | COVERED |
| REQ | DATA-01 | 01–08 | COVERED |
| CONTEXT | D-01/D-02/D-03/D-11/D-15 | 01,02,04 | COVERED |
| CONTEXT | D-04/D-09/D-10/D-12 | 04 | COVERED |
| CONTEXT | D-05/D-06/D-07/D-08 | 03 | COVERED |
| CONTEXT | D-13/D-14/D-16 | 05 | COVERED |
| RESEARCH | Native CRUD/permissions/atomic save | 02,03,06 | COVERED |
| RESEARCH | Native active field ordering/dynamic resolution | 01,03 | COVERED |
| RESEARCH | Separate applicability tags/unused-tag discovery | 01,04 | COVERED |
| RESEARCH | Queryset/deferred deletion, reverse/clear/set, idempotence/rollback | 05 | COVERED |
| RESEARCH | Isolated native PostgreSQL and zero-test rejection | 01 | COVERED |
| RESEARCH | Packaged assets, drag/keyboard/browser evidence | 03,04,06 | COVERED |
| RESEARCH | Native preservation and signal bypass boundary | 05,06 | COVERED |
| RESEARCH | Additive schema, runtime retirement, approved schema deletion, restart/checks | 01,07,08 | COVERED |
| RESEARCH | No new packages, no legacy upgrade mapping, roadmap boundaries | All plans | COVERED |

## Deterministic edge probe accounting

23 surfaced items = 18 explicit truth entries + 5 flagged unclassified assumptions. None is silently dismissed.

- Plan 02: PROF-01 adjacency/empty/ordering/idempotency/concurrency and PROF-03 adjacency/empty/ordering (8).
- Plan 03: PROF-05 adjacency/empty/ordering (3).
- Plan 04: MATCH-02 boundary/precision and MATCH-03 adjacency/empty/ordering/idempotency/concurrency (7).
- Flagged: PROF-02 in 02; PROF-04/PROF-06 in 03; MATCH-01 in 04; DATA-01 in 06 (5).

## Prohibition recall

Plan 06 retains the ten-candidate recall disposition: explicit authoritative product fences remain covered, routine engineering/security controls remain in normal validation/threat models, and no new implied values/safety prohibition survives precision/canon-referral filtering. Projection input is empty; no invented prohibition descriptor is emitted.

## Dependency and revision sizing

Eight serial waves reflect real preparation and shared file dependencies. Plan 01 prepares/proves the native schema and runner in 8 files (5/4 per task); the first meaningful production end-to-end tracer in 02-02 modifies 6 files (5/2 per task) and must pass before feature expansions. It reuses verified installed generic/object*.html templates; dedicated templates move to 03. All plans are below 10 modified files. Reversible runtime retirement 07 passes independently before 08's explicit decision and destructive migration. No scope or locked decision was dropped. Estimates retain measured calibration factor 1 and low confidence (zero samples).
