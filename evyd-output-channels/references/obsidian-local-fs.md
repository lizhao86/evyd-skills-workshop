# Channel: obsidian + local-fs

> 场景：本地写入 Obsidian vault。

## Config

```yaml
obsidian_vault_path: /Users/Li.ZHAO/我赵立的仓库
templates_dir: Template
default_subdir: 00-Inbox-收集💡
```

## Vault 一级目录

```
00-Inbox-收集💡          ← 默认落点（未指定 subdir 时）
10-Notes-晨夕日记 📝
11-Notes-见感思行 🗂️
12-Notes-碎片阅读 📰
13-Notes-阅读笔记 📙
14-Notes-产品剪报 ✂️
15-Notes-提示词🔬
21-Work-会议纪要 💼
22-Work-工作思考 🤔
23-Work-团队管理 👑
24-Work-周报汇总
26-Work-竞品分析👊
27-Work-Mermaid文件
28-Work-需求收集🛳️
30-Life-跑团
99-Memo-备忘
```

## 模板映射

用户说模板名时，按下表解析为实际文件名并推断默认 subdir：

| 模板别名 | 实际文件名（Template/） | 推荐 subdir |
|---|---|---|
| `analysis` | `👊「Analysis」System - Company_ProductName - Module {{date}}.md` | `26-Work-竞品分析👊` |
| `requirements` | `🛳️ 「模板」需求收集.md` | `28-Work-需求收集🛳️` |
| `work-thinking` | `🤔 「模板」工作思考.md` | `22-Work-工作思考 🤔` |
| `meeting` | `💼 {{date}} 「模板」会议纪要.md` | `21-Work-会议纪要 💼` |
| `reflection` | `🗂️「模板」见感思行 {{date}}.md` | `11-Notes-见感思行 🗂️` |
| `book` | `📙 《「模板」书名》{{date}}.md` | `13-Notes-阅读笔记 📙` |
| `article` | `📰 《「模板」文章标题》{{date}}.md` | `12-Notes-碎片阅读 📰` |
| `prompt` | `🔬「模板」「Prompts」提示词  {{date}}.md` | `15-Notes-提示词🔬` |
| `product-clip` | `✂️「模板」「产品剪报」产品 - 功能 {{date}}.md` | `14-Notes-产品剪报 ✂️` |
| `ai-chat` | `🤖「模板」「AI-Chat」AI 问答  {{date}}.md` | `00-Inbox-收集💡` |

> 用户未指定 subdir 时，优先用模板映射中的推荐 subdir；两者都没有则用 `default_subdir`。

## 运行时参数

- `subdir` — 目标子目录（覆盖模板推荐值）
- `template` — 模板别名；未指定则不套模板

## Write Protocol

1. **确定目标路径**
   - 解析 `subdir`：用户指定 > 模板推荐 subdir > `default_subdir`
   - 完整文件路径：`{obsidian_vault_path}/{subdir}/{filename}.md`
2. **处理模板**（如指定 `template`）
   - 按模板映射找到实际文件名，读取 `{obsidian_vault_path}/Template/{实际文件名}`
   - 将 `{{date}}` 替换为 `YYYY-MM-DD`，`{{title}}` 替换为实际标题
   - 将正文内容追加或插入模板结构中
   - 若模板文件不存在 → 跳过，直接写纯正文，并告知用户
3. **写入文件**：用 Write 工具一次性写入完整内容
4. **验证**：用 Read 工具确认文件存在且非空

## Format Constraints

- ✅ 完整 Markdown，**包括表格**
- ✅ 支持 Wikilink `[[...]]` 和 frontmatter（YAML `---` 块）
- 无飞书渲染器限制

## File Naming Convention

```
For {User昵称} - {Type} - {Title} - {YYYYMMDD}.md
```

### 调用示例

> 用户：`用 analysis 模板，输出 Obsidian`
> → `template = analysis`，`subdir = 26-Work-竞品分析👊`（模板推荐）
> → 写入 `/Users/Li.ZHAO/我赵立的仓库/26-Work-竞品分析👊/For Li - Analysis - xxx - 20260329.md`

> 用户：`放到工作思考目录`（未指定模板）
> → `subdir = 22-Work-工作思考 🤔`，不套模板，写入纯正文
