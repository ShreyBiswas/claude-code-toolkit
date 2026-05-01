---
name: visual-design
description: MUST READ before creating, modifying, or reviewing any plot, chart, figure, notebook visual, dashboard, UI, terminal output, or report. Non-negotiable reference for visual work. Core goal of every visual is clear, intuitive, pedagogical, aesthetic, attractive, beautiful, informative, and accurate.
paths: "**/*.py,**/*.ipynb,**/*.md,**/*.html,**/*.css,**/*.tsx,**/*.jsx"
---

# Visual Design

Apply these principles whenever producing or reviewing anything visual: user interfaces, dashboards, data visualisations, matplotlib/seaborn plots, terminal output, log formatting, reports, or any other visual artefact.

## The core goal

Every visual you produce — a matplotlib figure, a dashboard tile, a report table, a terminal banner — must be:

- **clear** — the reading order is unambiguous, the message arrives without effort
- **intuitive** — meaning lands before the caption does; encoding matches the data
- **pedagogical** — the visual teaches, not just decorates; a viewer should *learn* something from looking
- **aesthetic, attractive, beautiful** — typography, colour, whitespace, and alignment used with intent, not by default
- **informative** — every ink mark carries meaning; nothing decorative survives
- **accurate** — axes, proportions, and colours honestly represent the data; no misleading scales or truncations

If a visual isn't doing all of these, keep editing. These are not optional stylistic preferences — they are the brief.

This skill covers **general aesthetics and design thinking**. Web-specific advice (accessibility, responsive layout, browser quirks) is handled by dedicated web plugins when installed.

---

## Scope

Read `.claude/toolkit-config.json` in the current project directory. If `plugins.visual-design.config.visual_domains` exists, apply only the Core Principles section (always) plus the domain-specific sections that match the configured domains:

- `"data_viz"` → "Data visualisation" section
- `"dashboards"` → "Dashboards and admin panels" section
- `"terminal"` → "Terminal and log output" section
- `"reports"` → "Reports and documents" section

If the config file is absent or `visual_domains` is not set, apply all sections (backward compatible). Skip non-matching sections silently — do not mention them to the user.

---

## Core Principles

### 1. Visual hierarchy

Every visual artefact needs a clear reading order. The viewer's eye should land on the most important thing first, then flow naturally through the rest.

- **Size and weight** signal importance — the most important element should be the largest or boldest
- **Contrast** draws attention — use it deliberately, not accidentally
- **Proximity** implies relationship — group related elements, separate unrelated ones
- **Alignment** creates order — misalignment creates visual noise even when the viewer can't articulate why

### 2. Colour

- **Start with a constrained palette** — 1 primary colour, 1-2 accent colours, and neutrals. Adding more colours adds more decisions; most of those decisions will be wrong.
- **Use colour functionally**: semantic meaning (red = error, green = success, amber = warning) should be consistent across the entire artefact
- **Ensure sufficient contrast** — not just for accessibility (though that matters), but because low-contrast elements look muddy and unfinished
- **Prefer sequential/diverging colormaps for data**: `viridis`, `plasma`, `coolwarm` over `jet` or `rainbow`. These are perceptually uniform and colourblind-safe.
- **Dark themes**: use off-black backgrounds (`#1a1a2e`, `#0f0f1a`) rather than pure `#000000`. Use desaturated/muted accent colours — saturated neons on dark backgrounds cause eye strain.

### 3. Typography and text

- **One typeface is usually enough.** Two at most (one for headings, one for body). More than two is almost always a mistake.
- **Respect the type scale** — establish a consistent size ratio (e.g., 1.25x or 1.333x) and stick to it. Do not invent new sizes ad hoc.
- **Line length matters** — 45-75 characters per line for body text. Longer lines are hard to track; shorter lines create too many line breaks.
- **Labels on plots and charts**: always legible, never overlapping. Rotate or abbreviate before allowing overlap. Use `tight_layout()` or `constrained_layout=True` in matplotlib.

### 4. Whitespace

- **Whitespace is not wasted space** — it is a design element. Cramped layouts look amateur; generous spacing looks intentional.
- **Consistent margins and padding** — pick a base unit (4px, 8px, etc.) and use multiples of it everywhere
- **Plots**: use `plt.subplots_adjust()` or `fig.tight_layout()` to prevent label clipping. Add padding between subplots.

### 5. Simplicity

- **Remove before adding.** If something can be removed without loss of meaning, remove it.
- **Reduce chartjunk**: no unnecessary gridlines, no decorative 3D effects on bar/line/scatter charts, no gradient fills on bar charts, no decorative borders on plots. (Smooth 2D scientific functions and genuinely 3-axis data are not chartjunk — see Scientific landscapes.)
- **Default to clean**: `sns.set_style("whitegrid")` or `plt.style.use("seaborn-v0_8-whitegrid")` — then remove even the grid if it adds no value
- **One message per visual** — if a chart is trying to say two things, split it into two charts

---

## Domain-Specific Guidance

### Data visualisation (matplotlib, seaborn, plotly)

- **Choose the right chart type**: bar for comparison, line for trends, scatter for relationships, histogram for distribution. Never use pie charts for more than 3-4 slices.
- **Annotate key points** — the viewer should not have to guess what matters. Use `ax.annotate()` for callouts.
- **Axis labels and titles are mandatory** — no unlabelled axes, no titleless plots. Include units.
- **Legend placement**: outside the plot area when possible (`bbox_to_anchor`). Inside only if there's clear empty space.
- **Figure sizing**: set explicit `figsize` for the output context. Print → larger with higher DPI. Screen → match the display width. Do not rely on defaults.
- **Colour consistency across subplots** — if "Group A" is blue in one subplot, it must be blue in all subplots. Use a shared colour mapping.
- **Statistical plots**: always show uncertainty (error bars, confidence intervals, shaded regions). A point estimate without uncertainty is incomplete.
- **Scientific landscapes (loss, energy, response surfaces)** are a special case where 2D heatmaps with contour overlays — and sometimes 3D surface plots — are the *right* tool, not chartjunk. A smooth function over a 2D parameter plane carries topology (basins, ridges, troughs, saddles) that a 1D slice or a bar comparison cannot show. Default to a 2D heatmap with overlaid contours and labelled landmarks (optima, baselines, named points); show iso-magnitude rings or contours so readers can read distance off the figure.
- **3D rendering for genuinely 3-axis data**: when the data has three real variables (e.g. loss over a 2D parameter plane × training step, or any function of three coordinates), 3D rendering is a legitimate option. The choice between *(a) 3D surface plot*, *(b) 2D heatmap × small-multiples on the third axis* (e.g. `01_baselines.ipynb` Figure 1.5: loss landscapes across training steps), and *(c) animated/interactive surface* depends on what the reader needs to compare. Small-multiples are the safer default when the third axis is discrete or low-cardinality and the reader needs to compare panels directly. Reach for true 3D when basin depth, ridge structure, and the third-axis variation all matter simultaneously and a static 2D facet collapses one of those. Use perspective sparingly (low elevation, near-orthographic), label the third axis explicitly, and never use 3D for purely decorative effect on 2D data — that remains chartjunk.

### Dashboards and admin panels

- **Information density is a feature** — dashboards should be dense but not cluttered. The difference is organisation.
- **Cards and panels**: use consistent border-radius, shadow depth, and padding. A dashboard of mismatched cards looks like a ransom note.
- **Numbers should be scannable**: large font for KPIs, smaller for supporting detail. Right-align numbers in tables for easy comparison.
- **Status indicators**: use colour + icon, not colour alone. Colour-only status is inaccessible and ambiguous in poor lighting.
- **Real-time data**: show the last-updated timestamp. Stale data with no indicator is worse than no data.

### Terminal and log output

- **Structured output**: align columns, use consistent separators. `tabulate` or `rich` for Python, not hand-crafted string formatting.
- **Colour in terminals**: use sparingly and semantically. Red for errors, yellow for warnings, green for success, dim/grey for secondary info. Use `rich` or `colorama`, not raw ANSI codes.
- **Progress indicators**: use `tqdm` or `rich.progress` for long operations. Never print a wall of identical lines with no progress context.
- **Log formatting**: timestamp, level, source, message — in that order, consistently. Use structured logging (`structlog`, `python-json-logger`) for machine-readable output.

### Reports and documents

- **Consistent heading hierarchy** — do not skip levels (h1 → h3)
- **Tables**: header row distinct from body. Zebra striping for long tables. Right-align numbers, left-align text.
- **Figures in reports**: always include captions. Reference figures by number in the text.

---

## Anti-Patterns to Avoid

- **Rainbow colour maps on sequential data** — use perceptually uniform colormaps
- **3D charts for 2D data** — 3D adds perspective distortion and occlusion for no benefit. *Distinct from genuinely 3-axis data*: when the data has three real variables, 3D rendering or small-multiples are both legitimate; see Scientific landscapes / 3D rendering under Data visualisation.
- **Pie charts with many slices** — use a horizontal bar chart instead
- **Truncated y-axes without marking** — either start at 0 or clearly mark the break
- **Dual y-axes** — almost always confusing. Use two separate plots instead.
- **Decorative gradients, shadows, or textures** on data elements — these obscure the data
- **Inconsistent styling across related visuals** — if they are part of the same artefact, they should look like they belong together
