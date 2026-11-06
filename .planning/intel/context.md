# Existing implementation context

See the seven `.planning/codebase/*.md` maps for source-backed details.

- Main checkout has documentation; plugin source is in
  `.worktrees/feature/implement-plugin/` on feature/implement-plugin.
- Worktree metadata references an old filesystem location. Do not prune it.
- The rename and earlier edits are still uncommitted in the implementation tree.
- Current CustomTabConfig has OneToOne ContentType, incompatible with multiple
  profiles per model. It renders full_width_page(), which is a panel hook.
- Group configuration stores group_name strings; the original group FK design
  does not match actual implementation.
- Existing CRUD, inline formsets, weighted memberships, tests, and Docker stack
  are useful starting points, not verified implementations of new requirements.
- 45 test methods exist. No successful runtime test baseline was established;
  syntax checks after rename passed for 28 Python files.
- Initial migration warns it was handwritten and needs regeneration/verification.
- Basic API and migration command scaffolds are untracked implementation work.
- CMTS/CPE is an acceptance example, not a hard-coded taxonomy or filter type.

## Onboarding execution

- Mapping was completed inline; no subagents were used.
- GSD runtime identity: @opengsd/gsd-core 1.19.0.
- Seven mapping documents committed in 7b31bdd.
- GSD runtime warns that installed static Codex agent model settings are stale.
  This did not prevent inline onboarding; no global tool configuration was changed.
- The presence of .planning/codebase alone does not constitute an existing
  project scaffold; ingestion is explicitly new/bootstrap mode.
