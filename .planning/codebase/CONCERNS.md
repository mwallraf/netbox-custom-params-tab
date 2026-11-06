---
last_mapped_commit: 3668f64a7f49effd8a6848dab96944de069a370c
last_mapped_at: 2026-11-06
---
# Concerns

**Analysis Date:** 2026-11-06

Scope: main checkout documentation and the existing implementation in
`.worktrees/feature/implement-plugin/`. Paths below are relative to that
implementation directory unless explicitly identified as repository-root paths.
Working files include uncommitted changes; HEAD alone is not the source snapshot.

## Tech Debt
- Repository root and implementation worktree are split; Git links are stale.
- Rename and earlier development changes remain uncommitted.
- `migrations/0001_initial.py` warns it was handcrafted and needs regeneration.
- App-label rename has no verified existing-database migration strategy.
## Known Bugs / Inspection Findings
- Field picker in `forms.py` offers all CustomField records without model scoping.
- Group rendering queries fields by group_name without object-type scoping.
- `extra_models` rendering registration is absent from form type choices.
- Detail ObjectView exists but its model-specific detail template was not found.
## Security Considerations
- Edit view requires both add and change config permissions for either operation.
- Native device object permission behavior is not yet exercised by tests.
- Applicability rules must never substitute for authorization.
## Performance Bottlenecks
- Current group fields are fetched in one query; explicit fields use select_related.
- Multiple profiles and dynamic field mode need query-count checks later.
## Fragile Areas
- Legacy group names are strings; renames/deletions can leave empty sections.
- Raw template values do not provide native type-aware formatting.
- Inline formset UI does not visibly render per-field validation errors.
## Scaling Limits
- OneToOne ContentType blocks multiple profiles for a model.
- Fixed template extensions currently span 12 models, beyond agreed initial scope.
## Dependencies at Risk
- Container tag and declared NetBox minimum are not verified as a support matrix.
- SQLite test settings may not represent real NetBox requirements.
## Missing Critical Features
- Profiles, matching filters, dedicated tab, and value editing are absent.
- Existing API scaffold does not manage fields or matching rules.
## Test Coverage Gaps
- No confirmed green suite, real tab UI checks, native permission parity,
  migration verification, package-install checks, or release validation.
