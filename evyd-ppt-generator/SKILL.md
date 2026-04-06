---
name: evyd-ppt-generator
description: >
  Generate professional PPTX presentations from a content JSON file.
  All slides are code-drawn (free mode) — no external template dependency.
  Use when the user asks to 生成PPT, 做幻灯片, 演示文稿, make slides, create presentation, ppt generator, or EVYD ppt.
---

# EVYD PPT Generator Skill

Generates native-PPTX presentations from a compact content JSON file.
One renderer (`gen_pptx.py`), 14 slide types, eight pluggable styles.
All slides are drawn from code — no template file required.

**Skill location**: `/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator/`

### Design reference (MUST read before generating content.json)

**`references/design-guidelines.md`** — Typography hierarchy, layout selection rules,
color psychology, slide sequencing, content writing rules, and style vocabulary.
Always consult this file when deciding:
- Which slide type to use for what content
- Which style to recommend for the audience
- How many items per slide (max limits)
- Whether to use `"blue"` or `"white"` background
- How to write concise titles and bullets

### Optional upstream skills (style brainstorming)

When the user's style direction is vague ("做个好看的"、"科技感一点") and the built-in
`design-guidelines.md` style mapping is not enough, check if the **ui-ux-pro-max** skill
is available. If installed, use it **before** Phase 2 (content.json generation) to
explore palettes, font pairings, and design directions. If not installed, fall back
to `design-guidelines.md` — the core workflow does not depend on it.

> **Key rule**: This skill is an **optional enhancement**, not a dependency. Never fail
> or ask the user to install it. If unavailable, silently use built-in guidelines.

---

## Architecture

```
content.json  ← Model generates this (~400 tokens per 15 slides)
      │
      └── gen_pptx.py  ← Free-mode renderer (Python / python-pptx)
            │
            └── styles/<name>.json  ← Pluggable color/font/motif config
```

Three-layer separation:
1. **Content** — `content.json` (what to say)
2. **Layout** — slide-type renderers in `gen_pptx.py` (where to put it)
3. **Style** — `styles/*.json` (how it looks) — renderer-independent, portable

---

## Workflow

### Phase 1 — Gather requirements (ask user)
1. **Topic / purpose** of the presentation
2. **Audience** (internal team, external client, MOH, etc.)
3. **Key sections** / what needs to be covered
4. **Date, venue, presenter** (for cover slide)
5. **Style** preference (consult `references/design-guidelines.md` to recommend)

### Phase 2 — Generate content.json

Generate ONLY the JSON file. Do NOT regenerate `gen_pptx.py` or style files.

**You (Claude) decide the slide type for each slide** based on the content.
Use the layout selector guide below — the user does not need to specify types.

```json
{
  "meta": {
    "style": "evyd_blue",
    "output": "/Users/Li.ZHAO/Desktop/Output.pptx"
  },
  "slides": [ ... ]
}
```

Save to `/tmp/<project-name>/content.json` or `examples/<project-name>.json`.

### Phase 3 — Run renderer

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"

python3 gen_pptx.py content.json --style evyd_blue \
  --output "/Users/Li.ZHAO/Desktop/Output.pptx"
```

`--style` and `--output` override `meta` values. The renderer runs `validate_and_fix()`
automatically before saving — font sizes are shrunk up to 4pt if overflow is detected.

### Phase 4 — QA & verification loop

After generating, always do a full pass before delivering.

#### Content QA (text extraction)
```bash
# Extract all text — check for missing content, typos, wrong slide order
python -m markitdown output.pptx

# Detect leftover placeholders or dummy text
python -m markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert"
```

#### Visual QA (convert to images)
```bash
# Convert to images for per-slide inspection
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  --convert-to pdf "/path/to/output.pptx" --outdir /tmp/
pdftoppm -jpeg -r 150 /tmp/output.pdf /tmp/slide
open /tmp/slide-*.jpg
```

#### QA checklist

Assume there are problems — your job is to find them:

- Overlapping elements (text through shapes, lines through words)
- Text overflow or cut off at edges / box boundaries
- Elements too close (< 0.3" gaps) or uneven spacing
- Insufficient margin from slide edges (< 0.5")
- Low-contrast text (light gray on cream, dark icons on dark backgrounds)
- Leftover placeholder content or template dummy text
- Columns or similar elements not aligned consistently
- Text boxes too narrow causing excessive wrapping

Fix coordinates in `gen_pptx.py` or adjust content.json, then re-run.
Repeat until a full pass finds no new issues.

#### File hygiene

All intermediate files (QA images, PDF conversions, temp JSON) go to `/tmp/`.
Only the final `.pptx` goes to the user's output directory.

---

## Layout Selector Guide

**Claude auto-selects the slide type** based on content. Use this table:

| Content characteristics | → Use type |
|---|---|
| Topic title / opening of entire deck | `cover` |
| List of agenda items with times | `agenda` |
| Transition between major sections | `section_divider` |
| Final slide, thank-you, call-to-action | `ending` |
| **Bullets + pull-quote or ground rules on the side** | `bullets_with_panel` |
| **Two opposing lists (✓ vs ✗, scope in/out)** | `two_column_check` |
| **6–8 parallel numbered items** | `cards_grid` |
| **2–6 rows with number + label + description** | `criteria_rows` |
| **Classification levels / tiers with color coding** | `scope_tiers` |
| **Two topic panels with bullet items each** | `two_panel` |
| **Numbered step cards in two columns** | `two_column_steps` |
| **2–4 scenario cases with tags** | `scenario_cards` |
| **Survey/activity with QR code** | `survey` |
| **2–4 key statistics / big numbers** | `stat_highlight` |
| **Timeline or roadmap with phases** | `timeline` |
| **One impactful quote or statement** | `quote_full` |
| **Single key message / strategic focus** | `center_focus` |
| **Multi-column structured comparison** | `comparison_table` |

**Background rhythm**: alternate `"blue"` and `"white"` slides. Start and end with blue.
Use `"white"` for data-heavy slides (`comparison_table`, `two_column_check`).

---

## Style System (styles/*.json)

All styles use **Aptos** font. Each JSON file defines colors and motifs:

```json
{
  "name": "my_style",
  "description": "Short description.",
  "font": "Aptos",

  "accent":     "2CD5C3",
  "accent2":    "0076B3",
  "navy":       "172E41",
  "white":      "FFFFFF",
  "card":       "003B6B",
  "card_side":  "004F7D",
  "card_num":   "3388BB",
  "text_dim":   "BBCCDD",
  "text_num":   "CCE8F5",
  "card_white": "EFF7FD",
  "text_gray":  "446688",
  "text_dark":  "172E41",
  "line_gray":  "225588",
  "bg_content": "0A3A5C",

  "motifs": {
    "left_bar_colors": ["2CD5C3", "0076B3"],
    "header_tag_color": "2CD5C3",
    "number_color": "0076B3",
    "divider_color": "0076B3"
  }
}
```

Hex colors without `#` prefix. Style files are pure data — portable.

### Available styles

| Style | Base tone | Accent | Best for |
|-------|-----------|--------|----------|
| `evyd_blue` | Navy `172E41` | Teal `2CD5C3` | Default — internal / MOH |
| `evyd_white` | White | Blue `0076B3` | Printed handouts |
| `evyd_teal` | Dark navy `0A1E30` | Teal `2CD5C3` | External events, high-contrast |
| `dark_navy` | Deep navy `0B1F3A` | Orange `E87722` | Strategy, research |
| `cooltech` | Space blue `0D1B2A` | Cyan `00C9C8` | AI / SaaS / healthtech |
| `morandi` | Slate `5C7080` | Dusty rose `C4857A` | Culture, brand |
| `warm` | Espresso `2C1810` | Coral `E8622A` | Education, training |
| `monochrome` | Charcoal `111111` | Grey `EEEEEE` | Executive, editorial |

---

## Content JSON Schema

### Common fields (all content slides)

- `"section"`: label in top-left corner (e.g. `"01 — Welcome"`)
- `"background"`: `"blue"` or `"white"` (controls background color)
- `"num"`: slide number override — auto-calculated if omitted

Chrome slides: `cover`, `agenda`, `section_divider`, `ending`
Content slides: all others (code-drawn, Aptos font, style-driven)

---

#### `cover`
```json
{ "type": "cover", "title": "...", "subtitle": "...", "tag": "PRESENTATION", "logo": "EVYD · 2025" }
```
`tag` and `logo` are optional.

---

#### `agenda`
```json
{
  "type": "agenda",
  "items": [
    { "num": "1", "title": "Introduction", "time": "10:00–10:10  ·  10 min" }
  ]
}
```
Max 5 items.

---

#### `section_divider`
```json
{ "type": "section_divider", "num": "01", "title": "Section Name", "bg_color": [4, 30, 20] }
```
`bg_color` is `[r, g, b]` — use a dark color variant of the section theme.

---

#### `bullets_with_panel`
Left side: bullet list + optional ground-rules block. Right side: large pull-quote panel.
```json
{
  "type": "bullets_with_panel",
  "section": "01 — Welcome", "title": "...", "background": "blue",
  "bullets": ["...", "..."],
  "ground_rules": ["...", "..."],
  "side_panel": { "type": "quote", "text": "Quote text." }
}
```

---

#### `two_column_check`
Side-by-side columns with colored headers and markers.
```json
{
  "type": "two_column_check",
  "section": "...", "title": "...", "subtitle": "...", "background": "white",
  "left":  { "title": "✅  IN SCOPE",     "color": [39,174,96],  "light_color": "green", "marker": "✓", "items": ["..."] },
  "right": { "title": "🚫  OUT OF SCOPE", "color": [231,76,60],  "light_color": "red",   "marker": "✗", "items": ["..."] }
}
```

---

#### `cards_grid`
2-column grid of numbered cards. Supports 2–8 cards; row height auto-adjusts.
```json
{
  "type": "cards_grid",
  "section": "...", "title": "...", "background": "blue",
  "cards": [{ "num": "01", "text": "Card description" }]
}
```

---

#### `criteria_rows`
Horizontal rows: large number + uppercase label + description. Supports 2–6 rows; height auto-adjusts.
```json
{
  "type": "criteria_rows",
  "section": "...", "title": "...", "subtitle": "...", "background": "blue",
  "footnote": "Optional footnote",
  "criteria": [{ "num": "01", "label": "CATEGORY LABEL", "text": "Description text" }]
}
```

---

#### `scope_tiers`
Horizontal bands with colored left stripe. Supports 2–5 tiers; height auto-adjusts.
```json
{
  "type": "scope_tiers",
  "section": "...", "title": "...", "subtitle": "...", "background": "blue",
  "tiers": [
    { "color": [39,174,96], "icon": "🟢", "label": "IN SCOPE — ...", "desc": "...", "example": "e.g. ..." }
  ]
}
```

---

#### `two_panel`
Two side-by-side panels with header bar and bullet items.
```json
{
  "type": "two_panel",
  "section": "...", "title": "...", "background": "white",
  "panels": [
    { "color": [224,96,32], "icon": "⚠️", "title": "PANEL TITLE", "items": ["...", "..."] }
  ]
}
```

---

#### `two_column_steps`
Two columns of numbered step cards. Optional red warning bar at bottom.
```json
{
  "type": "two_column_steps",
  "section": "...", "title": "...", "background": "blue",
  "columns": [
    { "title": "🖐  During", "steps": [{ "bold": "Action label", "normal": "Supporting detail" }] }
  ],
  "warning": "⚠️  Warning text shown at the bottom."
}
```
Max 4 steps per column, 2 columns.

---

#### `scenario_cards`
2×2 grid of scenario cards with accent top bar and tag badge.
```json
{
  "type": "scenario_cards",
  "section": "...", "title": "...", "subtitle": "...", "background": "blue",
  "scenarios": [
    { "num": "01", "icon": "💊", "title": "Scenario Title", "desc": "Task description.", "tag": "Tag Label" }
  ]
}
```
Max 4 scenarios.

---

#### `survey`
Left: numbered steps. Right: QR code placeholder panel.
```json
{
  "type": "survey",
  "section": "...", "title": "...", "subtitle": "...", "background": "white",
  "steps": [{ "title": "Step Title", "desc": "Step description." }],
  "qr_label": "SURVEY QR CODE",
  "qr_note": "(Link provided on the day)",
  "qr_hint": "Moderator will circulate\nto assist."
}
```

---

#### `stat_highlight` *(new)*
2–4 large statistics displayed as bold data cards in a horizontal row.
```json
{
  "type": "stat_highlight",
  "section": "01 — Results", "title": "Key Metrics", "background": "blue",
  "stats": [
    { "value": "87%", "label": "Adoption Rate", "desc": "Across all departments" },
    { "value": "2.3x", "label": "Productivity", "desc": "vs. 2023 baseline" }
  ]
}
```
Card width auto-adjusts to number of stats. Value at 60pt bold in accent color.

---

#### `timeline` *(new)*
Horizontal timeline with phase labels above the line and titles/descriptions below.
```json
{
  "type": "timeline",
  "section": "02 — Roadmap", "title": "Implementation Timeline", "background": "blue",
  "items": [
    { "phase": "Q1 2025", "title": "Discovery", "desc": "Stakeholder interviews" },
    { "phase": "Q2 2025", "title": "Design", "desc": "Architecture & prototypes" },
    { "phase": "Q3 2025", "title": "Build", "desc": "Core development & testing" },
    { "phase": "Q4 2025", "title": "Launch", "desc": "Deployment & training" }
  ]
}
```
Supports 3–5 items. Nodes equally spaced across 18".

---

#### `quote_full` *(new)*
Full-slide featured quote with large decorative treatment. For impactful statements.
```json
{
  "type": "quote_full",
  "section": "03 — Vision", "background": "blue",
  "quote": "AI is not replacing doctors — it is giving them superpowers.",
  "attribution": "— Dr. Sarah Chen, Chief Medical Officer"
}
```
Large decorative opening quotation mark (120pt), quote at 28pt italic, attribution below.

---

#### `center_focus` *(new)*
Center-dominant layout for strategic focus, section openers, or key conclusions.
```json
{
  "type": "center_focus",
  "section": "04 — Strategy", "background": "blue",
  "title": "2025 Strategic Focus",
  "message": "Patient-centred intelligent healthcare ecosystem",
  "context": "Connecting clinicians, patients, and data in one unified platform"
}
```
`title` appears as small-caps label above `message`. `message` at 36pt bold, centered.
Decorative large circle in background. `context` as smaller line below divider.

---

#### `comparison_table` *(new)*
Multi-column structured comparison with label column and data columns.
```json
{
  "type": "comparison_table",
  "section": "05 — Comparison", "title": "Feature Comparison", "background": "white",
  "columns": ["Traditional", "AI-Powered", "Our Solution"],
  "rows": [
    { "label": "Processing Speed", "values": ["4 hours", "30 min", "< 5 min"] },
    { "label": "Accuracy",         "values": ["82%",    "91%",    "97%"] },
    { "label": "Cost",             "values": ["High",   "Medium", "Low"] }
  ]
}
```
Header row in accent color. Alternating row backgrounds. Row height auto-adjusts.
Supports 2–4 columns, 2–8 rows.

---

#### `ending`
Thank-you / call-to-action slide.
```json
{
  "type": "ending",
  "title": "Thank You",
  "subtitle": "Supporting line",
  "actions": [
    { "icon": "🔓", "title": "Action Title", "desc": "Action description." }
  ]
}
```

---

## Extending the Skill

### Add a new style
1. Copy `styles/dark_navy.json` → `styles/<new_name>.json`
2. Edit color values and motifs
3. No code changes needed

### Add a new slide type
1. Write a `render_<type>(slide, data, st, num, total)` function in `gen_pptx.py`
2. Add it to `CONTENT_RENDERERS` dict
3. Document the JSON schema here

---

## Examples

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"

# Default run (evyd_blue style)
python3 gen_pptx.py examples/bruai-focusgroup.json

# Override style and output
python3 gen_pptx.py content.json --style dark_navy \
  --output "/Users/Li.ZHAO/Desktop/Output.pptx"
```

## File Structure

```
evyd-ppt-generator/
├── SKILL.md                          # This file
├── gen_pptx.py                       # Free-mode renderer (14 slide types)
├── references/
│   └── design-guidelines.md          # Design rules for content.json generation
├── styles/
│   ├── evyd_blue.json                # EVYD brand — default
│   ├── evyd_white.json               # EVYD brand — print
│   ├── evyd_teal.json                # EVYD brand — high contrast
│   ├── dark_navy.json                # Navy + orange + teal
│   ├── cooltech.json                 # Space blue + cyan + purple
│   ├── morandi.json                  # Muted pastels
│   ├── warm.json                     # Espresso + coral + amber
│   └── monochrome.json               # Black/white/grey
└── examples/
    ├── bruai-focusgroup.json
    ├── evyd-1person-fullstack.json
    └── evyd-skills-fullstack.json
```
