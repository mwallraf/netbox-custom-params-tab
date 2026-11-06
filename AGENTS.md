# Project context

Read `docs/REQUIREMENTS.md` before planning or implementing changes. It records
the agreed NetBox Custom Field Profiles milestone and supersedes conflicting
assumptions in the original panel-based design and implementation plan.

GSD onboarding is complete. Read `.planning/STATE.md` for current workflow state,
`.planning/ROADMAP.md` for the five phases, and `.planning/REQUIREMENTS.md` for
traceable requirement IDs. Next step: `$gsd-discuss-phase 1`.

Read `README.md` for the source location, rename status, and environment caveats.
`CLAUDE.md` contains additional background about the earlier implementation.

The current stage is requirements capture and phase planning. Do not infer an
instruction to implement new features from the requirements document alone.
Follow the user's subsequent instructions when development is authorized.

The implementation currently lives in `.worktrees/feature/implement-plugin/`.
Preserve its existing uncommitted changes. Its worktree metadata still references
the repository's previous location; do not prune it as an abandoned worktree.
