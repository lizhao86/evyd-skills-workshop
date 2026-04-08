# EVYD PPT Generator

Generate professional PPTX presentations from a compact JSON content file.  
All slides are code-drawn — no external template dependency.

## Quick start

```bash
pip install python-pptx

python3 gen_pptx.py examples/bruai-focusgroup.json \
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
- **Renderer** (`gen_pptx.py`) — 14 slide types, all drawn from code via python-pptx
- **Style** (`styles/*.json`) — pluggable color/font/motif configs, no code changes needed

## Available styles

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

## Slide types

`cover` · `agenda` · `section_divider` · `ending` · `bullets_with_panel` · `two_column_check` · `cards_grid` · `criteria_rows` · `scope_tiers` · `two_panel` · `two_column_steps` · `scenario_cards` · `survey` · `stat_highlight` · `timeline` · `quote_full` · `center_focus` · `comparison_table`

## Adding a new style

1. Copy any `styles/*.json` → `styles/my_style.json`
2. Edit color values (hex without `#`) and motifs
3. Run with `--style my_style`

## Claude Code skill

This project is designed to be used as a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code). See `SKILL.md` for the full specification that Claude reads when generating presentations.

## Design references

- `references/design-guidelines.md` — Typography, layout rules, color psychology, rendering implementation rules
- When discussing style direction, the skill uses [ui-ux-pro-max](https://github.com/lizhao86/ui-ux-pro-max) for palette and typography brainstorming (optional, falls back to built-in guidelines)

## License

MIT
