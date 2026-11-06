# Constraints and unresolved engineering details

## Constraints

- Use NetBox native custom field storage, types, validation, and permissions.
- Keep native definition/settings pages and editing screens unchanged.
- External scripts continue populating native values without plugin dependency.
- Preserve existing source and uncommitted work during baseline restoration.
- No implementation or shipping is part of this onboarding.
- Root `docs/REQUIREMENTS.md` remains product authority; generated GSD requirements
  must trace to it and must not silently add product decisions.

## Resolve during phase discussion/research

- Phase 1: supported NetBox version, real test environment, canonical source
  checkout, renamed app migration policy, and whether legacy configuration exists
  in any database that must be preserved. No deployment history is assumed.
- Phase 2: model design, delete behavior for referenced fields/filter targets,
  deterministic ordering ties, and all-fields ordering. Avoid deletion silently
  broadening a restrictive filter; precise policy needs an explicit design.
- Phase 3: tab behavior with no matches and empty-value presentation.
- Phase 4: use actual target-version NetBox field widgets/validation and object
  permission checks; preserve values outside the submitted applicable field set.
- No promise of compatibility with every NetBox 4.x version follows from the
  earlier minimum-version declaration or Docker tag.
