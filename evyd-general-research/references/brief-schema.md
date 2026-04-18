# Research Brief — Output Schema

Every research session ends with a brief in this exact format: **markdown for
humans + a JSON block for downstream skills**. Both must be consistent.

Output target: `/tmp/<topic-slug>-brief.md` (overwrite allowed within session).

---

## Markdown structure

```markdown
# Research Brief — <Topic in one sentence>

**Scope**: <what was researched and what was not>
**Time window**: <when searches ran, e.g. 2026-04-18>
**Tools used**: WebSearch ✓ / WebFetch ✓ / Exa ✓ / Firecrawl ✗
**Overall confidence**: high | medium | low
**Queries run**: <count>

## Summary (≤ 5 sentences)

<Plain-language TL;DR. No jargon, no hedging beyond the confidence tag.>

## Key findings

### <Sub-question 1>

**Claim**: <specific, measurable statement with qualifiers intact>
**Evidence**: <1-3 sentence distillation of what the source says>
**Source**: [<title>](<url>) — <publisher> [★★★★★ · 2024-11]
**Confidence**: high

### <Sub-question 2>

... (repeat per sub-question)

## Contradictions & open questions

### <Contradiction topic>

- **Source A**: [<title>](<url>) — [★★★★ · 2024-06] says X
- **Source B**: [<title>](<url>) — [★★★★ · 2024-10] says Y
- **My read**: <one sentence: which I'd pick and why, OR "unresolved, flag to user">

## Gaps — what we could NOT find

- <specific thing you looked for, what you tried, why it didn't surface>
- <...>

## Source inventory

- ★★★★★ <title> — <publisher> — <url>
- ★★★★ <title> — <publisher> — <url>
- ... (every source cited above)

---

```json
<machine-readable block — see JSON schema below>
```
```

---

## JSON block schema

The last block in every brief is a fenced `json` code block. Downstream
skills (e.g. `evyd-ppt-generator`) parse this directly.

```json
{
  "topic": "Singapore digital health market size",
  "scope": "Market sizing for SG digital health, FY2024, public + private spend",
  "time_window": "2026-04-18",
  "tools_used": ["WebSearch", "WebFetch"],
  "overall_confidence": "medium",
  "queries_run": 14,

  "findings": [
    {
      "sub_question": "Total market size",
      "claim": "Singapore digital health market = S$3.8B in FY2024",
      "evidence": "MOH Budget Speech 2024 listed digital health allocation of S$3.8B for financial year 2024, including Healthier SG transformation budget.",
      "source_url": "https://www.moh.gov.sg/...",
      "source_title": "MOH Committee of Supply Debate 2024 — Budget Speech",
      "publisher": "Ministry of Health, Singapore",
      "tier": 5,
      "date": "2024-02",
      "confidence": "high"
    },
    {
      "sub_question": "Growth rate",
      "claim": "Digital health CAGR 14% from 2020 to 2024",
      "evidence": "Frost & Sullivan SEA healthcare IT report estimates 14% CAGR based on tracked vendor revenues; methodology section clarifies bottom-up vendor survey.",
      "source_url": "https://...",
      "source_title": "SEA Healthcare IT Forecast 2024",
      "publisher": "Frost & Sullivan",
      "tier": 4,
      "date": "2024-06",
      "confidence": "medium"
    }
  ],

  "contradictions": [
    {
      "topic": "Vendor market share — Synapxe vs private sector",
      "source_a": {
        "title": "Synapxe Annual Report 2023",
        "claim": "Synapxe handles 80%+ public health IT",
        "tier": 5, "date": "2024-01"
      },
      "source_b": {
        "title": "Frost & Sullivan SEA Report",
        "claim": "Public-private split is 60/40",
        "tier": 4, "date": "2024-06"
      },
      "resolution": "Likely not a true contradiction — Synapxe figure is for public-cluster IT services specifically, F&S figure is for total digital health spend including devices and apps. I'd note both with scope qualifiers."
    }
  ],

  "gaps": [
    {
      "question": "Private telehealth market size (Doctor Anywhere, MyDoc, etc.)",
      "why_not_found": "Private telehealth companies in SG don't file public financials; no analyst covers this slice at sub-segment depth. Would need direct company interviews."
    }
  ]
}
```

---

## Field specs

### `findings[]`

| Field | Required | Type | Notes |
|---|---|---|---|
| `sub_question` | yes | string | One of the 3-7 sub-questions scoped in pre-flight |
| `claim` | yes | string | The atomic factual statement. Keep scope qualifiers. |
| `evidence` | yes | string | 1-3 sentence distillation. Don't paraphrase away specifics. |
| `source_url` | yes | string | Direct URL to the page where the fact lives |
| `source_title` | yes | string | Exact page title |
| `publisher` | yes | string | Organization, not the author |
| `tier` | yes | integer 1-5 | Per `source-tiers.md` |
| `date` | yes | string | YYYY-MM or YYYY-MM-DD. Use "n.d." only if truly undated (flag in brief). |
| `confidence` | yes | "high" / "medium" / "low" | Based on source count + agreement |

### `contradictions[]`

| Field | Required | Type | Notes |
|---|---|---|---|
| `topic` | yes | string | Short name for the disagreement |
| `source_a`, `source_b` | yes | object | Subset of finding schema |
| `resolution` | yes | string | Either "I'd pick X because…" or "unresolved — flag to user" |

### `gaps[]`

| Field | Required | Type | Notes |
|---|---|---|---|
| `question` | yes | string | What we were looking for |
| `why_not_found` | yes | string | What was tried, what the barrier was |

### Top-level `overall_confidence`

- **high**: ≥70% of findings are high-confidence AND no unresolved contradictions
- **medium**: some findings medium/low, but answers exist for all sub-questions
- **low**: major gaps OR unresolved high-impact contradictions

---

## How downstream skills consume this

### `evyd-ppt-generator` integration

When the PPT skill is generating a research-backed deck, it:
1. Reads the latest `/tmp/*-brief.md` (or user-specified path)
2. Parses the JSON block at the end
3. Maps findings to slide content:
   - `stat_highlight` slides pull numbers from high-confidence findings
   - `comparison_table` slides pull from findings with consistent structure
   - `chart` slides consume numeric findings with methodology notes
   - Low-confidence findings get an italic caveat footnote
   - Contradictions become a dedicated `two_column_check` or `comparison_table` slide
   - Gaps show up in the ending slide as "open questions"
4. Every source cited in a slide's `footnote` references the `source_url` + tier

### Future consumers

Any skill that needs vetted data should read this JSON schema, not re-run research. The brief is the contract.

---

## Brief hygiene

- **Don't inflate**: if a finding is medium-confidence, say so. Downstream skills will render it with caveats.
- **Don't collapse**: "Singapore EHR market = S$1.2B" is not the same as "Singapore digital health market = S$3.8B". Keep sub-question granularity.
- **Don't promote**: the brief is the evidence layer; recommendations / opinions belong in the downstream deliverable, not here.
- **Do version**: if you re-run research later, use `topic-slug-v2.md` — don't silently overwrite earlier briefs unless the user asks.
