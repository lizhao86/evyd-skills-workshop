# Channel: jira + community-mcp

> 场景：通过社区开源 MCP Server（sooperset/mcp-atlassian）写入 Jira。适用于非 Claude Code 环境（OpenClaw、Cursor 等）。

## 前置条件

1. 安装 sooperset/mcp-atlassian：`uvx mcp-atlassian` 或 Docker
2. 配置 Atlassian API Token：
   - 在 https://id.atlassian.com/manage-profile/security/api-tokens 生成 token
   - 配置到 MCP server 环境变量（`ATLASSIAN_URL`、`ATLASSIAN_USERNAME`、`ATLASSIAN_API_TOKEN`）
3. 在 MCP 客户端中注册该 server

验证可用：调用 server 的 Jira 相关工具，若返回结果则正常。

## Config

```yaml
site: "evyd.atlassian.net"
default_project: "BACKLOG"
```

> ⚠️ 社区 MCP 不使用 cloudId，改用 site URL 认证。工具名称取决于 MCP server 注册名（如 `mcp__mcp-atlassian__jira_create_issue`），以实际配置为准。

## Skill 路由表

与 `jira-claude-mcp.md` 相同：

| Skill | 操作 | Issue Type | 备注 |
|---|---|---|---|
| evyd-requirement-breakdown | 创建 ticket | `Requirement` | Summary 格式: `[Platform] Module - Title` |
| evyd-user-story-writer | 创建 ticket | `Story` | link `split from` 上游 Requirement |
| evyd-ai-intention-brainstorm | 创建 ticket | `Story` | link `split from` 上游 Requirement |
| evyd-lofi-figma-maker | 添加 comment | — | 贴到关联的 Story |
| evyd-design-review | 添加 comment | — | 贴到关联的 Story / Requirement |

## Write Protocol — 创建 Ticket

1. 使用 server 提供的 issue 创建工具（参考 sooperset/mcp-atlassian 文档）：
   - project: `BACKLOG`
   - issue_type: `<按路由表>`
   - summary: `<标题>`
   - description: `<Markdown 正文>`
2. 记录返回的 issue key
3. 如需关联上游 Requirement，使用 server 提供的 link 创建工具：
   - link_type: `Work item split`
   - inward_issue: `<新建的 Story key>` (split from)
   - outward_issue: `<Requirement key>` (split to)

## Write Protocol — 添加 Comment

1. 确定目标 ticket key（关联策略同 `jira-claude-mcp.md`）
2. 使用 server 提供的 comment 添加工具：
   - issue_key: `<ticket key>`
   - body: `<Markdown 内容>`

## 关联策略

与 `jira-claude-mcp.md` 完全相同：自动 → 问用户 → 跳过并提醒。

## Format Constraints

与 `jira-claude-mcp.md` 相同。
