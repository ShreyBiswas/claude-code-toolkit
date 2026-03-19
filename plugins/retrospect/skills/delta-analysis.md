---
name: delta-analysis
description: Cluster the diff into themes and extract patterns, capabilities, and gotchas
---

# Thematic Delta Analysis

Analyse the delta from Phase 1 and cluster it into meaningful themes.

## Process

### 1. Parse the diff into file-level changes

For each changed file, note:
- Path and filename
- Change type (added, modified, deleted, renamed)
- Key content changes (new imports, new functions, structural changes)

### 2. Classify by domain signal

Assign domain signals based on:
- **File path patterns**: `src/auth/` → auth, `tests/` → testing, `*.config.*` → configuration, `ci/` → CI/CD
- **Content patterns**: new imports, new error handling, new API endpoints, new types/interfaces
- **Dependency changes**: package.json, requirements.txt, Cargo.toml, go.mod, pyproject.toml

### 3. Cluster into themes

Group related changes into themes. A theme is a coherent unit of work:
- "Added OAuth authentication flow"
- "Refactored database layer to use connection pooling"
- "Set up CI/CD pipeline"

Each file change belongs to exactly one theme. Prefer fewer, broader themes over many narrow ones.

### 4. Extract per-theme signals

For each theme, extract:

- **New patterns**: coding conventions, architectural decisions, recurring idioms that Claude should know about
- **New capabilities**: what the codebase can now do that it couldn't before
- **New dependencies**: external tools, libraries, services introduced
- **Removed/changed patterns**: things that used to be true but aren't anymore (migrations, renames, deprecations)
- **Gotchas discovered**: build quirks, workarounds, non-obvious behaviours, environment requirements

## Output

A list of themes, each containing:
- Theme name (descriptive, 3-8 words)
- 1-2 sentence summary
- Files involved
- Extracted signals (patterns, capabilities, dependencies, removals, gotchas)
