---
name: retrospect
description: End-of-session config reconciliation — audits and reconciles all project configuration
---

# /retrospect — Config Reconciliation

You are running the retrospect reconciliation flow. This is a sequential four-phase process. Execute each phase by reading and following the corresponding skill file, then proceed to the next.

**Important constraints:**
- Never propose modifications to retrospect's own plugin files
- Never propose MCP server additions (note them, suggest running setup instead)
- All file writes are proposed-then-confirmed — never write without user approval
- Be conservative with additions, aggressive with removals

---

## Phase 1: Context Gathering

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/config-inventory.md`

This phase detects git/non-git, computes the delta from baseline, checks significance, and inventories all existing configuration.

**If the significance check says to skip**: print the skip message and stop here. Exception: since this is a manual `/retrospect` invocation, always run the full audit regardless of the significance threshold. The threshold only applies to the nudge hook (stretch goal, not yet implemented).

Store the results (delta + inventory) in your working context for the next phases.

---

## Phase 2: Thematic Delta Analysis

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/delta-analysis.md`

Pass the delta from Phase 1. This phase clusters changes into themes and extracts patterns, capabilities, and gotchas.

Store the themed analysis for Phase 3.

---

## Phase 3: Reconciliation

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/reconciler.md`

Pass the themed analysis (Phase 2) and the config inventory (Phase 1). This phase cross-references themes against existing config to generate proposals.

Store the proposals for Phase 4.

---

## Phase 4: Presentation

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/presenter.md`

Pass the proposals from Phase 3. This phase formats them as themed groups, presents them to the user, and applies accepted changes.

---

## Finalisation

After Phase 4 completes:

1. If in a git repo, update `.claude/.retrospect-baseline` to the current HEAD SHA:
   ```bash
   git rev-parse HEAD > .claude/.retrospect-baseline
   ```
2. Print a summary: _"Applied N changes across M files. Removed K stale entries."_
