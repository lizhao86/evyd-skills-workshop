# 数据格式规范

## team-todo.md 格式

```markdown
# Team TODO

## 姓名
- [ ] 任务内容 | Created:2026-04-13 | Due:2026-04-15
- [ ] 任务内容 | Created:2026-04-13
```

### 字段说明

| 字段 | 必填 | 格式 | 说明 |
|---|---|---|---|
| checkbox | ✅ | `- [ ]` | 永远未完成（完成即删除） |
| 任务内容 | ✅ | 自由文本 | 不含 `|` 字符 |
| Created | ✅ | YYYY-MM-DD | 创建日期 |
| Due | 可选 | YYYY-MM-DD | 截止日期，不写则无截止 |

完成的 TODO 直接从文件删除，不保留。

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
