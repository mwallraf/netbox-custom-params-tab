---
phase: 04-edit-parameters
plan: 01
status: implemented_automated_pass
requirements: [EDIT-01, EDIT-02, EDIT-03, EDIT-04, AUTH-02]
---

# Edit Parameters implementation

Implemented a registered native Device Edit Parameters view and a partial native
Device ModelForm. Current matching fields are deduplicated in first-occurrence
order; native UI editability and restricted related-object choices apply.
Inaccessible saved reference sets are omitted intact. A signed field scope
rejects stale definitions/membership. Native validation, stale-Device detection,
change logging and transactional post-save permission checks are retained.
Device row locking precedes POST value reads. Excluded fields/properties/tags and
profile/native definitions are preserved. Native validation's orphan-key pruning
is corrected only for pre-existing storage outside this partial form's edit set.

## Observed verification

- Initial focused suite caught loss of orphaned stored keys during native model
  cleaning; untouched values are now restored after native validation.
- Final full native suite: 104 tests in 22.676 seconds; end to end 28.19 seconds.
  Includes 15 new editor tests covering real GET/POST, all 13 native types,
  deduplication, preservation, hidden/read-only fields, invalid/unique values,
  stale scope/timestamp, constrained viewers/references, CSRF, post-save authority
  rollback and forged clone/quick-add flags.
- PROFILE_TESTS_ISOLATED and PROFILE_LIVE_UNCHANGED observed.
- Required baseline: 35 helper tests pass; CONFIG_OK, RUNTIME_OK,
  BASELINE_SMOKE_OK and SEED_IDEMPOTENT_OK observed.

No migration was added. No browser test was attempted: the user explicitly moved
all browser UAT to final manual acceptance on 2026-11-10. Eight editor cases remain
pending in 04-UAT.md, alongside Phase 3’s 15 cases. Phase 3’s no-edit-action
expectation is intentionally superseded for authorized editors.
