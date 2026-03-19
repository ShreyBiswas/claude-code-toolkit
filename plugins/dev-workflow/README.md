# dev-workflow

Personal TDD overlay that supplements Anthropic's `feature-dev` plugin with test-first conventions.

## What it does

The `tdd-overlay` skill activates automatically during feature development and enforces:

- **Test-first design** — write a comprehensive, failing test suite before implementation
- **Non-shortcuttable tests** — no mocking the thing under test, no tautological assertions, no testing implementation details
- **Verification** — run formatters, type checkers, linters, and review agents alongside tests
- **Iteration loop** — fix implementation not tests; consult user after 3 failed iterations
- **Reporting** — include test counts and pass/fail breakdown in summaries

## Relationship to feature-dev

This plugin layers on top of Anthropic's `feature-dev` workflow phases:

- Inserts test design between phases 4 (architecture) and 5 (implementation)
- Supplements phase 6 (review) with automated verification tooling
- Supplements phase 7 (reporting) with test result summaries

Install `feature-dev` separately: `claude plugin install feature-dev@claude-plugins-official --scope user`

## Testing

```bash
claude --plugin-dir ./plugins/dev-workflow
```
