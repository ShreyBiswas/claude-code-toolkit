# retrospect

End-of-session config reconciliation plugin for Claude Code.

## Usage

```
/retrospect
```

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
