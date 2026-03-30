---
name: tdd-overlay
description: TDD conventions — run existing tests first for reconnaissance, test-first design, non-shortcuttable tests, verify/iterate loop. Apply during any coding task, bug fix, refactor, or feature implementation.
---

# TDD Overlay

Supplements Anthropic's feature-dev workflow with test-first conventions. Apply these rules during any coding task, feature development, bug fix, refactor, or configuration change.

## Phase 0: Test Baseline

Before making any code changes, run the existing test suite. This is reconnaissance — it tells you what you're working with.

**Why this matters:**
- **Framework discovery** — learn the test runner, config, and conventions without guessing
- **Scope map** — the test suite reveals what the project covers and where the boundaries are
- **Blame boundary** — any new failure after your changes is unambiguously yours

**Steps:**

1. **Detect the test framework** — look for signals: `package.json` scripts, `pytest.ini` / `pyproject.toml` / `setup.cfg`, `Makefile` / `Justfile` test targets, `test/` or `tests/` directories, CI config files
2. **Run the suite** — execute using the project's standard test command. Capture pass/fail/skip counts
3. **Record the baseline** — note total tests, passes, failures, skips, and any flaky or pre-existing failures. This is your comparison point for Phase: Verification
4. **If no test framework is found** — note the absence and move on. Don't invent infrastructure that isn't there

## Phase: Test Design (before implementation)

After requirements and architecture are understood (feature-dev phases 1–4) but **before writing implementation code**:

1. **Design a comprehensive, initially-failing test suite**
   - Unit tests: happy paths, edge cases, boundary conditions, error paths
   - Integration tests: component interactions, end-to-end flows where applicable
   - Match the project's existing test framework and conventions

2. **Non-shortcuttable tests** — every test must satisfy ALL of these:
   - Tests the **observable behavior**, not implementation details
   - No mocking the thing under test
   - No tautological assertions (`assert x == x`, mocking then asserting the mock)
   - No testing private internals — only public API / contract
   - Each test fails for a **distinct, meaningful reason** when the feature is absent
   - Tests would still pass if the implementation were completely rewritten with the same contract

3. **Run the test suite before implementation** — confirm tests fail, and fail for the right reasons (missing function, wrong return value — not import errors or syntax errors)

## Phase: Implementation

- Follow the `coding-style` skill conventions
- Write the **simplest approach** that satisfies requirements and makes tests pass
- Do not gold-plate — if tests pass, the feature is done

## Phase: Verification

After implementation, run **all** of the following (supplements feature-dev phase 6):

1. The full test suite — all tests must pass
2. **Compare against Phase 0 baseline** — no previously-passing test should now fail. New failures that weren't in the baseline are regressions you introduced
3. Project formatters (e.g., `black`, `prettier`, `ruff format`)
4. Type checkers (e.g., `mypy`, `tsc`, `pyright`)
5. Linters (e.g., `ruff check`, `eslint`)
6. Code review agents (e.g., `/simplify`)

All must pass before the feature is considered complete.

## Phase: Iteration Loop

If tests fail after implementation:

- **Fix the implementation, not the tests** — tests encode the spec
- Only modify tests if they contain a genuine spec error (confirm with user first)
- Loop: fix → run tests → fix → run tests
- **After 3 iterations on the same failure**: stop and consult the user — the spec or approach may need rethinking

## Phase: Reporting

When summarizing completed work (supplements feature-dev phase 7), include:

- Total test count, pass/fail breakdown
- Comparison to Phase 0 baseline (new tests added, regressions caught)
- Coverage summary if tooling is available
- Any tests that were modified and why
