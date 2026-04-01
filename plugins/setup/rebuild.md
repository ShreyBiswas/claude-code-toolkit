# Rebuild Instructions: setup plugin

These are the instructions to give Claude to recreate this plugin from scratch.

---

## Plugin overview

Create a Claude Code plugin called `setup` (v2.0.0, author: Shrey Biswas) with:
- 1 slash command: `/toolkit-setup` — orchestrator for the 5-phase bootstrap flow
- 5 skills (one per phase): project-scanner, setup-interview, plugin-matcher, plugin-configurator, plugin-installer
- 1 Python script: `scripts/apply-settings.py` — idempotent settings applicator

Category: productivity. Keywords: bootstrap, setup, settings. This plugin is never recommended for installation by itself — it is the installer.

---

## Command: /toolkit-setup (orchestrator)

Create a slash command that runs a sequential five-phase process.

**Important constraints:**
- All plugin installations require user approval — nothing installed silently
- Core plugins are pre-selected but can be deselected
- Keep interviewing until project context is fully clear — do not cap question count
- Do not ask what the project scan already answered

**Flow:**
1. Phase 1: Project Scan → `skills/project-scanner.md`
2. Phase 2: User Interview → `skills/setup-interview.md`
3. Phase 3: Plugin Matching → `skills/plugin-matcher.md`
4. Phase 4: Configuration → `skills/plugin-configurator.md` (skip if no configurable plugins)
5. Phase 5: Installation → `skills/plugin-installer.md`

Re-run shortcuts from Phase 2:
- Keep existing plugins → skip to Phase 5
- Evaluate new only → Phase 3 with `evaluate_new` flag
- Review fresh → Phase 3 normally

---

## Skill 1: project-scanner (Phase 1)

Read-only phase. Scan the project directory to build a profile.

**Step 1: Detect existing toolkit config**
Check `.claude/toolkit-config.json`. If exists: this is a re-run — record previous profile and installed plugins, note `installed_at` date.

**Step 2: Scan project files** (use glob/read in parallel)

Build/config files to check:
- `package.json` → JS/TS, parse deps for frameworks/test runners/UI/build tools
- `tsconfig.json` → TypeScript
- `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt` → Python, parse deps
- `Cargo.toml` → Rust
- `go.mod` → Go
- `Gemfile` → Ruby
- `pom.xml`, `build.gradle` → Java/Kotlin
- `Dockerfile`, `docker-compose.yml` → Containerised
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` → CI/CD

Directory patterns to check:
- `tests/`, `test/`, `__tests__/`, `spec/` → Tests exist
- `src/`, `lib/`, `app/` → Has code
- `docs/`, substantial README → Documentation
- `*.ipynb` → Jupyter/data science
- `public/`, `static/`, `assets/`, `templates/` → Visual content/frontend

Dependencies of interest: web/UI frameworks, data/visualisation libs, testing frameworks, backend frameworks, CLI/terminal tools, ML frameworks, database ORMs, etc.

Existing Claude config: `./CLAUDE.md`, `.claude/settings.json`, `.mcp.json`

**Step 3: Git context** (if available)
- `git log --oneline -10`
- `git remote -v`

**Step 4: Synthesise profile**
Natural-language summary covering: languages, frameworks/libraries, project character (what it is and does), notable characteristics, is-re-run flag, existing Claude config summary.

Output goes to Phase 2 — do not present to user yet.

---

## Skill 2: setup-interview (Phase 2)

Present scan findings, confirm with user, fill gaps.

**Step 1: Present scan findings**
Concise summary of what was detected (languages, frameworks, tests, CI, project type). Ask: "Does this look right? Anything I'm missing?" Incorporate corrections.

**Step 2: Gap-filling questions**
Ask as many questions as needed for full clarity. Keep going until no remaining ambiguity.

Question selection logic:
- Ambiguous project type → "What are you building?"
- Multiple languages, unclear primary → "Which is the primary language?"
- Multiple directions possible → "What's the main goal?"
- Re-run with changed profile → "Has the direction shifted?"

Plugin-specific questions: check marketplace for plugins with `interview_hint` field whose signals match the project. Include those questions.

Do NOT ask: questions the scan already answered, or questions the user can't know yet.

**Step 3: Re-run handling**
If `.claude/toolkit-config.json` exists:
1. Show previously installed plugins
2. Detect new marketplace plugins (compare marketplace against config)
3. Present options:
   - If new plugins available: (1) Keep current, (2) Keep + evaluate new only, (3) Review fresh
   - If no new plugins: (1) Keep current, (2) Review fresh

**Output:** Augmented profile with original scan data (confirmed/corrected), user answers, plugin config hints, re-run decision, and new_plugins list if applicable.

---

## Skill 3: plugin-matcher (Phase 3)

Recommend plugins based on project context.

**Step 1:** Read `.claude-plugin/marketplace.json` from marketplace root. Skip `setup` plugin.

**Step 1b: Evaluate-new-only re-runs**
If `rerun_decision: "evaluate_new"`: carry forward all existing plugins, filter marketplace to only new plugins, present carried-forward as confirmed + new for evaluation.

**Step 2: Assess each plugin**
Read description, relevance hint, interview_hint. Decide:
- **Recommend and pre-select** if clearly useful. "Core" plugins almost always recommended.
- **Suggest but don't pre-select** if might be useful but not confident.
- **Omit** if clearly irrelevant.

**Design plugin assessment** (extra care needed):
- `visual-design`: recommend if ANY visual output (broadest design plugin)
- `frontend-design`: ONLY for web frontends (React, Vue, Svelte, Angular). NOT for CLI, data science, backend APIs, HTML reports.
- `web-design-guidelines`: ONLY for interactive web interfaces with form behaviour. NOT for static sites, dashboards without forms, API-only.

When in doubt about design plugins, place in "Also available" rather than recommending.

**Step 3: Present recommendations**
Group into recommended (pre-selected) and suggested (not pre-selected), with one-line reason for each. Offer: (1) Install all recommended, (2) Customise, (3) Add/remove specific.

**Step 4: User confirmation**
Handle flexibly: "yes"/default, "customise", "skip X", "add X", any other reasonable response.

**Output:** Final approved install list + which plugins have `configurable: true`.

---

## Skill 4: plugin-configurator (Phase 4)

Configure plugins with `configurable: true`. Skip entirely if none in install list.

**Step 1:** Cross-reference marketplace with install list, filter to configurable plugins.

**Step 2: Configure each plugin**
1. Read the plugin's `interview_hint` from marketplace
2. Use project profile to pre-fill obvious answers
3. Ask remaining config questions (brief — 1-2 per plugin max)
4. Frame as choices, not open-ended. Use profile to narrow options.

**Step 3: Confirm configuration**
Show captured config per plugin, ask "Look right? (yes / edit)"

**Output:** Configuration map: `{ plugin_name: { key: value } }`. Unconfigured plugins omitted.

---

## Skill 5: plugin-installer (Phase 5)

Install plugins and persist state.

**Step 1: Install plugins**
For each approved plugin:
1. Determine install identifier:
   - External (`"external": true`): use `plugin.source` directly (e.g., `feature-dev@claude-plugins-official`)
   - Internal: use `<plugin.name>@ShreyBiswas-claude-code-toolkit`
2. Run: `claude plugin install <identifier> --scope user`
3. Track: success, already installed, or failure

**Step 2: Write toolkit config**
Write `.claude/toolkit-config.json` in the current project directory:
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
    "<configurable_name>": { "installed": true, "config": { "..." } }
  }
}
```
Create `.claude/` if needed. Overwrite on re-run.

**Step 3: Apply shared settings**
Copy `scripts/apply-settings.py` to project root. Tell user to run it. Do NOT edit `~/.claude/settings.json` directly.

The script applies:
- `attribution.commit`: "" and `attribution.pr`: "" (disable attribution)
- `env.ENABLE_CLAUDEAI_MCP_SERVERS`: "false"
- `showClearContextOnPlanAccept`: true
- Removes stale keys: `disableBypassPermissionsMode`, `skipDangerousModePermissionPrompt`

The script is idempotent, supports `--dry-run`, does deep-merge into existing settings.

**Step 4: CLAUDE.md — proactive skill usage**
If CLAUDE.md exists and doesn't already mention proactive skill usage, append:
```markdown
## Skills

Claude has access to skills (via plugins and built-in features). Use them eagerly and proactively wherever they apply — don't wait to be asked. If a skill matches the current task, invoke it automatically.
```
If no CLAUDE.md exists, tell user to create one with that instruction.

**Step 5: Print summary**
Dynamic summary of: project description, plugin install results (installed/already installed/failed), settings script status, CLAUDE.md changes, config file location.

---

## Script: apply-settings.py

A standalone Python 3 script (no dependencies beyond stdlib). Features:
- Reads `~/.claude/settings.json` (creates if missing)
- Deep-merges wanted settings without overwriting unrelated keys
- Removes specified stale keys
- `--dry-run` flag to preview changes
- Idempotent — safe to run multiple times

---

## File structure

```
plugins/setup/
  .claude-plugin/plugin.json
  commands/toolkit-setup.md
  skills/project-scanner.md
  skills/setup-interview.md
  skills/plugin-matcher.md
  skills/plugin-configurator.md
  skills/plugin-installer.md
  scripts/apply-settings.py
  rebuild.md
```
