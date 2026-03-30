---
name: plugin-matcher
description: Use the project profile to recommend relevant plugins from the marketplace catalogue
---

# Plugin Matcher

Use the project context from Phases 1 and 2 to recommend plugins. This is a judgement call, not a rigid algorithm — use the project profile, the user's stated goals, and each plugin's description and `relevance` hint to decide what is useful.

## Step 1: Read the marketplace catalogue

Read `.claude-plugin/marketplace.json` from the marketplace root (find the closest ancestor directory containing this file). Parse the `plugins` array.

Skip the `setup` plugin itself — it is never recommended for installation by itself.

## Step 1b: Handle evaluate-new-only re-runs

If the augmented profile has `rerun_decision: "evaluate_new"`:

1. **Carry forward** all previously installed plugins from `.claude/toolkit-config.json` — do not re-evaluate them
2. **Filter** the marketplace to only the plugins in the `new_plugins` list
3. Proceed to Step 2, but assess only the new plugins
4. In Step 3, present carried-forward plugins as confirmed and new plugins for evaluation:

```
Keeping your current plugins:
  ✓ retrospect, writing-style, dev-workflow, feature-dev

New plugins to evaluate:
  [x] visual-design — your project produces D3 charts (recommended)
  [ ] code-simplifier — available but not clearly needed

Install recommended new plugins? (yes / customise / skip all)
```

If `rerun_decision` is not `"evaluate_new"`, proceed normally with all plugins.

## Step 2: Assess each plugin

For each plugin, read its `description`, `relevance` (a natural-language hint about when it is useful), and `interview_hint` (if present). Then decide:

- **Recommend and pre-select** if the plugin is clearly useful for this project based on what you know from the scan and interview. Plugins marked as "core" in their relevance should almost always be recommended.
- **Suggest but do not pre-select** if the plugin might be useful but you are not confident — e.g., the project could plausibly produce visual output but nothing in the scan or interview confirmed it.
- **Omit** if the plugin is clearly irrelevant to this project.

Use your judgement. The `relevance` field is a hint, not a rule. A plugin with relevance "useful when building web interfaces" might still be worth suggesting for a project that generates HTML reports, even though it is not a "web interface" project per se.

### Design plugin assessment

The `design` category plugins require extra care — installing all of them wastes significant context on projects that don't need them:

- **visual-design**: recommend if the project produces ANY visual output (UI, plots, terminal formatting, reports). This is the broadest design plugin.
- **frontend-design**: recommend ONLY for projects with a web frontend (React, Vue, Svelte, Angular, or similar). NOT for: CLI tools, data science projects, backend APIs, or projects that only generate HTML reports.
- **web-design-guidelines**: recommend ONLY for interactive web interfaces where accessibility and form behaviour matter. NOT for: static sites, data dashboards without form input, API-only projects.

When in doubt about a design plugin, place it in "Also available" (suggest, do not pre-select) rather than recommending.

## Step 3: Present recommendations

Group plugins into recommended (pre-selected) and suggested (not pre-selected), with a brief reason for each:

```
Recommended plugins for your [project type]:

  [x] retrospect — config reconciliation (useful for any project)
  [x] writing-style — coding/prose style conventions
  [x] dev-workflow — TDD overlay (you have pytest tests)
  [x] feature-dev — feature development workflow

Also available:
  [ ] visual-design — general visual aesthetics (your project may produce plots)
  [ ] frontend-design — frontend UI design (not clearly needed, but available)

Would you like to install these? You can:
1. Install all recommended (default)
2. Customise — I'll go through each one
3. Add or remove specific plugins — just tell me
```

Include a one-line reason for each recommendation so the user can make an informed choice. Adapt the grouping to what makes sense — if everything is clearly relevant, just show one list.

## Step 4: User confirmation

Wait for the user to confirm or customise. Handle responses flexibly:

- **"yes" / "install" / default**: proceed with all pre-selected plugins
- **"customise"**: present each plugin individually for accept/reject
- **"skip X" / "remove X"**: remove specific plugin(s)
- **"add X" / "also install X"**: add a suggested or omitted plugin
- **Any other response**: interpret it reasonably

## Output

A **final plugin install list**: the plugin names the user has approved for installation. Also note which plugins have `configurable: true` — these need Phase 4.
