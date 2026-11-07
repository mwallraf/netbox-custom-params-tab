# Roadmap: NetBox Custom Field Profiles

## Overview

Deliver the first Device-profile milestone from the existing panel-based code.
Restore a trustworthy baseline, then build administration/matching, display,
editing, and release verification. No feature phase has started.

## Phases

- [x] **Phase 1: Reproducible baseline** - A developer can install, run, and test the renamed plugin from a usable checkout without losing prior work. (completed 2026-11-06)
- [ ] **Phase 2: Profile administration and matching** - Administrators can define reusable Device profiles and determine which profiles match a Device.
- [ ] **Phase 3: Parameters tab** - Users can view relevant native fields as ordered profile sections in a dedicated Device tab.
- [ ] **Phase 4: Edit Parameters** - Authorized users can edit relevant native values once, with native validation and safe persistence.
- [ ] **Phase 5: Release verification** - The agreed Device workflow is verified, installable, and documented.

## Phase Details

### Phase 1: Reproducible baseline
**Goal**: A developer can install, run, and test the renamed plugin from a usable checkout without losing prior work.
**Depends on**: Nothing (first phase)
**Requirements**: BASE-01, BASE-02, BASE-03, BASE-04
**Success Criteria** (what must be TRUE):
  1. Existing source and uncommitted changes are preserved in a documented usable checkout; stale worktree metadata no longer obstructs development.
  2. A documented supported NetBox version runs the renamed plugin and its reproducible test stack.
  3. Schema checks and the chosen legacy-app/config migration policy are verified before applying destructive or incompatible changes.
  4. Required baseline checks pass; known residual failures and their scope are explicitly recorded.
**Plans**: 4/4 complete.
**Wave 1**
- [x] 01-01-PLAN.md

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 01-02-PLAN.md

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 01-03-PLAN.md

**Wave 4** *(blocked on Wave 3 completion)*
- [x] 01-04-PLAN.md

### Phase 2: Profile administration and matching
**Goal**: Administrators can define reusable Device profiles and determine which profiles match a Device.
**Depends on**: Phase 1
**Requirements**: PROF-01, PROF-02, PROF-03, PROF-04, PROF-05, PROF-06, MATCH-01, MATCH-02, MATCH-03, DATA-01
**Success Criteria** (what must be TRUE):
  1. An authorized administrator can create multiple Device profiles with title, enable state, order, and only Device-applicable field choices.
  2. Selected mode preserves ordered membership; all-fields mode includes a newly created applicable field without editing the profile.
  3. Profiles support Device Type, role, and tag filters; tests demonstrate AND across rules, OR within values, and no-rules matching all Devices.
  4. Profiles allow duplicate native fields across sections and managing profiles changes neither native settings nor values.
**Plans**: 8/8 plans executed.
**Wave 1**
- [x] 02-01-PLAN.md — Bounded additive schema, native resolver and isolated test preparation.

**Wave 2** *(blocked on Wave 1 completion)*
- [x] 02-02-PLAN.md — First meaningful native CRUD/resolution tracer and navigation.

**Wave 3** *(blocked on Wave 2 completion)*
- [x] 02-03-PLAN.md — Ordered field selection, native All mode and drag/keyboard controls.

**Wave 4** *(blocked on Wave 3 completion)*
- [x] 02-04-PLAN.md — Searchable fixed rules, deterministic matching and scope summaries.

**Wave 5** *(blocked on Wave 4 completion)*
- [x] 02-05-PLAN.md — Safe target deletion and selected-field applicability cleanup.

**Wave 6** *(blocked on Wave 5 completion)*
- [x] 02-06-PLAN.md — Native permission, preservation and browser evidence.

**Wave 7** *(blocked on Wave 6 completion)*
- [x] 02-07-PLAN.md — Reversible runtime retirement and verified old-row inventory.

**Wave 8** *(blocked on Wave 7 completion)*
- [x] 02-08-PLAN.md — Approved legacy schema retirement and final native checks.

### Phase 3: Parameters tab
**Goal**: Users can view relevant native fields as ordered profile sections in a dedicated Device tab.
**Depends on**: Phase 2
**Requirements**: TAB-01, TAB-02, TAB-03, AUTH-01
**Success Criteria** (what must be TRUE):
  1. A real Device detail page has a dedicated Parameters tab rather than an injected main-page panel.
  2. Only matching enabled profiles appear, in a deterministic section/field order.
  3. Native values, repeated fields, and supported field types render correctly; no-match and empty-value behavior is agreed and verified.
  4. Native viewing rules apply on both navigation and direct URLs.
**Plans**: TBD — created during phase planning.

### Phase 4: Edit Parameters
**Goal**: Authorized users can edit relevant native values once, with native validation and safe persistence.
**Depends on**: Phase 3
**Requirements**: EDIT-01, EDIT-02, EDIT-03, EDIT-04, AUTH-02
**Success Criteria** (what must be TRUE):
  1. A single Edit Parameters page offers each applicable field once, including fields repeated in display sections.
  2. Native field validation and widgets work; invalid values show actionable errors without saving invalid data.
  3. Successful saves update native values and preserve fields outside the edit set.
  4. Unauthorized direct requests and POSTs cannot read or change restricted objects; permission behavior matches native editing.
**Plans**: TBD — created during phase planning.

### Phase 5: Release verification
**Goal**: The agreed Device workflow is verified, installable, and documented.
**Depends on**: Phase 4
**Requirements**: REL-01, REL-02, REL-03
**Success Criteria** (what must be TRUE):
  1. CMTS, CPE, and shared profiles pass end-to-end matching/display/edit acceptance, including dynamic fields and duplicates.
  2. Native script writes appear in the tab and plugin edits remain available through native NetBox facilities.
  3. Clean package installation and migration checks pass on the supported version.
  4. Installation/configuration/limitations documentation and manual UI evidence are present; all 26 requirements have verified evidence.
**Plans**: TBD — created during phase planning.

## Discussion and Research Gates

- Phase 1: supported version, source location, existing deployment/data needs,
  app rename and legacy configuration migration policy.
- Phase 2: model design, deletion behavior for filter targets/fields, ordering
  ties and all-fields ordering. Prevent accidental filter broadening.
- Phase 3: no-matching-profile tab behavior and empty-value presentation.
- Phase 4: native form, validation, permission, and safe-save integration.

These details are not silently decided by this roadmap. No arbitrary object
filter engine or multi-object-type scope is included.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Reproducible baseline | 4/4 | Complete    | 2026-11-06 |
| 2. Profile administration and matching | 8/8 | Awaiting browser acceptance | - |
| 3. Parameters tab | 0/TBD | Not started | - |
| 4. Edit Parameters | 0/TBD | Not started | - |
| 5. Release verification | 0/TBD | Not started | - |

*Last updated: 2026-11-06 after Phase 1 verification.*
