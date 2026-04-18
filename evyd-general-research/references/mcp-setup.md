# MCP Setup — Exa & Firecrawl / Jina

Placeholders for semantic search (Exa) and clean page extraction (Firecrawl or
Jina Reader). The skill works without these — WebSearch + WebFetch are adequate
for most queries. These MCPs raise the quality floor when you need:
- Exa: better-than-SEO search for exploratory / semantic queries
- Firecrawl/Jina: reliable markdown extraction for JS-heavy pages and PDFs

> **Status**: not yet configured. Tokens available — drop them into the
> config blocks below when ready, remove the `TODO` lines, commit.

---

## ① Exa — semantic search

Exa (<https://exa.ai>) searches for "pages that talk about X" semantically
rather than "pages matching keyword X". Dramatically better for exploratory
queries like "find case studies about hospitals rolling back Epic deployments".

### When to use

- Exploratory research (Round 1 scoping): replace WebSearch
- Finding non-obvious primary sources a keyword search misses
- Cross-lingual topic discovery

### When NOT to use

- Looking for a specific known URL (just fetch it)
- Fact-check of a specific known claim (WebSearch with exact phrase is fine)
- Inside known trusted domains (use `site:` with WebSearch)

### Setup

1. Get API key from <https://dashboard.exa.ai>
2. Add to repo-level `.mcp.json` (create if absent):

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "TODO-paste-exa-key-here"
      }
    }
  }
}
```

3. Restart the Claude Code session. Verify with:
   ```
   /mcp
   ```
   You should see `exa` listed as connected.

4. Tools become available as `mcp__exa__search`, `mcp__exa__get_contents`,
   `mcp__exa__find_similar`. The skill auto-detects and prefers these.

### Rate limits / cost

- Exa base plan: 1000 searches/month
- Each "deep" research session (3 rounds) typically uses 10–30 Exa calls
- Budget for ~30 sessions/month on base plan

---

## ② Firecrawl — clean markdown extraction

Firecrawl (<https://firecrawl.dev>) turns any web page into clean markdown,
handling JavaScript rendering, PDFs, and pagination. Solves the `WebFetch`
failure mode where you get back raw HTML + JS blobs.

### When to use

- Government portals (often JS-rendered: MOH, IMDA, MAS)
- PDF documents (annual reports, policy papers, academic PDFs)
- Single-page apps where WebFetch returns nothing useful
- Scraping a whole section of a site (Firecrawl has `crawl` mode)

### Setup

1. Get API key from <https://firecrawl.dev>
2. Add to repo-level `.mcp.json`:

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "TODO-paste-firecrawl-key-here"
      }
    }
  }
}
```

3. Restart and verify via `/mcp`.

4. Primary tool: `mcp__firecrawl__scrape` (single URL → clean markdown).
   Advanced: `mcp__firecrawl__crawl` (whole site → batched markdown).

### Alternative: Jina Reader (free tier, simpler)

Jina Reader (<https://jina.ai/reader>) is a lighter-weight alternative.
No API key required for low-volume use.

```json
{
  "mcpServers": {
    "jina": {
      "command": "npx",
      "args": ["-y", "jina-reader-mcp"]
    }
  }
}
```

Tool: `mcp__jina__read_url`. Same use case as Firecrawl scrape, slightly less
reliable on heavy JS pages but no token needed.

### Choice between them

- High-volume / reliable / corporate use → **Firecrawl**
- Occasional use / free / just works → **Jina Reader**
- Run both? No benefit. Pick one.

---

## ③ Composite `.mcp.json` (when both tokens ready)

When you have both Exa and Firecrawl tokens, the full config is:

```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "TODO-paste-exa-key-here"
      }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "TODO-paste-firecrawl-key-here"
      }
    }
  }
}
```

Drop this into `.mcp.json` at repo root. Do **not** commit the tokens. Best practice:

1. Commit a `.mcp.json.template` with `TODO-paste-*-here` placeholders
2. Add `.mcp.json` to `.gitignore`
3. Each dev copies the template locally and fills in their own tokens

---

## Tool-preference logic in the skill

`SKILL.md` says:

> Check which tools are available in this session and prefer in order:
> 1. Exa MCP
> 2. Firecrawl / Jina Reader MCP
> 3. WebSearch (built-in)
> 4. WebFetch (built-in)

In practice this means when running the skill:

```
# Round 1 — scoping
if mcp__exa__search available:  use it for all 3-5 scoping queries
else:                            use WebSearch

# Round 2 — fetching full content of candidate pages
if mcp__firecrawl__scrape available:  use it for all fetches
elif mcp__jina__read_url available:   use it
else:                                   use WebFetch (with degraded quality on JS pages)

# Round 3 — cross-validation
if mcp__exa__find_similar available:  use it to find alternative sources for key claims
else:                                   use WebSearch with "alternative estimate" / "criticism" suffixes
```

The skill should always print at the start which tools are being used:

```
Tools: WebSearch ✓ / WebFetch ✓ / Exa ✗ / Firecrawl ✗ / Jina ✗
(running in fallback mode — expect lower source quality on JS-heavy sites)
```

That way, the research brief's `tools_used` field is traceable.

---

## When you add a new research MCP

Update:
1. `SKILL.md` — tool preference order
2. `references/search-playbook.md` — query hygiene (if the new tool has syntax quirks)
3. `references/brief-schema.md` — no change, tools_used is free-form
4. This file — how to set it up + when to use

Don't add an MCP just because it exists. Each new tool adds cognitive load; the
AI has to pick between them every call. Prefer 2–3 well-understood tools over
a swiss-army kit.
