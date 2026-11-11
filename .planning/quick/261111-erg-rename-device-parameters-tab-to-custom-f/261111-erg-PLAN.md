---
mode: quick
quick_id: 261111-erg
status: planned
---
# Rename the Device tab to Custom Fields

Execute inline using the skill adapter fallback; no agents or worktrees.

1. Change the tab label, edit action/title/heading and related user-facing messages
   to Custom Fields / Edit Custom Fields. Preserve routes, identifiers and storage.
2. Update metadata and current documentation. Preserve historical records and
   screenshot bytes; identify the screenshot's former label accurately.
3. Update existing label assertions, run focused native navigation/editor/metadata
   tests, reload the sandbox and check the runtime registration. Commit code/docs,
   then record summary and update STATE through the quick-task registry.

Success: native navigation displays Custom Fields; editing uses consistent labels;
existing URLs and all functional permission/data behavior are retained.

<threat_model>
ASVS level 1; high threshold. Presentation-only change. Preserve constrained Device
lookups, native permissions, signed scope, URL registration and persistence.
No new external service integration, schema change or identity generalization.
</threat_model>
