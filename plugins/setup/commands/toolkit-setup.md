---
name: toolkit-setup
description: Context-aware toolkit bootstrap — scans project, interviews user, recommends and installs relevant plugins
---

# Toolkit Setup

You are running the context-aware toolkit bootstrap. This is a sequential five-phase process. Execute each phase by reading and following the corresponding skill file, then proceed to the next.

**Important constraints:**
- All plugin installations require user approval — nothing is installed silently
- Core plugins are pre-selected but can be deselected
- Keep interviewing until the project context is fully clear — do not cap the number of questions
- Do not ask what the project scan already answered

---

## Phase 1: Project Scan

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/project-scanner.md`

This phase scans the project directory to detect languages, frameworks, signals (e.g., `is_python`, `has_tests`, `is_frontend`), and existing toolkit configuration.

Store the project profile in your working context for the next phases.

---

## Phase 2: User Interview

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/setup-interview.md`

Pass the project profile from Phase 1. This phase presents the scan findings, confirms them with the user, and asks targeted gap-filling questions.

If this is a re-run:
- If the user wants to keep existing plugins → skip to Phase 5
- If the user wants to evaluate new plugins only → proceed to Phase 3 with `rerun_decision: "evaluate_new"` and the `new_plugins` list
- If the user wants to review fresh → proceed to Phase 3 normally

Store the augmented profile for Phase 3.

---

## Phase 3: Plugin Matching

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/plugin-matcher.md`

Pass the augmented profile from Phase 2. This phase reads the marketplace catalogue, scores plugins against the profile, and presents grouped recommendations for user approval.

Store the approved install list for Phase 4.

---

## Phase 4: Configuration

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/plugin-configurator.md`

Pass the approved install list from Phase 3. This phase runs per-plugin configuration for any `configurable: true` plugins.

**If no configurable plugins are in the install list, skip this phase entirely.**

Store the configuration map for Phase 5.

---

## Phase 5: Installation

Read and follow the skill at: `${CLAUDE_PLUGIN_ROOT}/skills/plugin-installer.md`

Pass the approved install list (Phase 3), configuration map (Phase 4), and project profile (Phase 2). This phase installs plugins, writes `.claude/toolkit-config.json`, applies shared settings, and prints a summary.
