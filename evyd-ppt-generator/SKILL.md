---
name: evyd-ppt-generator
description: >
  Generate professional PPTX presentations from a content JSON file.
  Supports three modes: free (no template), template (EVYD Aptos), hybrid (template chrome + free content).
  Use when the user asks to 生成PPT, 做幻灯片, 演示文稿, make slides, create presentation, ppt generator, or EVYD ppt.
---

# EVYD PPT Generator Skill

Generates native-PPTX presentations from a compact content JSON file.
One renderer (`gen_pptx.py`), three modes, eight pluggable styles.

| Mode | Template needed? | Chrome slides | Content slides | Best for |
|------|-----------------|---------------|----------------|----------|
| **`free`** | No | Code-drawn | Code-drawn | Custom visual styles, non-EVYD decks |
| **`template`** | Yes | Template layouts | Template layouts | Strict EVYD brand compliance |
| **`hybrid`** (default) | Yes | Template layouts | Code-drawn with style colors | EVYD chrome + custom content colors |

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
`design-guidelines.md` style mapping is not enough, check if either of these skills
is available. If installed, use them **before** Phase 2 (content.json generation) to
explore palettes, font pairings, and design directions. If not installed, fall back
to `design-guidelines.md` — the core workflow does not depend on them.

| Skill | What it does | How to use with PPT |
|-------|-------------|---------------------|
| **typeui** | 66 pre-built design system specs (glassmorphism, corporate, etc.) | `npx typeui.sh pull <slug>` → read the color/typography tokens → inform style choice |
| **ui-ux-pro-max** | Searchable DB: 67 UI styles, 161 palettes, 57 font pairings | `python3 search.py "<query>" --design-system` → extract recommended colors/style → map to a `styles/*.json` or create a new one |

**Integration pattern:**
```
User: "帮我做个科技感的 AI 产品 PPT"
  │
  ├─ [if ui-ux-pro-max available] → search "AI tech modern" → get palette + style direction
  ├─ [if typeui available]        → pull "futuristic" or "corporate" → read tokens
  └─ [fallback]                   → design-guidelines.md § Color Psychology → recommend cooltech
  │
  ▼
Select/create styles/<name>.json → generate content.json → run gen_pptx.py
```

> **Key rule**: These skills are **optional enhancements**, not dependencies. Never fail
> or ask the user to install them. If unavailable, silently use built-in guidelines.

---

## Architecture

```
content.json  ← Model generates this (~400 tokens per 15 slides)
      │
      └── gen_pptx.py  ← Unified renderer (Python / python-pptx)
            │
            ├── --mode free      → Presentation() from scratch
            ├── --mode template  → Presentation(EVYD Aptos .pptx)
            └── --mode hybrid    → Template chrome + style-driven content
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
5. **Mode** preference (default: `hybrid`)
6. **Style** preference (consult `references/design-guidelines.md` to recommend)

### Phase 2 — Generate content.json

Generate ONLY the JSON file. Do NOT regenerate `gen_pptx.py` or style files.

```json
{
  "meta": {
    "title": "Presentation Title",
    "mode": "hybrid",
    "style": "evyd_blue",
    "template": "/Users/Li.ZHAO/Documents/EVYD PPT Template Aptos.pptx",
    "output": "/Users/Li.ZHAO/Desktop/Output.pptx"
  },
  "slides": [ ... ]
}
```

Save to `/tmp/<project-name>/content.json` or `examples/<project-name>.json`.

### Phase 3 — Run renderer

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"

# Hybrid mode (default) — EVYD chrome + custom style
python3 gen_pptx.py content.json --style cooltech \
  --output "/Users/Li.ZHAO/Desktop/Output.pptx"

# Free mode — no template dependency
python3 gen_pptx.py content.json --mode free --style dark_navy \
  --output "/Users/Li.ZHAO/Desktop/Output.pptx"

# Template mode — strict EVYD branding
python3 gen_pptx.py content.json --mode template --style evyd_blue \
  --output "/Users/Li.ZHAO/Desktop/Output.pptx"
```

CLI flags override `meta` values.

### Phase 4 — Visual QA loop

After generating, always do a visual pass before delivering:

```bash
# Option A: Convert to images for quick inspection
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  --convert-to pdf "/path/to/output.pptx" --outdir /tmp/
pdftoppm -jpeg -r 150 /tmp/output.pdf /tmp/slide
open /tmp/slide-*.jpg

# Option B: Open directly in PowerPoint
open "/path/to/output.pptx"
```

Inspect each slide for text overflow, overlap, wrapping issues. Fix coordinates
in `gen_pptx.py` if needed, then re-run.

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
    "bullet_dot_color": "2CD5C3",
    "number_color": "0076B3",
    "row_border_color": "0076B3",
    "quote_mark_color": "2CD5C3",
    "divider_color": "0076B3",
    "tier_dot_size": 14
  }
}
```

Hex colors without `#` prefix. Style files are pure data — portable to any future renderer.

### Available styles

#### EVYD brand styles (template/hybrid mode)

| Style | Background | Accent | Best for |
|-------|-----------|--------|----------|
| `evyd_blue` | Navy `172E41` | Teal `2CD5C3` | Default — internal / MOH |
| `evyd_white` | White | Blue `0076B3` | Printed handouts |
| `evyd_teal` | Dark navy `0A1E30` | Teal `2CD5C3` | External events, high-contrast |

#### Custom styles (free/hybrid mode)

| Style | Base tone | Primary | Secondary | Best for |
|-------|-----------|---------|-----------|----------|
| `dark_navy` | Deep navy `0B1F3A` | Orange `E87722` | Teal `17A589` | Strategy, research |
| `cooltech` | Space blue `0D1B2A` | Cyan `00C9C8` | Purple `7B61FF` | AI / SaaS / healthtech |
| `morandi` | Slate `5C7080` | Dusty rose `C4857A` | Sage `8FAF9F` | Culture, brand |
| `warm` | Espresso `2C1810` | Coral `E8622A` | Amber `F0A830` | Education, training |
| `monochrome` | Charcoal `111111` | White-grey `EEEEEE` | Mid-grey `888888` | Executive, editorial |

### Add a new style
1. Copy `styles/dark_navy.json` → `styles/<new_name>.json`
2. Edit color values and motifs
3. Use via `--style <new_name>` or `"style": "<new_name>"` in content.json
4. No changes to `gen_pptx.py` needed

---

## Content JSON Schema

### Slide types

All content slides support:
- `"section"`: label in top-left corner (e.g. `"01 — Welcome"`)
- `"background"`: `"blue"` or `"white"` (controls background color)
- `"num"`: slide number override. Auto-calculated if omitted.

Chrome slides: `cover`, `agenda`, `section_divider`, `ending`
Content slides: all others (code-drawn, support style customization)

---

#### `cover`
```json
{ "type": "cover", "title": "...", "subtitle": "...", "tag": "PRESENTATION", "logo": "EVYD · 2025" }
```
`tag` and `logo` are optional (free mode only).

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
{
  "type": "section_divider",
  "num": "01",
  "title": "Section Name",
  "bg_color": [4, 30, 20]
}
```
`bg_color` is `[r, g, b]` — use a dark color variant of the section's theme.

---

#### `bullets_with_panel`
Left side: bullet list + optional ground-rules block.
Right side: large pull-quote panel.
```json
{
  "type": "bullets_with_panel",
  "section": "01 — Welcome",
  "title": "Welcome & Introductions",
  "background": "blue",
  "bullets": ["...", "..."],
  "ground_rules": ["...", "..."],
  "side_panel": { "type": "quote", "text": "Quote goes here." }
}
```

---

#### `two_column_check`
Side-by-side IN SCOPE / OUT OF SCOPE columns with colored headers.
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
2-column grid of numbered cards. Max 6 cards (3 rows × 2).
```json
{
  "type": "cards_grid",
  "section": "...", "title": "...", "background": "blue",
  "cards": [
    { "num": "01", "text": "Card description text" }
  ]
}
```

---

#### `criteria_rows`
Horizontal rows: large number + uppercase label + description text.
```json
{
  "type": "criteria_rows",
  "section": "...", "title": "...", "subtitle": "...", "background": "blue",
  "footnote": "Optional footnote text",
  "criteria": [
    { "num": "01", "label": "CATEGORY LABEL", "text": "Description of this criterion" }
  ]
}
```
Max 4 rows.

---

#### `scope_tiers`
4 horizontal bands with colored left stripe (traffic-light pattern).
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
    {
      "title": "🖐  During",
      "steps": [
        { "bold": "Action label", "normal": "Supporting detail" }
      ]
    }
  ],
  "warning": "⚠️  Warning text shown at the bottom of the slide."
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

---

#### `survey`
Left: numbered steps. Right: QR code placeholder panel.
```json
{
  "type": "survey",
  "section": "...", "title": "...", "subtitle": "...", "background": "white",
  "steps": [
    { "title": "Step Title", "desc": "Step description." }
  ],
  "qr_label": "SURVEY QR CODE",
  "qr_note": "(Link provided on the day)",
  "qr_hint": "Moderator will circulate\nto assist."
}
```

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

Style ideas: `vibrant` (活力橙/玫红/电光蓝), `forest` (森林绿 + 米白), `morandi_light` (all-light pastel).

### Add a new slide type
1. Write a `render_<type>(slide, data, st, num, total)` function in `gen_pptx.py`
2. Add it to `CONTENT_RENDERERS` dict (or `CHROME_RENDERERS` with a free variant)
3. Document the JSON schema here

### Change the template
Update `DEFAULT_TEMPLATE` in `gen_pptx.py`, or pass `--template` on the CLI.
Layout indices (L_COVER, L_AGEND, etc.) may need updating for a different template:
```python
from pptx import Presentation
prs = Presentation('template.pptx')
for i, layout in enumerate(prs.slide_layouts):
    print(i, layout.name)
```

---

## Examples

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"

# Hybrid mode (default) — EVYD chrome + evyd_blue style
python3 gen_pptx.py examples/bruai-focusgroup.json

# Free mode — dark_navy style, no template
python3 gen_pptx.py examples/bruai-focusgroup.json --mode free --style dark_navy \
  --output "/Users/Li.ZHAO/Desktop/BruAI-DarkNavy.pptx"

# Template mode — strict EVYD branding
python3 gen_pptx.py examples/bruai-focusgroup.json --mode template --style evyd_teal \
  --output "/Users/Li.ZHAO/Desktop/BruAI-Teal.pptx"
```

## File Structure

```
evyd-ppt-generator/
├── SKILL.md                          # This file
├── gen_pptx.py                       # Unified renderer (free/template/hybrid)
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
