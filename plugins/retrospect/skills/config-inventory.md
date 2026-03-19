---
name: config-inventory
description: Detect git/non-git, compute delta from baseline, inventory all existing configuration
---

# Config Inventory

Gather all context needed for reconciliation: the delta (what changed) and the inventory (what config exists).

## Step 1: Detect environment

Run `git rev-parse --is-inside-work-tree` to determine if this is a git repo.

## Step 2: Compute delta

### Git repos

1. Read `.claude/.retrospect-baseline` to get `baseline_sha`
2. If missing (first run): compute a reasonable baseline:
   - Try `git merge-base HEAD $(git symbolic-ref refs/remotes/origin/HEAD --short 2>/dev/null || echo main)` for the merge-base with the default branch
   - Fall back to `HEAD~20`
   - Use whichever is more recent (closer to HEAD)
3. Run `git diff --stat baseline_sha..HEAD` to get file-level summary
4. Run `git diff --name-status baseline_sha..HEAD` to get adds/deletes/modifies
5. Run `git diff baseline_sha..HEAD` for the full content diff (store for Phase 2)

### Non-git repos

No baseline. Use the current session's conversation context:
- What files were created, modified, or deleted?
- What commands were run?
- What patterns were established?

Reconstruct an approximate delta from this context.

## Step 3: Significance check

**This check is informational only for manual `/retrospect` runs — always proceed regardless.**

Compute whether ALL of the following are true:
- Fewer than 5 files changed
- Fewer than 30 lines of non-whitespace diff
- No new files created
- No files deleted

If all true, note: _"Trivial changes since last /retrospect (N files, ~M lines)."_ but continue.

For non-git repos, skip the significance check entirely.

## Step 4: Inventory existing configuration

Read all of the following that exist. For each, note whether it exists, its size, and store its content:

| Target | Location | What to read |
|--------|----------|-------------|
| CLAUDE.md files | `./CLAUDE.md`, `**/CLAUDE.md`, `.claude.local.md` | Full content |
| Auto-memory | `~/.claude/projects/*/memory/` (match current project) | All `.md` files |
| Agent memory | `.claude/agent-memory/` | All files |
| Hooks | `.claude/settings.json` → `hooks` key | Hook definitions |
| Agents | `.claude/agents/` | All agent `.md` files |
| Skills | `.claude/skills/` | All `SKILL.md` files |
| MCP config | `.mcp.json` | Server definitions |
| Rules | `.claude/rules/` | All rule files |

Use `glob` and `read` tools to gather these efficiently. Read in parallel where possible.

## Output

Produce two artifacts for subsequent phases:
1. **Delta**: the full diff content, file-level change summary, and significance assessment
2. **Inventory**: a catalogue of all existing config with content, organized by target type
