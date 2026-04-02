---
name: evyd-ppt-generator
description: >
  Generate professional EVYD-branded PPTX presentations from a content JSON file.
  Uses the EVYD Aptos template for native-editable slides (real shapes + text, not screenshots).
  Use when the user asks to 生成PPT, 做幻灯片, 演示文稿, make slides, create presentation, ppt generator, or EVYD ppt.
---

# EVYD PPT Generator Skill

Generates native-PPTX presentations from a compact content JSON file.
Two rendering modes are available:

| Mode | Renderer | Style source | When to use |
|------|----------|-------------|-------------|
| **Template mode** (default) | `gen_pptx.py` | EVYD Aptos `.pptx` template | EVYD-branded deliverables, MOH submissions |
| **Free-design mode** | `gen_free.js` | `styles/<name>.js` (code-driven) | Custom visual styles, non-EVYD decks |

**Skill location**: `/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator/`

---

## Architecture

```
content.json  ← Model generates this (~400 tokens per 15 slides)
               │
               ├── gen_pptx.py   ← Template-mode renderer (Python / python-pptx)
               │     ├── styles.py          ← EVYD color presets
               │     └── EVYD Aptos .pptx   ← Source template
               │
               └── gen_free.js   ← Free-design renderer (Node / PptxGenJS)
                     └── styles/dark_navy.js   ← Pluggable style config
                         styles/cyberpunk.js   ← (add more here)
                         styles/red_line.js    …
```

---

## Template Mode Workflow (gen_pptx.py)

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

---

## Free-Design Mode Workflow (gen_free.js)

Use this mode when:
- The user wants a custom visual style (not EVYD-branded)
- You want no dependency on a `.pptx` template file
- You want the design fully code-driven and version-controllable

### Prerequisites

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"
npm install pptxgenjs   # one-time; installs to local node_modules/
```

### Phase 1 — Choose (or add) a style

Available styles in `styles/`:
| Name | Description |
|------|-------------|
| `dark_navy` | Deep navy + teal + orange. Premium look for strategy / research decks. |

To add a new style: copy `styles/dark_navy.js`, rename it, and edit the `colors`, `fonts`, and `motifs` blocks. No other files need changing.

### Phase 2 — Author content.json

Same JSON structure as template mode (same slide types).
Optionally set `meta.free_style` to pre-select a style:

```json
{
  "meta": {
    "title": "My Deck",
    "free_style": "dark_navy",
    "output": "/Users/Li.ZHAO/Desktop/MyDeck.pptx"
  },
  "slides": [ ... ]
}
```

### Phase 3 — Run renderer

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"
node gen_free.js examples/my-deck.json \
  [--style dark_navy] \
  [--output "/Users/Li.ZHAO/Desktop/MyDeck.pptx"]
```

CLI flags override `meta` values when both are present.

### Phase 4 — Visual QA loop

After generating, always do a visual pass before delivering:

```bash
# 1. Convert to images (run on user's Mac via Desktop Commander)
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  --convert-to pdf "/path/to/output.pptx" --outdir /tmp/

pdftoppm -jpeg -r 150 /tmp/output.pdf /tmp/slide

# 2. Open all slide images
open /tmp/slide-*.jpg

# 3. Inspect each slide for: text overflow, overlap, wrapping issues
# 4. Fix in gen_free.js (adjust x/y/w/h, font size, or rowH constants)
# 5. Re-run node gen_free.js and repeat until clean
```

Alternatively, open the `.pptx` directly in PowerPoint to inspect slide-by-slide.

---

## Style System (styles/*.js)

Each style file exports a single config object:

```javascript
module.exports = {
  name: "my_style",
  description: "Short description shown in CLI error messages.",

  colors: {
    bg_primary:    "0B1F3A",  // cover / ending background
    bg_content:    "1A5276",  // main content background
    accent_orange: "E87722",  // primary accent
    accent_teal:   "17A589",  // secondary accent
    // ... (copy dark_navy.js for the full list of required keys)
  },

  fonts: {
    heading: "Georgia",    // serif — titles, large numbers
    body:    "Calibri",    // sans — body text, labels, bullets
  },

  motifs: {
    left_bar_colors:  ["E87722", "17A589"],  // cover decorative bar
    header_tag_color: "E87722",              // section tag text
    bullet_dot_color: "E87722",
    number_color:     "17A589",
    row_border_color: "17A589",
    quote_mark_color: "17A589",
    divider_color:    "17A589",
    tier_dot_size:    14,
  },
};
```

> ⚠️ **No `#` prefix on hex colors** — PptxGenJS requires bare hex strings (e.g. `"E87722"` not `"#E87722"`). Using `#` causes file corruption.

---

## Content JSON Schema

### meta (required)
```json
{
  "meta": {
    "title":      "Presentation title (for reference only)",
    "style":      "evyd_blue",
    "free_style": "dark_navy",
    "template":   "/Users/Li.ZHAO/Documents/EVYD PPT Template Aptos.pptx",
    "output":     "/Users/Li.ZHAO/Desktop/Output.pptx"
  }
}
```

`style` → used by `gen_pptx.py` (template mode)
`free_style` → used by `gen_free.js` (free-design mode)

### Available template-mode styles
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

### Add a new free-design style
1. Copy `styles/dark_navy.js` → `styles/<new_name>.js`
2. Edit `colors`, `fonts`, `motifs` blocks
3. Set `"free_style": "<new_name>"` in your `content.json`, or pass `--style <new_name>` at CLI
4. No changes to `gen_free.js` needed

Style ideas: `cyberpunk` (neon green on black), `red_line` (bold red + white), `minimal` (grey + mono), `sunrise` (warm orange + cream).

### Add a new slide type (free-design mode)
1. Write a renderer function in `gen_free.js`:
   ```javascript
   function renderMyType(s, d, n, total) {
     // s = PptxGenJS slide, d = slide data from JSON, n = slide index, total = total slides
   }
   ```
2. Add to `RENDERERS` dict: `my_type: renderMyType`
3. Document the JSON schema here in SKILL.md

### Add a new slide type (template mode)
1. Write a `render_<type>(slide, data, st, num, total)` function in `gen_pptx.py`
2. Add it to the `RENDERERS` dict
3. If it uses a fixed layout (not blue/white), add the type name to `FIXED_LAYOUTS`
4. Document the JSON schema here in SKILL.md

### Change the template (template mode)
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
# Template mode — BruAI Focus Group
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"
python3 gen_pptx.py examples/bruai-focusgroup.json

# Free-design mode — EVYD Skills全栈团队课题 (dark_navy style)
node gen_free.js examples/evyd-skills-fullstack.json \
  --output "/Users/Li.ZHAO/Desktop/EVYD-Skills全栈团队课题.pptx"
```
