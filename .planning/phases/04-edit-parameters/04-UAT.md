---
phase: 04-edit-parameters
status: passed
owner: user
passed: 8
pending: 0
---

# Final manual editing acceptance

Deferred by explicit user instruction on 2026-11-10. No browser automation or
visual pass is claimed. Use the combined guide `docs/development/final-uat.md`.

1. An authorized matching Device shows Edit Parameters. A view-only user, no-match
   Device, and Device with no editable fields do not show the action.
2. One edit page shows each repeated field once, in first-occurrence order. Native
   Hidden/noneditable fields and inaccessible saved references cannot be edited.
3. Correct representative native types using their native widgets, including
   object/multiobject, date/time, JSON, choices, false and zero. Save; all repeated
   Parameters rows and native Device editing/API show identical saved values.
4. Submit required/range/regex/choice/JSON errors. Errors are readable, entered
   values remain available for correction, and no native value is partially saved.
5. Cancel returns to Parameters without saving. Successful Save returns there.
6. Change profile membership/field definition in another tab, then submit the old
   edit form. Reload guidance appears without changing stored values. Repeat with
   a native Device modification after form load; native stale-form error appears.
7. Verify unauthorized and constrained users cannot use direct edit URLs or POSTs.
   Reference selectors expose only allowed objects; inaccessible existing
   reference sets remain intact while other fields are saved.
8. At desktop and narrow widths, verify label/help/input/error readability, native
   dynamic selector interactions, keyboard focus and Save/Cancel reachability.

Record actual browser/version, viewport, Device/profile IDs, steps, observed
result and redacted evidence for each case. All eight cases remain pending.

## Final user acceptance — 2026-11-11

User reported overall manual UAT passed on 2026-11-11: “ok, pass UAT”. This is user-reported acceptance of the final checklist; no agent-run browser observations, screenshots, viewport details or individual execution logs were supplied.
All cases are recorded passed on that overall sign-off. Earlier pending/deferral descriptions are retained as historical context. Phase 3 case 15 uses the documented Phase 4 superseding action-permission expectation.
