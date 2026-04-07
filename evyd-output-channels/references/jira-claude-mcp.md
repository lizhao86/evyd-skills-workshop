# Channel: jira + claude-mcp

> 场景：通过 Claude Code 内置 Atlassian MCP 写入 Jira（零配置，OAuth 绑定 claude.ai 账号）。

## 前置条件

- 使用 Claude Code（CLI / Desktop / Web）
- claude.ai 账号已授权 Atlassian OAuth

验证可用：调用任意 `mcp__claude_ai_Atlassian__*` 工具，若返回结果则正常。

## Config

```yaml
cloudId: "3420c790-a8e3-4d4c-96fa-44ceadf1fe5a"
site: "evyd.atlassian.net"
default_project: "BACKLOG"
```

## Skill 路由表

| Skill | 操作 | Issue Type | 备注 |
|---|---|---|---|
| evyd-requirement-breakdown | 创建 ticket | `Requirement` (id: 11113) | Summary 格式: `[Platform] Module - Title` |
| evyd-user-story-writer | 创建 ticket | `Story` (id: 11116) | link `split from` 上游 Requirement |
| evyd-ai-intention-brainstorm | 创建 ticket | `Story` (id: 11116) | link `split from` 上游 Requirement |
| evyd-lofi-figma-maker | 添加 comment | — | 贴到关联的 Story |
| evyd-design-review | 添加 comment | — | 贴到关联的 Story / Requirement |

## Write Protocol — 创建 Ticket

1. 调用 `mcp__claude_ai_Atlassian__createJiraIssue`：
   ```
   cloudId: "3420c790-a8e3-4d4c-96fa-44ceadf1fe5a"
   projectKey: "BACKLOG"
   issueTypeName: "<按路由表>"
   summary: "<标题>"
   description: "<Markdown 正文>"
   contentFormat: "markdown"
   ```
2. 记录返回的 issue key（如 `BACKLOG-456`）
3. 如需关联上游 Requirement，调用 `mcp__claude_ai_Atlassian__createIssueLink`：
   ```
   cloudId: "3420c790-a8e3-4d4c-96fa-44ceadf1fe5a"
   type: "Work item split"
   inwardIssue: "<新建的 Story key>"     # split from
   outwardIssue: "<Requirement key>"     # split to
   ```
4. 验证：调用 `mcp__claude_ai_Atlassian__getJiraIssue` 确认 ticket 已创建

## Write Protocol — 添加 Comment

1. 确定目标 ticket key：
   - 优先：上下文中已知的关联 ticket key
   - 其次：问用户 "请提供关联的 Jira ticket key（如 BACKLOG-xxx），或输入'跳过'"
   - 跳过：fallback 到 Active Config 中的其他渠道，并提醒 "此输出未关联 Jira ticket"
2. 调用 `mcp__claude_ai_Atlassian__addCommentToJiraIssue`：
   ```
   cloudId: "3420c790-a8e3-4d4c-96fa-44ceadf1fe5a"
   issueIdOrKey: "<ticket key>"
   commentBody: "<Markdown 内容>"
   contentFormat: "markdown"
   ```

## 关联策略（统一）

确定上游 Requirement ticket 的优先级：
1. **自动**：当前对话中刚由 `evyd-requirement-breakdown` 创建 → 直接使用其 issue key
2. **问用户**：无上下文线索 → "请提供关联的 Requirement ticket key（如 BACKLOG-xxx），或输入'跳过'不关联"
3. **跳过**：用户选择跳过 → 创建 ticket 但不建立 link，提醒 "此 ticket 未关联 Requirement，可后续手动 link"

## Format Constraints

- Jira 渲染器支持 Markdown（标题、列表、表格、代码块）
- contentFormat 始终传 `"markdown"`
- Summary 字段不支持 Markdown，纯文本
- Requirement 类型的 Summary 必须遵循格式：`[Platform Name] Module - Requirement Title`
