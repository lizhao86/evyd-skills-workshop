# MCP Connections Checklist

These MCP connections use OAuth and must be connected manually by the user through the Claude Code UI.

## How to Connect MCP Services

In Claude Code, MCP connections are managed via the sidebar or the `/mcp` command. Most connections use browser-based OAuth — Claude Code will open a browser window for you to authorize.

---

## 1. Atlassian (Jira + Confluence)

**What it provides:** Read/write access to Jira issues, Confluence pages, search, comments, transitions.

**How to connect:**
1. In Claude Code, the Atlassian MCP connector is built-in
2. When you first use a Jira/Confluence tool, Claude Code will prompt you to authenticate
3. Click the OAuth link and authorize with your Atlassian account
4. Select the Atlassian site (e.g., `yourteam.atlassian.net`)

**Verify:**
```
Ask Claude: "list my Jira projects" or "search Jira for recent issues"
```

---

## 2. Gmail

**What it provides:** Read emails, search messages, create drafts, read threads.

**How to connect:**
1. The Gmail MCP connector is built-in to Claude Code
2. When you first use a Gmail tool, you'll be prompted to authenticate
3. Authorize with your Google account via browser OAuth
4. Grant the requested permissions (read, compose)

**Verify:**
```
Ask Claude: "search my recent emails" or "show my Gmail profile"
```

---

## 3. Figma

**What it provides:** Read design files, get screenshots, inspect nodes, access design tokens and variables.

**How to connect:**
1. Figma MCP is available as a built-in connector
2. Authenticate via Figma OAuth when first using a Figma tool
3. Grant read access to your Figma files

**Verify:**
```
Ask Claude: "get a screenshot of [Figma URL]" or use /figma commands
```

---

## 4. Granola

**What it provides:** Access meeting notes, transcripts, search across meetings, query meeting content.

**How to connect:**
1. Granola MCP is available as a built-in connector
2. Authenticate via Granola OAuth when prompted
3. Grant access to your meeting notes

**Verify:**
```
Ask Claude: "list my recent meetings" or "query my meetings about [topic]"
```

---

## Connection Status Check

After connecting all services, run `/mcp` in Claude Code to verify all servers are online:

```
Expected output:
  ✓ Atlassian — connected
  ✓ Gmail — connected  
  ✓ Figma — connected
  ✓ Granola — connected
```

If any service shows as disconnected, try:
1. Re-run the OAuth flow by using a tool from that service
2. Check your network connection (especially behind corporate firewall)
3. Verify your account has the necessary permissions
