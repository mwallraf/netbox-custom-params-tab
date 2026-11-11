> **Historical record.** Preserved for provenance; not current installation or feature guidance.
> See the [documentation index](../README.md) and [current architecture](../development/architecture.md).

# Phase 1 baseline status

Executed 2026-11-06 from milestone/custom-field-profiles, canonical root checkout.

| Check | Actual result |
| --- | --- |
| Source provenance | SOURCE_SNAPSHOT_OK at 4dba67e; feature 42ad9c2 reachable |
| Root layout | SOURCE_LAYOUT_OK; no active linked worktree; original retained ignored |
| Image | netboxcommunity/netbox:v4.7.4-5.1.1 |
| Upstream index digest | sha256:69cd72d0b0e4928a90940a7011954aaa7060c75fddd8dc6cea2f19407bae45b1 |
| Runtime | NetBox 4.7.4-Docker-5.1.1, Python 3.14.4, Django 6.1.2 |
| Package | netbox-custom-field-profiles 0.1.0 editable install, native app registry confirmed |
| Schema | Initial schema generated in native interpreter before bootstrap; clean migration applied; native checks and zero drift pass |
| setup | SANDBOX_READY, actual web/worker healthy |
| Baseline tests | 35 stdlib helper tests pass; CONFIG_OK and RUNTIME_OK |
| Authentication | BASELINE_SMOKE_OK: actual CSRF admin login/session, generated native API token, negative controls |
| Dummy seed | SEED_IDEMPOTENT_OK: CMTS/CPE Devices with native field values |
| Legacy tests | Unexecuted: runner-unavailable, exit 1, pytest absent; local sanitized report .sandbox/legacy-tests.json |
| Lifecycle | LIFECYCLE_OK: two setups, down/up preserve data; reset recreates DB, stable credentials and unrelated container IDs |

Existing workstation NetBox remains separate and healthy. No credentials, DB
contents, configuration or volumes from that installation were accessed.

## Deferred scope

No profile administration/matching (Phase 2), Parameters tab (Phase 3), native
edit workflow (Phase 4), or full feature release verification (Phase 5) is claimed.
The legacy runner is unavailable, so there is no measured feature-failure list.
Old SQLite settings and panel tests remain unverified and may require adaptation
in their relevant feature phases. See [the development sandbox](../development/sandbox.md) for the optional declared-extra
installation path. Missing optional pytest is not a successful legacy run.

This new undeployed plugin has no legacy database upgrade requirement. Clean
sandbox migrations are verified; migration of any preexisting deployment is
outside this baseline. Ordinary restart retains .env and volumes; explicit reset
recreates this project's disposable data only.
