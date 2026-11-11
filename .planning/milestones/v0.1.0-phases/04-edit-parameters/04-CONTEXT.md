# Phase 4: Edit Parameters

Authorized 2026-11-10 by “Continue with the project.” Browser UAT deferred to final user-run acceptance.

## Decisions

- One Device Edit Parameters destination covers currently matching enabled profiles. Deduplicate native fields in first-occurrence profile/field order.
- Reuse native NetBoxModelForm fields, widgets, serialization, required/type/custom validation, native change logging and constrained Device change permission. Native hidden/noneditable edit policy remains authoritative.
- Preserve native fields outside the editable set, unrelated Device properties, tags, profile configuration and field definitions. Re-resolve on POST; forged nonmember inputs cannot expand the editable set.
- Save/cancel return to Parameters. No add, clone or arbitrary return destination. No matching editable fields produces an explanatory page without a Save action.
- Browser tests remain pending for the user at project end. Automated native tests remain required.
