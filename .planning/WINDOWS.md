---
schema_version: 1
open_count: 0
waived_count: 0
fixed_count: 2
total_count: 2
last_updated: 2026-11-07T06:16:09.179Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 02 | unrun-verify | netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js |  | Plan 02-03 browser drag, keyboard and mode-round-trip verification pending: browser access host unavailable; native Safari target timed out. Recheck in Plan 02-06. | fixed |  | 2026-11-06T19:06:48.877Z | 2026-11-07T06:16:09.112Z |
| 2 | 02 | unrun-verify | netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html |  | Live unused-tag widget search/save/reload and dynamic unrestricted-notice interaction unverified: browser access host unavailable; Plan 02-06 must verify. | fixed |  | 2026-11-06T19:16:21.944Z | 2026-11-07T06:16:09.179Z |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js",
    "line": null,
    "description": "Plan 02-03 browser drag, keyboard and mode-round-trip verification pending: browser access host unavailable; native Safari target timed out. Recheck in Plan 02-06.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-11-06T19:06:48.877Z",
    "resolved_at": "2026-11-07T06:16:09.112Z",
    "milestone": null
  },
  {
    "id": 2,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "netbox_custom_field_profiles/templates/netbox_custom_field_profiles/customfieldprofile_edit.html",
    "line": null,
    "description": "Live unused-tag widget search/save/reload and dynamic unrestricted-notice interaction unverified: browser access host unavailable; Plan 02-06 must verify.",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-11-06T19:16:21.944Z",
    "resolved_at": "2026-11-07T06:16:09.179Z",
    "milestone": null
  }
]
````
