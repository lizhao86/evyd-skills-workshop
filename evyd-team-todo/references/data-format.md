# 数据格式规范

## team-todo.md 格式

```markdown
# Team TODO

## 姓名
- [ ] 任务内容 | Created:2026-04-13 | Due:2026-04-15
- [ ] 任务内容 | Created:2026-04-13
```

### 核心字段

| 字段 | 必填 | 格式 | 说明 |
|---|---|---|---|
| checkbox | ✅ | `- [ ]` | 未完成 |
| 任务内容 | ✅ | 自由文本 | 不含 `|` 字符 |
| Created | ✅ | YYYY-MM-DD | 创建日期 |
| Due | 可选 | YYYY-MM-DD | 截止日期，不写则无截止 |

### 可选扩展字段

以下字段为可选扩展，不强制使用。用户自然使用时自动支持，不主动引导。

| 字段 | 格式 | 说明 |
|---|---|---|
| checkbox `[~]` | `- [~]` | 进行中（区别于 `[ ]` 未开始） |
| checkbox `[x]` | `- [x]` | 已完成（搭配 Done 字段使用） |
| Done | YYYY-MM-DD | 完成日期，仅 `[x]` 时出现 |
| Updated | YYYY-MM-DD | 最后更新日期，内容有变动时追加 |

### Checkbox 状态机

```
[ ] 未开始 → [~] 进行中 → [x] 已完成
                ↑                ↓
                └── 可直接 ──→ 删除
```

- **默认行为：** 完成的 TODO 直接从文件删除
- **可选行为：** 如用户或 admin 明确要求保留记录，改为 `[x]` + `Done:YYYY-MM-DD`，不删除
- `[x]` 条目在 ② 查看待办和 ④ 全员汇总中**不计入未完成数**，单独展示在末尾（如果存在）

### 缩进子项（可选）

TODO 条目下方可追加缩进子项，用于记录备注、拆解细节、待确认事项等：

```markdown
- [~] RT 的 21DHF Figma UI：与 MA 和 Lynn Tan 对齐 | Created:2026-04-14 | Updated:2026-04-14
  - UI 待更新设计项：
    - 21DHF report：nutrition 四个目标要同时显示
    - Benefits of joining 21D 放到 onboarding
  - MA 待提供：
    - Reminder 默认时间
    - Nudge 逻辑重新整理
```

**规则：**
- 子项用 2 空格缩进，以 `- ` 开头
- 子项可多层嵌套（4 空格、6 空格…）
- 子项不含 `| Created:` 等字段，不是独立 TODO
- 子项在输出时跟随父条目展示，不单独编号
- 子项内容为自由文本，不做格式校验

### 完整示例

```markdown
# Team TODO

## 赵立
- [ ] 更新 openclaw 版本 | Created:2026-04-13
- [ ] 年度 roadmap 要拆分 | Created:2026-04-13 | Due:2026-04-14
- [~] AI POC 切 member 问题 | Created:2026-04-14 | Updated:2026-04-14
  - 已与研发讨论，ticket 已写好
  - 等待 UI 设计
- [x] 给康宁团队分享运营后台 | Created:2026-04-13 | Done:2026-04-14
```

## members.md 格式

```markdown
# 团队成员

| 姓名 | userid | 角色 |
|------|--------|------|
| 赵立 | 149681207 | admin |
| 张三 | zhangsan | member |
```

- `userid`：企微/飞书等渠道的用户 ID，用于自动匹配身份
- `角色`：`admin`（管理员，可管理全员 TODO）或 `member`（成员，只能操作自己的）
