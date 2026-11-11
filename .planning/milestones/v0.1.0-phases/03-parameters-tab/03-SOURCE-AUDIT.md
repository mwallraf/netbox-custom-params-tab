# Phase 03 — Source Coverage and Planning Assumptions

Planning only; no Phase 03 execution or completion is asserted. Source authority:
docs/REQUIREMENTS.md, ROADMAP, REQUIREMENTS, 03-CONTEXT, 03-RESEARCH and current
tracked root/PATTERNS. Historical worktree maps are excluded.

| SOURCE | ID | Feature/constraint | Plan/task | Status | Notes |
|---|---|---|---|---|---|
| GOAL | — | Relevant native fields in ordered Device profile tab | 03-01–04 | COVERED | Native registration → safe complete display → evidence |
| REQ | TAB-01 | Dedicated Device tab | 03-01-T1/T2, 03-04-T2 | COVERED | Cold process and browser |
| REQ | TAB-02 | Matching ordered profiles and fields | 03-02-T1 | COVERED | Existing resolvers, real responses |
| REQ | TAB-03 | Native types/duplicates/relevant empties | 03-02-T1/T2, 03-03-T2, 03-04-T1/T2 | COVERED | 13 types, freshness, visual evidence |
| REQ | AUTH-01 | Native viewing authority | 03-01-T2, 03-03-T1, 03-04-T1 | COVERED | Device and related-object constraints |
| CONTEXT | D-01 | Match-based tab visibility | 03-01-T1/T2 | COVERED | Zero fields still a match |
| CONTEXT | D-02 | Authorized no-match direct page | 03-01-T2 | COVERED | Native authority first; exact message |
| CONTEXT | D-03 | Matching empty section retained | 03-01-T2, 03-02-T1 | COVERED | Exact distinct message |
| CONTEXT | D-04 | No profile-admin grant needed | 03-01-T2 | COVERED | Device-only viewer subject |
| CONTEXT | D-05 | All relevant fields; Not set | 03-02-T2 | COVERED | Muted type-aware placeholder |
| CONTEXT | D-06 | False/zero/JSON empty semantics | 03-02-T2 | COVERED | Explicit typed cases |
| CONTEXT | D-07 | Independent ui_visible, unchanged authority/settings | 03-02-T2, 03-03-T1, 03-04-T1 | COVERED | Hidden/unset If Set plus real access |
| CONTEXT | D-08 | Expanded stacked native cards | 03-02-T1, 03-03-T2, 03-04-T2 | COVERED | No nested/collapse/layout-state features |
| CONTEXT | D-09 | Duplicate titles, deterministic order | 03-02-T1 | COVERED | Ordered records; resolver order |
| CONTEXT | D-10 | Native label/raw-name fallback/help | 03-02-T2, 03-03-T2 | COVERED | Secondary escaped help |
| CONTEXT | D-11 | Duplicate live native values | 03-02-T1, 03-04-T1 | COVERED | No copied values/cross-request cache |
| CONTEXT | D-12 | Supported native rendering | 03-02-T2, 03-03-T1/T2 | COVERED | No parallel type formatter |
| CONTEXT | D-13 | Full long values and sanitization | 03-03-T2, 03-04-T2 | COVERED | URL, Markdown, JSON/browser |
| CONTEXT | D-14 | Device and reference restrictions | 03-01-T2, 03-03-T1 | COVERED | Native constrain/restrict before disclosure |
| CONTEXT | D-15 | Read-only, no inactive edit action | 03-01-T2, 03-04-T1/T2 | COVERED | POST unsupported, preservation |
| RESEARCH | R-01 | Early ready import/native Device ObjectView/ViewTab | 03-01-T1 | COVERED | Fresh process, no test-side import repair |
| RESEARCH | R-02 | Reuse active-field/matching helpers, dynamic membership | 03-02-T1 | COVERED | No new matching/lifecycle engine |
| RESEARCH | R-03 | Native formatter leaks unrestricted reference lookups | 03-01-T1, 03-03-T1 | COVERED | Restrict before rendering; never raw-deserialize again |
| RESEARCH | R-04 | Scalar missing/denied and mixed/all-denied multiobjects | 03-03-T1 | COVERED | Neutral unavailable, no IDs/labels/links/counts |
| RESEARCH | R-05 | Native URL visible text truncation | 03-03-T2 | COVERED | Complete text, native scheme safety |
| RESEARCH | R-06 | All 13 types and meaningful empty JSON | 03-02-T2 | COVERED | Datetime explicitly included |
| RESEARCH | R-07 | Full line breaks/JSON overflow require browser proof | 03-03-T2, 03-04-T2 | COVERED | HTML evidence does not close visual UAT |
| RESEARCH | R-08 | Native sanitization, safe help/metadata | 03-03-T2 | COVERED | Hostile persisted payload matrix |
| RESEARCH | R-09 | Native writes/freshness and request preservation | 03-02-T1, 03-04-T1 | COVERED | Complete snapshot boundaries |
| RESEARCH | R-10 | Isolated PostgreSQL runner, nonzero tests/live preservation | Every automated behavioral task | COVERED | Existing supported labels/commands |
| RESEARCH | R-11 | No install/schema change; HTML packaging | 03-02-T2, 03-03-T2, 03-04-T1 | COVERED | Scoped template styles, native schema baseline |
| RESEARCH | R-12 | Native administration/panel retirement retained | 03-01-T1, 03-04-T1 | COVERED | Existing suites and no panel test |
| RESEARCH | R-13 | Accurate capability and pending-browser documentation | 03-04-T2 | COVERED | Actual evidence only |
| RESEARCH | R-14 | Explicit dispositions for research open questions | 03-01-T1, 03-04-T2 | COVERED | All three marked RESOLVED for planning; cold-start/browser execution still pending |

All in-scope source items are planned. Phase 4 editing and Phase 5 release-wide
verification remain excluded by roadmap/context; they are not missing Phase 03
items. Prohibitions are carried in each plan's flat statement/status/verification
must_haves entries and have concrete owning tests or evidence tasks.

## Dependency and ownership graph

03-01 (wave 1, first end-to-end tracer) → 03-02 (wave 2, complete native
sections/types) → 03-03 (wave 3, reference/full-value refinements) → 03-04 (wave 4,
integrated preservation/browser evidence). Each task consumes its prior runnable
slice and improves the real Device workflow. Shared presentation/template/test
files prevent concurrent plans; there are no same-wave file conflicts. New test
modules are created within their owning behavioral tasks, before their commands.
The final acceptance plan owns six files: one integration test module plus five
documentation/evidence files. Its preservation/freshness cases are consolidated
in test_parameter_permissions.py; the other focused modules remain read-only
regression inputs. Any implementation defect reopens its original owning task
in plans 01–03 before final acceptance resumes; no optional production seams are
reserved by plan 04. All eight tasks and their acceptance cases remain intact.

## Discovery, assumptions and contribution decisions

- Discovery Level 1 is satisfied by completed exact-runtime/official-doc research;
  the phase does not select a new dependency or external service. Context7 was
  unavailable during research; exact NetBox 4.7.4 evidence governs mechanics.
- The spec-less edge classifier returned TAB-01, TAB-02, TAB-03 and AUTH-01 as
  unclassified/unresolved because no SPEC exists. This is a classifier limitation,
  not proof that there are no edge cases or that any classifier item was resolved.
  Concrete tests cover authorization-before-empty-state, match-with-zero-fields,
  native type empties, hidden/If Set presentation, missing/mixed references,
  cross-user requests, unsafe/full URLs, native freshness and preservation.
- No UI-SPEC exists. The UI gate reports frontend=true, hasUiSpec=false,
  block=false. The adopted CONTEXT and native patterns define this phase's UI;
  actual browser evidence remains mandatory for acceptance.
- API contribution: no external API capability surface exists; COVERAGE.md gives
  the reasoned in-process-only declaration, including potential terminology false
  positives from native APIs/plugin integration.
- Assumption-delta contribution: no-change. Device remains the primary native
  object and custom_field_data the sole value authority; multiple profiles and
  Selected/All were already established in Phase 2. No identity generalization,
  newly optional anchor or additional source of truth is introduced.
- Schema contribution: no schema-push task applies. No model/migration/schema file
  is modified; native schema drift remains checked by the required baseline.
- Reversibility: all new choices are local view/adapter/markup decisions behind
  existing native storage. No new one-way decision or human checkpoint is needed.
- Estimate calibration returned factor=1, samples=0, confidence=low. Raw and
  calibrated estimates are therefore equal; 2 tasks per plan, at most 5 modified
  files per task. No external account/user setup is required.
- Parent authorization is planning only. No production/configuration edit, service
  restart, feature execution, branch/worktree or commit was performed by planning.
