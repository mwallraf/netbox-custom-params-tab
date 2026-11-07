# Phase 03 — UI Review

**Resolution update:** The confirmed help-focus defect was fixed in `575ad7b`.
The trigger is now a semantic button with an escaped accessible description and
native hover/focus activation. All eight rendering tests and the full 89-test
native suite pass after the fix, with live data unchanged. The assessments below
preserve the original code-only audit; actual tooltip interaction, touch behavior
and visual scores remain pending UAT, not silently upgraded to a browser pass.

**Audited:** 2026-11-07
**Baseline:** `03-CONTEXT.md` D-01–D-15; native NetBox 4.7.4 styling. No UI-SPEC.md exists.
**Screenshots:** not captured — browser access host unavailable; parent audit discovery returned `browsers: []`. No alternate browser automation attempted.
**Interaction captures:** off (workflow.ui_interaction_capture is absent); no interaction state observed.
**Scope:** code-only review of Phase 03. No tests rerun, fixtures changed, production edits or commits made.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 4/4 (code) | Both exact agreed empty messages and distinct Not set/Unavailable states are present. |
| 2. Visuals | Unverified | Native cards and table hierarchy exist; actual desktop/narrow rendering was inaccessible. |
| 3. Color | Unverified | Native semantic classes only; rendered contrast and accent distribution cannot be established from class counts. |
| 4. Typography | Unverified | Native typography inherited; computed sizing and narrow-screen readability were not observed. |
| 5. Spacing | Unverified | Native card/table spacing inherited; dense 20–30-field layout and overflow need browser inspection. |
| 6. Experience Design | 2/4 (code) | Help icons cannot receive keyboard focus; other read-only states have implementation and recorded response-test coverage. |

**Overall: not established /24.** Two code-assessable pillars score 6/8. Assigning numeric visual scores without observing the inherited runtime styles would imply evidence this audit does not have. This is an incomplete visual acceptance gate, not a rendered UI pass or a claim that the four unverified pillars have defects. No task-blocking implementation defect was established by this review.

---

## Top 3 Priority Fixes

1. **WARNING — Make field descriptions reachable by keyboard and touch.** `device_parameters.html:43–48` puts the only help text on a nonfocusable `<i>` with a title tooltip. Use a semantic, focusable help control with an accessible name and a description relationship; provide a reliable touch activation or visible secondary help. Verify focus, Escape/dismissal and accessible description in the native shell.
2. **WARNING — Complete the pending responsive visual gate.** Run UAT-08 and UAT-13 at the recorded 1440×900 and 390×844 sizes using 20–30 fields, long labels/URLs/Markdown and wide JSON. Confirm full-width cards, readable columns and local JSON overflow. Change the 30%/38% column rules only if the observed result warrants it; this audit has not demonstrated clipping.
3. **WARNING — Complete native-shell accessibility and theme evidence.** Run UAT-04, UAT-10, UAT-12 and UAT-14 with Device-only/constrained viewers. Inspect focus/help, muted text and informational-icon contrast, native type formatting and permitted links in supported themes. Record actual results and screenshots before assigning the remaining pillar scores. No color or typography rework is justified solely by this evidence gap.

Items 2–3 are verification work, not confirmed product defects. They must not be converted into invented failing screenshots or speculative production fixes.

---

## Detailed Findings

### Pillar 1: Copywriting (4/4, code)

- **PASS:** Exact D-02 copy appears at `templates/netbox_custom_field_profiles/device_parameters.html:63`: “No parameter profiles apply to this device.” Exact D-03 copy appears at line 59: “No fields are available in this profile.” These distinguish relevance from a matching section with no available fields.
- **PASS:** `templates/netbox_custom_field_profiles/parameter_value.html:1–4` distinguishes neutral “Unavailable” references from “Not set” values. `presentation.py:23–31` preserves false, zero and meaningful JSON. Field labels fall back to native names at `device_parameters.html:41`.
- No generic Submit/OK/Save action appears in the Phase 03 templates. An Edit Parameters CTA is intentionally absent under D-15; it is not a missing-state defect.

### Pillar 2: Visuals (unverified)

- **Code evidence:** `device_parameters.html:1,33–57` extends the native Device shell and renders one expanded card with an h2 and label/value table per section. Labels use row headers with `scope="row"`; profile titles remain escaped. No custom decorative imagery or icon-only action buttons were added.
- **WARNING — confirmed semantic gap:** Help icons at lines 43–48 have neither a focusable element nor an accessible control name. Their `title` does not make them keyboard reachable. This is the same defect scored under Experience Design, not a second independent defect.
- **Pending evidence:** Native visual hierarchy, active navigation and actual line wrapping require UAT-08/10/12. An h2/card class is structural evidence, not proof of visual correctness.

### Pillar 3: Color (unverified)

- **Code distribution:** One explicit `text-primary` occurrence, on the per-field help icon (`device_parameters.html:44`); two `text-muted` occurrences for section/page empty states (lines 59,63); two `text-muted` occurrences for unavailable/unset values (`parameter_value.html:2,4`). These are source occurrences, not rendered element counts: a 30-field section can produce 30 primary-colored help icons.
- No literal hex/RGB colors occur in either Phase 03 template. Native field renderers can introduce type/choice colors, so the five explicit class occurrences do not describe the entire rendered palette.
- **WARNING — verification gap:** Neither muted-state contrast nor repeated help-icon emphasis in a dense section has visual evidence. No arbitrary 60/30/10 redesign is imposed on the agreed native NetBox interface.

### Pillar 4: Typography (unverified)

- **Code distribution:** Zero explicit font-size or font-weight declarations in Phase 03 templates; h2, table headers, native value output and the inherited Device shell determine typography. There is no evidence of a competing plugin type scale.
- `device_parameters.html:18–24` preserves multiline Markdown whitespace and preformatted JSON; `parameter_value.html:13` retains full URL text. These preserve content but do not establish the computed line height or actual readability.
- **WARNING — verification gap:** Inspect long-label wrapping, headings with duplicate titles and multiline text at desktop/narrow widths. No browser measurement exists to justify either a typography failure or a 4/4 score.

### Pillar 5: Spacing (unverified)

- **Code distribution:** Zero custom padding, margin or gap declarations and no Tailwind spacing classes; native `card`, `card-header`, `card-body`, `table` and `attr-table` supply spacing (`device_parameters.html:34–37,59,63`). Native token inheritance is appropriate to D-08, not an arbitrary-spacing defect.
- Local layout rules use a fixed full-width table with 30% label columns and 38% below 575.98px (`device_parameters.html:11–29`). Values wrap anywhere and preformatted content has local horizontal overflow. Percentage widths and the breakpoint are layout decisions, not off-scale padding values.
- **WARNING — verification gap:** UAT-08/13 must establish whether nested native Markdown tables or other rich content interact poorly with the broad descendant table/header selectors. This is a risk to inspect, not an observed overflow defect. Card separation and narrow column usability remain unobserved.

### Pillar 6: Experience Design (2/4, code)

- **WARNING — concrete defect:** `device_parameters.html:43–48` makes native field descriptions available only through a tooltip on a plain `<i>`. Keyboard navigation cannot focus that trigger; touch support and assistive description delivery are not established. D-10/UAT-10 explicitly require usable secondary help. Replace the trigger as described in priority fix 1, then verify actual native tooltip behavior.
- **Positive code evidence:** The native Device ObjectView and matching visibility predicate are at `views.py:11–23`; unauthorized objects remain under native restrictions. `views.py:25–29` performs constrained object lookup before unsupported-method handling. `presentation.py:34–43` restricts related objects before formatting and suppresses hidden-reference counts/IDs. `presentation.py:46–65` reads native values per request and reuses prepared rows within that request.
- Both empty states are explicit; missing and denied values have distinct neutral text. `parameter_value.html:11–18` uses native URL policy and delegates ordinary types to native rendering. There is no client-side fetch or mutation in these templates, so adding a spinner, save-disabled state or destructive confirmation is not warranted for this read-only phase.
- Existing response tests cover registration/order/empty states (`test_parameters.py`), 13 types and escaping (`test_parameter_rendering.py`), constrained access and preservation (`test_parameter_permissions.py`). `03-04-SUMMARY.md` records 89 native tests passing. These are historical recorded results, not a fresh execution by this audit. HTML assertions do not prove focus, tooltip usability or local scrolling. All 15 cases in `03-UAT.md` remain pending.

---

## Files Audited

Registry audit skipped: no `components.json` or third-party registry contract exists. No packages installed.

- `AGENTS.md`, `docs/REQUIREMENTS.md`, `README.md`, `CLAUDE.md`
- `.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/config.json`
- `.planning/phases/03-parameters-tab/03-CONTEXT.md`
- `.planning/phases/03-parameters-tab/03-01-PLAN.md` through `03-04-PLAN.md`
- `.planning/phases/03-parameters-tab/03-01-SUMMARY.md` through `03-04-SUMMARY.md`
- `.planning/phases/03-parameters-tab/03-UAT.md`
- `netbox_custom_field_profiles/views.py`
- `netbox_custom_field_profiles/presentation.py`
- `netbox_custom_field_profiles/templatetags/parameter_tags.py`
- `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/device_parameters.html`
- `netbox_custom_field_profiles/templates/netbox_custom_field_profiles/parameter_value.html`
- `netbox_custom_field_profiles/tests/test_parameters.py`
- `netbox_custom_field_profiles/tests/test_parameter_rendering.py`
- `netbox_custom_field_profiles/tests/test_parameter_permissions.py`

**Recommendation count:** 1 confirmed priority defect; 2 priority verification tasks; 0 additional independent minor defects. Screenshot storage was not changed because no captures were attempted and this audit owns only this report. The screenshot gitignore gate remains mandatory before a future capture.
