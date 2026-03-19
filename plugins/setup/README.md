# setup

Bootstrap plugin for the Claude Code Toolkit marketplace.

## Usage

```
/toolkit-setup
```

Installs all other plugins from the marketplace with `--scope user` and applies preferred Claude Code settings (disables commit/PR attribution).

## What it does

1. Reads `.claude-plugin/marketplace.json` to discover all available plugins
2. Installs each plugin (except itself) with `--scope user`
3. Merges preferred settings into `~/.claude/settings.json`
4. Prints a summary of what was installed and configured
