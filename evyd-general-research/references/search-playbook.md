# Search Playbook — 3-round method with templates

Concrete query templates + stop conditions. Use this after reading `SKILL.md`
for the high-level flow.

---

## Pre-flight

Before any search, write down explicitly:

```
Topic: <one sentence>
Downstream use: <PPT? Strategy doc? Fact check?>
Key dimensions: <3-5 things the brief must answer>
Hard constraints: <geography, time window, specificity>
```

If you can't fill these in, ask the user first. Research without scope is
the #1 way to burn an hour producing nothing.

---

## Round 1 — Scoping scan (20% effort)

**Goal**: map the landscape. Not to answer — to find where the answers live.

### Query template

For each dimension, generate 3 query variants:
1. **Literal**: exact phrase the user used
2. **Technical**: what an expert in the field would type
3. **Adversarial**: query phrased to surface counter-evidence or criticism

Example — topic: "Singapore digital health market size":

```
Q1  "Singapore digital health market size"                      # literal
Q2  "Singapore healthtech TAM 2024 forecast"                    # technical
Q3  "Singapore healthtech market skepticism OR overestimate"    # adversarial
```

### Tool preference (round 1)

- **Exa** if available: `search` with `category="company"` or `category="research paper"` when appropriate
- Else **WebSearch**: 2-3 variants of the main question

### What to extract in round 1

For each result page: **title + publisher + date + is-primary-source** (yes/no).
Don't go deep. Don't fetch full content yet. Just build a map.

Output mental model:
```
Primary sources found: [...]
Secondary sources found: [...]
Gaps (no good source yet): [...]
```

### Stop condition for round 1

- 3–5 queries run
- At least one ★★★★+ source identified per dimension (or explicitly marked as gap)
- Maximum 5 minutes

---

## Round 2 — Targeted deep dive (50% effort)

**Goal**: fill in specific evidence for each sub-question.

### Break the topic down first

Write 3–7 sub-questions the brief must answer. Example:

```
Topic: Singapore digital health market size
  S1. Total market size (S$) — latest
  S2. Growth rate (CAGR) — last 3-5 years
  S3. Segment breakdown (EHR / telehealth / wearables / AI diagnostics)
  S4. Top 5 vendors by share
  S5. Government spending vs private sector
```

### Query strategy per sub-question

For each sub-question:
1. One precise query targeted at a **specific primary source** you found in round 1.
   Example: `site:moh.gov.sg digital health spending FY2024`
2. One broad query on the sub-question itself:
   `Singapore EHR market segment 2024 MOH Synapxe`
3. If nothing primary surfaces after 2 queries, try: `"Singapore" "digital health" filetype:pdf 2024`

### Fetching full content

Once a page is identified as worth reading:
- Prefer **Firecrawl / Jina Reader MCP** (cleaner markdown output, handles JS & PDF)
- Fallback: **WebFetch** with a prompt like "Extract: the specific number for X, the methodology, the date"

### Running log

Keep a spreadsheet-like log as you go:

```
| Sub-Q | Claim found                             | Source            | Tier   | Date     | Confidence |
|-------|-----------------------------------------|-------------------|--------|----------|------------|
| S1    | Market size S$3.8B in 2024              | MOH Budget Speech | ★★★★★  | 2024-02  | high       |
| S2    | CAGR 14% 2020-24                        | F&S SEA Report    | ★★★★   | 2024-06  | medium     |
| S3    | EHR = 45% of spend                      | IHiS annual rpt   | ★★★★★  | 2024-01  | high       |
```

### Stop condition for round 2

- Each sub-question has at least one ★★★★+ source OR is marked "not found in available sources"
- Maximum 3 queries per sub-question (don't rabbit-hole)
- Total round-2 budget: 15–25 queries for a typical brief

---

## Round 3 — Cross-validation (30% effort)

**Goal**: raise confidence on key claims, surface contradictions.

### For each claim labeled "medium" or "high" confidence

Run ONE more query that specifically looks for disagreement:

Templates:
- `<claim> revised` — find if a number was later updated
- `<claim> criticism OR methodology OR overestimate` — find skeptics
- `<claim> <alternative source>` — triangulate from a different tier

Example:
```
Claim: "Singapore digital health market = S$3.8B in 2024"
Q: "Singapore digital health market size" revised estimate 2024-2025
Q: "Frost & Sullivan" "Singapore" methodology healthcare
```

### Upgrade / downgrade confidence

- Two ★★★★+ sources agree (within 10% for numbers) → **high confidence**
- Only one source → **medium confidence**
- Sources disagree significantly → **low confidence**, both listed in brief under `contradictions`

### Date freshness check

For each claim, compare source date to topic's time-sensitivity:
- Regulation / policy / pricing / market size → source must be ≤18 months old
- Academic benchmarks → ≤12 months (field moves fast)
- Historical narratives / biographical facts → no time limit
- Geography-locked facts → no time limit IF the source is authoritative

If a claim relies on a source that's too old, either (a) find a newer source or (b) flag it in the brief as "last verified [date]".

### Stop condition for round 3

- Every claim has: 2+ sources OR "medium/low confidence" tag
- Contradictions are documented
- Gaps are explicitly listed
- Total budget: 5–10 queries

---

## Query hygiene

### DO

- Use quotes for exact phrases: `"AI Verify framework"`
- Use `site:` to pin domain: `site:moh.gov.sg`
- Use `filetype:` for PDFs: `filetype:pdf "digital health masterplan"`
- Use Chinese keywords when the topic is China-relevant — WebSearch weights English, you'll miss 50% of Chinese-native content without it
- Add year anchors for fast-moving topics: `... 2024` or `... 2024..2025`

### DON'T

- Ask multi-part questions in one query — split them
- Use LLM-style long queries (`can you find me sources that discuss...`) — search engines aren't chatbots
- Query with opinions baked in (`why Epic is bad in Singapore`) — you get biased results; ask neutrally and let the evidence decide
- Trust a number unless you've seen the underlying source at least once (Statista often aggregates primary sources — go to the primary)

---

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Stacking blogs | 5 similar-worded blog posts, feels authoritative | Find the original primary source; most blogs are copies |
| Statista trap | Cited from Statista, not its underlying source | Open Statista, find the "Source:" line, cite that |
| Press release laundering | Vendor press release reported by industry rag, feels like third-party | Note both as ★★★, don't inflate |
| Geography creep | US study applied to SG without adjustment | Flag explicitly: "US data, directional only for SG" |
| Date confusion | Report published in 2024 but all figures from 2021 | Cite the figure date, not the report date |
| AI hallucination laundering | Another AI's summary repeated as fact | Always check: can I find the original? If not, discard |

---

## When to stop researching

Hard stops:
1. Every sub-question has an answer (with confidence label)
2. Budget limit reached (see `SKILL.md` typical session table)
3. User interrupts with "enough"

Soft signals that you're done:
- New queries return the same sources you've already used
- Confidence labels have stabilized
- You can write the brief without needing to "look up one more thing"

If you find yourself running query #30+ on a narrow topic, stop and ship the
brief with gaps honestly labeled. Over-researching is a procrastination tax.
