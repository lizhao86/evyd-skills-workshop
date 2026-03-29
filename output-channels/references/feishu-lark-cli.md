# Channel: feishu + lark-cli

> 场景：本地运行 Claude Code CLI，通过 lark-cli 写入飞书文档。

## Write Protocol

1. `lark-cli docs +create --title "..." --folder-token "..." --markdown "..."` — 创建文档并写入正文
2. `lark-cli docs +fetch --doc "<doc_id>"` — 验证文档可访问且非空
3. 若第 1 步报错或文档为空 → 拆分内容，改用 `lark-cli docs +update` 逐段追加

## Format Constraints

飞书渲染器限制：

- ✅ 标题（H1/H2/H3）、段落、bullet list、有序列表
- ❌ **禁止 Markdown 表格** — 飞书不渲染
- ❌ 禁止超过 2 层的复杂嵌套
- 推荐结构：`H1 → H2 → bullet list`

## File Naming Convention

```
For {User昵称} - {Type} - {Title} - {YYYYMMDD}
```

- `{User昵称}` — 飞书可读显示名；无法获取时用对话上下文中的可读名；不得使用 open_id
- `{Type}` — 由各 skill 自定义（如「Manual」「Research」「UserStory」「Spec」）
- `{Title}` — 从内容派生的简短标题
- `{YYYYMMDD}` — 创建日期
