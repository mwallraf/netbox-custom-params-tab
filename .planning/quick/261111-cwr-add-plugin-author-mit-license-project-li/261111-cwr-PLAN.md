---
status: planned
mode: quick
---

# Plugin metadata and user documentation

User decisions: Author Maarten Wallraf; GitHub project
https://github.com/mwallraf/netbox-custom-params-tab; MIT license; add origin.
Documentation belongs in System > Plugins, not profile administration screens.

1. Add MIT LICENSE, consistent PEP 621 author/project/documentation/license metadata
   and native PluginConfig author plus concise explanation and Markdown links.
2. Write a minimal user guide covering native custom fields, profiles, Parameters,
   native edits and hiding main-detail visibility without changing editability.
3. Verify the real native System plugin detail response exposes the explanation
   and links. NetBox 4.7 does not map local package URLs/license to its catalog rows;
   use the supported Description field rather than patching upstream code.
4. Verify built wheel metadata/license and existing packaged assets, then record
   results, commit code/docs and append the quick-task state row. No remote push.

Run inline under the skill's Codex single-agent fallback. No new branch/worktree.
