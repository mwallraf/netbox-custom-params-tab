---
phase: 01-reproducible-baseline
plan: "02"
status: complete
requirements-completed: [BASE-02, BASE-03]
provides: [isolated-netbox-runtime]
key-files:
  created: [scripts/sandbox.py, docker/plugins.py, .env.example]
  modified: [docker-compose.yml, docker/Dockerfile, Makefile, netbox_custom_field_profiles/migrations/0001_initial.py]
---

# Plan 02: Dedicated native sandbox

Pinned `netboxcommunity/netbox:v4.7.4-5.1.1`, index digest `sha256:69cd72d0b0e4928a90940a7011954aaa7060c75fddd8dc6cea2f19407bae45b1` (amd64/arm64 manifests verified). Runtime reports `4.7.4-Docker-5.1.1`, Python 3.14.4 and Django 6.1.2. Plugin minimum is 4.7.0; only this patch is exercised.

- Task 1 commit d122e38: atomic/stable 0600 local environment, safe data parser, fixed Compose argv.
- Task 2 commit e6596d8: isolated localhost 18047 stack, PostgreSQL 18 and Valkey 9.1, upstream native launcher/configuration plus plugin-only supplement.
- Task 3: native direct-interpreter generation before bootstrap emitted PRE_BOOTSTRAP_SCHEMA_ABSENT and NATIVE_SCHEMA_GENERATED_BEFORE_BOOTSTRAP. Replaced handwritten initial migration and removed bypass command. Native web/worker then booted successfully.
- `make setup`: exit 0, RUNTIME_OK and SANDBOX_READY.
- `verify-runtime`: exit 0; Django check, migrate --check, plugin makemigrations --check --dry-run, exact version, installed-app and applied migration assertions pass.
- 11 helper tests pass, including concurrency and failed generation blocking startup.
- Existing workstation containers remained healthy; no external/shared volume or nonlocal port is configured.

## Deviations

Docker runtime version includes a packaging suffix; corrected the version assertion to match actual settings.VERSION. Subagent tool calls repeatedly stalled awaiting execution/approval, so parent resumed runtime verification inline. Two preexisting planning trailing spaces were removed to satisfy required diff check. No feature implementation added.

## Self-Check: PASSED

Actual image build and native startup/schema/registry checks passed. Admin authentication is verified in Plan 03.
