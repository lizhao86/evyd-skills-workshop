---
name: evyd-team-todo
description: 团队待办管理技能。通过本地 Markdown 文件管理团队 TODO，支持布置任务、查看待办、自然语言更新进度、全员汇总。当用户说"加个todo"、"我的待办"、"XX做完了"、"汇总"、"团队进度"、"给XX布置任务"时触发。适用于企微/飞书/webchat 等任意渠道。
---

# Team TODO 管理

通过读写本地 Markdown 文件 `todo/team-todo.md` 管理团队待办事项。无外部 API 依赖。

## 数据文件

- **主数据：** `todo/team-todo.md` — 所有成员的 TODO（workspace 根目录下）
- **成员映射：** `todo/members.md` — 姓名 ↔ userid ↔ 角色

> 路径相对于 workspace 根目录 `/root/.openclaw/workspace/`。

## 数据格式

每条 TODO 一行：
```
- [ ] 任务内容 | Created:YYYY-MM-DD | Due:YYYY-MM-DD
- [ ] 任务内容 | Created:YYYY-MM-DD
```

- `Created`：必填，YYYY-MM-DD 格式
- `Due`：可选，YYYY-MM-DD 格式
- **无其他字段**（无来源、无优先级、无备注）
- 完成的 TODO **直接从文件中删除**，不保留

## 权限模型

根据 `todo/members.md` 中的角色字段判断权限：

| 操作 | admin | member |
|---|---|---|
| 创建 TODO（给任何人） | ✅ | ❌ |
| 查看 TODO | ✅ 全员 | ✅ 仅自己 |
| 更新/完成 | ✅ 全员 | ✅ 仅自己 |
| 删除 TODO | ✅ | ❌ |
| 查看全员汇总 | ✅ | ❌ |

### 身份识别与自动注册

1. 从会话上下文中获取发送者信息（企微 userid、飞书 userid 等）
2. 在 `todo/members.md` 中匹配姓名或 userid
3. **匹配不到时自动注册：**
   - 问用户你叫什么名字
   - 用户回复后，写入 `todo/members.md`（角色 = member）
   - 同时在 `todo/team-todo.md` 新建该成员的 section
   - 回复注册成功提示

## 四个核心操作

### ① 布置任务

**触发词：** "给XX加个todo"、"给XX布置任务"、"新增待办"

**流程：**
1. 解析：目标成员、任务内容、截止日期（可选）
2. 校验权限：仅 admin 可创建
3. 读取 `todo/team-todo.md`
4. 在目标成员的 section 下追加：`- [ ] 任务内容 | Created:YYYY-MM-DD | Due:YYYY-MM-DD`（Due 可选）
5. 若目标成员 section 不存在，新建 `## 姓名` section
6. 写回文件，回复确认

### ② 查看待办

**触发词：** "我的待办"、"今天有什么任务"、"待办列表"

**流程：**
1. 识别当前用户身份
2. 读取 `todo/team-todo.md`
3. member：只展示自己的未完成 TODO
4. admin：展示自己的，并提示可用"汇总"查看全员

**输出格式：**
- 按 Due 从近到远排序（无 Due 的放最后）
- 每条用 ` | ` 分隔
- 有 Due 显示日期 + 动态标记（🔥逾期 / 🔴今天截止 / ⚠️明天截止），无 Due 不加标记

```
📋 你的待办（N条未完成）：

1. 任务A | Due:2026-04-14 ⚠️
2. 任务B | Due:2026-04-18
3. 任务C | No Due

搞完了跟我说，我帮你删。
```

### ③ 自然语言更新

**触发词：** "XX做完了"、"PRD写好了"、"把截止日改到下周五"

**流程：**
1. 识别当前用户身份
2. 读取 `todo/team-todo.md`
3. 在该用户（member）或全员（admin）的 TODO 中模糊匹配最相关条目
4. 若唯一匹配：直接执行
5. 若多条匹配：列出让用户确认
6. 支持的操作：
   - **标记完成：** 直接从文件中删除该行
   - **改截止日：** 更新 Due 字段（YYYY-MM-DD 格式）
7. 写回文件，回复确认

### ④ 全员汇总

**触发词：** "汇总"、"全员进度"、"团队报告"、"今日报告"

**权限：** 仅 admin

**流程：**
1. 读取 `todo/team-todo.md`
2. 按成员分组统计：未完成数、逾期数
3. 输出格式见 [references/report-format.md](references/report-format.md)

## 注意事项

- 每次写文件前先读取最新内容，避免覆盖并发修改
- 完成的 TODO 直接删除，不做标记保留
- 不依赖任何外部 API（企微待办、智能表格等均不使用）
