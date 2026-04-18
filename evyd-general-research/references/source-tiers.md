# Source Tiers — 5-level credibility rubric

Every claim in a research brief carries a tier tag. Tiers are domain-aware:
a ★★★★★ source for healthcare regulation is different from a ★★★★★ source for
consumer tech trends.

Rule: **when a higher-tier source exists for the same fact, cite it. Never stack
low-tier sources as a substitute for one high-tier source.**

---

## Universal tier rubric

| Tier | Label | Typical qualities |
|---|---|---|
| **★★★★★** | Primary / authoritative | Original data or rule-setter; direct producer of the fact |
| **★★★★** | Expert / vetted secondary | Peer-reviewed, audited, institutionally accountable |
| **★★★** | Reputable media / disclosure | Named author + editorial process; company official statements |
| **★★** | Industry-aware commentary | Analyst firms, industry blogs, podcasts with transcripts |
| **★** | Unverified / anonymous | Forum posts, social media threads, AI-generated content summaries |

Downgrade by one star if the source is:
- >3 years old for a fast-moving topic (tech/AI/regulation)
- Geography mismatch (a US blog cited for a SG fact)
- Clearly promotional (vendor case study, press release quoting only themselves)

---

## By domain

### Healthcare — Singapore / SEA

| Tier | Examples |
|---|---|
| ★★★★★ | MOH Singapore (moh.gov.sg), IHiS / Synapxe, HSA Singapore, WHO, WHO SEARO, Singapore Government Gazette, parliamentary hansards |
| ★★★★ | SingHealth / NUHS / NHG official publications, peer-reviewed journals (Lancet, NEJM, JAMIA, Singapore Medical Journal), Oxford Population Health |
| ★★★ | The Straits Times health desk, CNA, Reuters Health, named analyst reports (Frost & Sullivan SEA healthcare) |
| ★★ | Industry blogs (Mobihealth News, Healthcare IT News), vendor-authored whitepapers, LinkedIn posts by named executives |
| ★ | Reddit r/medicine, anonymous forum threads, press releases without named authors, vendor case studies with no named customer |

### Healthcare — US (comparison reference)

| Tier | Examples |
|---|---|
| ★★★★★ | HHS, FDA, CMS, ONC, NIH, CDC, peer-reviewed journals (NEJM, JAMA, Health Affairs) |
| ★★★★ | KLAS Research, ECRI, Advisory Board, academic medical center publications |
| ★★★ | WSJ / NYT / Reuters health desks, STAT News, Becker's Hospital Review |
| ★★ | Healthcare IT News, industry analyst blogs |
| ★ | Twitter/X threads, anonymous Reddit |

### Regulation / policy — AI & data

| Tier | Examples |
|---|---|
| ★★★★★ | EU AI Act (eur-lex), US NIST AI RMF, Singapore IMDA AI Verify, China CAC, UK AI Safety Institute |
| ★★★★ | OECD AI Principles, G7 Hiroshima Process, Oxford / Stanford AI index reports |
| ★★★ | Reuters / Bloomberg policy desks, Politico, FT AI coverage |
| ★★ | Law firm bulletins (Baker McKenzie, Clifford Chance), think-tank commentaries |
| ★ | Twitter legal commentary, non-attributed policy summaries |

### Fintech / financial regulation

| Tier | Examples |
|---|---|
| ★★★★★ | MAS Singapore, BIS, IMF, SEC, FINRA, company SEC filings (10-K / 10-Q) |
| ★★★★ | IOSCO publications, academic finance journals, McKinsey Global Institute |
| ★★★ | Reuters, Bloomberg, FT, WSJ, The Banker |
| ★★ | CoinDesk (crypto), Fintech Futures, named analyst notes |
| ★ | Telegram / Discord signal groups, unverified Medium posts |

### Market sizing / industry data

| Tier | Examples |
|---|---|
| ★★★★★ | National statistical offices (SingStat, US Census), World Bank data, OECD stat portal |
| ★★★★ | Named McKinsey / BCG / Bain reports, Gartner / IDC with methodology, peer-reviewed industry studies |
| ★★★ | Statista (when citing underlying source), press releases from public companies with audited data |
| ★★ | Paid "market research" reports without methodology (Grand View, IMARC, Mordor — caveat before citing) |
| ★ | AI-generated "top 10 market" listicles, blog-aggregated stats without original source |

### Academic / technical (AI, CS, clinical)

| Tier | Examples |
|---|---|
| ★★★★★ | Peer-reviewed journals, NeurIPS/ICML/ACL (peer-reviewed track), JAMIA, Lancet Digital Health |
| ★★★★ | ArXiv preprints from established labs (OpenAI, DeepMind, Anthropic, FAIR, MIT CSAIL, etc.), official model cards, reproducible eval benchmarks (MMLU, HumanEval, MedQA) |
| ★★★ | Lab blog posts accompanying papers, conference workshop papers |
| ★★ | Medium / Substack technical posts by named practitioners, hacker news commentary |
| ★ | Anonymous blog posts, LLM-summarized research claims |

### Chinese-language sources (when topic needs)

| Tier | Examples |
|---|---|
| ★★★★★ | 国家卫健委 (NHC), 药监局 (NMPA), 工信部 (MIIT), 国务院政策文件, 学术期刊（新英格兰医学杂志中文版、中华医学杂志） |
| ★★★★ | 央视新闻, 新华社, 丁香园学术板块, 36氪研究院报告 |
| ★★★ | 财新, 第一财经, 虎嗅深度, 知乎盐选专栏（带作者身份） |
| ★★ | 36氪快讯, 钛媒体, 普通知乎回答 |
| ★ | 百家号, 自媒体微信公众号（无作者背景）, 小红书笔记 |

---

## Handling source conflicts

When two sources of the same tier disagree on a factual claim:

1. Check dates — newer wins if the fact is time-sensitive (market sizes, regulations)
2. Check scope — "Singapore EHR market" ≠ "SEA EHR market"; often not a real conflict
3. Check methodology — if one source discloses methodology and the other doesn't, the disclosed one wins
4. If still unresolved: **report both in the brief under `contradictions`**, state which I'd pick and why, let the user decide

When a ★★★★★ source and a ★★★ source disagree:
- The ★★★★★ source usually wins, unless it's clearly outdated for a fast-moving topic
- Never bury the ★★★ as if it didn't exist — mention it as "popular interpretation" if widespread

---

## Source-tier output format in briefs

Every claim in a research brief ends with: `[<tier> · <date>]`

Examples:
- `[★★★★★ · 2024-11]` — primary, recent
- `[★★★ · 2023-03]` — reputable media, older
- `[★★★★ · n.d.]` — expert source without clear date (flag as caveat)

When citing a source explicitly, use this template:
```
Source: <Title> — <Publisher> [<tier> · <date>]
URL: <link>
```
