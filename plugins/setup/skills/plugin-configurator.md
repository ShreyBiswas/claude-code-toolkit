---
name: plugin-configurator
description: Run per-plugin configuration for configurable plugins in the install list
---

# Plugin Configurator

Configure plugins that need project-specific settings. This phase only runs if the install list from Phase 3 contains plugins with `configurable: true`.

## Step 1: Check for configurable plugins

Read the marketplace catalogue and cross-reference with the approved install list from Phase 3. Filter to only plugins where `configurable: true`.

If none are configurable, **skip this phase entirely** and pass an empty configuration map to Phase 5.

## Step 2: Configure each plugin

For each configurable plugin, in order:

1. **Read the plugin's `interview_hint`** from the marketplace entry. This provides the primary configuration question.
2. **Use the project profile** from Phase 2 to pre-fill obvious answers. For example, if the profile already says `framework: "react"`, do not ask the user which framework they are using.
3. **Ask the user** any remaining configuration questions. Keep it brief — one or two questions per plugin at most.
4. **Store the configuration** as a key-value object for that plugin.

### Configuration question guidelines

- Frame questions as choices, not open-ended prompts: _"Is this a marketing site, dashboard, or internal tool?"_ not _"Describe your frontend."_
- Use the project profile to narrow options: if `is_data_science` is set, offer relevant choices (matplotlib, plotly, d3) rather than generic ones
- Accept freeform answers gracefully — if the user types something unexpected, use it as-is

## Step 3: Confirm configuration

For each configured plugin, show the user what was captured:

```
Configuration for frontend-design:
  project_type: dashboard
  framework: react
  design_system: tailwind

Look right? (yes / edit)
```

## Output

A **configuration map**: `{ plugin_name: { key: value, ... } }` for each configured plugin. Plugins with no configuration are omitted (they get `{ "installed": true }` in the config file, with no `config` key).
