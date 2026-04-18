---
name: evyd-ppt-generator
description: >
  Generate professional PPTX presentations from a content JSON file.
  All slides are code-drawn (free mode) — no external template dependency.
  Use when the user asks to 生成PPT, 做幻灯片, 演示文稿, make slides, create presentation, ppt generator, or EVYD ppt.
---

# EVYD PPT Generator Skill

Generates native-PPTX presentations from a compact content JSON file.
One renderer (`gen_pptx.py`), 22 slide types (18 content + 4 chrome), **28 pluggable styles**
across 6 chrome identities (classic / gradient / neon-grid / magazine / minimal / brutalist).
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

### Theme catalog (MUST consult before recommending a style)

**`references/theme-catalog.md`** — complete directory of 28 built-in themes with
category, chrome style, vibe tags, best-for hints, and paired narrative templates.

### Style recommendation UX (Phase 1 deliverable)

Don't ask "which style do you want?" cold — the user rarely knows. Instead:

1. Extract 2–4 **keywords** from the user's brief covering: topic, audience, vibe.
2. Open `references/theme-catalog.md`, score each theme by keyword match on
   `category` + `vibe_tags` + `best_for`.
3. Filter by audience (decision-maker / engineer / consumer / external / internal).
4. **Present 2–3 top candidates** in a compact table: theme name, 1-line "why it
   fits", recommended narrative template.
5. If the user is undecided, offer a **preview**: render the cover slide for each
   candidate into `/tmp/preview_<theme>.pptx` so they can compare visually.
6. After the user picks, proceed to Phase 3 content generation.

Example:
```
User: 想做一个对外的 AI 新产品发布会 PPT，要有冲击力
→ keywords: [product-launch, external, bold, ai]
→ 3 candidates:
  1. cyberpunk_neon  — neon-grid chrome, max visual punch (template H)
  2. tokyo_night     — IDE-style neon, fits AI framing (template H or I)
  3. pitch_vc        — confident rather than loud (template H)
```

### Design direction brainstorming (style & color)

If the user wants to explore beyond the built-in 28 themes, use the
`ui-ux-pro-max` skill (if available) to brainstorm novel palettes, font pairings,
and direction. Run `--design-system` with relevant keywords, then materialize the
result as a new theme JSON following the v2 schema
(see `styles/tokyo_night.json` as reference).

The core workflow does not depend on `ui-ux-pro-max` —
never fail or ask the user to install it.

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
3. **User background** — ask directly: "你的行业/角色是什么？PPT 给谁看的？" Do NOT guess or infer from context. Use the answer to select narrative template and slide density.
4. **Key sections** / what needs to be covered
5. **Date, venue, presenter** (for cover slide)
6. **Style** preference — run the **Style recommendation UX** above: extract
   keywords → consult `references/theme-catalog.md` → propose 2–3 candidates →
   let user pick (optionally preview). Only fall back to `ui-ux-pro-max`
   brainstorm when no existing theme scores ≥ 2 keyword matches.

#### Audience analysis matrix

| Audience type | Structure | Slide density | Key slide types |
|---|---|---|---|
| Decision-makers (高管/政府) | Conclusion-first, pyramid | Low (3-4 points/page) | `stat_highlight`, `chart`, `center_focus` |
| Executors (团队/工程师) | Process steps, detailed plan | Medium-high (5-6 points) | `two_column_steps`, `scope_tiers`, `comparison_table` |
| External clients (MOH/partners) | Problem → solution, trust-building | Medium (4-5 points) | `bullets_with_panel`, `cards_grid`, `chart` |
| Mixed audience | Overview structure, breadth + depth | Medium (4-5 points) | `cards_grid`, `two_panel`, `stat_highlight` |

#### Narrative templates

Based on audience and purpose, recommend one of these templates.
User confirms with "OK" or "switch to B/C/D/E".

**A. Problem → Solution** (客户提案、项目启动)
```
cover → agenda → section_divider("背景") → bullets_with_panel(痛点) →
scope_tiers(问题分层) → section_divider("方案") → cards_grid(方案要点) →
two_column_steps(实施路径) → criteria_rows(预期效果) → ending
```

**B. Timeline** (项目回顾、季度汇报)
```
cover → agenda → section_divider("回顾") → timeline(关键里程碑) →
stat_highlight(KPI达成) → chart(趋势数据) → section_divider("下一步") →
two_column_steps(行动计划) → ending
```

**C. Comparison** (竞品分析、方案评估)
```
cover → agenda → section_divider("现状") → two_column_check(对比维度) →
comparison_table(详细对比) → chart(数据对比) → section_divider("建议") →
bullets_with_panel(推荐方案) → ending
```

**D. Process / Training** (操作指南、培训材料)
```
cover → agenda → section_divider("准备") → scope_tiers(适用范围) →
section_divider("步骤") → two_column_steps(具体操作) →
scenario_cards(场景演练) → survey(反馈收集) → ending
```

**E. Pyramid / Executive** (管理层汇报、战略规划)
```
cover → stat_highlight(核心结论) → section_divider("支撑论据") →
chart(数据支撑) → cards_grid(关键发现) → two_panel(风险与机会) →
section_divider("行动") → two_column_steps(下一步) → ending
```

**F. Spatial / Market Layout** (市场布局、地域分析、组织架构)
```
cover → agenda → section_divider("全景") → image_full(地图/架构图) →
cards_grid(各区域/部门概况) → comparison_table(跨区域对比) →
chart(数据对比) → section_divider("聚焦") → bullets_with_panel(重点区域) →
two_column_steps(行动计划) → ending
```

**G. Comprehensive Review** (综述报告、年度总结、白皮书)
```
cover → agenda → section_divider("背景") → bullets_with_panel(背景概述) →
stat_highlight(关键数字) → section_divider("分析") → chart(趋势数据) →
comparison_table(多维对比) → scope_tiers(分层发现) →
section_divider("结论") → center_focus(核心结论) →
two_column_steps(建议行动) → ending
```

**H. Product Launch** (发布会、产品上线、新功能宣发)
```
cover → section_divider("The Problem") → bullets_with_panel(痛点) →
quote_full(用户声音) → section_divider("Introducing") →
center_focus(产品名+slogan) → cards_grid(核心特性) →
stat_highlight(benchmark) → image_full(产品图) →
section_divider("Availability") → timeline(roadmap) → ending(CTA)
```
推荐主题：`tokyo_night` / `cyberpunk_neon` / `pitch_vc` / `fintech_navy`

**I. Tech Sharing** (技术分享、brown-bag、工程专题)
```
cover → agenda → section_divider("Background") → bullets_with_panel →
freeform(架构图) → comparison_table(方案对比) → chart(benchmark) →
scenario_cards(use cases) → section_divider("Takeaways") →
center_focus → ending
```
推荐主题：`terminal_green` / `cooltech` / `tokyo_night` / `dark_navy`

**J. XHS Post / Short-Form Card Deck** (小红书图文、短 feed，9-10 页)
```
cover(大标题+emoji) → stat_highlight(钩子数字) →
bullets_with_panel(痛点) → cards_grid(方法 3-4 张) →
quote_full(金句) → stat_highlight(结果) →
center_focus(CTA) → ending(关注引导)
```
密度覆写：每页 2-3 points / 标题 ≤ 10 中文字符 / 尽量单屏可读。
推荐主题：`xhs_white` / `xhs_warm` / `pastel_dream` / `warm_soft`

**K. Magazine Feature** (长文深度报道、品牌故事、白皮书节选)
```
cover → quote_full(引言) → section_divider("第一章") →
bullets_with_panel(叙事) → image_full(氛围图) → stat_highlight(数据) →
section_divider("第二章") → comparison_table → scope_tiers →
section_divider("尾声") → center_focus(主张) → ending
```
推荐主题：`magazine_bold` / `newspaper_editorial` / `vogue_serif` / `morandi`

#### Content density controls

- **3–5 key points per page**, hard maximum 7
- Bullet text: max 2 lines per bullet
- Title: max 8 words (English) / 16 characters (Chinese)
- If content overflows limits, split into two slides

### Phase 2 (optional) — Content research

**Trigger**: user says "帮我查一下" / "需要数据" / "help me research",
or AI judges user-provided content is insufficient (missing data, cases, or trends).

**When not triggered**: skip directly to Phase 3.

#### Three-round search strategy

**Round 1 — Broad scan (20% of effort)**
- 5–8 keywords, establish topic framework
- Map the information landscape: which dimensions have ready data, which need deep research

**Round 2 — Deep search (50% of effort)**
- Per-slide material needs, 3–5 precise keywords each
- Prioritize official sources and industry reports
- Use `WebSearch` for each query

**Round 3 — Verification (30% of effort)**
- Key data must have **2+ independent sources** cross-validated
- When sources contradict, flag both and let user decide

#### 5-level credibility rating

| Level | Source type | Action |
|-------|-----------|--------|
| ★★★★★ | Government / international org (WHO, MOH, World Bank) | Use directly |
| ★★★★ | Authoritative reports (Gartner, McKinsey, academic papers) | Cite source |
| ★★★ | Major media / corporate disclosures (Reuters, annual reports) | Cite source |
| ★★ | Industry blogs / analyst opinions | Mark as opinion |
| ★ | Unverified / single source | Backup only, do not use directly |

#### Material list format

Output Markdown table for user confirmation:

| Slide | Material | Source | Credibility | Usage |
|-------|----------|--------|-------------|-------|
| #4 KPI | SG healthcare IT spend $2.1B | MOH Annual Report 2024 | ★★★★★ | Must-use |
| #6 Trend | SEA AI healthcare CAGR 42.8% | Grand View Research | ★★★ | Backup |

User confirms → proceed to Phase 3.

### Phase 3 — Generate content.json

Generate ONLY the JSON file. Do NOT regenerate `gen_pptx.py` or style files.

#### Image sourcing (when using `image_full` slides)

1. Based on the slide topic, use `WebSearch` to find high-quality images:
   - Keywords: `[topic] + [scene] + "high resolution" OR "wide"`
   - Prefer royalty-free sources: Unsplash, Pexels, Pixabay
2. Download to local temp:
   ```bash
   mkdir -p /tmp/<project>/images
   curl -L -o /tmp/<project>/images/slide_N.jpg "<url>"
   ```
3. Verify file: size > 50KB, format is jpg/png
4. **Aesthetic check** — Read the downloaded image and evaluate:
   - Composition: is the subject clear? Enough whitespace for text overlay?
   - Resolution: sharp enough for 20″ canvas? No visible compression artifacts?
   - Color harmony: does it clash with the selected style palette?
   - Relevance: does it match the slide topic, not just the keyword?
   - If the image fails any check, search again with refined keywords
5. Use local path in content.json: `"image_path": "/tmp/<project>/images/slide_N.jpg"`

Skip this step for slides that don't use `image_full`.

#### Data-driven chart slides (when user provides CSV/Excel)

If the user provides a data file, use the helper script:
```bash
python3 scripts/data_to_chart.py <data.csv> --type bar --title "Title"
```
Paste the output JSON fragment directly into content.json's slides array.

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

### Phase 4 — Run renderer

```bash
cd "/Users/Li.ZHAO/我的代码/技能 skills 作坊/evyd-ppt-generator"

python3 gen_pptx.py content.json --style evyd_blue \
  --output "/Users/Li.ZHAO/Desktop/Output.pptx"
```

`--style` and `--output` override `meta` values. The renderer runs `validate_and_fix()`
automatically before saving — font sizes are shrunk up to 4pt if overflow is detected.

### Phase 5 — QA & verification loop

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
- Emoji / icons not rendering or displaying as tofu (□)
- Slide numbering not continuous or sequential
- Colors inconsistent with selected style (e.g. wrong accent color)

#### Narrative coherence check

After visual QA, review the slide sequence as a story:

- Does the deck follow the selected narrative template (A–G)?
- Is there a clear transition between sections (section_divider before topic shifts)?
- Does each slide logically follow from the previous one (no abrupt jumps)?
- Are data slides placed near the claims they support?
- Is the conclusion/ending consistent with the arguments presented?
- Would a first-time viewer understand the flow without verbal explanation?

If coherence issues are found, reorder slides or add bridging content in content.json.

Fix coordinates in `gen_pptx.py` or adjust content.json, then re-run.
Repeat until a full pass finds no new issues.

#### Delivery summary (after QA passes)

When delivering the PPTX, include this information:

1. **File info**: path, slide count, style used
2. **Content overview**: section titles and slide distribution
3. **Data sources** (if research phase was used): key data with source attribution
4. **Editing tips**:
   - All text and charts are natively editable in PowerPoint
   - Chart data: double-click any chart to modify the underlying data
   - Restyle: re-run with `--style <name>` to switch visual theme
   - Font: Aptos (built into macOS / Windows)
5. **Known limitations** (if any): e.g. backup-source data, placeholder images

#### File hygiene

All intermediate files (QA images, PDF conversions, temp JSON) go to `/tmp/`.
Only the final `.pptx` goes to the user's output directory.

---

## Layout Selector Guide — Freeform-First Strategy

**`freeform` is the DEFAULT type for ALL slides — including covers, agendas,
section dividers, and endings.** Claude must use freeform unless the content
falls into one of the few structured exceptions below.

Freeform gives AI full control over element positions, sizes, colors, and gradients,
producing visually superior results compared to the fixed-coordinate renderers.
Use gradient backgrounds, decorative shapes, deliberate whitespace, and layered
composition to create polished, magazine-quality slides.

### Decision flow

```
Does the content REQUIRE a structured renderer? (see table below)
  → YES: use that structured type
  → NO: use `freeform` (covers, agendas, dividers, endings, and all content)
```

### Structured types (use ONLY when freeform cannot replicate the functionality)

| Content REQUIRES... | → Type | Why not freeform |
|---|---|---|
| Native editable chart (bar/line/pie/doughnut/scatter) | `chart` | Needs python-pptx chart objects |
| Native editable table with sortable columns | `comparison_table` | Needs python-pptx table objects |

### Everything else → `freeform`

**ALL** of the following should be rendered as **freeform** with creative, bespoke layouts:

- **Cover / title slides** — gradient background, bold typography, decorative shapes
- **Agenda slides** — styled numbered items, accent bars, visual rhythm
- **Section dividers** — large typography, gradient or full-color background, decorative motifs
- **Ending / thank-you slides** — centered message, CTA actions, decorative composition
- Bullet points, key messages, quotes, statistics
- Step-by-step processes, numbered items, cards
- Timelines, roadmaps, tier/scope breakdowns
- Two-column comparisons (non-table), panels
- Scenario descriptions, feature highlights
- Survey / QR code layouts
- Any narrative or conceptual content

**Freeform design principles:**
- Use `gradient` backgrounds for premium feel (diagonal or vertical, 2–3 color stops)
- Layer decorative `oval` shapes with high transparency (88–95%) for depth
- Maintain consistent margins (min 0.8" from edges)
- Use accent `line` elements as visual dividers
- Vary layouts across slides — avoid repeating the same element grid
- For "white" background slides, use subtle card `rect` shapes with `card_white` fill

Aliases: `key_metrics` → `stat_highlight`, `quote_highlight` → `quote_full`.

**Background rhythm**: alternate `"blue"` and `"white"` slides. Start and end with blue.
Use `"white"` for data-heavy slides (`comparison_table`, `chart`).

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
| `sunrise` | Medium navy `1B2838` | Coral `E8634A` + Amber `F5A623` | Progress, AI transformation, hopeful narratives |
| `charcoal_gold` | Charcoal `1C1C22` | Gold `C9A96E` | Strategic workshops, board meetings |

### Style auto-recommendation

During Phase 1, after identifying audience and topic, recommend a style:

| Scenario | Recommended style |
|---|---|
| EVYD internal / MOH / government | `evyd_blue` (default) |
| Printed materials / handouts | `evyd_white` |
| External speaking / conference | `evyd_teal` |
| Executive / formal report | `dark_navy` or `charcoal_gold` |
| AI / tech / SaaS / data topic | `cooltech` |
| Culture / brand / design | `morandi` |
| Education / training / workshop | `warm` |
| Minimal / editorial / executive | `monochrome` |
| Progress / hopeful / AI transformation | `sunrise` |

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

#### `chart` *(new)*
Data chart using native PowerPoint chart objects. Supports bar, line, pie, doughnut.
```json
{
  "type": "chart",
  "section": "02 — Data", "title": "Monthly Growth", "background": "white",
  "chart_type": "bar",
  "categories": ["Jan", "Feb", "Mar", "Apr", "May"],
  "series": [
    { "name": "New Users", "values": [120, 180, 240, 310, 400] },
    { "name": "Active Users", "values": [80, 130, 190, 260, 350] }
  ],
  "footnote": "Source: Internal analytics"
}
```
`chart_type`: `bar` | `bar_stacked` | `bar_horizontal` | `line` | `line_marker` | `area` | `pie` | `doughnut` | `radar` | `scatter`

Chart colors from style `chart_colors`. For pie/doughnut, use only one series.
Max 5 series (bar/line/area), 8 slices (pie/doughnut), 6 dimensions (radar).

**Scatter** uses a different data format (`x_values` / `y_values` instead of `categories` / `values`):
```json
{
  "type": "chart",
  "chart_type": "scatter",
  "section": "03 — Analysis", "title": "Response Time vs Load", "background": "white",
  "series": [
    { "name": "Server A", "x_values": [10, 20, 30, 40], "y_values": [1.2, 1.8, 2.5, 4.1] },
    { "name": "Server B", "x_values": [10, 20, 30, 40], "y_values": [0.8, 1.2, 1.9, 3.0] }
  ],
  "footnote": "Load in concurrent requests; time in seconds"
}
```

---

#### `image_full` *(new)*
Full-bleed image with semi-transparent overlay and centered text.
```json
{
  "type": "image_full",
  "section": "...",
  "title": "Our Vision",
  "subtitle": "Accessible healthcare for everyone",
  "image_path": "/path/to/image.jpg",
  "overlay": "dark"
}
```
`overlay`: `"dark"` (navy tint) or `"light"` (white tint). Image fills entire slide.
If `image_path` does not exist, renders a placeholder with error note.

---

#### `freeform` *(new)*
Creative free-layout slide. AI specifies exact position and size of every element.
Use for layouts that don't fit any fixed type. Colors can reference style keys.
```json
{
  "type": "freeform",
  "section": "05 — Vision", "title": "Custom Layout", "background": "blue",
  "elements": [
    { "kind": "rect", "x": 1.0, "y": 2.0, "w": 8.0, "h": 7.5, "fill": "card", "radius": true },
    { "kind": "text", "x": 1.5, "y": 2.5, "w": 7.0, "h": 1.2, "text": "Big Idea", "sz": 36, "bold": true, "color": "accent" },
    { "kind": "text", "x": 1.5, "y": 4.0, "w": 7.0, "h": 3.0, "text": "Supporting details here...", "sz": 18, "color": "text_dim" },
    { "kind": "image", "x": 10.0, "y": 2.0, "w": 9.0, "h": 7.5, "path": "/tmp/photo.jpg" },
    { "kind": "oval", "x": 16.0, "y": 0.0, "w": 6.0, "h": 6.0, "fill": "accent2", "transparency": 92 },
    { "kind": "line", "x": 1.5, "y": 3.7, "w": 2.0, "h": 0.06, "color": "accent" }
  ]
}
```
Element kinds: `text` (textbox), `rect` (rectangle), `oval`, `image`, `line` (thin rect), `gradient`.

**Gradient** creates a rectangle with linear color gradient:
```json
{ "kind": "gradient", "x": 0, "y": 0, "w": 20, "h": 11.25,
  "colors": ["navy", "0D1B2A", "accent"], "angle": 135, "transparency": 0 }
```
`colors`: 2–3 color stops (style keys or hex). `angle`: 0=left→right, 90=top→bottom, 135=diagonal.
Use as full-slide background for the "premium" look that Kimi/Manus achieve with CSS gradients.
Colors accept style key names (`"accent"`, `"card"`, `"text_dim"`) or hex strings (`"FF6600"`).
`title` is optional — omit it for a headerless full-canvas layout.

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
├── gen_pptx.py                       # Free-mode renderer (22 slide types)
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
│   ├── monochrome.json               # Black/white/grey
│   ├── sunrise.json                  # Navy + coral + amber (progress/AI)
│   └── charcoal_gold.json            # Charcoal + gold (strategic/premium)
└── examples/
    ├── bruai-focusgroup.json
    ├── evyd-1person-fullstack.json
    ├── evyd-skills-fullstack.json
    └── fullstack-v2.json
```
