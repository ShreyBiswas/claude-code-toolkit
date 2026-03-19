# Claude Code Toolkit

Personal Claude Code plugin marketplace. Repo: `ShreyBiswas/claude-code-toolkit` (private).

## Structure

```
.claude-plugin/marketplace.json   — Plugin catalogue (lists all available plugins)
plugins/<name>/                   — Each plugin is a self-contained directory
  .claude-plugin/plugin.json      — Plugin manifest
  commands/                       — Slash commands (*.md)
  skills/                         — Model-invoked skills (*.md)
```

## Adding a new plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json`, `commands/`, and optionally `skills/`
2. Add an entry to `.claude-plugin/marketplace.json` under `plugins[]`
3. Test locally: `claude --plugin-dir ./plugins/<name>`
4. Commit and push — the marketplace update propagates automatically

## Testing

Use `--plugin-dir` for local testing before committing:
```bash
claude --plugin-dir ./plugins/retrospect
```

## Current plugins

- **setup** — `/toolkit-setup`: installs all marketplace plugins and applies preferred settings
- **retrospect** — `/retrospect`: end-of-session config reconciliation and audit
- **writing-style** — `coding-style` skill (always active) + `/prose-style` command (on demand)
- **feature-dev** (external) — `/feature-dev`: Anthropic's feature development workflow
- **code-simplifier** (external) — autonomous code refinement agent
- **dev-workflow** — `tdd-overlay` skill (always active): TDD conventions layered on feature-dev

## Built-in Claude Code tools

- `/skill-creator` — Anthropic's built-in skill for creating, improving, and evaluating custom skills. Use it when adding new skills to this toolkit.

## Conventions

- Concise skill descriptions — say what it does, not how
- Conservative recommendations — only propose changes with clear evidence
- No unnecessary complexity — each skill handles one phase
- Skills are sequential, not parallel — no subagents needed for the retrospect flow
