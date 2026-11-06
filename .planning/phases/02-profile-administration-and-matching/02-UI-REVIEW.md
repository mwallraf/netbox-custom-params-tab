# Phase 2 — UI Review

**Audited:** 2026-11-06
**Baseline:** Phase 02 CONTEXT D-01–D-16 and abstract six-pillar standards, retaining native NetBox design. No UI-SPEC.md exists.
**Screenshots:** Not captured. Bounded HTTP probes of localhost ports 3000, 5173, 8080 and the documented sandbox port 18047 returned 000 from this restricted session. This does not establish that the sandbox is down elsewhere. A CUA inventory retry returned `Browsers: Error: The browser access host is unavailable`, with no browser targets.
**Interaction captures:** off (interaction_capture: false); no browser interaction state captured.
**Confidence:** Code-derived findings only. Desktop 1440×900, mobile 375×812 and tablet 768×1024 rendering, contrast, focus visibility, drag/drop, searchable widgets and actual screen-reader announcements remain unassessed. WINDOWS entries 1/2 remain pending.

The screenshot-storage gate was executed before attempting browser discovery: `.planning/ui-reviews/.gitignore` contains all eight required patterns. No screenshot or interaction artifact was produced. Computer interaction used CUA only; no alternative CLI browser automation was attempted.

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4, code only | Mode help promises remembered selection without disclosing that All-mode saves discard unsaved manual changes. |
| 2. Visuals | N/A | Native cards/headings and labelled controls exist; rendered hierarchy and responsive layout unassessed. |
| 3. Color | N/A | Native semantic classes only in active profile UI; actual contrast and distribution unassessed. |
| 4. Typography | N/A | Native headings and button sizing; rendered sizes/weights unassessed. |
| 5. Spacing | N/A | Native spacing utilities; long-row/mobile fit unassessed. |
| 6. Experience Design | 2/4, code only | Unsaved manual state is not remembered through All-mode saves; changing scope lacks a live announcement. |

**Overall: Not scoreable out of 24.** Assessed subtotal: **5/8** for copy and code-derived experience. Four visual pillars lack the evidence needed for a numeric assessment; they are neither passed nor failed.

## Top 3 Priority Fixes

1. **Preserve pending manual selection/order when saving All mode** — changing fields or order and then selecting All silently drops those manual edits — carry a separately validated remembered-state payload and persist it atomically in All mode while keeping it inactive. Preserve existing remembered state when the payload is absent. Cover edit → reorder/change selection → All → save/reopen → Selected, including invalid-form recovery.
2. **Announce changes to applicability scope** — clearing the last criterion reveals “Applies to all Devices” without an explicit assistive-technology announcement — update an always-present polite status region with unrestricted/restricted scope after selector changes; retain the visible notice.
3. **Explain an unavailable ordering editor** — Selected-mode saves depend on JS producing an exact order, but there is no fallback message if the asset is unavailable — provide a visible loading/failure or noscript explanation and recovery action, or a server-rendered ordered-input fallback; avoid presenting a usable-looking Selected editor that can only fail validation.

## Detailed Findings

### Pillar 1: Copywriting (3/4, code only)

- **WARNING C1:** `templates/netbox_custom_field_profiles/customfieldprofile_edit.html:10` says “your manual selection is remembered.” `docs/development/profiles.md:34` describes switching back as restoring the selection/order. This is accurate for previously persisted memberships, but not edits made before an All-mode save (E1). Fix behavior first; make mode help explicitly describe the current remembered state. The current copy creates an expectation the implementation does not fully meet.
- Specific actionable validation exists: `forms.py:76` asks an administrator to review inaccessible references; `forms.py:85` requires an applicable selection. AND/OR help and the exact agreed “Applies to all Devices” text are present (`customfieldprofile_edit.html:5–6`, `matching.py:29–37`). Native generic templates own Save/Cancel/delete copy; their presence is not itself a defect.
- Minor recommendation C2: `customfieldprofile.html:17` labels remembered membership “Configured fields” even in All mode; the explanation follows at line 18. Label this “Remembered selected fields” in All mode so the list cannot be mistaken for the current dynamically effective fields.

### Pillar 2: Visuals (unassessed)

- Code evidence: detail and edit pages inherit native generic bases; cards and h2/h3 headings provide structural grouping (`customfieldprofile.html:1–6`, `customfieldprofile_edit.html:1–8`). Every generated icon-only drag handle has a field-specific aria-label; Move up/down have visible text and field-specific names (`static/netbox_custom_field_profiles/profile_fields.js:35–54`).
- No screenshot proves hierarchy, icon rendering, focus-ring visibility or layout fit. No visual defect or numeric score is inferred solely from component existence. Inspect all three target viewports and long field/filter labels when browser access returns.

### Pillar 3: Color (unassessed)

- Active custom templates/JS contain two semantic message colors: one `alert-info` notice (`customfieldprofile_edit.html:6`) and one `text-danger` validation rendering (`:11`); reorder buttons use `btn-outline-secondary` (`profile_fields.js:36,51`). No hardcoded hex/RGB values or plugin primary/accent classes occur in these files.
- Native NetBox supplies actual colors and themes. No 60/30/10 branding redesign is warranted by the contract. Contrast, disabled-button appearance, light/dark themes and rendered color distribution remain unassessed.

### Pillar 4: Typography (unassessed)

- No custom font-size/weight declarations or Tailwind text-size/weight classes occur in active profile templates/JS. Source uses h2 and h3, native card headers, and `btn-sm` for movement actions (`customfieldprofile.html:3,6,17`; `customfieldprofile_edit.html:8`; `profile_fields.js:51`).
- These are semantic/native choices, not measured typography evidence. Actual size/weight distribution, truncation and legibility remain unassessed; arbitrary two-weight/four-size thresholds are not imposed on inherited NetBox styling.

### Pillar 5: Spacing (unassessed)

- Explicit custom spacing consists of one `mt-3` card margin, one generated `gap-2` row class and one generated `me-auto` label class (`customfieldprofile_edit.html:7`; `profile_fields.js:33,48`). There are no arbitrary pixel/rem spacing declarations in the active profile UI.
- Responsive verification target: each generated row contains a drag button, label and two text buttons in a single `d-flex` row without an explicit wrap policy (`profile_fields.js:33–55`). Verify long labels at 375px before deciding whether a wrapping/stacking rule is needed. Overflow has not been observed and is not asserted as a defect.

### Pillar 6: Experience Design (2/4, code only)

- **WARNING E1 — pending manual state lost across an All save:** `profile_fields.js:59` disables selected_fields in All mode, so browsers omit that input. The hidden order remains submitted, but `forms.py:79–80` returns before reading/validating it for All mode; `_save_m2m` writes membership only for Selected mode (`:111–118`). Thus, for an existing saved `[A,B]`, reorder to `[B,A]`, select All and save: membership remains `[A,B]`; returning to Selected restores the older order. Selection additions/removals are similarly lost. This diverges from D-07's remembered manual-state expectation. Existing `tests/test_selection.py:35–53,94–107` checks already-saved membership round trips, not this pending-edit sequence. A failed All-mode form also lacks the disabled selected_fields POST values for bound-form redisplay. Fix with an explicit authoritative remembered-state payload and test these sequences; do not trust arbitrary hidden IDs.
- **WARNING E2 — dynamic scope is not announced:** the unrestricted notice is a normal paragraph with `hidden` toggled by change handlers (`customfieldprofile_edit.html:6,24–25`). It has no status/live-region semantics or association with the criterion controls. Sighted users receive a changing notice; there is no explicit announcement mechanism for assistive technology when clearing the final restriction broadens scope. Add a persistent status region whose text changes; verify actual announcements in a browser.
- **WARNING E3 — no recovery for unavailable ordering JS:** `forms.py:90–97` requires an exact JSON order for Selected mode. The template renders an empty ordered list and no noscript/loading/error message (`customfieldprofile_edit.html:10–16`); only `profile_fields.js:14,25–64` builds the order. With that asset unavailable, selecting fields and saving cannot satisfy validation. This is a concrete degraded-path gap, not a claim that normal asset delivery is broken. Provide an actionable unavailable-editor state or fallback.
- Positive code evidence: reorder controls restore focus after rebuilding rows and announce position (`profile_fields.js:19–23`); boundary actions and All-mode controls disable (`:53,56,59`). Server form validation and atomic persistence are present (`forms.py:67–99,108–124`). Delete delegates to native ObjectDeleteView and its confirmation template (`views.py:25–28`). Optional rule fields use native dynamic widgets (`forms.py:16–26`); unused-compatible-tag query parameters are supplied (`:47–49`). These facts do not prove browser drag, keyboard focus, mode switching or live search passed.
- Static profile pages do not introduce a separate asynchronous data-loading flow, so absence of a plugin spinner is not a defect. Native list-empty, form errors and deletion behavior are inherited and still need rendered verification.

## Registry audit

Not applicable: no components.json and no third-party registry contract. No shadcn command or new dependency was introduced.

## Files Audited

- AGENTS.md; docs/REQUIREMENTS.md; README.md; .planning/STATE.md; .planning/ROADMAP.md; .planning/REQUIREMENTS.md; .planning/config.json.
- Phase 02 CONTEXT, execution PLAN/SUMMARY artifacts 02-01 through 02-08, and docs/development/profiles.md.
- netbox_custom_field_profiles/forms.py; views.py; tables.py; models.py; matching.py.
- netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile.html and customfieldprofile_edit.html.
- netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js.
- netbox_custom_field_profiles/tests/test_selection.py (coverage inspection; not rerun for this documentation-only audit).
- GSD ui-review workflow, ui-brand reference and agent-skills bootstrap. Project skill directories are absent; the configured auditor-skills query returned no skill entries.

**Recommendation count:** 3 priority warnings; 1 minor copy recommendation. No demonstrated task-blocking defect is classified BLOCKER. Browser acceptance and all four visual pillars remain open; this review is not a ship approval.

## Finding resolutions after audit

E1/C1, E2, E3 and C2 were corrected in commit 5b99080; see 02-UI-FIX.md for exact behavior/test evidence. The later independent standard code review covered the UI fix and found no remaining UI-code defect. Follow-up lifecycle findings were separately fixed and independently closed in 02-REVIEW.md. Original audit observations above are historical; no active code finding is being deferred. Four visual pillars and actual drag/keyboard/widget/assistive-technology acceptance remain unassessed because browser access is unavailable; code fixes do not change that evidence limit.
