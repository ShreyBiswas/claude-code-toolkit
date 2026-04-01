# Rebuild Instructions: dev-workflow plugin

These are the instructions to give Claude to recreate this plugin from scratch.

---

## Plugin overview

Create a Claude Code plugin called `dev-workflow` (v1.1.0, author: Shrey Biswas) with:
- 1 always-active skill: `tdd-overlay` — TDD conventions layered on top of Anthropic's feature-dev workflow

Category: development. Keywords: tdd, testing, baseline, workflow. Relevance: useful when the project has or will have tests. Not configurable.

---

## Skill: tdd-overlay

Create a skill that supplements Anthropic's feature-dev workflow with test-first conventions. Apply during any coding task, feature development, bug fix, refactor, or configuration change.

### Phase 0: Test Baseline (before any code changes)

Run the existing test suite as reconnaissance. This matters for three reasons:
1. **Framework discovery** — learn the test runner, config, and conventions without guessing
2. **Scope map** — the test suite reveals what the project covers and where boundaries are
3. **Blame boundary** — any new failure after changes is unambiguously yours

Steps:
1. Detect the test framework — look for: `package.json` scripts, `pytest.ini` / `pyproject.toml` / `setup.cfg`, `Makefile` / `Justfile` test targets, `test/` or `tests/` directories, CI config files
2. Run the suite using the project's standard test command. Capture pass/fail/skip counts.
3. Record the baseline: total tests, passes, failures, skips, flaky/pre-existing failures
4. If no test framework found — note the absence and move on. Don't invent infrastructure.

### Phase: Test Design (after requirements understood, BEFORE implementation)

This runs after feature-dev phases 1-4 (requirements and architecture) but before writing implementation code.

1. Design a comprehensive, initially-failing test suite:
   - Unit tests: happy paths, edge cases, boundary conditions, error paths
   - Integration tests: component interactions, end-to-end flows
   - Match the project's existing test framework and conventions

2. **Non-shortcuttable tests** — every test MUST satisfy ALL of these:
   - Tests observable behaviour, not implementation details
   - No mocking the thing under test
   - No tautological assertions (`assert x == x`, mocking then asserting the mock)
   - No testing private internals — only public API / contract
   - Each test fails for a distinct, meaningful reason when the feature is absent
   - Tests would still pass if implementation were completely rewritten with the same contract

3. Run tests before implementation — confirm they fail for the right reasons (missing function, wrong return value — NOT import errors or syntax errors)

### Phase: Implementation

- Follow the `coding-style` skill conventions
- Write the simplest approach that satisfies requirements and makes tests pass
- Do not gold-plate — if tests pass, the feature is done

### Phase: Verification

After implementation, run ALL of:
1. Full test suite — all tests must pass
2. Compare against Phase 0 baseline — no previously-passing test should now fail (regressions)
3. Project formatters (black, prettier, ruff format)
4. Type checkers (mypy, tsc, pyright)
5. Linters (ruff check, eslint)
6. Code review agents (`/simplify`)

All must pass before feature is complete.

### Phase: Iteration Loop

If tests fail after implementation:
- Fix the implementation, NOT the tests (tests encode the spec)
- Only modify tests if they contain a genuine spec error (confirm with user first)
- Loop: fix → run tests → fix → run tests
- After 3 iterations on the same failure: stop and consult the user

### Phase: Reporting

When summarising completed work, include:
- Total test count, pass/fail breakdown
- Comparison to Phase 0 baseline (new tests added, regressions caught)
- Coverage summary if tooling is available
- Any tests that were modified and why

---

## File structure

```
plugins/dev-workflow/
  .claude-plugin/plugin.json
  skills/tdd-overlay.md
  rebuild.md
```
