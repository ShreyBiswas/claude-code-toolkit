# Claude Code Toolkit

Personal Claude Code plugin marketplace.

## Quick start

```bash
# On a new machine (requires claude CLI + gh CLI):
./install.sh

# Then inside Claude Code:
/toolkit-setup
```

## Plugins

| Plugin | Command | Description |
|--------|---------|-------------|
| **setup** | `/toolkit-setup` | Installs all plugins and applies preferred settings |
| **retrospect** | `/retrospect` | End-of-session config reconciliation and audit |
| **writing-style** | `/prose-style` (+ auto coding skill) | Coding and prose style conventions |
| **feature-dev** | `/feature-dev` | Anthropic's feature development workflow (external) |
| **code-simplifier** | (autonomous agent) | Anthropic's code refinement agent (external) |
| **dev-workflow** | (auto TDD skill) | TDD overlay — test-first conventions for feature-dev |

> **Tip**: Use Anthropic's built-in `/skill-creator` to help author and test new skills.

## Adding a plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json` and `commands/`
2. Add entry to `.claude-plugin/marketplace.json`
3. Test: `claude --plugin-dir ./plugins/<name>`
4. Commit and push

## Local development

```bash
# Test a single plugin
claude --plugin-dir ./plugins/retrospect

# Test the whole marketplace
claude --plugin-dir .
```
