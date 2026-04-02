# Channel: feishu + lark-cli

> 场景：通过 lark-cli 写入飞书 / Lark 文档。

## ⚠️ 执行环境说明

`lark-cli` 安装在**用户本机**，不在 Claude sandbox 里。

- **Cowork 模式**：必须通过 `Desktop Commander` 的 `start_process` 工具在用户本机 shell 执行
- **Claude Code CLI 模式**：可直接用 `Bash` 工具执行

执行前先确认可用：
```
lark-cli --version
```
如果报 "command not found"，说明在 sandbox 里执行了，需切换到 Desktop Commander。

## ⚠️ 内容长度限制

`--markdown` 参数直接传长文本会触发 shell "command too long" 错误。

**正确做法**：
1. 先用 Desktop Commander 的 `write_file` 把内容写入本机临时文件（如 `/tmp/content.md`）
2. 再用 `--markdown "$(cat /tmp/content.md)"` 引用文件内容

## Write Protocol

1. 将内容写入临时文件：`write_file("/tmp/content.md", markdownContent)`
2. `lark-cli docs +create --title "..." --folder-token "..." --markdown "$(cat /tmp/content.md)"` — 创建文档并写入正文
3. `lark-cli docs +fetch --doc "<doc_id>"` — 验证文档可访问且非空
4. 若第 2 步报错或文档为空 → 拆分内容，改用 `lark-cli docs +update` 逐段追加

## Brand 配置（feishu vs lark）

lark-cli 支持两种 brand，对应不同服务端：

- `feishu` — 飞书国内版（feishu.cn），默认值
- `lark` — Lark 国际版（larksuite.com），文莱 / 海外团队使用

查看当前配置：
```
lark-cli config show
```

切换到 Lark 国际版（需要准备好 Lark 国际版 App ID / App Secret）：
```
lark-cli config init --brand lark --app-id <YOUR_APP_ID> --app-secret-stdin
```

切换后输出的文档链接会变为 `larksuite.com/docx/...`。

## Format Constraints

飞书 / Lark 渲染器限制：

- ✅ 标题（H1/H2/H3）、段落、bullet list、有序列表
- ❌ **禁止 Markdown 表格** — 不渲染
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
