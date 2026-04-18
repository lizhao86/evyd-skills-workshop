---
name: evyd-general-research
description: |
  General-purpose desk research for EVYD — policy, regulation, market data, academic,
  trend analysis. NOT for competitor intel (use evyd-competitor-research for that).

  Output: a structured research brief (markdown + machine-readable JSON block) with
  tiered source attribution, confidence labels, and contradiction tracking. The brief
  is consumable by downstream skills like evyd-ppt-generator.

  Trigger on: 帮我查一下, 帮我研究一下, 做个调研, 查一下资料, research, desk research,
  find data on, what's known about, literature review.

  Examples:
  - user: "帮我查一下新加坡数字医疗市场规模" → general-research
  - user: "MOH 对 AI 医疗器械的监管框架是什么" → general-research
  - user: "Epic 在东南亚的部署情况" → evyd-competitor-research (competitor intel)
  - user: "临床 RAG 最近有什么 benchmark" → general-research (academic/technical)
---

# EVYD General Research Skill

Single-topic / single-question desk research. Distilled into a structured brief
that downstream skills can consume directly.

## When to use this vs evyd-competitor-research

| Situation | Use |
|---|---|
| User names a **competitor company** or asks for competitive comparison | `evyd-competitor-research` |
| User asks a **topic / question / data** — policy, market size, trend, academic | **this skill** |
| User says "查一下 X"  where X is a **named company** in our space | `evyd-competitor-research` |
| User says "查一下 X"  where X is a **topic / metric / concept** | **this skill** |
| Output needs structured Feishu doc with 5 competitive dimensions | `evyd-competitor-research` |
| Output feeds into PPT / requirement doc / strategy deck | **this skill** |

When in doubt, ask the user: "这个是要拿 X 作为对比对象，还是作为话题研究？"

---

## Hard rules (non-negotiable)

1. **Every claim carries a source tag**: `[source-tier · date]`. No bare claims, ever.
2. **2+ independent sources required** for any claim upgraded to "high confidence".
3. **Contradictions are surfaced, not hidden**. If two high-tier sources disagree, the brief flags both and states my reading.
4. **No fabrication**. If I can't find a number within 3 search rounds, the brief says "not found in available sources" — never guess.
5. **Tier-weighted citation**: never cite a blog (★★) when a primary source (★★★★+) exists for the same fact.
6. **Output is structured**: markdown for humans + JSON block for programmatic consumers. Both kept in sync.

---

## Tool preference

Check which tools are available in this session and prefer in order:

1. **Exa MCP** (`mcp__exa__*`) — semantic search, surfaces high-quality non-SEO sources
   *Placeholder: not yet configured, see `references/mcp-setup.md` for setup when tokens available.*
2. **Firecrawl MCP** (`mcp__firecrawl__*`) OR **Jina Reader MCP** (`mcp__jina__*`) — clean markdown extraction from JS-heavy / PDF pages
   *Placeholder: not yet configured, see `references/mcp-setup.md`.*
3. **WebSearch** (built-in) — general web search, fallback when Exa unavailable
4. **WebFetch** (built-in) — single URL fetch, fallback when Firecrawl/Jina unavailable

At the start of every research session, declare which tools are active:
```
Tools available: WebSearch ✓ / WebFetch ✓ / Exa ✗ / Firecrawl ✗
```

---

## Workflow (3 rounds)

See `references/search-playbook.md` for detailed prompts and query templates.

### Round 1 — Scoping scan (20% effort)

Goal: map the information landscape. Which dimensions have ready data, which need digging?

1. Turn the user's question into 5–8 search-engine keywords, covering
   (a) entity/topic, (b) geography, (c) time window, (d) synonym variants.
2. Issue 3–5 broad searches (WebSearch or Exa).
3. From results, identify: what's the authoritative primary source? What's the 2–3 best secondary sources? Which claims show up in multiple places?

**Output of Round 1**: a mental map, not yet a brief. If the user gave a scoping-ambiguous request, pause here and ask clarifying questions.

### Round 2 — Targeted deep dive (50% effort)

Goal: fill in the actual evidence for each sub-question.

1. Break the topic into 3–7 sub-questions (think: "what would the PPT need?").
2. For each sub-question, run 2–3 precise queries. Prefer high-tier sources (see `references/source-tiers.md`).
3. For each relevant page: fetch full content (WebFetch / Firecrawl), extract the specific claim + exact numbers + publication date.
4. Keep a running log: `claim | source | tier | date | confidence`.

Stop conditions:
- Each sub-question has at least one ★★★★+ source
- OR: 3 rounds of queries exhausted and nothing primary surfaced → mark as "not found in available sources"

### Round 3 — Cross-validation (30% effort)

Goal: upgrade confidence where possible, surface contradictions honestly.

1. For each claim with only one source: run one more search specifically for "disagreement" — e.g. add "criticism", "controversy", "revised estimate" to the query.
2. For key numbers: verify against at least one independent source. If ≥2 sources agree → confidence = high. If only 1 → confidence = medium. If sources disagree → confidence = low, both listed.
3. Check dates. A 2018 stat used for a 2026 briefing is a red flag unless it's a historical reference.

---

## Output format

See `references/brief-schema.md` for the full schema. Summary:

**Human-readable markdown** — findings listed with tier tags + dates + source links.

**Machine-readable JSON block** (fenced code block at end of brief) — consumable by downstream skills. Fields:
```json
{
  "topic": "...",
  "scope": "...",
  "time_window": "YYYY-MM-DD → YYYY-MM-DD",
  "overall_confidence": "high | medium | low",
  "findings": [
    { "claim": "...", "evidence": "...", "source_url": "...", "source_title": "...",
      "tier": 5, "date": "YYYY-MM", "confidence": "high" }
  ],
  "contradictions": [
    { "topic": "...", "source_a": "...", "source_b": "...", "resolution": "..." }
  ],
  "gaps": [ "what we couldn't find and why" ]
}
```

The PPT generator (`evyd-ppt-generator`) reads this JSON directly when building
content.json for research-backed decks.

---

## Anti-patterns (don't do these)

- **Stacking low-tier sources to fake authority**: 5 blog posts saying the same thing ≠ one primary source. Tier-based confidence must be honest.
- **Citing the first Google result**: WebSearch returns SEO-optimized, not truth-optimized. Always filter for tier before extracting.
- **Paraphrasing away nuance**: "Epic has 40% market share" — where? when? defined how? The brief keeps the scope qualifiers.
- **Hiding uncertainty**: if you're unsure, say "medium confidence" in the tag. Never promote an assumption to "high" to make the brief look stronger.
- **Running research when user has content**: research is opt-in. If the user gave you a full outline + data, don't re-research out of habit. Ask first.

---

## Typical session length

| Task size | Rounds | Total queries | Wall time |
|---|---|---|---|
| Single fact check | 1 | 2–3 | 2 min |
| Narrow topic (one slide's worth) | 2 | 6–10 | 10 min |
| Wide topic (half a deck) | 3 full rounds | 20–30 | 30–45 min |
| Comprehensive review (full deck) | Multi-topic, each 3 rounds | 50+ | 1–2 hr |

If the request looks >1 hr, break it into sub-topics and surface the plan to the user before starting.

---

## References (read before running)

- `references/source-tiers.md` — 5-level credibility rubric with domain-specific examples (healthcare SG, fintech regulation, academic, market research)
- `references/search-playbook.md` — round-by-round query templates + stop conditions
- `references/brief-schema.md` — full output schema (markdown structure + JSON fields)
- `references/mcp-setup.md` — how to enable Exa / Firecrawl / Jina MCPs when API tokens are available
