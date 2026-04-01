---
name: evyd-ppt-generator
description: >
  Generate professional EVYD-branded PPTX presentations from a content JSON file.
  Uses the EVYD Aptos template for native-editable slides (real shapes + text, not screenshots).
  Use when the user asks to 生成PPT, 做幻灯片, 演示文稿, make slides, create presentation, ppt generator, or EVYD ppt.
---

# EVYD PPT Generator Skill

Generates native-PPTX presentations from a compact content JSON file.
All slides use the EVYD Aptos template layouts — real editable shapes, not images.

## Architecture

```
content.json  ← Model generates this (~400 tokens per 15 slides)
styles.py     ← Pre-defined presets, never regenerated
gen_pptx.py   ← Fixed renderer, never regenerated
    └→ .pptx  ← Fully editable in PowerPoint
```

**Skill location**: `/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator/`

## Workflow

### Phase 1 — Gather requirements (ask user)
1. **Topic / purpose** of the presentation
2. **Audience** (internal team, external client, MOH, etc.)
3. **Key sections** / what needs to be covered
4. **Date, venue, presenter** (for cover slide)
5. **Style** preference (default: `evyd_blue`)

### Phase 2 — Generate content.json

Generate ONLY the JSON file. Do NOT regenerate `gen_pptx.py` or `styles.py`.

Save the JSON to a sensible path, e.g.:
```
/tmp/<project-name>/content.json
```

Or directly to the examples folder for reuse:
```
examples/<project-name>.json
```

### Phase 3 — Run renderer

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"
python3 gen_pptx.py /tmp/<project-name>/content.json \
  --output "/Users/Li.ZHAO/Desktop/<OutputName>.pptx"
```

Override style or template if needed:
```bash
python3 gen_pptx.py content.json --style evyd_white --output output.pptx
```

## Content JSON Schema

### meta (required)
```json
{
  "meta": {
    "title":    "Presentation title (for reference only)",
    "style":    "evyd_blue",
    "template": "/Users/Li.ZHAO/Documents/EVYD PPT Template Aptos.pptx",
    "output":   "/Users/Li.ZHAO/Desktop/Output.pptx"
  }
}
```

### Available styles
| Name | Description |
|------|-------------|
| `evyd_blue` | Navy header + blue backgrounds. Default for internal/MOH presentations. |
| `evyd_white` | White backgrounds throughout. Good for printed handouts. |
| `evyd_teal`  | Dark navy + teal accent. High-contrast for external events. |

### Slide types

All content slides support:
- `"section"`: label in top-left corner (e.g. `"01 — Welcome"`)
- `"background"`: `"blue"` or `"white"` (controls which EVYD layout is used)
- `"num"`: slide number override (e.g. `"04 / 12"`). Auto-calculated if omitted.

---

#### `cover`
```json
{ "type": "cover", "title": "...", "subtitle": "..." }
```

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
`light_color`: `"green"`, `"red"`, `"blue"`, or `"yellow"`.

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
2×2 grid of scenario cards with teal top bar and tag badge.
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
Thank-you slide using EVYD's End_P1 layout (EVYD logo provided by template).
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

## Extending the skill

### Add a new style
Edit `styles.py` — copy an existing entry and change the color values.

### Add a new slide type
1. Write a `render_<type>(slide, data, st, num, total)` function in `gen_pptx.py`
2. Add it to the `RENDERERS` dict
3. If it uses a fixed layout (not blue/white), add the type name to `FIXED_LAYOUTS`
4. Document the JSON schema here in SKILL.md

### Changing the template
Update `DEFAULT_TEMPLATE` in `gen_pptx.py`, or pass `--template` on the CLI.
Layout indices (L_COVER, L_AGEND, etc.) may need updating for a different template —
check layout indices by running:
```python
from pptx import Presentation
prs = Presentation('template.pptx')
for i, layout in enumerate(prs.slide_layouts):
    print(i, layout.name)
```

## Example

```bash
# Regenerate the BruAI Focus Group v3
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"
python3 gen_pptx.py examples/bruai-focusgroup.json
```
