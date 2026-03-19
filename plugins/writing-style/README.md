# writing-style

Coding and prose style conventions for Claude Code.

## Components

### `coding-style` (skill — always active)

Model-invoked skill that applies automatically whenever code is written, reviewed, or refactored. Covers Better Comments syntax, verbose snake_case naming, Google-style docstrings with `@ param` prefix, modern type hints, and British English spelling.

### `/prose-style` (command — on demand)

User-invoked command for writing non-code text. Covers sentence structure, contextual tone, Obsidian-style callout formatting, intuition-first explanations, claim-evidence-consequence argumentation, and voice characteristics.

## Usage

```
# Coding style is always active — just write code

# Prose style on demand:
/prose-style
```
