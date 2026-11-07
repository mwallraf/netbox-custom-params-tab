---
status: testing
phase: 02-profile-administration-and-matching
source: [02-VERIFICATION.md]
started: 2026-11-06T21:12:23.019999+00:00
updated: 2026-11-06T21:12:23.019999+00:00
---

## Current Test

number: 1
name: Drag three selected fields, save, and reopen Edit.
expected: |
  Dragging the last field before the first persists the exact order.
awaiting: user response

## Setup

Use the dedicated disposable sandbox at http://127.0.0.1:18047 and an authorized administrator. For reorder checks, use three native fields applicable to Device. Follow docs/development/profiles.md. Browser control was unavailable during execution; no result below is inferred from native tests.

## Tests

### 1. Drag three selected fields, save, and reopen Edit.
expected: Dragging the last field before the first persists the exact order.
result: [pending]
reason: No executed browser drag/drop evidence; WINDOWS 1.

### 2. Use Tab and Enter/Space on Move up/down, save, and reopen.
expected: The moved field retains usable focus, position is announced, boundary actions are disabled correctly, and order persists.
result: [pending]
reason: Native POST tests do not exercise keyboard focus or assistive technology; WINDOWS 1.

### 3. Change pending manual membership/order, switch to All, save/reopen, then switch back to Selected.
expected: Pending additions/removals/order survive; All disables manual controls and retains native effective ordering.
result: [pending]
reason: Server regression passes; actual selector/hidden-payload synchronization remains unobserved; WINDOWS 1.

### 4. Submit empty title with selected fields/order/rules; correct and save. Repeat after pending manual changes followed by switching to All.
expected: Actionable title error, unchanged persisted aggregate, retained pending choices/order/rules, and successful correction.
result: [pending]
reason: Server bound-form recovery is tested, but browser reconstruction and input usability are unverified.

### 5. Search unused Device-compatible and unrestricted tags in the native profile widget; select/save/reopen.
expected: Both tags are discoverable and retained without needing prior Device assignment.
result: [pending]
reason: Native API/queryset proof does not execute the live search widget; WINDOWS 2.

### 6. Clear all three rule selectors, add a rule, then clear it again; save.
expected: Applies to all Devices immediately appears/hides/returns, scope changes are politely announced, and no extra unrestricted-save confirmation appears.
result: [pending]
reason: Source and server rendering are present; actual change events and announcements are unobserved; WINDOWS 2.

### 7. Disable JavaScript, then separately block the ordering asset; restore and reload.
expected: Actionable noscript/loading guidance remains visible on failure and clears after successful initialization.
result: [pending]
reason: The recovery copy exists, but the actual degraded browser paths have not been observed.

### 8. Review list, detail and edit pages at desktop 1440x900, tablet 768x1024 and mobile 375x812 with long field/filter labels.
expected: Readable layout and errors, usable controls and visible focus, no obstructive overflow, and acceptable native-theme contrast.
result: [pending]
reason: No screenshots or rendered visual assessment exist; the UI review left four visual pillars unassessed.

## Summary

total: 8
passed: 0
issues: 0
pending: 8
skipped: 0
blocked: 0

## Gaps

None reported by a human yet. Eight browser acceptance checks remain pending; WINDOWS entries 1/2 stay open.
