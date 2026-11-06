# Onboarding synthesis

## Sources and precedence

Three documents approved by the user for ingestion on 2026-11-06:
1. `docs/REQUIREMENTS.md` — PRD, precedence 0, authoritative.
2. May design — SPEC, precedence 10, historical context only.
3. May implementation plan — DOC, precedence 20, historical context only.

Explicit user authority overrides default SPEC-over-PRD precedence here.
See `manifest.yml` and `classifications/` for the ingest inputs.

## Project

Name: NetBox Custom Field Profiles.
Core value: Each Device shows and edits only the native custom fields relevant
through its matching profiles, without cluttering its main detail page.
Success: The CMTS/CPE/shared-profile examples work end to end, with native storage,
validation, permissions, and script interoperability preserved.
Runtime: NetBox plugin; exact supported version remains Phase 1 research.

## Consolidated context

- `decisions.md`: agreed constraints.
- `requirements.md`: 26 proposed traceable requirements across five phases.
- `constraints.md`: engineering boundaries and open questions.
- `context.md`: existing implementation and onboarding status.
- `../codebase/`: source-backed architecture and quality map.
- `../INGEST-CONFLICTS.md`: supersession and unresolved-conflict report.

## Approved roadmap

1. Reproducible baseline — source recovery, version, environment, renamed app,
   migrations and passing baseline checks.
2. Profile administration and matching — profile model/UI, field modes, and fixed
   filters; prove AND/OR behavior independently of rendering.
3. Parameters tab — matching sections and native field display with permission parity.
4. Edit Parameters — native validation/permissions, deduplicated inputs, safe saves.
5. Release verification — CMTS/CPE acceptance, scripts, installation and docs.

No executable phase plans or implementation are created by this synthesis.
The user approved scaffold creation on 2026-11-06. PROJECT.md, REQUIREMENTS.md,
ROADMAP.md, and STATE.md now exist. No phase execution has started.
