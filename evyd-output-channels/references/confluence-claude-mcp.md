# Channel: confluence + claude-mcp

> 场景：通过 Claude Code 内置 Atlassian MCP 写入 Confluence 页面（零配置，OAuth 绑定 claude.ai 账号）。

## 前置条件

- 使用 Claude Code（CLI / Desktop / Web）
- claude.ai 账号已授权 Atlassian OAuth

验证可用：调用任意 `mcp__claude_ai_Atlassian__*` 工具，若返回结果则正常。

## Config

```yaml
cloudId: "3420c790-a8e3-4d4c-96fa-44ceadf1fe5a"
site: "evyd.atlassian.net"
```

## Skill 路由表

| Skill | Space | 默认 Parent Page | 可覆盖 |
|---|---|---|---|
| evyd-competitor-research | `EPT1` (EVYD Product Team) | `298156068` (Overall Landscape) | 否 |
| evyd-user-manual | `BPS` | `1783070722` (To Be Moved) | 是，用户可指定 |

## Write Protocol

1. 调用 `mcp__claude_ai_Atlassian__createConfluencePage`：
   ```
   cloudId: "3420c790-a8e3-4d4c-96fa-44ceadf1fe5a"
   spaceId: "<按路由表>"
   parentId: "<按路由表，或用户指定>"
   title: "<标题>"
   body: "<Markdown 正文>"
   contentFormat: "markdown"
   status: "current"
   ```
2. 记录返回的 page id 和 webUrl
3. 验证：调用 `mcp__claude_ai_Atlassian__getConfluencePage` 确认页面已创建且非空
4. 向用户返回页面链接

## Override 机制

当用户主动指定目标位置时（如 "写到 BHMPD space" 或提供 Confluence URL），从用户输入中提取 spaceId / parentId，覆盖路由表默认值。

## Format Constraints

- Confluence 支持 Markdown（标题、列表、表格、代码块）
- contentFormat 始终传 `"markdown"`
- 注意：Confluence Markdown 渲染对复杂嵌套表格支持有限，尽量保持表格结构简单

## File Naming Convention

```
{Type} - {Title} - {YYYYMMDD}
```

- `{Type}` — 由各 skill 自定义（如 `Research`、`Manual`）
- `{Title}` — 从内容派生的简短标题
- `{YYYYMMDD}` — 创建日期
