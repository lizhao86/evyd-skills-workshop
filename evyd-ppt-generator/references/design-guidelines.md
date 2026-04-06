# PPT Design Guidelines

This reference is read by the AI when generating `content.json`.
It codifies the design rules from the Kimi PPT Style Reference Manual (v2.0)
into actionable guidance for our slide types, styles, and content decisions.

---

## 1. Typography Hierarchy (Aptos)

All styles use **Aptos** font. Follow this size hierarchy strictly:

| Level | Size (pt) | Weight | Purpose |
|-------|-----------|--------|---------|
| Cover title | 36–44 | Bold | First slide, maximum impact |
| Section title | 24–32 | Bold | `section_divider` large text |
| Slide title | 22–26 | Bold | Header bar title in content slides |
| Card/row heading | 14–16 | Bold | `cards_grid` num, `criteria_rows` label |
| Body text | 12–15 | Regular | Main content in bullets, cards, steps |
| Caption/annotation | 9–11 | Regular/Italic | Section tag, slide number, footnote |

### Alignment rules

- **Titles**: left-aligned (content slides) or center-aligned (cover, ending)
- **Body text**: always left-aligned — never justified in slides
- **Numbers/labels**: center-aligned inside their container (card number, step circle)
- **Slide numbers**: right-aligned bottom corner

### Line spacing

- **Standard** (1.5x): default for body text — comfortable reading
- **Tight** (1.0–1.2x): use when a slide has 4+ rows/items to prevent overflow
- **Generous** (1.8–2.0x): cover subtitle, ending slide — premium feel

---

## 2. Layout Selection Rules

Match content type to the right slide type:

| Content need | Slide type | Max items | Density |
|---|---|---|---|
| Opening / welcome | `cover` | — | Minimal |
| Agenda / schedule | `agenda` | 5 items | Medium |
| Section break | `section_divider` | — | Minimal |
| Key points + elaboration + pull quote | `bullets_with_panel` | 4 bullets | Medium |
| In-scope / out-scope comparison | `two_column_check` | 6 per column | Dense |
| Feature showcase (numbered cards) | `cards_grid` | 6 cards (3x2) | Medium |
| Evaluation criteria (rows) | `criteria_rows` | 4 rows | Medium |
| Tiered classification (traffic-light) | `scope_tiers` | 4 tiers | Medium |
| Two-panel side-by-side | `two_panel` | 2 panels x 5 items | Dense |
| Process / steps (before-during-after) | `two_column_steps` | 2 cols x 4 steps | Dense |
| Scenarios / use cases | `scenario_cards` | 4 cards (2x2) | Medium |
| Survey / QR feedback | `survey` | 4 steps | Medium |
| Thank you / CTA | `ending` | 2 actions | Minimal |

### Whitespace rules

| Density | Margin (% of width) | When to use |
|---------|---------------------|-------------|
| Generous (15–20%) | High-end, cover, ending, section divider | Few elements, maximum impact |
| Standard (10–15%) | Content slides with 2–4 items | Default for most slides |
| Tight (5–10%) | Dense comparison, 6-card grids, scope tiers | Information-heavy slides |

### Content-per-slide limits

- **Never exceed** the max items listed above — if content overflows, **split into two slides**
- **Bullet text**: max 2 lines per bullet. If longer, move detail to a card or criteria row
- **Card text**: max 3 lines. If longer, split into two cards
- **Title text**: max 1 line. Shorten aggressively — detail belongs in body text

---

## 3. Color Psychology & Style Selection

When the user describes their audience or mood, map to a style:

| User says (zh) | User says (en) | Recommended style | Why |
|---|---|---|---|
| 科技感、未来感、AI | techy, futuristic | `cooltech` | Cyan + purple = innovation |
| 专业、稳重、企业 | professional, corporate | `evyd_blue` or `dark_navy` | Navy = authority |
| 简洁、极简、高端 | minimal, editorial | `monochrome` | No color = let content speak |
| 温馨、亲切、教育 | warm, friendly, training | `warm` | Coral + amber = human |
| 优雅、文艺、品牌 | elegant, artistic, culture | `morandi` | Muted tones = refinement |
| 对外演讲、高对比 | external, high-contrast | `evyd_teal` | Teal on dark = bold |
| 打印、白底 | print, handout | `evyd_white` | White background for paper |

### Industry defaults

| Industry | Primary style | Alternate |
|----------|--------------|-----------|
| Healthcare / MedTech | `evyd_blue` | `evyd_teal` |
| SaaS / AI / Data | `cooltech` | `dark_navy` |
| Finance / Insurance | `dark_navy` | `monochrome` |
| Education / Training | `warm` | `morandi` |
| Creative / Lifestyle | `morandi` | `monochrome` |
| Executive briefing | `monochrome` | `dark_navy` |
| Government / MOH | `evyd_blue` | `evyd_white` |

---

## 4. Color Usage Rules

### Dark-background slides (`background: "blue"`)

- **Title**: white or near-white (`text_white`)
- **Body text**: light tinted (`text_primary`) — never pure white for body (too harsh)
- **Accents** (tags, dots, borders): use `accent_orange` (primary) or `accent_teal` (secondary)
- **Cards**: use `card` background color — slightly lighter than slide background
- **Left bars/stripes**: always use accent colors, never grey

### Light-background slides (`background: "white"`)

- **Title**: dark navy or near-black (`text_dark` / `text_navy`)
- **Body text**: medium grey (`text_mid`) — never pure black (too heavy)
- **Cards**: use `card_white` — very light tinted background
- **Accents**: same accent colors, but ensure contrast ratio >= 4.5:1 on white

### Color DO NOTs

- Never use more than 2 accent colors per slide
- Never color body text with an accent color (accents are for labels, dots, borders only)
- Never use red/green to convey meaning alone (accessibility) — always pair with icon/text
- Never use gradients in text — only in decorative shapes

---

## 5. Visual Element Guidelines

### Decorative shapes

- **Left vertical bar**: always on cover slide, uses gradient from `left_bar_colors[0]` (top) to `[1]` (bottom)
- **Teal accent stripe**: thin (0.04–0.06 inch) horizontal rule below title — consistent brand mark
- **Card left border**: 0.05–0.14 inch, uses accent color to create visual anchor
- **Subtle circles**: large, low-opacity (90–95% transparency) decorative circles on cover/ending — adds depth without distraction

### When to use `background: "blue"` vs `"white"`

| Use blue when | Use white when |
|---|---|
| Slide is narrative / persuasive | Slide is data-dense / reference |
| Audience is external (presentation) | Audience will read later (handout) |
| Content has few elements (3-4) | Content has many elements (5+) |
| Slide follows a section_divider | Slide contains comparison tables |

### Image & icon conventions (for future extension)

- **Photography**: use only on cover/ending or full-bleed backgrounds, never inline
- **Icons**: prefer emoji shorthand in JSON (`icon` field) — renderer handles placement
- **QR codes**: always in a dedicated panel with clear label and instruction text

---

## 6. Slide Sequencing Best Practices

### Standard deck structure

```
1. cover
2. agenda (if 3+ sections)
3. section_divider → content slides → ...
4. section_divider → content slides → ...
5. survey (if feedback needed)
6. ending
```

### Rules

- **Always start with `cover`**, always end with `ending`
- **Use `section_divider`** before each major topic shift (not for every slide)
- **Alternate `blue` and `white`** backgrounds within a section for visual rhythm — don't make 5 blue slides in a row
- **Put the most important point on slides 3-5** — that's the attention peak
- **Max 15 slides** for a 30-min presentation, **max 25** for a 60-min talk
- **Keep consistent slide numbering**: auto-calculated is fine, don't override `num` unless splitting a section

---

## 7. Content Writing Rules (for content.json generation)

### Title writing

- Max 6 words for slide titles — be ruthless
- Use sentence case, not TITLE CASE (except for labels like "IN SCOPE")
- Include the "so what" — "Revenue Up 23%" not "Revenue Update"

### Bullet writing

- Start with a verb or noun — no filler words
- Max 15 words per bullet — if longer, it's a paragraph, not a bullet
- Use parallel structure (all bullets start the same way)

### Card/scenario writing

- `num` field: always zero-padded ("01", "02") for visual consistency
- `tag` field: max 2 words, uppercase
- `desc` field: 1-2 sentences, action-oriented

---

## 8. Style Description Vocabulary

When the user describes a style in natural language, parse using these dimensions:

| Dimension | Low end | Mid | High end |
|-----------|---------|-----|----------|
| Saturation | 莫兰迪/灰调/柔和 | 自然/日常 | 浓烈/鲜明/高饱和 |
| Temperature | 冷色调/蓝绿/理性 | 中性 | 暖色调/红黄/亲切 |
| Brightness | 深色/暗调/沉稳 | 标准 | 明亮/轻快/清新 |
| Complexity | 极简/单色/留白 | 标准 | 丰富/多彩/热闹 |
| Formality | 轻松/活泼/个性 | 专业 | 正式/庄重/官方 |

Use these dimensions to select the closest available style, or suggest creating a new one.
