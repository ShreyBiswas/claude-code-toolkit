---
name: plugin-installer
description: Install approved plugins, write toolkit config, apply shared settings, print summary
---

# Plugin Installer

Install the approved plugins and persist the setup state.

## Step 1: Install plugins

For each plugin in the approved install list from Phase 3:

1. **Determine the install identifier**:
   - If the plugin has `"external": true` in the marketplace: use `plugin.source` directly (e.g., `feature-dev@claude-plugins-official`)
   - Otherwise: use `<plugin.name>@ShreyBiswas-claude-code-toolkit`

2. **Run**: `claude plugin install <identifier> --scope user`

3. **Track the result**: success, already installed, or failure (with error message)

If a plugin is already installed, note it as "already installed" and continue.

## Step 2: Write toolkit config

Write `.claude/toolkit-config.json` in the **current project directory** (not the toolkit repo):

```json
{
  "toolkit_version": "2.0.0",
  "installed_at": "<ISO 8601 timestamp>",
  "project_profile": {
    "description": "<natural-language project summary from Phase 2>",
    "languages": ["<detected languages>"],
    "frameworks": ["<detected frameworks and libraries>"]
  },
  "plugins": {
    "<plugin_name>": {
      "installed": true
    },
    "<configurable_plugin>": {
      "installed": true,
      "config": { "<from Phase 4>" }
    }
  }
}
```

If `.claude/` does not exist, create it. If `toolkit-config.json` already exists (re-run), overwrite it with the new state.

## Step 3: Apply shared settings

Read `~/.claude/settings.json`. Apply the following changes (merge, do not overwrite existing keys):

### Disable attribution

```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

### Disable Claude.ai MCP servers

Claude.ai-connected integrations (e.g. Gmail, Google Calendar) are automatically injected into every session, wasting context. Disable them:

```json
{
  "env": {
    "ENABLE_CLAUDEAI_MCP_SERVERS": "false"
  }
}
```

### Ensure bypass permissions option is available

If `disableBypassPermissionsMode` is present in the settings, **remove it** so that the "Yes, clear context and bypass permissions" option appears in permission prompts.

If `~/.claude/settings.json` does not exist, create it with the attribution and env settings above.

## Step 4: Print summary

Print a clear summary of everything that happened:

```
Toolkit setup complete.

Project: Python web API (Flask, pytest)

Plugins:
  ✓ retrospect (installed)
  ✓ writing-style (installed)
  ✓ dev-workflow (installed)
  ✓ feature-dev (already installed)
  — setup (skipped, this plugin)

Settings:
  ✓ attribution.commit: disabled
  ✓ attribution.pr: disabled
  ✓ claude.ai MCP servers: disabled
  ✓ bypass permissions option: enabled

Config written to .claude/toolkit-config.json
```

Adapt the summary dynamically based on what actually happened. Include any failures with their error messages.
