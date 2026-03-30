---
name: setup-interview
description: Present scan findings and conduct a short gap-filling interview about the project
---

# Setup Interview

Use the project profile from Phase 1 to conduct a brief, targeted interview. The goal is to confirm what the scan found and fill in gaps — not to interrogate the user.

## Step 1: Present scan findings

Start with a concise summary of what was detected:

> **Project scan results:**
> - Languages: Python, JavaScript
> - Frameworks: Flask, D3
> - Tests: pytest (found `tests/` directory)
> - CI: GitHub Actions
> - Type: looks like a data visualisation web app

Adapt the format to what was actually found. Be specific. If very little was detected (e.g., empty repo, no recognisable files), say so honestly.

Ask: _"Does this look right? Anything I'm missing?"_

Let the user confirm or correct. Incorporate their corrections into the profile.

## Step 2: Gap-filling questions

Ask as many questions as needed to fully understand the project and the user's goals. Keep going until there is no remaining ambiguity — it is better to ask one more question than to guess wrong later. Skip this step entirely only if the project is completely clear-cut.

**Question selection logic** (choose from these, do not ask all):

- If project type is ambiguous: _"What are you building? (web app, CLI tool, library, data pipeline, API, etc.)"_
- If multiple languages but primary is unclear: _"Which language is the primary one for this project?"_
- If the project looks like it could go multiple directions: _"What's the main goal of this project?"_
- If this is a re-run and the profile has changed: _"The project seems to have changed since last setup — has the direction shifted?"_

**Plugin-specific questions**: check the marketplace catalogue for any plugins with an `interview_hint` field whose signals match the project. Include those questions. For example, if a frontend-design plugin has `interview_hint: "What kind of UI are you building?"` and the project has `is_frontend`, ask that question.

**Do not ask**:
- Questions the scan already answered definitively
- Questions about things the user can't know yet (architecture decisions for a new project)

## Step 3: Re-run handling

If this is a re-run (`.claude/toolkit-config.json` exists):

1. Show what was previously installed
2. **Detect new marketplace plugins**: read `.claude-plugin/marketplace.json` from the marketplace root and compare plugin names (excluding `setup`) against the plugin names in `.claude/toolkit-config.json`. Any plugin in the marketplace but not in the config is **new since last setup**.
3. Present options based on whether new plugins exist:

**If new plugins are available:**

```
Previously installed:
  - retrospect, writing-style, dev-workflow, feature-dev

New plugins available since last setup:
  - visual-design — general visual aesthetics for UIs, dashboards, plots
  - code-simplifier — autonomous code refinement agent

Options:
1. Keep current plugins (default)
2. Keep current + evaluate new plugins only
3. Review all recommendations fresh
```

- Option 1 → skip to Phase 5 (installation) to check for updates
- Option 2 → proceed to Phase 3 with `rerun_decision: "evaluate_new"` and the `new_plugins` list. Phase 3 carries forward existing plugins and only evaluates the new ones.
- Option 3 → proceed to Phase 3 normally (full re-evaluation)

**If no new plugins:**

```
Previously installed:
  - retrospect, writing-style, dev-workflow, feature-dev

No new plugins since last setup.

Options:
1. Keep current plugins (default)
2. Review all recommendations fresh
```

- Option 1 → skip to Phase 5
- Option 2 → proceed to Phase 3 normally

## Output

An **augmented project profile** that includes:
1. The original scan data (confirmed or corrected by the user)
2. User-provided answers to gap-filling questions
3. Any plugin-specific configuration hints from the interview
4. Re-run decision: `"keep"`, `"evaluate_new"`, or `"review_fresh"`
5. If `"evaluate_new"`: the `new_plugins` list (names and descriptions from marketplace)
