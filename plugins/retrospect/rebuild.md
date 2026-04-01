# Rebuild Instructions: retrospect plugin

These are the instructions to give Claude to recreate this plugin from scratch.

---

## Plugin overview

Create a Claude Code plugin called `retrospect` (v1.0.0, author: Shrey Biswas) with:
- 1 slash command: `/retrospect` — orchestrator for the 4-phase reconciliation flow
- 4 skills (one per phase): config-inventory, delta-analysis, reconciler, presenter

Category: productivity. Keywords: config, reconciliation, memory, audit. Relevance: core (useful for any project). Not configurable.

The plugin performs end-of-session config reconciliation — it audits what changed in the codebase, compares against existing Claude configuration (CLAUDE.md, memory, hooks, agents, skills, MCP, rules), and proposes additions, removals, and updates.

---

## Command: /retrospect (orchestrator)

Create a slash command that runs a sequential four-phase process. Each phase reads and follows its corresponding skill file.

**Important constraints (enforce in the command):**
- Never propose modifications to retrospect's own plugin files
- Never propose MCP server additions (note them, suggest running setup instead)
- All file writes are proposed-then-confirmed — never write without user approval
- Be conservative with additions, aggressive with removals

**Flow:**
1. Phase 1: Context Gathering → `skills/config-inventory.md`
2. Phase 2: Thematic Delta Analysis → `skills/delta-analysis.md`
3. Phase 3: Reconciliation → `skills/reconciler.md`
4. Phase 4: Presentation → `skills/presenter.md`

Phase 1 has a significance check. For manual `/retrospect` invocations, always run the full audit regardless of the threshold (the threshold is for a future auto-nudge hook).

**Finalisation** (after Phase 4):
1. If in a git repo, update `.claude/.retrospect-baseline` to current HEAD SHA
2. Print summary: "Applied N changes across M files. Removed K stale entries."

---

## Skill 1: config-inventory (Phase 1)

Gather context: the delta (what changed) and the inventory (what config exists).

**Step 1: Detect environment** — `git rev-parse --is-inside-work-tree`

**Step 2: Compute delta**

For git repos:
1. Read `.claude/.retrospect-baseline` for `baseline_sha`
2. If missing (first run): compute baseline via `git merge-base HEAD <default-branch>`, fall back to `HEAD~20`, use whichever is more recent
3. Run `git diff --stat baseline_sha..HEAD` (file summary)
4. Run `git diff --name-status baseline_sha..HEAD` (adds/deletes/modifies)
5. Run `git diff baseline_sha..HEAD` (full content diff for Phase 2)

For non-git repos: reconstruct approximate delta from conversation context (files created/modified/deleted, commands run, patterns established).

**Step 3: Significance check** (informational only for manual runs — always proceed)
Skip-conditions (ALL must be true): <5 files changed, <30 lines non-whitespace diff, no new files, no deleted files.

**Step 4: Inventory existing configuration**

Read all of these that exist:
- CLAUDE.md files: `./CLAUDE.md`, `**/CLAUDE.md`, `.claude.local.md`
- Auto-memory: `~/.claude/projects/*/memory/` (match current project)
- Agent memory: `.claude/agent-memory/`
- Hooks: `.claude/settings.json` → `hooks` key
- Agents: `.claude/agents/`
- Skills: `.claude/skills/`
- MCP config: `.mcp.json`
- Rules: `.claude/rules/`

Use glob and read tools in parallel.

**Output:** Two artifacts — (1) Delta: full diff, file-level summary, significance assessment; (2) Inventory: catalogue of all config with content.

---

## Skill 2: delta-analysis (Phase 2)

Analyse the delta from Phase 1 and cluster into themes.

**Process:**
1. Parse diff into file-level changes (path, change type, key content changes)
2. Classify by domain signal:
   - File path patterns: `src/auth/` → auth, `tests/` → testing, `ci/` → CI/CD
   - Content patterns: new imports, error handling, API endpoints, types
   - Dependency changes: package.json, requirements.txt, etc.
3. Cluster into themes — coherent units of work (e.g., "Added OAuth authentication flow"). Each file belongs to exactly one theme. Prefer fewer, broader themes.
4. Extract per-theme signals:
   - New patterns (conventions, architecture, idioms)
   - New capabilities (what the codebase can now do)
   - New dependencies (tools, libraries, services)
   - Removed/changed patterns (migrations, renames, deprecations)
   - Gotchas discovered (build quirks, workarounds, environment requirements)

**Output:** List of themes with name, summary, files, and extracted signals.

---

## Skill 3: reconciler (Phase 3)

Cross-reference themed analysis against config inventory to produce proposals.

**Proposal types:**

*Addition candidates — conservative, propose only if ALL conditions met:*
- Not already captured in any existing config
- Would materially change Claude's behaviour in a future session
- Durable (not a one-off workaround)
- Clear evidence in the diff (not inferred or speculative)

*Removal candidates — aggressive, propose if ANY condition met:*
- CLAUDE.md references files/patterns/conventions that no longer exist
- Hook references deleted tool or path
- Agent or skill duplicates built-in functionality or another plugin
- Auto-memory contradicted by current codebase
- Rule glob pattern matches nothing

*Update candidates:*
- Existing config partially correct but needs revision
- Hook pattern should be broadened or narrowed

**Quality audit** (internal, do NOT surface grades to user):
- CLAUDE.md: conciseness, specificity, stale commands, architecture overview, gotchas
- Auto-memory: contradictions, verbosity, outdated facts
- Hooks: overly broad patterns, missing error handling
- Rules: glob patterns matching nothing, overly generic instructions
- Grade A-F internally; convert anything below B into concrete proposals

**Dedup check** before finalising:
1. Not already covered by CLAUDE.md
2. Not already covered by auto-memory
3. Not redundant with another proposal in this batch
4. Would actually change Claude's behaviour

**Constraints:** Never modify retrospect's own files. Never propose MCP additions. Merge or flag conflicting proposals.

**Output:** List of proposals with target file, action (add/update/remove), content, reason, and theme.

---

## Skill 4: presenter (Phase 4)

Format and present proposals for user review.

**Grouping:**
1. Group by theme
2. Order by impact (most significant gap first)
3. Within each theme: removals before additions

**Presentation format** (per theme group):
```
## Theme: [name]
[1-2 sentence summary]

### Proposed changes:
1. **[target file]** — [add/update/remove]
   [diff or description]
   _Reason: [evidence]_

Accept this group? [y/n/edit]
```

Wait for user response before moving to next group.

**Handling responses:**
- y: accept all proposals in group
- n: discard all (baseline still advances)
- edit: present each proposal individually for modification

**Applying changes:**
1. Apply all accepted changes
2. Additions: append to appropriate section or create file
3. Updates: replace old with new
4. Removals: delete content (or entire file)
5. Show each write before executing (use Edit tool for diffs)

**Output:** Count of changes applied, files modified, stale entries removed.

---

## File structure

```
plugins/retrospect/
  .claude-plugin/plugin.json
  commands/retrospect.md
  skills/config-inventory.md
  skills/delta-analysis.md
  skills/reconciler.md
  skills/presenter.md
  rebuild.md
```
