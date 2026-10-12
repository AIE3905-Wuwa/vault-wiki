---
name: plugin
owner: framework
description: "Plugin lifecycle management: install/upgrade/uninstall/list. Mechanical steps (compliance, dependencies, injection regions, registry, copy sync) are executed by .meta/scripts/wiki_plugin_kernel.py; the agent does only the semantic part. Triggers on: plugin, 插件, 装插件, 卸插件, install plugin, uninstall plugin."
---

# plugin: plugin (un)install

The framework's self-management command. All mechanical steps go through scripts; the agent does only the semantic part (plugin body content, changelog review, flow smoke test). Lifecycle rules: self-check must pass before (un)installing; uninstalling a depended-on plugin is blocked.

## Scope

Write: `.meta/plugins/<id>/` ((un)install), the AGENTS.md injection region, the `.meta/protocol/registry.yaml` plugin section, `.agents/skills/` command copies, wiki/log.md (all four projection sites go through the script)
Read: all manifests, `.meta/scripts/wiki_plugin_kernel.py`

## Install <id>

1. Prepare `.meta/plugins/<id>/`:
   - PLUGIN.yaml: seven required fields id / version / depends / updated / attachment / fields / inject (`inject` is the plugin's one-line disclosure — the injection-region projection when tier is full) + optional commands (the commands this plugin drives) / usage / checks (block-style lists: the projection sources of write-side contracts and check rules) / usage_routes (additional commands the usage lands in, source-side routing — installing a plugin lands its projections) / inject_tier (full|member, default full — member exits the injection region, riding on the family root's roster line + skills + L-layer reads; domain family members set this, see the kernel reference tier law)
   - PLUGIN.md structure: design summary (why it exists / position in the family / key rulings including rejected alternatives / mechanics back-references) → Structure → Invariants → Changelog (pure documentation; all injection sources live in the manifest)
2. `python .meta/scripts/wiki_plugin_kernel.py validate` — compliance and dependency checks; errors block
3. `python .meta/scripts/wiki_plugin_kernel.py all` — injection region / registry / command-copy sync
4. Flow smoke test: `python .meta/scripts/wiki_plugin_kernel.py audit <id>` (if the plugin carries an attached-audit script) + walk the key flows from the new plugin's PLUGIN.md against test assets (the behavior layer of the draft three-tier check)
5. Prepend one line to wiki/log.md (type "plugin")

## Upgrade <id>

1. Modify the plugin; bump the manifest `version`, refresh `updated`; add a line to the PLUGIN.md changelog
2. `python .meta/scripts/wiki_plugin_kernel.py all` — validate + injection-block version sync
3. A wiki/log.md "plugin" line

## Uninstall <id>

1. `python .meta/scripts/wiki_plugin_kernel.py validate` — if any plugin depends on it → blocked (unless the user explicitly cascades)
2. Move the directory out of `.meta/plugins/` (kept as archive; physical deletion always belongs to the human)
3. `python .meta/scripts/wiki_plugin_kernel.py all` — it disappears from the injection region / registry accordingly
4. A wiki/log.md "plugin" line

## ls

- `python .meta/scripts/wiki_plugin_kernel.py ls` (list + dependencies)

## Boundaries

- The script touches only four sites: plugin directories in/out, injection-region marker blocks, the registry plugin section, and command copies; the protocol / reserved sections and the AGENTS.md handwritten region are never touched
- Attached-audit contract (optional): `scripts/check.py` defines `check(ctx)` returning an issue list (level + message), read-only with zero side effects, Chinese messages, no third-party dependencies; ctx.root = repository root, ctx.pages = the wiki page set from a single scan
- Uninstall archiving and deletion are separate: moving out = uninstalling; deletion belongs to the human
- Errors printed by the script always block the operation — rerun after fixing; warnings (e.g. orphan copies) are reported only
