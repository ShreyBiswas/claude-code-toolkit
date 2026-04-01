# Full Toolkit Rebuild

Rebuild the entire Claude Code Toolkit from scratch. This file is designed to be run with `/batch rebuild.md` from an empty (or nearly empty) project directory. It creates every file in the toolkit.

**Do not ask questions — execute all steps sequentially. Create every file exactly as specified.**

---

## Step 1: Directory structure

Create all directories:

```
.claude-plugin/
plugins/setup/.claude-plugin/
plugins/setup/commands/
plugins/setup/skills/
plugins/setup/scripts/
plugins/retrospect/.claude-plugin/
plugins/retrospect/commands/
plugins/retrospect/skills/
plugins/dev-workflow/.claude-plugin/
plugins/dev-workflow/skills/
plugins/writing-style/.claude-plugin/
plugins/writing-style/commands/
plugins/writing-style/skills/
plugins/visual-design/.claude-plugin/
plugins/visual-design/skills/
```

---

## Step 2: Root files

### CLAUDE.md

```markdown
# Claude Code Toolkit

Personal Claude Code plugin marketplace. Repo: `ShreyBiswas/claude-code-toolkit` (private).

## Structure

\```
.claude-plugin/marketplace.json   — Plugin catalogue (lists all available plugins)
plugins/<name>/                   — Each plugin is a self-contained directory
  .claude-plugin/plugin.json      — Plugin manifest
  commands/                       — Slash commands (*.md)
  skills/                         — Model-invoked skills (*.md)
\```

## Adding a new plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json`, `commands/`, and optionally `skills/`
2. Add an entry to `.claude-plugin/marketplace.json` under `plugins[]`
3. Test locally: `claude --plugin-dir ./plugins/<name>`
4. Commit and push — the marketplace update propagates automatically

## Testing

Use `--plugin-dir` for local testing before committing:
\```bash
claude --plugin-dir ./plugins/retrospect
\```

## Current plugins

- **setup** — `/toolkit-setup`: context-aware bootstrap — scans project, interviews user, recommends and installs relevant plugins
- **retrospect** — `/retrospect`: end-of-session config reconciliation and audit
- **writing-style** — `coding-style` skill (always active) + `/prose-style` command (on demand)
- **feature-dev** (external) — `/feature-dev`: Anthropic's feature development workflow
- **code-simplifier** (external) — autonomous code refinement agent
- **dev-workflow** — `tdd-overlay` skill (always active): run existing tests first for baseline, then TDD conventions layered on feature-dev
- **visual-design** — `visual-design` skill (conditional): general visual aesthetics for UIs, dashboards, plots, charts, logs, and any visual output
- **frontend-design** (external) — Anthropic's frontend design skill: bold, production-grade UI with distinctive aesthetic choices
- **web-design-guidelines** (external) — Vercel's web interface guidelines: accessibility, keyboard support, form behaviour, animation

## Built-in Claude Code tools

- `/skill-creator` — Anthropic's built-in skill for creating, improving, and evaluating custom skills. Use it when adding new skills to this toolkit.

## Conventions

- Concise skill descriptions — say what it does, not how
- Conservative recommendations — only propose changes with clear evidence
- No unnecessary complexity — each skill handles one phase
- Skills are sequential, not parallel — no subagents needed for the retrospect flow
```

### README.md

```markdown
# Claude Code Toolkit

Personal Claude Code plugin marketplace.

## Quick start

\```bash
# On a new machine (requires claude CLI + gh CLI):
./install.sh

# Then inside Claude Code:
/toolkit-setup
\```

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

\```bash
# Test a single plugin
claude --plugin-dir ./plugins/retrospect

# Test the whole marketplace
claude --plugin-dir .
\```
```

### install.sh

Create as executable (`chmod +x`):

```bash
#!/bin/bash
# Bootstrap the Claude Code Toolkit on a new machine
# Usage: ./install.sh
# Requires: claude CLI, gh CLI authenticated

set -euo pipefail

echo "Adding Claude Code Toolkit marketplace..."
claude plugin marketplace add ShreyBiswas/claude-code-toolkit

echo "Installing setup plugin..."
claude plugin install setup@ShreyBiswas-claude-code-toolkit --scope user

echo ""
echo "Marketplace added and setup plugin installed."
echo "Run /toolkit-setup inside Claude Code to complete installation."
```

### .claude-plugin/marketplace.json

```json
{
  "name": "ShreyBiswas-claude-code-toolkit",
  "owner": {
    "name": "Shrey Biswas"
  },
  "metadata": {
    "description": "Personal Claude Code plugin marketplace",
    "version": "2.0.0",
    "pluginRoot": "./plugins"
  },
  "plugins": [
    {
      "name": "setup",
      "source": "./plugins/setup",
      "description": "Context-aware toolkit bootstrap — scans project, interviews user, recommends and installs relevant plugins",
      "version": "2.0.0",
      "category": "productivity",
      "keywords": ["bootstrap", "setup", "settings"]
    },
    {
      "name": "retrospect",
      "source": "./plugins/retrospect",
      "description": "End-of-session config reconciliation — delta-aware audit of CLAUDE.md, memory, hooks, and more",
      "version": "1.0.0",
      "category": "productivity",
      "keywords": ["config", "reconciliation", "memory", "audit"],
      "relevance": "core — useful for any project",
      "configurable": false
    },
    {
      "name": "writing-style",
      "source": "./plugins/writing-style",
      "description": "Coding and prose style conventions — Better Comments, verbose naming, structured prose",
      "version": "1.0.0",
      "category": "style",
      "keywords": ["coding-style", "prose", "comments", "naming"],
      "relevance": "core — useful for any project",
      "configurable": false
    },
    {
      "name": "feature-dev",
      "source": "feature-dev@claude-plugins-official",
      "description": "Anthropic's feature development workflow — codebase exploration, architecture design, quality review",
      "version": "1.0.0",
      "category": "development",
      "keywords": ["feature", "development", "architecture", "review"],
      "external": true,
      "relevance": "useful for any project involving code — feature planning, architecture, review",
      "configurable": false
    },
    {
      "name": "code-simplifier",
      "source": "code-simplifier@claude-plugins-official",
      "description": "Anthropic's autonomous code refinement agent — simplifies for clarity and maintainability",
      "version": "1.0.0",
      "category": "development",
      "keywords": ["simplify", "refactor", "clarity", "maintainability"],
      "external": true,
      "relevance": "useful for any project with existing code that may benefit from simplification",
      "configurable": false
    },
    {
      "name": "dev-workflow",
      "source": "./plugins/dev-workflow",
      "description": "TDD overlay — run existing tests first, test-first design, non-shortcuttable tests, verify/iterate loop",
      "version": "1.1.0",
      "category": "development",
      "keywords": ["tdd", "testing", "baseline", "workflow"],
      "relevance": "useful when the project has or will have tests — enforces test-first development",
      "configurable": false
    },
    {
      "name": "visual-design",
      "source": "./plugins/visual-design",
      "description": "General visual design and aesthetics — UI/UX, data visualisation, dashboards, plots, logs, and any visual output",
      "version": "1.0.0",
      "category": "design",
      "keywords": ["design", "aesthetics", "visualisation", "UI", "UX", "plots", "dashboards"],
      "relevance": "useful when the project produces any visual output — UIs, plots, charts, dashboards, formatted terminal output, reports, documents",
      "configurable": true,
      "interview_hint": "Does this project produce any visual output? (UI, plots, charts, dashboards, formatted logs, reports)"
    },
    {
      "name": "frontend-design",
      "source": "frontend-design@claude-plugins-official",
      "description": "Anthropic's frontend design skill — bold, production-grade UI with distinctive aesthetic choices",
      "version": "1.0.0",
      "category": "design",
      "keywords": ["frontend", "design", "UI", "components", "CSS"],
      "external": true,
      "relevance": "useful when building frontend interfaces — web apps, component libraries, interactive UIs",
      "configurable": false
    },
    {
      "name": "web-design-guidelines",
      "source": "web-design-guidelines@vercel",
      "description": "Vercel's web interface guidelines — accessibility, keyboard support, form behaviour, animation, performance",
      "version": "1.0.0",
      "category": "design",
      "keywords": ["web", "accessibility", "a11y", "UI", "UX", "responsive"],
      "external": true,
      "relevance": "useful when building web interfaces — covers accessibility, responsive design, keyboard navigation, form UX, animation, and performance",
      "configurable": false
    }
  ]
}
```

---

## Step 3: Setup plugin

### plugins/setup/.claude-plugin/plugin.json

```json
{
  "name": "setup",
  "version": "2.0.0",
  "description": "Context-aware toolkit bootstrap — scans project, interviews user, recommends and installs relevant plugins",
  "author": {
    "name": "Shrey Biswas"
  }
}
```

### plugins/setup/README.md

```markdown
# setup

Bootstrap plugin for the Claude Code Toolkit marketplace.

## Usage

\```
/toolkit-setup
\```

Installs all other plugins from the marketplace with `--scope user` and applies preferred Claude Code settings (disables commit/PR attribution).

## What it does

1. Reads `.claude-plugin/marketplace.json` to discover all available plugins
2. Installs each plugin (except itself) with `--scope user`
3. Merges preferred settings into `~/.claude/settings.json`
4. Prints a summary of what was installed and configured
```

### plugins/setup/commands/toolkit-setup.md

Create the orchestrator command. Use `/skill-creator` or write directly. The command:

- Name: `toolkit-setup`
- Description: Context-aware toolkit bootstrap — scans project, interviews user, recommends and installs relevant plugins
- Runs 5 phases sequentially, each reading its skill file via `${CLAUDE_PLUGIN_ROOT}/skills/<name>.md`
- Phases: Project Scan → User Interview → Plugin Matching → Configuration → Installation
- Constraints: all installations require user approval, core plugins pre-selected but deselectable, keep interviewing until context is clear, don't ask what scan already answered
- Re-run shortcuts from Phase 2: keep existing → skip to Phase 5; evaluate new only → Phase 3 with flag; review fresh → Phase 3 normally
- Phase 4 is skipped entirely if no configurable plugins in the install list

### plugins/setup/skills/project-scanner.md

Create the Phase 1 skill. Name: `project-scanner`. Description: Scan the target project to build a profile of languages, frameworks, purpose, and existing config.

This is a read-only phase:

1. **Detect existing toolkit config** — check `.claude/toolkit-config.json`. If exists, it's a re-run (record previous profile, installed plugins, `installed_at` date).

2. **Scan project files** using glob/read in parallel. Check:
   - Build/config files: `package.json` (JS/TS + deps), `tsconfig.json`, `pyproject.toml`/`setup.py`/`setup.cfg`/`requirements.txt` (Python + deps), `Cargo.toml` (Rust), `go.mod` (Go), `Gemfile` (Ruby), `pom.xml`/`build.gradle` (Java/Kotlin), `Dockerfile`/`docker-compose.yml` (containers), `.github/workflows/`/`.gitlab-ci.yml`/`Jenkinsfile` (CI/CD)
   - Directory patterns: `tests/`/`test/`/`__tests__/`/`spec/` (tests), `src/`/`lib/`/`app/` (code), `docs/` or substantial README (docs), `*.ipynb` (data science), `public/`/`static/`/`assets/`/`templates/` (frontend/visual)
   - Dependencies of interest: web/UI frameworks, data/visualisation libs, testing frameworks, backend frameworks, CLI/terminal tools, ML frameworks, ORMs, etc.
   - Existing Claude config: `./CLAUDE.md`, `.claude/settings.json`, `.mcp.json`

3. **Git context** (if available): `git log --oneline -10`, `git remote -v`

4. **Synthesise profile** — natural-language summary: languages, frameworks/libraries, project character (what it is and does), notable characteristics, is-re-run flag, existing Claude config summary. Output goes to Phase 2 — do not present to user yet.

### plugins/setup/skills/setup-interview.md

Create the Phase 2 skill. Name: `setup-interview`. Description: Present scan findings and conduct a short gap-filling interview about the project.

1. **Present scan findings** — concise summary of detected languages, frameworks, tests, CI, project type. Ask "Does this look right? Anything I'm missing?" Incorporate corrections.

2. **Gap-filling questions** — ask as many as needed for full clarity, no cap. Question selection logic:
   - Ambiguous project type → "What are you building?"
   - Multiple languages, unclear primary → "Which is the primary language?"
   - Multiple directions → "What's the main goal?"
   - Re-run with changed profile → "Has the direction shifted?"
   - Plugin-specific: check marketplace for `interview_hint` fields matching project signals
   - Do NOT ask questions the scan already answered or things the user can't know yet

3. **Re-run handling** — if `.claude/toolkit-config.json` exists:
   - Show previously installed plugins
   - Detect new marketplace plugins (compare marketplace names against config, excluding setup)
   - If new plugins available: offer (1) Keep current, (2) Keep + evaluate new only, (3) Review fresh
   - If no new plugins: offer (1) Keep current, (2) Review fresh
   - Option mappings: keep → skip to Phase 5; evaluate new → Phase 3 with `rerun_decision: "evaluate_new"` and `new_plugins` list; review fresh → Phase 3 normally

Output: augmented profile with confirmed scan data, user answers, plugin config hints, re-run decision, and new_plugins list if applicable.

### plugins/setup/skills/plugin-matcher.md

Create the Phase 3 skill. Name: `plugin-matcher`. Description: Use the project profile to recommend relevant plugins from the marketplace catalogue.

1. **Read marketplace** — `.claude-plugin/marketplace.json`, parse `plugins` array. Skip `setup`.

2. **Handle evaluate-new-only re-runs** — if `rerun_decision: "evaluate_new"`: carry forward existing plugins, filter marketplace to only `new_plugins` list, present carried-forward as confirmed + new for evaluation.

3. **Assess each plugin** — read description, relevance, interview_hint. Decide: recommend+pre-select (clearly useful, "core" almost always), suggest but don't pre-select (might be useful), or omit (irrelevant). Design plugin extra care:
   - `visual-design`: recommend if ANY visual output (broadest)
   - `frontend-design`: ONLY for web frontends (React/Vue/Svelte/Angular). NOT CLI, data science, backend, HTML reports.
   - `web-design-guidelines`: ONLY for interactive web interfaces with forms. NOT static sites, dashboards without forms, API-only.
   - When in doubt → "Also available"

4. **Present recommendations** — grouped into recommended (pre-selected) and suggested, with one-line reason each. Offer: install all recommended / customise / add-remove specific.

5. **User confirmation** — handle flexibly: yes/default, customise, skip X, add X, any reasonable response.

Output: final approved install list + which have `configurable: true`.

### plugins/setup/skills/plugin-configurator.md

Create the Phase 4 skill. Name: `plugin-configurator`. Description: Run per-plugin configuration for configurable plugins in the install list.

Skip entirely if no configurable plugins. Otherwise:

1. Cross-reference marketplace with install list, filter to `configurable: true`
2. For each: read `interview_hint`, use profile to pre-fill obvious answers, ask remaining questions (1-2 max per plugin). Frame as choices not open-ended. Use profile to narrow options.
3. Confirm each config with user: show captured values, ask "Look right? (yes / edit)"

Output: configuration map `{ plugin_name: { key: value } }`. Unconfigured plugins omitted.

### plugins/setup/skills/plugin-installer.md

Create the Phase 5 skill. Name: `plugin-installer`. Description: Install approved plugins, write toolkit config, apply shared settings, print summary.

1. **Install plugins** — for each approved plugin:
   - External (`"external": true`): use `plugin.source` directly (e.g., `feature-dev@claude-plugins-official`)
   - Internal: use `<name>@ShreyBiswas-claude-code-toolkit`
   - Run: `claude plugin install <identifier> --scope user`
   - Track: success / already installed / failure

2. **Write toolkit config** — `.claude/toolkit-config.json` in current project directory:
   ```json
   {
     "toolkit_version": "2.0.0",
     "installed_at": "<ISO 8601>",
     "project_profile": {
       "description": "<summary>",
       "languages": ["..."],
       "frameworks": ["..."]
     },
     "plugins": {
       "<name>": { "installed": true },
       "<configurable>": { "installed": true, "config": { "..." } }
     }
   }
   ```

3. **Apply shared settings** — copy `scripts/apply-settings.py` to project root. Tell user to run it (`python3 apply-settings.py`, preview with `--dry-run`). Do NOT edit `~/.claude/settings.json` directly. The script applies: `attribution.commit`: "", `attribution.pr`: "", `env.ENABLE_CLAUDEAI_MCP_SERVERS`: "false", `showClearContextOnPlanAccept`: true, removes `disableBypassPermissionsMode` and `skipDangerousModePermissionPrompt`.

4. **CLAUDE.md proactive skills** — if CLAUDE.md exists and doesn't mention proactive skill usage, append a "## Skills" section telling Claude to use skills eagerly and proactively. If no CLAUDE.md, tell user to create one with that instruction.

5. **Print summary** — dynamic: project description, plugin results (installed/already/failed), settings script status, CLAUDE.md changes, config location.

### plugins/setup/scripts/apply-settings.py

Create this Python 3 script (no external deps). Make executable.

```python
#!/usr/bin/env python3
"""Apply Claude Code shared settings to ~/.claude/settings.json.

Idempotent — safe to run multiple times. Merges into existing settings
without overwriting unrelated keys.

Settings applied:
  - attribution.commit: ""  (disable commit attribution)
  - attribution.pr: ""      (disable PR attribution)
  - env.ENABLE_CLAUDEAI_MCP_SERVERS: "false"  (disable claude.ai MCP servers)
  - showClearContextOnPlanAccept: true  (show "clear context" on plan accept)

Run:  python3 apply-settings.py [--dry-run]
"""

import json
import os
import sys
from pathlib import Path

SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

WANTED = {
    "attribution": {"commit": "", "pr": ""},
    "env": {"ENABLE_CLAUDEAI_MCP_SERVERS": "false"},
    "showClearContextOnPlanAccept": True,
}

# Keys to remove if present (stale / superseded settings)
REMOVE_KEYS = ["disableBypassPermissionsMode", "skipDangerousModePermissionPrompt"]


def deep_merge(base: dict, overlay: dict) -> dict:
    """Merge overlay into base, recursing into nested dicts."""
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def remove_keys(d: dict, keys: list[str]) -> list[str]:
    """Remove top-level keys from dict. Returns list of keys actually removed."""
    removed = []
    for key in keys:
        if key in d:
            del d[key]
            removed.append(key)
    return removed


def main():
    dry_run = "--dry-run" in sys.argv

    # Read existing settings
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            settings = json.load(f)
    else:
        settings = {}

    # Apply
    deep_merge(settings, WANTED)
    removed = remove_keys(settings, REMOVE_KEYS)

    if dry_run:
        print("DRY RUN — would write:")
        print(json.dumps(settings, indent=2))
        if removed:
            print(f"\nRemoved keys: {', '.join(removed)}")
        return

    # Write
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")

    print("Settings applied to", SETTINGS_PATH)
    for key, value in WANTED.items():
        if isinstance(value, dict):
            for k, v in value.items():
                print(f"  ✓ {key}.{k}: {v!r}")
        else:
            print(f"  ✓ {key}: {value!r}")
    if removed:
        for key in removed:
            print(f"  ✗ {key}: removed")


if __name__ == "__main__":
    main()
```

---

## Step 4: Retrospect plugin

### plugins/retrospect/.claude-plugin/plugin.json

```json
{
  "name": "retrospect",
  "version": "1.0.0",
  "description": "End-of-session config reconciliation — audits and reconciles all project configuration",
  "author": {
    "name": "Shrey Biswas"
  }
}
```

### plugins/retrospect/README.md

```markdown
# retrospect

End-of-session config reconciliation plugin for Claude Code.

## Usage

\```
/retrospect
\```

Run after a productive session (or sequence of sessions) to reconcile project configuration with what actually changed.

## What it does

1. **Context Gathering** — detects git/non-git, computes delta from `.claude/.retrospect-baseline`, inventories all existing config (CLAUDE.md, memory, hooks, agents, skills, MCP, rules)
2. **Thematic Delta Analysis** — clusters the diff into themes, extracts patterns/capabilities/gotchas
3. **Reconciliation** — cross-references themes against existing config, generates proposals (additions, removals, updates) with dedup and staleness checks
4. **Presentation** — groups proposals by theme, shows diffs, collects accept/reject per group, applies accepted changes, updates baseline

## Design principles

- Conservative additions, aggressive removals
- Theme-based grouping (what you did, not which file changes)
- Internal quality audit (grades A-F internally, surfaces only concrete proposals)
- Delta-first, audit-second
- Significance threshold prevents noise on trivial sessions
- Non-git fallback uses session context as delta
```

### plugins/retrospect/commands/retrospect.md

Create the orchestrator command. Name: `retrospect`. Description: End-of-session config reconciliation — audits and reconciles all project configuration.

- Runs 4 phases sequentially via `${CLAUDE_PLUGIN_ROOT}/skills/<name>.md`
- Phases: Context Gathering → Thematic Delta Analysis → Reconciliation → Presentation
- Constraints: never propose modifications to retrospect's own plugin files, never propose MCP server additions (suggest running setup instead), all writes proposed-then-confirmed, conservative additions / aggressive removals
- Phase 1 significance check: for manual `/retrospect` invocations always run full audit regardless (threshold is for future auto-nudge hook)
- Finalisation: update `.claude/.retrospect-baseline` to current HEAD SHA, print "Applied N changes across M files. Removed K stale entries."

### plugins/retrospect/skills/config-inventory.md

Create Phase 1 skill. Name: `config-inventory`. Description: Detect git/non-git, compute delta from baseline, inventory all existing configuration.

1. **Detect environment** — `git rev-parse --is-inside-work-tree`

2. **Compute delta** — Git repos: read `.claude/.retrospect-baseline` for `baseline_sha`. If missing: compute via `git merge-base HEAD <default-branch>`, fall back to `HEAD~20`, use whichever is more recent. Run `git diff --stat`, `git diff --name-status`, `git diff` (full content). Non-git: reconstruct from conversation context.

3. **Significance check** — informational only, always proceed on manual runs. Skip conditions (ALL must be true): <5 files, <30 lines non-whitespace, no new files, no deleted files.

4. **Inventory existing config** — read all that exist, in parallel:
   - CLAUDE.md files: `./CLAUDE.md`, `**/CLAUDE.md`, `.claude.local.md`
   - Auto-memory: `~/.claude/projects/*/memory/` (match current project)
   - Agent memory: `.claude/agent-memory/`
   - Hooks: `.claude/settings.json` → `hooks` key
   - Agents: `.claude/agents/`
   - Skills: `.claude/skills/`
   - MCP config: `.mcp.json`
   - Rules: `.claude/rules/`

Output: (1) Delta — full diff, file-level summary, significance; (2) Inventory — catalogue of all config with content.

### plugins/retrospect/skills/delta-analysis.md

Create Phase 2 skill. Name: `delta-analysis`. Description: Cluster the diff into themes and extract patterns, capabilities, and gotchas.

1. Parse diff into file-level changes (path, change type, key content changes)
2. Classify by domain signal — file path patterns (`src/auth/` → auth, `tests/` → testing, `ci/` → CI/CD), content patterns (new imports, error handling, endpoints, types), dependency changes
3. Cluster into themes — coherent units of work, each file belongs to exactly one theme, prefer fewer broader themes
4. Extract per-theme: new patterns, new capabilities, new dependencies, removed/changed patterns, gotchas

Output: list of themes with name (3-8 words), 1-2 sentence summary, files, extracted signals.

### plugins/retrospect/skills/reconciler.md

Create Phase 3 skill. Name: `reconciler`. Description: Cross-reference themes against existing config, generate addition/removal/update proposals.

**Addition candidates** — conservative, ALL conditions: not already captured, would materially change Claude's behaviour, durable (not one-off), clear evidence in diff.

**Removal candidates** — aggressive, ANY condition: CLAUDE.md references nonexistent files/patterns, hook references deleted path, agent/skill duplicates built-in or another plugin, auto-memory contradicted by codebase, rule glob matches nothing.

**Update candidates** — existing config partially correct but needs revision.

**Quality audit** (internal, never surface grades): CLAUDE.md (conciseness, specificity, stale commands, architecture, gotchas), auto-memory (contradictions, verbosity, outdated), hooks (broad patterns, error handling), rules (empty globs, generic instructions). Grade A-F, convert below B to proposals.

**Dedup check**: not in CLAUDE.md, not in auto-memory, not redundant with another proposal, would actually change behaviour.

**Constraints**: never modify retrospect's own files, never propose MCP additions, merge or flag conflicting proposals.

Output: proposals with target file, action (add/update/remove), content, reason, theme.

### plugins/retrospect/skills/presenter.md

Create Phase 4 skill. Name: `presenter`. Description: Format proposals as themed groups, present for review, apply accepted changes.

- Group by theme, order by impact (most significant first), removals before additions within each theme
- Present each group with summary + numbered proposals + diff/description + reason. Ask "Accept this group? [y/n/edit]". Wait for response before next group.
- Responses: y = accept all in group, n = discard (baseline still advances), edit = present individually for modification
- Apply: all accepted changes to target files. Additions append or create. Updates replace. Removals delete. Show each write via Edit tool.
- Output: counts of changes applied, files modified, stale entries removed.

---

## Step 5: Writing-style plugin

### plugins/writing-style/.claude-plugin/plugin.json

```json
{
  "name": "writing-style",
  "version": "1.0.0",
  "description": "Coding and prose style conventions — Better Comments, verbose naming, structured prose",
  "author": {
    "name": "Shrey Biswas"
  }
}
```

### plugins/writing-style/README.md

```markdown
# writing-style

Coding and prose style conventions for Claude Code.

## Components

### `coding-style` (skill — always active)

Model-invoked skill that applies automatically whenever code is written, reviewed, or refactored. Covers Better Comments syntax, verbose snake_case naming, Google-style docstrings with `@ param` prefix, modern type hints, and British English spelling.

### `/prose-style` (command — on demand)

User-invoked command for writing non-code text. Covers sentence structure, contextual tone, Obsidian-style callout formatting, intuition-first explanations, claim-evidence-consequence argumentation, and voice characteristics.

## Usage

\```
# Coding style is always active — just write code

# Prose style on demand:
/prose-style
\```
```

### plugins/writing-style/skills/coding-style.md

Create the always-active coding style skill. Name: `coding-style`. Description: Shrey's personal coding style and philosophy. Apply whenever writing, reviewing, or refactoring any code — Python or otherwise. Trigger on any code-writing task, feature implementation, bug fix, or code review.

Content must cover ALL of the following sections with full detail:

**Better Comments** — 8 prefixes (`# *`, `# ~`, `# ?`, `# >`, `# !`, `# //`, `PERF:`, `BUGFIX:`) plus `HACK:` and `TODO:`. Include the layering pattern explanation (`# *` for sections → `# ~` for step narration → `# >` for theory → `# ?` for questions). Include a concrete SLERP code example demonstrating the layered pattern.

**Variable naming** — snake_case everywhere, PascalCase for classes, UPPER_SNAKE_CASE for constants, verbose full-word names (`interpolation_alpha` not `alpha`), short names only when maths is documented in `# >` comment, prefixed `d` for derivatives (`dCost_dWeights`), boolean prefixes (`use_`, `is_`, `has_`), camelCase only for ML framework constructor params.

**Comment philosophy** — explain why/what not how, narrate algorithms with `# ~`, document maths with `# >`, cite references with URLs, full sentences, pedagogical tone, end-of-line comments only for quick clarifications.

**Code organisation** — PEP 8 import grouping (no `from __future__`), modern Python 3.10+ type hints (`str | None` never `Optional[str]`, `list[str]` never `List[str]`), `Literal` for constrained strings, type aliases in `types.py`, typed `@dataclass` with `@classmethod` factories, Google-style docstrings with `@ param_name` prefix in Args, `if __name__ == "__main__"` guards, argparse at module level, registry pattern, `tqdm` progress bars, pre-condition validation.

**Error handling** — Loguru with context prefixes and custom levels (`SUCCESS`, `CONFIG`, `STEP`, `RESULT`), specific exception types, log then re-raise, graceful degradation, descriptive `FileNotFoundError`, atomic file writes (temp → `os.replace()`).

**Memory and performance (PyTorch)** — explicit `del` for large tensors, `torch.cuda.empty_cache()`, non-blocking transfers, layer-wise processing, `PERF:` comments.

**Spelling** — British English (`colour`, `normalised`, `serialisable`, `behaviour`, `maths`, `organisation`). No emojis. No filler comments.

### plugins/writing-style/commands/prose-style.md

Create the on-demand prose style command. Name: `prose-style`. Description: Shrey's prose writing style — apply when drafting essays, documentation, explanations, speeches, or any non-code text.

Content must cover ALL of the following:

**Sentence structure** — rhythmic variation (short punchy + longer building), single-clause for impact, active voice by default, tricolon (rule of three), anaphora (repeated openings), spaced hyphens ` - ` for parenthetical asides (NOT em-dashes), semicolons for tight connections, start with "But," "And," "So," freely.

**Tone** — contextual: technical/pedagogical (thinking-aloud, collaborative "we", curious), persuasive/rhetorical (emotionally charged, crescendo), explanatory/conversational (direct, enthusiastic), formal/academic (measured but not dry, still contractions). Always emotionally honest, never hedge excessively, never impersonal register.

**Formatting** — Obsidian callout boxes (`[!definition]`, `[!important]`, `[!warning]`, `[!danger]`, `[!example]`, `[!info]`, `[!resources]`), **bold** for introduced terms, *italics* for stress, `<mark class="hltr-yellow">` for key insights, `<mark class="hltr-purple">` for new terminology, 2-3 header levels, numbered lists for sequential, bullets for unordered, `[[Topic Name]]` internal links.

**Explaining concepts** — intuition-first pattern: (1) Motivation, (2) Intuition/analogy, (3) Formal definition, (4) Worked example. Rephrasing ("That is," / "In other words,"), dual-view explanations, collaborative "we", progressive complexity.

**Argumentation** — persuasive: Claim → Evidence → Gut-punch. Statistical precision (specific, sourced). Paradox openings. Technical: build inductively, rhetorical questions as pivots. Rebuttals: opponent's claim → punchy counter in `[!danger]` blocks.

**Voice** — contrasts as thinking tools, self-aware reflexivity, genuine enthusiasm ("immensely fascinating"), intellectual humour (dry, self-deprecating, darkly ironic), repetition for force, direct address, extended metaphors.

**Vocabulary** — sophisticated but unpretentious, active verbs, concrete over abstract, contractions freely, British English, favourite connectors ("So,", "Note that", "Crucially,", "After all,", "Now,", "Still,"), natural intensifiers ("immensely", "incredibly", "genuinely"). No emojis, no excessive hedging.

---

## Step 6: Visual-design plugin

### plugins/visual-design/.claude-plugin/plugin.json

```json
{
  "name": "visual-design",
  "version": "1.0.0",
  "description": "General visual design and aesthetics — UI/UX, data visualisation, dashboards, plots, logs, and any visual output",
  "author": {
    "name": "Shrey Biswas"
  }
}
```

### plugins/visual-design/skills/visual-design.md

Create the conditionally-active visual design skill. Name: `visual-design`. Description: Apply visual design principles to any visual output. Trigger on any task that creates, modifies, or reviews UI, dashboards, plots, charts, data visualisations, terminal formatting, log output, reports, or any other visual artefact — even if the user doesn't ask for design help.

Note: covers general aesthetics. Web-specific advice handled by dedicated web plugins.

**Scope/domain filtering** — read `.claude/toolkit-config.json`. If `plugins.visual-design.config.visual_domains` exists, apply Core Principles (always) + matching domains: `"data_viz"` → Data visualisation, `"dashboards"` → Dashboards, `"terminal"` → Terminal, `"reports"` → Reports. If absent/unset, apply all. Skip non-matching silently.

**Core Principles (always):**

1. Visual hierarchy — size/weight signal importance, contrast draws attention, proximity implies relationship, alignment creates order
2. Colour — constrained palette (1 primary, 1-2 accents, neutrals), functional colour (red=error, green=success, amber=warning), sufficient contrast, sequential/diverging colormaps (`viridis`, `plasma`, `coolwarm` — never `jet`/`rainbow`), dark themes use off-black (`#1a1a2e`, `#0f0f1a`) with desaturated accents
3. Typography — one typeface usually enough, consistent type scale (1.25x or 1.333x), 45-75 chars/line, plot labels always legible/non-overlapping (`tight_layout()` or `constrained_layout=True`)
4. Whitespace — design element not wasted space, consistent margins/padding (base unit multiples), plots use `subplots_adjust()`/`tight_layout()`
5. Simplicity — remove before adding, reduce chartjunk, default to clean (`sns.set_style("whitegrid")`), one message per visual

**Domain: Data visualisation** — right chart type (bar=comparison, line=trends, scatter=relationships, histogram=distribution, no pie >3-4 slices), annotate key points (`ax.annotate()`), mandatory axis labels/titles with units, legend outside (`bbox_to_anchor`), explicit `figsize`, consistent colour across subplots, always show uncertainty on statistical plots.

**Domain: Dashboards** — dense but organised, consistent card styling, large KPI font / smaller detail / right-align numbers, status = colour + icon, show last-updated timestamp for real-time data.

**Domain: Terminal/logs** — `tabulate` or `rich` not manual formatting, colour sparingly and semantically, `tqdm`/`rich.progress` for progress, structured logging (timestamp, level, source, message).

**Domain: Reports** — consistent heading hierarchy (no skipping levels), tables with distinct header / zebra striping / right-aligned numbers, figures always captioned and referenced by number.

**Anti-patterns** — rainbow colormaps on sequential data, 3D for 2D data, pie with many slices, truncated y-axes without marking, dual y-axes, decorative gradients/shadows/textures, inconsistent styling across related visuals.

---

## Step 7: Dev-workflow plugin

### plugins/dev-workflow/.claude-plugin/plugin.json

```json
{
  "name": "dev-workflow",
  "version": "1.1.0",
  "description": "TDD overlay — run existing tests first, test-first design, non-shortcuttable tests, verify/iterate loop",
  "author": { "name": "Shrey Biswas" }
}
```

### plugins/dev-workflow/README.md

```markdown
# dev-workflow

Personal TDD overlay that supplements Anthropic's `feature-dev` plugin with test-first conventions.

## What it does

The `tdd-overlay` skill activates automatically during any coding task and enforces:

- **Test baseline** — run existing tests before making changes for framework discovery, scope mapping, and a blame boundary (inspired by Simon Willison's [agentic engineering patterns](https://simonwillison.net/guides/agentic-engineering-patterns/first-run-the-tests/))
- **Test-first design** — write a comprehensive, failing test suite before implementation
- **Non-shortcuttable tests** — no mocking the thing under test, no tautological assertions, no testing implementation details
- **Verification** — run formatters, type checkers, linters, and review agents alongside tests; compare against baseline
- **Iteration loop** — fix implementation not tests; consult user after 3 failed iterations
- **Reporting** — include test counts, pass/fail breakdown, and baseline comparison in summaries

## Relationship to feature-dev

This plugin layers on top of Anthropic's `feature-dev` workflow phases:

- Inserts test design between phases 4 (architecture) and 5 (implementation)
- Supplements phase 6 (review) with automated verification tooling
- Supplements phase 7 (reporting) with test result summaries

Install `feature-dev` separately: `claude plugin install feature-dev@claude-plugins-official --scope user`

## Testing

\```bash
claude --plugin-dir ./plugins/dev-workflow
\```
```

### plugins/dev-workflow/skills/tdd-overlay.md

Create the always-active TDD skill. Name: `tdd-overlay`. Description: TDD conventions — run existing tests first for reconnaissance, test-first design, non-shortcuttable tests, verify/iterate loop. Apply during any coding task, bug fix, refactor, or feature implementation.

Supplements Anthropic's feature-dev workflow.

**Phase 0: Test Baseline** — before any code changes, run existing suite as reconnaissance. Why: framework discovery, scope map, blame boundary. Steps: detect framework (package.json scripts, pytest.ini/pyproject.toml/setup.cfg, Makefile/Justfile, test dirs, CI config), run suite, record baseline (total/pass/fail/skip/flaky). If no framework found, note absence and move on.

**Phase: Test Design** — after requirements/architecture (feature-dev 1-4), BEFORE implementation. Design comprehensive failing suite: unit tests (happy paths, edge cases, boundaries, error paths) + integration tests. Match existing conventions. Non-shortcuttable tests must satisfy ALL: tests observable behaviour not internals, no mocking thing under test, no tautological assertions, no testing private internals, each fails for distinct meaningful reason, would pass if implementation rewritten with same contract. Run before implementation — confirm they fail for right reasons (missing function, wrong value — NOT import/syntax errors).

**Phase: Implementation** — follow `coding-style` skill. Simplest approach. Don't gold-plate.

**Phase: Verification** — full suite (all pass), compare against Phase 0 baseline (no regressions), formatters, type checkers, linters, `/simplify`. All must pass.

**Phase: Iteration Loop** — fix implementation not tests. Only modify tests for genuine spec errors (confirm with user). After 3 iterations on same failure: stop, consult user.

**Phase: Reporting** — total count, pass/fail, baseline comparison, coverage if available, modified tests and why.

---

## Step 8: Per-plugin rebuild files

For each plugin, read the corresponding `rebuild.md` instructions from `plugins/<name>/rebuild.md` in this repository. If they don't exist yet (because we're doing a full rebuild), generate them from the skill/command content created above. Each rebuild.md should contain all instructions needed to recreate that plugin from scratch — the same content as described in Steps 3-7 above, but scoped to a single plugin.

---

## Step 9: Verification

After creating all files:

1. Run `find . -name "*.md" -path "*/skills/*" | sort` to confirm all skill files exist
2. Run `find . -name "*.md" -path "*/commands/*" | sort` to confirm all command files exist
3. Run `find . -name "plugin.json" | sort` to confirm all manifests exist
4. Verify `marketplace.json` lists all 9 plugins (5 internal + 4 external)
5. Run `cat .claude-plugin/marketplace.json | python3 -m json.tool` to validate JSON
6. Run `chmod +x install.sh plugins/setup/scripts/apply-settings.py`
