---
name: evyd-output-channels
description: Output channel protocols for writing skill results to Feishu, Obsidian, local Markdown, Jira, or Confluence. Use when a skill needs to write output and must follow the correct write protocol, format constraints, and file naming convention for the active channel.
---

# EVYD Output Channels

Shared output protocol for all EVYD skills.

## Active Config

```yaml
destination: feishu      # feishu | obsidian | local-markdown | jira | confluence
executor: lark-cli       # lark-cli | openclaw | local-fs | claude-mcp | community-mcp
```

改这两行即可切换全部 skill 的输出方式。
- `destination` — 写到哪里
- `executor` — 用什么工具写

### Executor 环境说明

| executor | 运行环境 | 认证方式 | 安装要求 |
|---|---|---|---|
| `lark-cli` | 用户本机 | lark-cli 配置 | 需安装 lark-cli |
| `openclaw` | 飞书机器人 | OpenClaw 接口 | 待接入 |
| `local-fs` | 本机文件系统 | 无 | 无 |
| `claude-mcp` | Anthropic 云端 | claude.ai OAuth | 需 Claude Code，零配置 |
| `community-mcp` | 用户本机 | Atlassian API Token | 需安装 sooperset/mcp-atlassian |

## Channel map

Read the Active Config above, then load the matching reference file only.

| destination | executor | Reference |
|---|---|---|
| `feishu` | `lark-cli` | `references/feishu-lark-cli.md` |
| `feishu` | `openclaw` | `references/feishu-openclaw.md` |
| `obsidian` | `local-fs` | `references/obsidian-local-fs.md` |
| `local-markdown` | `local-fs` | `references/local-markdown-local-fs.md` |
| `jira` | `claude-mcp` | `references/jira-claude-mcp.md` |
| `jira` | `community-mcp` | `references/jira-community-mcp.md` |
| `confluence` | `claude-mcp` | `references/confluence-claude-mcp.md` |
| `confluence` | `community-mcp` | `references/confluence-community-mcp.md` |

Do not load all files. Load only the one that matches.

## Per-skill routing（Jira / Confluence 专用）

Jira 和 Confluence 渠道按 skill 分别路由到不同操作，详见各 reference 文件中的 Skill 路由表。摘要：

| Skill | Jira 操作 | Confluence 操作 |
|---|---|---|
| evyd-competitor-research | — | 创建页面 → EPT1 / Overall Landscape |
| evyd-requirement-breakdown | 创建 Requirement ticket | — |
| evyd-user-story-writer | 创建 Story ticket + link Requirement | — |
| evyd-ai-intention-brainstorm | 创建 Story ticket + link Requirement | — |
| evyd-lofi-figma-maker | Comment 贴到关联 ticket | — |
| evyd-user-manual | — | 创建页面 → BPS / To Be Moved（可覆盖） |
| evyd-design-review | Comment 贴到关联 ticket | — |
| evyd-pd-roadmap | —（继续飞书多维表） | — |
| evyd-ppt-generator | —（本地文件输出） | — |
