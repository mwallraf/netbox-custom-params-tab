# Project context

Read `docs/REQUIREMENTS.md` before planning or implementing changes. It records
the agreed NetBox Custom Field Profiles milestone and supersedes conflicting
assumptions in the original panel-based design and implementation plan.

GSD onboarding is complete. Read `.planning/STATE.md` for current workflow state,
`.planning/ROADMAP.md` for milestone status, and
`.planning/milestones/v0.1.0-REQUIREMENTS.md` for
traceable requirement IDs. The five-phase Device milestone and final user UAT are
accepted; consult current STATE.md for subsequent work and accepted audit debt.

Read `README.md` for the public overview, `docs/README.md` for user/admin guides,
and `docs/development/README.md` for maintainer instructions. `CLAUDE.md` summarizes
the current implementation; superseded panel records are under `docs/history/`.

Do not infer authorization for new features or additional object types from
requirements alone. Follow the user's subsequent instructions for new work.

The implementation is canonical in the repository root on milestone/custom-field-profiles.
Do not create worktrees or per-phase branches. The retired source is retained locally
in ignored .recovery/implement-plugin; never edit it or prune it as a worktree.
