---
name: project-scanner
description: Scan the target project to build a profile of languages, frameworks, purpose, and existing config
---

# Project Scanner

Gather context about the project being set up. This is a read-only phase — do not modify any files.

## Step 1: Detect existing toolkit config

Check if `.claude/toolkit-config.json` exists in the current project directory. If it does, read it and note:
- This is a **re-run** — record the previous profile and installed plugins
- Note the `installed_at` date for staleness assessment

If it does not exist, this is a **first run**.

## Step 2: Scan project files

Use `glob` and `read` tools to detect project characteristics. Read in parallel where possible. The goal is to build a rich understanding of the project — not to produce a fixed set of labels.

### Build/config files (check existence and read if found)

| File | What it tells you |
|------|-------------------|
| `package.json` | JavaScript/TypeScript project; parse dependencies for frameworks, test runners, UI libraries, build tools |
| `tsconfig.json` | TypeScript in use |
| `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt` | Python project; parse for frameworks and libraries |
| `Cargo.toml` | Rust project; parse for crate dependencies |
| `go.mod` | Go project; parse for module dependencies |
| `Gemfile` | Ruby project |
| `pom.xml`, `build.gradle` | Java/Kotlin project |
| `Dockerfile`, `docker-compose.yml` | Containerised deployment |
| `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` | CI/CD in use |

### Directory structure (check existence)

| Pattern | What it tells you |
|---------|-------------------|
| `tests/`, `test/`, `__tests__/`, `spec/` | Tests exist |
| `src/`, `lib/`, `app/` with source files | Has code |
| `docs/`, substantial `README.md` (>100 lines) | Documentation exists |
| `*.ipynb` files | Jupyter notebooks, likely data science or research |
| `public/`, `static/`, `assets/`, `templates/` | Serves visual content or has a frontend |

### Dependencies of interest

When reading dependency files, note anything relevant — not just from a predefined list. Pay particular attention to:
- **Web/UI frameworks**: React, Vue, Svelte, Angular, Flask templates, Django templates, etc.
- **Data/visualisation**: matplotlib, seaborn, plotly, d3, bokeh, chart.js, recharts, etc.
- **Testing**: pytest, jest, mocha, vitest, etc.
- **Backend frameworks**: Flask, Django, FastAPI, Express, Nest, etc.
- **CLI/terminal**: rich, textual, click, argparse, etc.
- **Anything else notable**: ML frameworks, database ORMs, API clients, etc.

### Existing Claude config

| Target | Location |
|--------|----------|
| CLAUDE.md | `./CLAUDE.md` |
| Settings | `.claude/settings.json` |
| MCP | `.mcp.json` |

Read these to understand what the project already has configured.

## Step 3: Git context (if available)

Run `git rev-parse --is-inside-work-tree` to check if this is a git repo.

If yes:
- `git log --oneline -10` for recent activity context
- `git remote -v` to identify the repository

## Step 4: Synthesise profile

Produce a **project profile** — a natural-language summary of:

1. **Languages**: what programming languages are in use
2. **Frameworks and libraries**: what notable dependencies exist
3. **Project character**: your best understanding of what this project is and does (e.g., "Python web API with Flask and pytest", "React dashboard with D3 charts", "Rust CLI tool", "Jupyter notebook collection for ML research"). Be specific but honest about uncertainty.
4. **Notable characteristics**: anything that stands out — has tests, has CI, produces visual output, has a frontend, is a monorepo, etc.
5. **Is re-run**: whether toolkit config already exists, with previous profile if applicable
6. **Existing Claude config**: summary of what CLAUDE.md, settings, MCP already have

## Output

A structured project profile for Phase 2 (interview). Do not present this to the user yet — Phase 2 handles that.
