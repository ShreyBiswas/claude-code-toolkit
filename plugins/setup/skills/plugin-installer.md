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

This step is handled by a script to avoid unreliable JSON manipulation.

1. **Copy the script** from `${CLAUDE_PLUGIN_ROOT}/../setup/scripts/apply-settings.py` to the project root as `apply-settings.py`
2. **Tell the user** to run it:

```
A settings script has been copied to your project root: apply-settings.py

Please run it to apply shared Claude Code settings:
  python3 apply-settings.py

(You can preview changes first with: python3 apply-settings.py --dry-run)

It applies:
  • attribution.commit / attribution.pr: "" (disable attribution)
  • env.ENABLE_CLAUDEAI_MCP_SERVERS: "false" (disable claude.ai MCP servers)
  • showClearContextOnPlanAccept: true (show "clear context" on plan accept)
  • Removes stale keys: disableBypassPermissionsMode, skipDangerousModePermissionPrompt

Delete the script after running — it's not needed again.
```

3. **Do NOT attempt to edit `~/.claude/settings.json` yourself** — the script handles it correctly.

## Step 4: CLAUDE.md — proactive skill usage

Check whether the project has a `CLAUDE.md` file.

- **If it exists**: read it and check whether it already contains instructions about proactively using skills. If not, append the following block (or a project-appropriate variant) to the file:

```markdown
## Skills

Claude has access to skills (via plugins and built-in features). Use them eagerly and proactively wherever they apply — don't wait to be asked. If a skill matches the current task, invoke it automatically.
```

- **If it does not exist**: tell the user they should add a `CLAUDE.md` to their project, and recommend including the instruction above so that skills are used proactively in every session.

In both cases, mention this in the summary so the user knows what happened.

## Step 5: Print summary

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
  → apply-settings.py copied to project root — run it to apply shared settings

CLAUDE.md:
  ✓ proactive skill usage instruction added

Config written to .claude/toolkit-config.json
```

Adapt the summary dynamically based on what actually happened. Include any failures with their error messages.
