---
phase: 03-parameters-tab
status: pending
recorded_at: 2026-11-07T14:47:24Z
source: 03-04-T2
browser_cases_passed: 0
browser_cases_pending: 15
---

# Phase 3 Device Parameters browser acceptance

Browser acceptance is **pending**. During 03-04 execution, the actual
`mcp__cua_repl` call `await cua.getState();` returned native app inventory but
`browsers: []` and `Browsers: Error: The browser access host is unavailable`.
The required CUA completion summary was then recorded. No browser tab, viewport,
page, keyboard action or screenshot was available to observe. No alternate OS or
browser automation was attempted. The timestamp above records this evidence log.

This availability check is the only observed browser result. Each row below has
the same actual result: **not observed — browser access host unavailable**. A dash
means no actual viewport/screenshot exists. Proposed fixtures and viewport sizes
are preparation instructions, not objects or browser states claimed to exist.
Server response tests are listed separately and do not constitute visual proof.

## Fixture and restoration boundary

Target the dedicated sandbox at `http://127.0.0.1:18047`. Existing objects may be
used only when adequate and safe. Otherwise create a uniquely named disposable
`phase03-uat-<timestamp>` fixture group: CMTS/CPE Devices, appropriate hardware/role/
tag rules, a shared profile, 20–30 native fields, duplicate titles/memberships,
and Device-only/constrained viewer accounts. Capture complete native definitions,
applicability, choice data, Device values and plugin aggregate tables before any
fixture operation; restore and compare exact baseline snapshots afterward.
Never reset live data or print generated credentials. Do not restart services
during tests. If safe restoration cannot be established, keep affected cases
pending. No extra fixture was created in this attempt; no restoration operation
was necessary and live state was untouched by the browser attempt.

## Manual case matrix

For every case: expected desktop viewport 1440×900 and narrow viewport 390×844
unless specified; actual viewport **—**; actual timestamp/evidence **—**;
status **pending**; reason **browser access host unavailable**. Record browser,
actual viewport, fixture IDs, actions, observed result, UTC timestamp and redacted
screenshot/browser reference when these cases can be executed.

| Case | Decision | Proposed fixture/action | Expected result |
|------|----------|-------------------------|-----------------|
| UAT-01 | D-01 | Matching CMTS and nonmatching CPE; open native detail pages | Parameters appears only when an enabled profile matches, including an empty matching profile |
| UAT-02 | D-02 | Authorized Device viewer; visit nonmatching Device's direct Parameters URL | Native Device shell and exact message: No parameter profiles apply to this device. |
| UAT-03 | D-03 | Matching profile resolving zero active fields; open Parameters | Section remains visible with exact message: No fields are available in this profile. |
| UAT-04 | D-04 | Device-only viewer without profile/field-definition administration grants | Tab/direct page usable; profile administration actions/links absent from Parameters |
| UAT-05 | D-05 | Matching unset text/null/missing/multivalue fields | Every relevant row present with muted Not set; excluded fields absent |
| UAT-06 | D-06 | Boolean false, numeric zero, JSON {}, [], false, 0 and empty string | False and zero display as values; JSON remains readable JSON, not Not set |
| UAT-07 | D-07 | Hidden and unset If Set fields; compare native settings before/after | Relevant rows present in Parameters; native main-page visibility/settings unchanged |
| UAT-08 | D-08 | CMTS section of 20–30 fields plus CPE/shared sections; inspect both widths | Expanded full-width vertical cards; readable label/value wrapping, no unwanted page overflow |
| UAT-09 | D-09 | Duplicate-title sections, Selected ordering, All ordering/new field | Duplicate headings retained; deterministic section/field order, dynamic field appears next request |
| UAT-10 | D-10 | Labeled/unlabeled fields with escaped help; use pointer and keyboard Tab | Exact internal-name fallback, safe secondary native help, usable focus/help; no filter/mode metadata |
| UAT-11 | D-11 | Shared repeated field; perform legitimate native value save, reload ordinary tab | Every occurrence shows identical new native value with no profile save/import/synchronization |
| UAT-12 | D-12 | Native text, longtext, numeric, boolean, date/time, URL, JSON, select/multiselect and object/multiobject values | Native type formatting, friendly choice labels/colors and permitted object links; consistent duplicates |
| UAT-13 | D-13 | Complete long URL, multiline Markdown, long word and nested wide JSON; inspect both widths and scroll JSON | Full values remain readable, line breaks retained, URL wraps, horizontal overflow stays local to JSON; escaped metadata/value text never executes |
| UAT-14 | D-14 | Device-only/constrained/denied viewers; native navigation and direct URLs; restricted scalar/mixed/all-denied references | Native Device denial; active Parameters tab for allowed viewer; no denied IDs/labels/links/counts, neutral Unavailable where needed |
| UAT-15 | D-15 | Allowed/no-match/empty-section tab; inspect actions and keyboard focus | Read-only page with no Edit Parameters action or inactive button; native storage unchanged |

## Automated evidence (separate from visual acceptance)

- `test_parameters`: native registration/navigation, active-tab markup, matching,
  deterministic order, dynamic fields, empty states and response freshness.
- `test_parameter_rendering`: all 13 native types, unset/false-like values,
  visibility, native help/escaping, full URL text, multiline/JSON markup and XSS.
- `test_parameter_permissions`: native/constrained Device and related-object
  authority, unsupported POST, full native/profile snapshots and external-save
  freshness in repeated rows. Snapshot coverage includes choice definitions,
  field applicability, all rule through tables and retained excluded values.

Measured command results are in `03-VALIDATION.md` and `03-04-SUMMARY.md`. No
manual case is passed by those commands. No phase visual acceptance or Nyquist
sign-off is granted by this record.
