# Rebuild Instructions: writing-style plugin

These are the instructions to give Claude to recreate this plugin from scratch.

---

## Plugin overview

Create a Claude Code plugin called `writing-style` (v1.0.0, author: Shrey Biswas) with:
- 1 always-active skill: `coding-style` — personal coding style conventions
- 1 slash command: `/prose-style` — prose writing guide, invoked on demand

Category: style. Keywords: coding-style, prose, comments, naming. Relevance: core (useful for any project). Not configurable.

---

## Skill: coding-style

Create an always-active skill that applies Shrey's personal coding style whenever writing, reviewing, or refactoring code. It should trigger on any code-writing task, feature implementation, bug fix, or code review.

### Content to capture

**Better Comments** — a structured inline documentation system using 8 prefixes and 3 special tags:

| Prefix | Purpose |
|--------|---------|
| `# *` | Major sections, conceptual breaks |
| `# ~` | Procedural narration — what the next lines do |
| `# ?` | Questions, uncertainty, design decisions |
| `# >` | Theory, citations, references, formulas |
| `# !` | Critical warnings, danger zones |
| `# //` | Deprecated code, no-longer-relevant notes |
| `PERF:` | Performance-motivated decisions |
| `BUGFIX:` | Why a fix exists |
| `HACK:` | Acknowledged workarounds |
| `TODO:` | Future improvements |

Include a **layering pattern** explanation showing how `# *` → `# ~` → `# >` → `# ?` creates narrative flow through algorithmic code. Provide a concrete SLERP interpolation example demonstrating the layered pattern in practice.

**Variable naming conventions:**
- snake_case everywhere (variables, functions, methods, params)
- PascalCase for classes
- UPPER_SNAKE_CASE for constants
- Verbose full-word names (`interpolation_alpha` not `alpha`)
- Short names only when maths is documented in a `# >` comment directly above
- Prefixed `d` for derivatives: `dCost_dWeights`
- Boolean prefixes: `use_`, `is_`, `has_`
- camelCase only for ML class constructor params inherited from frameworks

**Comment philosophy:**
- Explain why and what, not how
- Narrate algorithms step-by-step with `# ~`
- Document maths inline with `# >`
- Cite academic references with URLs
- Full sentences, proper grammar
- Pedagogical tone for complex algorithms
- End-of-line comments only for quick clarifications

**Code organisation:**
- PEP 8 import grouping (stdlib → third-party → local), no `from __future__`
- Modern Python 3.10+ type hints: `str | None`, `list[str]` — never `Optional`, `List`, `Dict`
- `Literal` for constrained strings, type aliases in `types.py`
- Typed `@dataclass` with `@classmethod` factory methods
- Google-style docstrings with `@ param_name` prefix in Args
- `if __name__ == "__main__"` guards, argparse at module level
- Registry pattern for extensibility
- `tqdm` progress bars for anything taking >1 second
- Pre-condition validation with descriptive errors

**Error handling:**
- Structured logging with Loguru, context prefixes, custom levels
- Specific exception types (never bare `except:`)
- Log then re-raise for unexpected errors
- Graceful degradation for non-fatal issues
- Atomic file writes (temp file → `os.replace()`)

**Memory and performance (PyTorch):**
- Explicit `del` for large tensors
- `torch.cuda.empty_cache()` after GPU-heavy ops
- Non-blocking transfers
- Layer-wise processing to avoid full VRAM load
- `PERF:` comments on every performance decision

**Spelling:** British English throughout (`colour`, `normalised`, `behaviour`, `maths`, `organisation`). No emojis.

---

## Command: /prose-style

Create a slash command for on-demand prose writing guidance. Apply when drafting essays, documentation, explanations, speeches, or any non-code text.

### Content to capture

**Sentence structure:**
- Rhythmic variation: alternate short punchy + longer building sentences
- Single-clause sentences for impact
- Active voice by default
- Tricolon (rule of three) for rhetorical lists
- Anaphora: repeat sentence openings deliberately for force
- Spaced hyphens ` - ` for parenthetical asides (not em-dashes)
- Semicolons for tight clause connections
- Start sentences with "But," "And," "So," freely

**Tone** — contextual, matched to purpose:
- Technical/pedagogical: thinking-aloud, collaborative "we", curious
- Persuasive/rhetorical: emotionally charged, rhythmic, crescendo
- Explanatory/conversational: direct, enthusiastic, unfiltered
- Formal/academic: measured but not dry, still uses contractions
- Always emotionally honest, never hedge excessively, never impersonal register

**Formatting:**
- Obsidian-style callout boxes: `[!definition]`, `[!important]`, `[!warning]`, `[!danger]`, `[!example]`, `[!info]`, `[!resources]`
- **Bold** for formally introduced terms, *italics* for stress/emphasis
- `<mark class="hltr-yellow">` for key insights, `<mark class="hltr-purple">` for new terminology
- 2-3 header levels, descriptive headers
- Numbered lists for sequential, bullets for non-ordered
- Internal links with `[[Topic Name]]`

**Explaining concepts** — intuition-first, formalism-second pattern:
1. Motivation (why care?)
2. Intuition (analogy, mental model)
3. Formal definition (precise statement)
4. Worked example (concrete instance)

Plus: rephrasing complex ideas, dual-view explanations, collaborative "we", progressive complexity.

**Argumentation:**
- Persuasive: Claim → Evidence → Gut-punch pattern
- Statistical precision (specific, sourced numbers)
- Paradox openings for longer pieces
- Technical: build inductively, rhetorical questions as pivots
- Rebuttals: opponent's claim → immediate punchy counter in `[!danger]` blocks

**Voice characteristics:**
- Contrasts as thinking tools
- Self-aware reflexivity
- Genuine enthusiasm ("immensely fascinating", "incredibly powerful")
- Intellectual humour (dry, self-deprecating, darkly ironic)
- Repetition for rhetorical force
- Direct address to the reader
- Extended metaphors sustained across sentences

**Vocabulary:** sophisticated but unpretentious, active verbs, concrete over abstract, contractions freely, British English, favourite connectors ("So,", "Note that", "Crucially,"), natural intensifiers. No emojis.

---

## File structure

```
plugins/writing-style/
  .claude-plugin/plugin.json
  skills/coding-style.md
  commands/prose-style.md
  rebuild.md
```

The plugin.json should list name, version, description, and author. The skill and command files use YAML frontmatter with `name` and `description` fields.
