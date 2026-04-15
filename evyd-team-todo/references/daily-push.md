# 每日待办推送配置

## 概述

通过 OpenClaw cron job 定时读取 `todo/team-todo.md`，为每位成员生成个人待办摘要并推送。

**渠道无关**：推送依赖 OpenClaw cron 的 `delivery` 机制路由到具体渠道（企微、飞书、Telegram、webchat 等），skill 本身不绑定任何渠道。

## 架构

```
cron job (per member)
  ├─ schedule: 定时触发
  ├─ payload: agentTurn → 读数据 + 格式化输出
  └─ delivery: announce → 路由到目标渠道
```

每位成员一个独立 cron job。不共用 job，因为：
- 每人的推送渠道/语言可能不同
- 独立 job 便于单独启停、调试
- 失败不影响其他成员

## Cron Job 配置模板

```json
{
  "name": "{姓名} 每日待办推送",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "30 8 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "<见下方 prompt 模板>",
    "timeoutSeconds": 90
  },
  "delivery": {
    "mode": "announce",
    "channel": "<渠道名>",
    "to": "<渠道:userid>"
  }
}
```

### 字段说明

| 字段 | 说明 | 示例 |
|---|---|---|
| `schedule.expr` | cron 表达式，默认每天 08:30 | `30 8 * * *` |
| `schedule.tz` | 时区 | `Asia/Shanghai` |
| `sessionTarget` | 固定 `isolated`（隔离 session，不污染主会话） | `isolated` |
| `delivery.mode` | 固定 `announce`（由系统投递结果） | `announce` |
| `delivery.channel` | 目标渠道名 | `wecom` / `telegram` / `feishu` |
| `delivery.to` | 渠道内的目标地址 | `wecom:149681207` / `telegram:123456` |

### Prompt 模板

**中文版（默认）：**

```
读取文件 {workspace}/todo/team-todo.md，找到「## {姓名}」section。今天日期用于计算标记：Due<今天=⚠️P0, Due=今天=P1, Due=明天=P2。

你的完整输出必须严格是以下格式，不得有任何额外文字、解释、思考或前言：

📋 你的待办（{N}条未完成）：

{编号}. {任务内容} | Due:{YYYY-MM-DD} {⚠️P0/P1/P2标记，无则不加}
{编号}. {任务内容} | No Due Date

搞完了跟我说，我帮你删。

规则：
- N只计 [ ] 和 [~] 条目，不计 [x]
- [~] 条目加 [~] 前缀
- 按Due从近到远排序，无Due放最后
- 如有 [x] 条目，尾句后加：
─── 已完成（{M}条）───
{内容} | Done:{日期}
- 如果该成员没有任何 TODO 条目，输出：
📋 今天没有待办，轻松一下！

禁止输出任何不属于上述格式的文字。
```

**英文版：**

```
读取文件 {workspace}/todo/team-todo.md，找到「## {姓名}」section。今天日期用于计算标记：Due<今天=⚠️P0, Due=今天=P1, Due=明天=P2。

你的完整输出必须严格是以下格式，不得有任何额外文字、解释、思考或前言：

📋 Your TODOs ({N} pending):

{编号}. {任务内容} | Due:{YYYY-MM-DD} {⚠️P0/P1/P2标记，无则不加}
{编号}. {任务内容} | No Due Date

Done? Tell me and I'll remove it.

规则：
- N只计 [ ] 和 [~] 条目，不计 [x]
- [~] 条目加 [~] 前缀
- 按Due从近到远排序，无Due放最后
- 如有 [x] 条目，尾句后加：
─── Completed ({M}) ───
{内容} | Done:{日期}
- 如果该成员没有任何 TODO 条目，输出：
📋 No pending TODOs. Enjoy your day!

禁止输出任何不属于上述格式的文字。
```

### 语言选择

- 看 `members.md` 里成员的姓名判断：中文名 → 中文模板，英文名 → 英文模板
- 也可由 admin 手动指定

## 配置流程

admin 对助手说「给 XX 开每日推送」时：

1. 在 `todo/members.md` 中查找该成员的 userid
2. 确认推送渠道（默认跟随当前通道，或由 admin 指定）
3. 确认推送时间（默认 08:30）
4. 确认语言（默认按姓名推断）
5. 用 OpenClaw cron API 创建 job
6. 立即触发一次测试
7. 回复确认

## 管理操作

| 操作 | 说明 |
|---|---|
| 开启推送 | `给 XX 开每日推送` → 创建 cron job |
| 关闭推送 | `关掉 XX 的推送` → disable 或删除 cron job |
| 修改时间 | `把推送改到 9 点` → 更新 schedule |
| 测试推送 | `测试一下 XX 的推送` → 手动触发 cron run |
| 查看推送状态 | `推送状态` → 列出所有推送 cron job 的状态 |

## 注意事项

- 每个成员一个独立 cron job，命名格式：`{姓名} 每日待办推送`
- `sessionTarget` 必须是 `isolated`，避免推送任务污染主会话上下文
- `delivery.mode` 必须是 `announce`，这是当前验证过的稳定投递模式
- prompt 内严格禁止额外输出，确保 announce 原样投递格式化消息
- workspace 路径在 prompt 中使用绝对路径（`/root/.openclaw/workspace/`）
