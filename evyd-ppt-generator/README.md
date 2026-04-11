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

## v2.2 Features

- **7 narrative templates** (A–G): problem→solution, timeline, comparison, process, pyramid, spatial/market, comprehensive review — with audience-driven auto-selection
- **Direct user profiling**: asks user's industry/role explicitly — no guessing
- **3-round content research**: broad scan → deep search → verification, with 5-level credibility rating (★–★★★★★)
- **10 chart types**: bar, bar_stacked, bar_horizontal, line, line_marker, area, pie, doughnut, radar, scatter — all native PowerPoint charts
- **Image sourcing + aesthetic check**: WebSearch→download→Claude vision evaluation (composition, resolution, color harmony, relevance)
- **Data pipeline**: `scripts/data_to_chart.py` converts CSV/Excel to chart JSON via pandas
- **Narrative coherence check**: QA verifies story flow, transitions, data placement, and conclusion consistency
- **Delivery summary**: structured handoff with editing tips and source attribution
- **QA verification**: 11-item visual checklist + coherence check with soffice→image conversion

## Available styles (10)

| Style | Base tone | Accent | Best for |
|-------|-----------|--------|----------|
| `evyd_blue` | Navy | Teal | Default — internal / MOH |
| `evyd_white` | White | Blue | Printed handouts |
| `evyd_teal` | Dark navy | Teal | External events, high-contrast |
| `dark_navy` | Deep navy | Orange | Strategy, research |
| `cooltech` | Space blue | Cyan | AI / SaaS / healthtech |
| `morandi` | Slate | Dusty rose | Culture, brand |
| `warm` | Espresso | Coral | Education, training |
| `monochrome` | Charcoal | Grey | Executive, editorial |
| `sunrise` | Medium navy | Coral + Amber | Progress, AI transformation |
| `charcoal_gold` | Charcoal | Gold | Strategic workshops, board meetings |

Each style includes `chart_colors` (5-color palette for chart series) and `best_for` metadata for auto-recommendation.

## Slide types (21)

**Chrome**: `cover` · `agenda` · `section_divider` · `ending`

**Content**: `bullets_with_panel` · `two_column_check` · `cards_grid` · `criteria_rows` · `scope_tiers` · `two_panel` · `two_column_steps` · `scenario_cards` · `survey` · `stat_highlight` · `timeline` · `quote_full` · `center_focus` · `comparison_table` · `chart` · `image_full`

**Aliases**: `key_metrics` → `stat_highlight` · `quote_highlight` → `quote_full`

## Adding a new style

1. Copy any `styles/*.json` → `styles/my_style.json`
2. Edit color values (hex without `#`), motifs, `best_for`, and `chart_colors`
3. Run with `--style my_style`

## Claude Code skill

This project is designed to be used as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code). See `SKILL.md` for the full specification that Claude reads when generating presentations.

### Workflow (5 phases)

1. **Gather requirements** — audience matrix + narrative template selection + style recommendation
2. **Content research** (optional) — WebSearch with cross-validation, triggered on demand
3. **Generate content.json** — AI auto-selects slide types based on content
4. **Run renderer** — `python3 gen_pptx.py content.json`
5. **QA verification** — soffice→image conversion + 11-item visual checklist

## Design references

- `references/design-guidelines.md` — Typography, layout rules, color psychology, chart design rules, rendering implementation rules
- When discussing style direction, the skill uses [ui-ux-pro-max](https://github.com/lizhao86/ui-ux-pro-max) for palette and typography brainstorming (optional, falls back to built-in guidelines)

## License

MIT
