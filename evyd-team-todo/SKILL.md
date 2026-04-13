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

## 权限模型

根据 `todo/members.md` 中的角色字段判断权限：

| 操作 | admin | member |
|---|---|---|
| 创建 TODO（给任何人） | ✅ | ❌ |
| 查看 TODO | ✅ 全员 | ✅ 仅自己 |
| 更新状态/备注 | ✅ 全员 | ✅ 仅自己 |
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
1. 解析：目标成员、任务内容、截止日期（可选）、优先级（可选，默认"中"）
2. 校验权限：仅 admin 可创建
3. 读取 `todo/team-todo.md`
4. 在目标成员的 section 下追加一行：`- [ ] 任务内容 | 优先级:X | 截止:MM-DD | 创建人:XX | 创建:YYYY-MM-DD`
5. 若目标成员 section 不存在，新建 `## 姓名 (userid: xxx)` section
6. 写回文件，回复确认

### ② 查看待办

**触发词：** "我的待办"、"今天有什么任务"、"待办列表"

**流程：**
1. 识别当前用户身份
2. 读取 `todo/team-todo.md`
3. member：只展示自己的未完成 TODO
4. admin：展示自己的，并提示可用"汇总"查看全员

**输出格式：**
```
📋 你的待办（共 N 条未完成）：

1. [ ] 任务A（高优，截止04-15）
2. [ ] 任务B（中优，截止04-18）

搞完了跟我说，我帮你打勾。
```

### ③ 自然语言更新

**触发词：** "XX做完了"、"PRD写好了"、"bug修到一半预计明天搞定"、"把截止日改到下周五"

**流程：**
1. 识别当前用户身份
2. 读取 `todo/team-todo.md`
3. 在该用户（member）或全员（admin）的 TODO 中模糊匹配最相关条目
4. 若唯一匹配：直接更新
5. 若多条匹配：列出让用户确认
6. 支持的更新操作：
   - **标记完成：** `- [ ]` → `- [x]`，追加 `| 完成:YYYY-MM-DD`
   - **加备注：** 追加 `| 备注:内容`
   - **改截止日：** 更新截止字段
   - **改优先级：** 更新优先级字段
7. 写回文件，回复确认

### ④ 全员汇总

**触发词：** "汇总"、"全员进度"、"团队报告"、"今日报告"

**权限：** 仅 admin

**流程：**
1. 读取 `todo/team-todo.md`
2. 按成员分组统计：未完成数、已完成数、逾期数
3. 输出格式见 [references/report-format.md](references/report-format.md)

## 数据格式规范

详见 [references/data-format.md](references/data-format.md)。

## 注意事项

- 每次写文件前先读取最新内容，避免覆盖并发修改
- 不要删除已完成的条目，保留历史记录
- 日期格式统一：字段内用 `MM-DD`，创建/完成日期用 `YYYY-MM-DD`
- 不依赖任何外部 API（企微待办、智能表格等均不使用）
