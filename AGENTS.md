# Project context

Read `docs/REQUIREMENTS.md` before planning or implementing changes. It records
the agreed NetBox Custom Field Profiles milestone and supersedes conflicting
assumptions in the original panel-based design and implementation plan.

GSD onboarding is complete. Read `.planning/STATE.md` for current workflow state,
`.planning/ROADMAP.md` for the five phases, and `.planning/REQUIREMENTS.md` for
traceable requirement IDs. Phase 1 execution is authorized; consult current STATE.md for the next step.

Read `README.md` for the source location, rename status, and environment caveats.
`CLAUDE.md` contains additional background about the earlier implementation.

The current stage is requirements capture and phase planning. Do not infer an
instruction to implement new features from the requirements document alone.
Follow the user's subsequent instructions when development is authorized.

The implementation is canonical in the repository root on milestone/custom-field-profiles.
Do not create worktrees or per-phase branches. The retired source is retained locally
in ignored .recovery/implement-plugin; never edit it or prune it as a worktree.
