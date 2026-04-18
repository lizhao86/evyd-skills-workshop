# Theme Catalog — 28 styles

Full directory of built-in themes. Use this table to recommend 2–3 candidate styles based on the user's topic, audience, and vibe words.

Columns:
- **Theme** — `--style` name (exact match)
- **Category** — `business` / `tech-dark` / `editorial` / `lifestyle` / `minimal`
- **Chrome** — visual identity layer (`classic` / `gradient` / `neon-grid` / `magazine` / `minimal` / `brutalist`)
- **Vibe tags** — keyword match targets
- **Best for** — use-case shorthand
- **Templates** — which narrative templates (A–K) this theme pairs well with

---

## Business (6)

| Theme | Chrome | Vibe tags | Best for | Templates |
|---|---|---|---|---|
| `evyd_blue` | gradient | corporate, trust, gov, internal | EVYD internal, MOH, government, default | A, B, C, E, F, G |
| `evyd_white` | minimal | clean, print, light, handout | Printed handouts, light projection | A, C, D, G |
| `evyd_teal` | gradient | bold, high-contrast, conference, external | External events, conferences | A, B, E, H |
| `dark_navy` | gradient | strategy, premium, research, finance | Strategy decks, research, finance | B, C, E, G |
| `charcoal_gold` | classic | premium, board, strategy, workshop, luxury | Board meetings, premium corporate | E, G, K |
| `boardroom_slate` | classic | board, formal, legal, exec, gravitas | Board meetings, compliance | E, G |
| `fintech_navy` | gradient | fintech, compliance, clean, banking | Fintech demo, compliance | C, E, G, H |
| `pitch_vc` | magazine | pitch, vc, investor, confident, fundraising | VC pitch, investor meetings | E, H |
| `investor_deck` | minimal | pitch, restrained, one-color, accent | Seed/Series A deck | E, H |

## Tech-dark (3)

| Theme | Chrome | Vibe tags | Best for | Templates |
|---|---|---|---|---|
| `cooltech` | neon-grid | ai, saas, futuristic, tech, healthtech | AI/SaaS/healthtech, innovation | B, H, I |
| `tokyo_night` | neon-grid | neon, night, futuristic, developer, ai, ide | AI demo, hackathon, developer tools | H, I |
| `cyberpunk_neon` | neon-grid | neon, bold, vibrant, cyberpunk, launch | Product launch, hackathon demo, bold brand | H |
| `terminal_green` | neon-grid | mono, terminal, engineer, retro, matrix | Tech sharing, infra talk, engineer brown-bag | I |

## Editorial (6)

| Theme | Chrome | Vibe tags | Best for | Templates |
|---|---|---|---|---|
| `morandi` | magazine | calm, refined, brand, culture, design | Culture, brand, design | G, K |
| `warm` | magazine | warm, workshop, training, education, human | Education, training, workshops | D, K |
| `warm_soft` | magazine | paper, refined, soft, government, healthcare | Government alignment, healthcare | A, G, K |
| `sunrise` | magazine | hopeful, progress, transformation, narrative | Progress reports, AI transformation | B, E, K |
| `magazine_bold` | magazine | bold, serif, magazine, editorial, brand | Brand story, long-form feature | K |
| `newspaper_editorial` | magazine | editorial, newspaper, broadsheet, serif | Long-form story, retrospective | G, K |
| `vogue_serif` | magazine | fashion, editorial, aspirational, serif, luxury | Brand story, fashion/beauty/design | K |

## Lifestyle (4)

| Theme | Chrome | Vibe tags | Best for | Templates |
|---|---|---|---|---|
| `xhs_white` | minimal | xhs, lifestyle, clean, pastel, consumer | 小红书 post, consumer-facing short-form | J |
| `xhs_warm` | magazine | xhs, warm, cozy, wellness, peach | 小红书 lifestyle, home/food/wellness | J, K |
| `pastel_dream` | gradient | pastel, genz, dreamy, consumer, delight | Consumer app launch, Gen-Z brand | H, J |
| `cafe_cream` | magazine | hospitality, coffee, food, retail, community | Hospitality, F&B brand, retail | K |

## Minimal (4)

| Theme | Chrome | Vibe tags | Best for | Templates |
|---|---|---|---|---|
| `monochrome` | minimal | minimal, editorial, exec, high-end, mono | Executive briefings, editorial | E, G |
| `nordic_minimal` | minimal | minimal, nordic, airy, product, quiet, wood | Product design review, quiet confidence | E, G, K |
| `bauhaus_primary` | brutalist | bauhaus, geometric, bold, primary, design | Design manifesto, bold announcement | A, K |
| `zen_mono` | minimal | zen, japanese, calm, philosophy, quiet, washi | Calm keynote, brand philosophy | E, K |

---

## Recommendation logic (for the AI)

1. From the user's brief, extract 2–4 keywords spanning: **topic** (ai/fintech/brand/...), **audience** (exec/consumer/engineer/...), **vibe** (bold/calm/warm/...).
2. Score each theme by the number of matches against `category` + `vibe_tags` + `best_for`.
3. Filter by audience:
   - Decision-makers / board → business or minimal
   - Engineers / developers → tech-dark
   - Consumer / external → lifestyle or editorial
   - Internal EVYD → default to evyd_blue / evyd_white family
4. Return **2–3 top candidates** with one-line "why it fits" for each.
5. If the user says "不确定 / 都看看", render the cover slide for each candidate into `/tmp/preview_<theme>.pptx` and let the user pick.

Example dialogue:
> **User**: "帮我做一个讲 EVYD 新产品发布的 PPT，对外用，想要有冲击力"
>
> **Keywords**: [product-launch, external, bold, tech]
>
> **Top 3**:
> 1. `cyberpunk_neon` — neon-grid chrome + magenta/cyan, maximum visual impact (template H)
> 2. `tokyo_night` — developer aesthetic with softer neon, fits AI/tech products (template H or I)
> 3. `pitch_vc` — if tone should be confident rather than loud (template H)

---

## When to create a new theme

Only when the user's brief matches **no** existing theme within 2 vibe tags. Before creating, first try:
- Swapping `chrome_style` on an existing theme (e.g. `dark_navy` + `brutalist` for a harder look)
- Overriding `accent` via content.json `meta` (if the only issue is accent hue)

New themes should follow the schema in any of the v2 JSONs (see `styles/tokyo_night.json` as reference).
