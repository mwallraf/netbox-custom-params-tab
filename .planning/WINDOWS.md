---
schema_version: 1
open_count: 1
waived_count: 0
fixed_count: 0
total_count: 1
last_updated: 2026-11-06T19:06:48.877Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | 02 | unrun-verify | netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js |  | Plan 02-03 browser drag, keyboard and mode-round-trip verification pending: browser access host unavailable; native Safari target timed out. Recheck in Plan 02-06. | open |  | 2026-11-06T19:06:48.877Z |  |

````json
[
  {
    "id": 1,
    "kind": "unrun-verify",
    "phase": "02",
    "file": "netbox_custom_field_profiles/static/netbox_custom_field_profiles/profile_fields.js",
    "line": null,
    "description": "Plan 02-03 browser drag, keyboard and mode-round-trip verification pending: browser access host unavailable; native Safari target timed out. Recheck in Plan 02-06.",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-11-06T19:06:48.877Z",
    "resolved_at": null,
    "milestone": null
  }
]
````
