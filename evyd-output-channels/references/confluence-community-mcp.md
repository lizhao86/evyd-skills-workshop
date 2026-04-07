# Channel: confluence + community-mcp

> 场景：通过社区开源 MCP Server（sooperset/mcp-atlassian）写入 Confluence 页面。适用于非 Claude Code 环境（OpenClaw、Cursor 等）。

## 前置条件

1. 安装 sooperset/mcp-atlassian：`uvx mcp-atlassian` 或 Docker
2. 配置 Atlassian API Token：
   - 在 https://id.atlassian.com/manage-profile/security/api-tokens 生成 token
   - 配置到 MCP server 环境变量（`ATLASSIAN_URL`、`ATLASSIAN_USERNAME`、`ATLASSIAN_API_TOKEN`）
3. 在 MCP 客户端中注册该 server

验证可用：调用 server 的 Confluence 相关工具，若返回结果则正常。

## Config

```yaml
site: "evyd.atlassian.net"
```

> ⚠️ 社区 MCP 不使用 cloudId，改用 site URL 认证。工具名称取决于 MCP server 注册名（如 `mcp__mcp-atlassian__confluence_create_page`），以实际配置为准。

## Skill 路由表

与 `confluence-claude-mcp.md` 相同：

| Skill | Space | 默认 Parent Page | 可覆盖 |
|---|---|---|---|
| evyd-competitor-research | `EPT1` (EVYD Product Team) | `298156068` (Overall Landscape) | 否 |
| evyd-user-manual | `BPS` | `1783070722` (To Be Moved) | 是，用户可指定 |

## Write Protocol

1. 使用 server 提供的页面创建工具（参考 sooperset/mcp-atlassian 文档）：
   - space_key: `<按路由表>`
   - parent_id: `<按路由表，或用户指定>`
   - title: `<标题>`
   - body: `<Markdown 正文>`
2. 记录返回的 page id 和 URL
3. 验证页面已创建且非空
4. 向用户返回页面链接

## Override 机制

与 `confluence-claude-mcp.md` 相同：用户主动指定时覆盖路由表默认值。

## Format Constraints

与 `confluence-claude-mcp.md` 相同。

## File Naming Convention

```
{Type} - {Title} - {YYYYMMDD}
```
