# Project Retrospective

## Milestone: v0.1.0 — Device Profiles

**Completed locally:** 2026-11-11
**Phases:** 5 | **Plans:** 18 | **Tasks:** 41

### What Was Built

Reusable Device profiles, native Custom Fields display and editing, automatic
matching, lifecycle safety, isolated runtime/test tools and public documentation.

### What Worked

Native generic views/forms retained validation, authority and change logging.
Real constrained-user and complete-snapshot tests caught data-preservation issues.
Installed-wheel tests proved packaging/import/schema behavior beyond source tests.
User-performed final UAT closed the browser-host limitation without invented proof.

### What Was Inefficient

Repeated unavailable browser attempts delayed acceptance until a manual handoff.
Static delivery was initially assumed from installation; a live 404 caused a real
profile-create failure despite passing server tests. The new actual HTTP asset
check closes that gap. Inconsistent summary schemas and stale status/digests made
closeout require manual reconciliation and explicit overrides.

### Patterns Established

Native values remain authoritative; plugin tables own only presentation config.
Partial editing preserves all values outside its edit set. Field-before-profile
locks coordinate save/cleanup. Runtime static HTTP and fresh installed-wheel
checks complement isolated behavior tests. Separate user/admin/dev/history docs.

### Key Lessons

1. Verify served JavaScript after image installation/static collection, not only wheel contents.
2. Keep canonical summary/status metadata consistent and regenerate verification evidence after scope changes.
3. Arrange manual UAT early when the browser host is unavailable; preserve who observed what.
4. Review core-view compatibility adapters when adding supported NetBox versions.

### Cost Observations

Model mix, session totals and token/cost totals were not measured; no figures are
inferred. Work spanned 2026-11-06 to 2026-11-11. Targeted reruns and an isolated
installed-wheel gate supplied current evidence without resetting live data.

## Cross-Milestone Trends

Only one milestone is complete; repeated trends cannot yet be established.

| Milestone | Phases / plans | Quality evidence | Process change |
|---|---|---|---|
| v0.1.0 | 5 / 18 | 109 native tests, 37 helpers, accepted user UAT | Live static delivery plus installed-wheel verification |
