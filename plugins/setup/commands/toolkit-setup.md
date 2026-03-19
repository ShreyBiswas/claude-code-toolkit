---
name: toolkit-setup
description: Install all toolkit plugins and apply preferred Claude Code settings
---

# Toolkit Setup

You are running the toolkit bootstrap. Follow these steps exactly.

## Step 1: Read the marketplace catalogue

Read the file at the marketplace root: find the closest ancestor directory containing `.claude-plugin/marketplace.json` (this plugin's marketplace). Parse the `plugins` array to get the list of all available plugins.

## Step 2: Install all plugins

For each plugin in the marketplace catalogue (except `setup` itself):

1. If the plugin has `"external": true`, use `plugin.source` directly as the install identifier
2. Otherwise, construct the install identifier: `<plugin.name>@ShreyBiswas-claude-code-toolkit`
3. Run: `claude plugin install <identifier> --scope user`
3. Track success/failure for the summary

If a plugin is already installed, note it as "already installed" and continue.

## Step 3: Apply preferred settings

Read `~/.claude/settings.json`. Apply the following settings if not already present (merge, don't overwrite existing keys):

```json
{
  "attribution": {
    "commit": "",
    "pr": ""
  }
}
```

This disables the `Co-Authored-By` line on commits and the attribution footer on PRs.

**Do not overwrite** any existing settings keys that aren't listed above. Read the file first, merge, then write back.

If `~/.claude/settings.json` doesn't exist, create it with just these settings.

## Step 4: Print summary

Print a summary like:

```
Toolkit setup complete.

Plugins installed:
  ✓ retrospect (installed)
  — setup (skipped, this plugin)

Settings applied:
  ✓ attribution.commit: disabled
  ✓ attribution.pr: disabled
```

Adjust the list dynamically based on what the marketplace catalogue contained and what actually happened.
