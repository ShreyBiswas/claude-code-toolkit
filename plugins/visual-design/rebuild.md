# Rebuild Instructions: visual-design plugin

These are the instructions to give Claude to recreate this plugin from scratch.

---

## Plugin overview

Create a Claude Code plugin called `visual-design` (v1.0.0, author: Shrey Biswas) with:
- 1 conditionally-active skill: `visual-design` — general visual aesthetics for any visual output

Category: design. Keywords: design, aesthetics, visualisation, UI, UX, plots, dashboards. Relevance: useful when the project produces any visual output. Configurable: true. Interview hint: "Does this project produce any visual output? (UI, plots, charts, dashboards, formatted logs, reports)"

---

## Skill: visual-design

Create a skill that triggers on any task creating, modifying, or reviewing visual artefacts — UI, dashboards, plots, charts, data visualisations, terminal formatting, log output, reports, or any other visual artefact. Trigger proactively even if the user doesn't ask for design help.

Important: this skill covers **general aesthetics and design thinking**. Web-specific advice (accessibility, responsive layout) is handled by dedicated web plugins when installed.

### Scope / domain filtering

The skill should read `.claude/toolkit-config.json` in the current project. If `plugins.visual-design.config.visual_domains` exists, apply only the Core Principles (always) plus matching domain sections:
- `"data_viz"` → Data visualisation section
- `"dashboards"` → Dashboards and admin panels section
- `"terminal"` → Terminal and log output section
- `"reports"` → Reports and documents section

If config is absent or `visual_domains` not set, apply all sections. Skip non-matching sections silently.

### Core Principles (always apply)

**1. Visual hierarchy:**
- Size and weight signal importance
- Contrast draws attention deliberately
- Proximity implies relationship
- Alignment creates order

**2. Colour:**
- Constrained palette: 1 primary, 1-2 accents, neutrals
- Functional colour usage (red=error, green=success, amber=warning) — consistent throughout
- Sufficient contrast
- Sequential/diverging colormaps for data: `viridis`, `plasma`, `coolwarm` — never `jet` or `rainbow`
- Dark themes: off-black backgrounds (`#1a1a2e`, `#0f0f1a`), desaturated/muted accents

**3. Typography:**
- One typeface usually enough, two max
- Consistent type scale (1.25x or 1.333x ratio)
- 45-75 characters per line for body text
- Plot labels: always legible, never overlapping. Use `tight_layout()` or `constrained_layout=True`

**4. Whitespace:**
- Whitespace is a design element, not wasted space
- Consistent margins/padding using a base unit (4px, 8px) and multiples
- Plots: `plt.subplots_adjust()` or `fig.tight_layout()` to prevent label clipping

**5. Simplicity:**
- Remove before adding
- Reduce chartjunk: no unnecessary gridlines, no 3D effects on 2D data, no gradient fills on bar charts
- Default to clean: `sns.set_style("whitegrid")` then remove grid if no value
- One message per visual

### Domain: Data visualisation (matplotlib, seaborn, plotly)

- Right chart type: bar=comparison, line=trends, scatter=relationships, histogram=distribution. No pie charts with >3-4 slices.
- Annotate key points with `ax.annotate()`
- Mandatory axis labels and titles with units
- Legend outside plot area when possible (`bbox_to_anchor`)
- Explicit `figsize` for output context
- Consistent colour across subplots (shared colour mapping)
- Statistical plots: always show uncertainty (error bars, confidence intervals, shaded regions)

### Domain: Dashboards and admin panels

- Information density is a feature — dense but organised
- Consistent card styling (border-radius, shadow, padding)
- Large font KPIs, smaller supporting detail. Right-align numbers in tables.
- Status indicators: colour + icon, not colour alone
- Real-time data: show last-updated timestamp

### Domain: Terminal and log output

- Structured output: `tabulate` or `rich`, not hand-crafted string formatting
- Colour sparingly and semantically: red=errors, yellow=warnings, green=success, dim/grey=secondary. Use `rich` or `colorama`.
- Progress indicators: `tqdm` or `rich.progress`
- Log formatting: timestamp, level, source, message — in that order. Structured logging for machine-readable output.

### Domain: Reports and documents

- Consistent heading hierarchy (never skip levels)
- Tables: distinct header row, zebra striping for long tables, right-align numbers
- Figures always have captions, referenced by number in text

### Anti-patterns to explicitly call out

- Rainbow colormaps on sequential data
- 3D charts for 2D data
- Pie charts with many slices
- Truncated y-axes without marking
- Dual y-axes (use two plots instead)
- Decorative gradients/shadows/textures on data elements
- Inconsistent styling across related visuals

---

## File structure

```
plugins/visual-design/
  .claude-plugin/plugin.json
  skills/visual-design.md
  rebuild.md
```
