# Maintainer documentation

This directory covers development and verification, not end-user installation.

- [Sandbox](sandbox.md): prerequisites, startup, credentials and Make targets.
- [Architecture](architecture.md): native integration, data boundaries and System metadata.
- [Testing](testing.md): automated gates and repeatable manual acceptance checks.
- [CI and releases](releases.md): verified artifacts, Trusted Publishing and GitHub Releases.
- [Source recovery](source-recovery.md): preserved recovery manifest used by the provenance tool.

The implementation is canonical in the repository root on
`milestone/custom-field-profiles`. Do not edit or prune ignored
`.recovery/implement-plugin` and do not create per-phase worktrees.

The current agreed Device workflow is implemented and user UAT was accepted on
2026-11-11. Subsequent fixes have their own evidence in `.planning/`. Historical
milestone counts and validation debt belong there, not in installation guidance.
The optional legacy pytest suite is separate from the required native tests.

[User/admin documentation](../README.md) · [Historical records](../history/README.md)
