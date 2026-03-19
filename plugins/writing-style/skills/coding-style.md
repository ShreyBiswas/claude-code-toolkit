---
name: coding-style
description: Shrey's personal coding style and philosophy. Apply whenever writing, reviewing, or refactoring any code — Python or otherwise. Trigger on any code-writing task, feature implementation, bug fix, or code review.
---

# Coding Style Guide

Apply these conventions whenever writing, reviewing, or refactoring code. This is Shrey's personal style — follow it consistently.

---

## Better Comments

Use Better Comments syntax to structure inline documentation. Each prefix serves a distinct purpose:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `# *` | Major sections, conceptual breaks | `# * Interpolation Model` |
| `# ~` | Procedural narration — what the next lines do | `# ~ Determine direction vector` |
| `# ?` | Questions, uncertainty, design decisions | `# ? Is REPAIR implemented correctly?` |
| `# >` | Theory, citations, references, formulas | `# > Formula: (1-α)·w_a + α·w_b` |
| `# !` | Critical warnings, danger zones | `# ! Check the maths on this section` |
| `# //` | Deprecated code, no-longer-relevant notes | `# // Not using this anymore` |
| `PERF:` | Performance-motivated decisions | `# PERF: Store on CPU to save VRAM` |
| `BUGFIX:` | Why a fix exists | `# BUGFIX: Clamp dot product for acos` |
| `HACK:` | Acknowledged workarounds | `# HACK: Deterministic seed based on layer name` |
| `TODO:` | Future improvements | `# TODO: Implement NLERP` |

**Layering pattern**: Use `# *` for top-level section headers, `# ~` for step narration within a section, `# >` for the theoretical justification, and `# ?` for open questions. This creates a narrative flow through algorithmic code:

```python
# * SLERP (Spherical Linear Interpolation)
# > Interpolates along the shortest arc on the hypersphere,
# > preserving weight magnitude. Reference: Shoemake (1985)

# ~ Calculate the angle between weight vectors
dot_product = torch.dot(flat_first, flat_second)
# BUGFIX: Clamp to [-1, 1] — floating point errors can violate acos' domain
dot_product = torch.clamp(dot_product, -1.0, 1.0)
theta = torch.acos(dot_product)

# ? Does this implicitly apply REPAIR? It's an anti-norm-collapse measure.
```

---

## Variable Naming

- **snake_case everywhere**: variables, functions, methods, parameters
- **PascalCase for classes**: `WeightInterpolator`, `DatasetRegistry`, `CheckpointManager`
- **UPPER_SNAKE_CASE for constants**: `PRIMARY_COLORS`, `DEFAULT_COLORMAP_2D`
- **Verbose, full-word names**: `interpolation_alpha` not `alpha`, `vertical_direction_vector` not `v_dir`, `merged_weights` not `merged`
- **Short names only when maths is documented**: `w_a`, `w_b`, `s0`, `s1` are acceptable when the formula is in a `# >` comment directly above
- **Prefixed `d` for derivatives**: `dCost_dWeights`, `dOutput_dActivation` — follows mathematical notation
- **Boolean prefixes**: `use_wandb`, `use_jit`, `is_compiled`, `has_checkpoint`
- **camelCase only for ML class constructor params** inherited from frameworks (e.g. `learningRate`, `batchSize` in legacy code)

---

## Comment Philosophy

- **Explain why and what, not how** — the code shows how
- **Narrate algorithms step-by-step** using `# ~` as if telling a story
- **Document maths inline** with `# >` — include the formula, then implement it
- **Cite academic references** with URLs: `# > Reference: "REPAIR" (Jordan et al., 2022)`
- **Full sentences, proper grammar** — comments are prose, not telegrams
- **Pedagogical tone** for complex algorithms — write as if teaching
- **End-of-line comments** only for quick one-off clarifications

---

## Code Organisation

### Imports
Follow PEP 8 grouping, separated by blank lines:
1. Standard library (`os`, `pathlib`, `typing`)
2. Third-party (`torch`, `numpy`, `tqdm`)
3. Local/project (`from core.utils.logger import logger`)

No `from __future__` imports. Use lazy imports inside functions only when there's a genuine performance reason.

### Type Hints
- **Modern Python 3.10+ syntax**: `str | None`, `list[str]`, `dict[str, Any]`
- **Never** `Optional[str]`, `List[str]`, `Dict[str, Any]`
- **`Literal` for constrained strings**: `InterpolationStrategy = Literal["linear", "slerp"] | str`
- **Type aliases in dedicated `types.py`** files for complex signatures
- **Typed `@dataclass`** for configuration objects with sensible defaults
- **`@classmethod` factory methods**: `from_yaml()`, `from_dict()`

### Docstrings (Google-style)
```python
def interpolate(self, alpha: float) -> dict[str, torch.Tensor]:
    """Merge two models at the given interpolation point.

    Args:
        @ alpha: Interpolation coefficient in [0, 1]. 0 = model_first, 1 = model_second.

    Returns:
        State dict of merged weights.

    Raises:
        ValueError: If alpha is outside [0, 1].
    """
```

Note the `@ param_name` prefix in Args — this is a deliberate convention.

### Structure
- **`if __name__ == "__main__":` guards** on all executable scripts
- **`argparse` at module level**, `args = parser.parse_args()` inside `__main__`, then `main(**vars(args))`
- **Registry pattern** for extensibility: `@classmethod` methods for registration and retrieval
- **`tqdm` progress bars** for any loop that takes more than a second — use `tqdm.auto`, dynamic descriptions
- **Pre-condition validation** with descriptive errors: `raise ValueError(f"Alpha must be in [0, 1], got {alpha}")`

---

## Error Handling

- **Structured logging**: use Loguru with context prefixes: `[ClassName]`, custom levels (`SUCCESS`, `CONFIG`, `STEP`, `RESULT`)
- **Specific exception types**: `except torch.cuda.OutOfMemoryError:` not bare `except:`
- **Log then re-raise** for unexpected errors: `logger.error(f"Failed: {e}")` then `raise`
- **Graceful degradation** for non-fatal issues: log a warning and `continue` rather than crash
- **Descriptive `FileNotFoundError`**: `raise FileNotFoundError(f'{path} does not exist. Please download...')`
- **Atomic file writes**: write to temp file, then `os.replace()` to prevent corruption

---

## Memory and Performance (PyTorch)

- **Explicit `del`** to free large tensors: `del weights_first, weights_second`
- **`torch.cuda.empty_cache()`** after GPU-heavy operations
- **Non-blocking transfers**: `.to(self.device, non_blocking=True)`
- **Layer-wise processing** to avoid loading full models into VRAM
- **`PERF:` comments** on every performance-motivated decision

---

## Spelling and Conventions

- **British English**: `colour`, `normalised`, `serialisable`, `behaviour`, `maths`, `organisation`
- **No emojis** in code or comments
- **No filler comments**: every comment earns its place
