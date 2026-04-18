# EVYD PPT Generator

Generate professional PPTX presentations from a compact JSON content file.
All slides are code-drawn — no external template dependency.

## Quick start

```bash
pip install python-pptx

python3 gen_pptx.py examples/fullstack-v2.json \
  --style evyd_blue \
  --output ~/Desktop/Output.pptx
```

## How it works

```
content.json  →  gen_pptx.py  →  Output.pptx
                     ↑
               styles/*.json
```

- **Content** (`content.json`) — what to say, which slides, in what order
- **Renderer** (`gen_pptx.py`) — 21 slide types (17 content + 4 chrome), all drawn from code via python-pptx
- **Style** (`styles/*.json`) — pluggable color/font/motif configs, no code changes needed

## v2.3 Features

- **11 narrative templates** (A–K): problem→solution, timeline, comparison,
  process, pyramid, spatial, comprehensive review, product launch, tech
  sharing, XHS post, magazine feature — picked by audience + intent + time
- **28 themes across 5 categories** (business / tech-dark / editorial /
  lifestyle / minimal) and **6 chrome identities** (classic / gradient /
  neon-grid / magazine / minimal / brutalist) — see
  `references/theme-catalog.md` for the full directory + recommendation logic
- **Direct user profiling**: asks user's industry/role explicitly — no guessing
- **3-round content research**: broad scan → deep search → verification, with
  5-level credibility rating (★–★★★★★)
- **10 chart types**: bar, bar_stacked, bar_horizontal, line, line_marker,
  area, pie, doughnut, radar, scatter — all native PowerPoint charts
- **Image sourcing + aesthetic check**: WebSearch → download → Claude vision
  evaluation (composition, resolution, color harmony, relevance)
- **Data pipeline**: `scripts/data_to_chart.py` converts CSV/Excel to chart
  JSON via pandas
- **Contrast audit**: `python3 gen_pptx.py --check-contrast` reports any
  text/background pair below WCAG floor across all 28 themes
- **QA verification**: 11-item visual checklist + coherence check with
  soffice→image conversion

## How content is sourced — workflow at a glance

The narrative template is **chosen first** (Phase 1), not derived from your
content. It then dictates what to look for if research happens.

```
Phase 1  pick template       ← audience + intent + time, 2 min
Phase 2  (optional) research ← only if you say "帮我查一下" or your input is thin
Phase 3  write content.json  ← fill the template; research-backed where needed
Phase 4  render              ← python3 gen_pptx.py
```

Three operating modes:

| You bring | I do |
|---|---|
| Full content + outline | Editor / typesetter — pick template, organize your material |
| Topic + rough outline | Ghost-writer — template guides what to research, I draft the rest |
| Just an intent | Discover — clarify audience/time first, then template, then ask if you want me to research |

The template is a **hypothesis**, not a contract. If during research the
evidence points to a stronger structure (e.g. data is so strong we should
flip from A *Problem→Solution* to E *Pyramid*), I'll surface the switch
explicitly and let you confirm.

**Default**: I do not auto-research. You must trigger it, otherwise I assume
you have the content. Reason: web research is high-cost and high-noise — your
judgment beats my generic search.

## Available styles (28)

Five categories, each themed for a different scenario. Full catalog with
vibe tags and template pairings: `references/theme-catalog.md`.

| Category | Themes |
|---|---|
| **business** | `evyd_blue` · `evyd_white` · `evyd_teal` · `dark_navy` · `charcoal_gold` · `boardroom_slate` · `fintech_navy` · `pitch_vc` · `investor_deck` |
| **tech-dark** | `cooltech` · `tokyo_night` · `cyberpunk_neon` · `terminal_green` |
| **editorial** | `morandi` · `warm` · `warm_soft` · `sunrise` · `magazine_bold` · `newspaper_editorial` · `vogue_serif` |
| **lifestyle** | `xhs_white` · `xhs_warm` · `pastel_dream` · `cafe_cream` |
| **minimal** | `monochrome` · `nordic_minimal` · `bauhaus_primary` · `zen_mono` |

Each theme includes `chart_colors` (5-color palette for chart series),
`vibe_tags` (for AI matching), `chrome_style` (one of 6 visual identities),
and `best_for` metadata.

Recommendation flow: I extract 2–4 keywords from your brief, score themes by
match against `vibe_tags` + `category` + `best_for`, and propose 2–3 candidates
with one-liner "why it fits". If undecided, I render the cover slide for each
into `/tmp/preview_<theme>.pptx` so you can compare.

## Slide types (22)

**Chrome**: `cover` · `agenda` · `section_divider` · `ending`

**Content**: `bullets_with_panel` · `two_column_check` · `cards_grid` · `criteria_rows` · `scope_tiers` · `two_panel` · `two_column_steps` · `scenario_cards` · `survey` · `stat_highlight` · `timeline` · `quote_full` · `center_focus` · `comparison_table` · `chart` · `image_full` · `freeform`

**Aliases**: `key_metrics` → `stat_highlight` · `quote_highlight` → `quote_full`

The `freeform` type gives AI full creative control — specify exact element positions, sizes, and colors for layouts that don't fit any fixed type. Supports gradient backgrounds (2-3 color stops, any angle) for the premium look of CSS gradients, but output is still 100% native editable PPTX.

## Adding a new style

1. Copy any `styles/*.json` → `styles/my_style.json`
2. Edit color values (hex without `#`), motifs, `best_for`, and `chart_colors`
3. Run with `--style my_style`

## Claude Code skill

This project is designed to be used as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code). See `SKILL.md` for the full specification that Claude reads when generating presentations.

### Workflow (5 phases)

1. **Gather requirements & pick template** — audience matrix → narrative
   template (A–K) → 2–3 theme candidates from `references/theme-catalog.md`.
   Template is chosen before any content work; it dictates what to look for.
2. **Content research** (optional, opt-in) — WebSearch with cross-validation,
   triggered only when you say "帮我查一下" or your input is clearly thin.
3. **Generate content.json** — AI fills the chosen template, picking slide
   types per the template's recipe + your content density.
4. **Run renderer** — `python3 gen_pptx.py content.json --style <theme>`
5. **QA verification** — `--check-contrast` + soffice→image + 11-item visual
   checklist

## Design references

- `references/design-guidelines.md` — Typography, layout rules, color psychology, chart design rules, rendering implementation rules
- When discussing style direction, the skill uses [ui-ux-pro-max](https://github.com/lizhao86/ui-ux-pro-max) for palette and typography brainstorming (optional, falls back to built-in guidelines)

## License

MIT
