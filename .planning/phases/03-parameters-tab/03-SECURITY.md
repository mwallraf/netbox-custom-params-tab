---
phase: "03"
slug: "parameters-tab"
status: verified
threats_open: 0
asvs_level: 1
created: "2026-11-07"
---

# Phase 03 — Security

Independent gsd-security-auditor verified the authored register at ASVS L1,
blocking threshold high. Seventeen unique threats are closed; repeated SC rows
denote one canonical no-install control. No accepted risks or unregistered flags.

## Trust Boundaries

Native constrained Device lookup precedes profile matching. Related-object native
querysets restrict references before rendering. Stored content crosses Django/native
escaping, Markdown sanitization and URL-scheme checks. Tests use isolated PostgreSQL;
browser evidence and documentation must not disclose credentials or invent outcomes.

## Threat Register

All dispositions are mitigate. Paths below are relative to the plugin package.

| ID | Severity | Mitigation and evidence | Status |
|----|----------|-------------------------|--------|
| T-03-01 | high | views.py constrained Device ObjectView; test_parameter_permissions denied resolver guards | closed |
| T-03-02 | high | Device tab permission; Device-only versus profile-only grant matrix | closed |
| T-03-03 | high | Constrained lookup before unsupported-method rejection; POST 405/403/404 and snapshots | closed |
| T-03-04 | high | presentation.py restricted reference queryset; prepared instances only in value template | closed |
| T-03-05 | high | Read-only resolution; full native definition/applicability/value snapshots | closed |
| T-03-06 | medium | Request-local row cache; repeated native-save freshness regression | closed |
| T-03-07 | high | Autoescaped headings/labels/help; hostile metadata and type-render tests | closed |
| T-03-08 | high | Restricted scalar/collection resolution; forbidden unrestricted-deserialization guard | closed |
| T-03-09 | high | Alternating superuser/constrained viewer requests detect cross-request reference leakage | closed |
| T-03-10 | high | Native Markdown/JSON formatter; response DOM checks reject executable content | closed |
| T-03-11 | high | Native configured URL decision; escaped full href/text; scheme matrix | closed |
| T-03-12 | low | Scoped wrapping/table width/local pre overflow; long-payload response tests | closed |
| T-03-13 | high | Complete native and plugin-aggregate snapshots per response class | closed |
| T-03-14 | high | Native runner rejects live/non-PostgreSQL database; live hashes unchanged; no browser fixtures created | closed |
| T-03-15 | medium | Existing runner error/output redaction; auditor in-memory scan of 18 evidence files found zero local-secret matches | closed |
| T-03-16 | medium | Timestamped unavailable-browser record; zero visual passes, fifteen pending UAT cases | closed |
| T-03-SC | high | Native/Python facilities only; no dependency/config/runner installation changes | closed |

Detailed test evidence is in tests/test_parameter_permissions.py,
tests/test_parameter_rendering.py and tests/test_parameters.py, with executed
commands/counts in 03-04-SUMMARY.md and 03-VALIDATION.md. The auditor inspected
actual code/assertions without rerunning Docker or modifying implementation.

## Verification Limits

Security controls are present at L1. This is not browser acceptance. In particular,
T-03-12's CSS and response checks do not establish actual narrow-screen readability.
UAT-01 through UAT-15 remain pending because the browser host was unavailable.

## Accepted Risks Log

No accepted risks.

## Security Audit Trail

| Date | Total | Closed | Blocking open | Auditor |
|------|-------|--------|---------------|---------|
| 2026-11-07 | 17 | 17 | 0 | gsd-security-auditor |

**Approval:** verified 2026-11-07 at L1; manual UI acceptance pending.
