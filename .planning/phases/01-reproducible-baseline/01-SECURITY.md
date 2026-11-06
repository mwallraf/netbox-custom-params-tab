---
phase: "01"
slug: reproducible-baseline
status: verified
threats_open: 0
asvs_level: 1
register_authored_at_plan_time: true
created: "2026-11-06"
---

# Phase 1 Security

L1 mitigation-presence audit of the plan-authored register. This is not ASVS certification.

| Threat | Severity | Mitigation evidence | Status |
| --- | --- | --- | --- |
| T-01-01 | high | source_snapshot.py hashes, preserved recovery directory, feature ancestry, verified canonical commit | closed |
| T-01-02 | medium | explicit source inventory excludes .env/generated data; original retained locally ignored | closed |
| T-01-03 | high | sandbox.py atomic 0600 stable env, safe parser, redaction; concurrent/invalid-file tests pass; build-context secret exclusions | closed |
| T-01-04 | high | fixed project/file/env argv, validated nonexternal network/volumes, localhost-only web; no shared names | closed |
| T-01-05 | high | direct-interpreter native schema generation before bootstrap, native migration/app/version checks gate readiness | closed |
| T-01-06 | high | smoke keeps credentials in memory, redacted bounded failures; report redaction tests | closed |
| T-01-07 | high | live positive/negative session/token auth, native transactional owned seed, true subprocess exit report | closed |
| T-01-08 | high | reset validates project resource declarations and actual volume ownership labels; real lifecycle unrelated IDs unchanged | closed |
| T-01-09 | medium | tracked documentation has evidence/versions only; .env/local reports ignored | closed |
| T-01-SC | high | official exact NetBox image verified; only local plugin installed; stdlib baseline, no optional third-party test install | closed |

Shared T-01-SC appears in each plan and is consolidated as one supply-chain boundary.
No accepted risks were substituted for missing controls. No blocking threats remain.

## Security Audit

2026-11-06: 10 register threats verified closed, 0 open. Tests and live checks in
Plan 02–04 summaries substantiate the named controls. No new feature authorization
model is implied by this baseline audit.
