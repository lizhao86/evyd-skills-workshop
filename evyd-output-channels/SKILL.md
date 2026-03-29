---
name: evyd-output-channels
description: Output channel protocols for writing skill results to Feishu, Obsidian, or local Markdown. Use when a skill needs to write output and must follow the correct write protocol, format constraints, and file naming convention for the active channel.
---

# EVYD Output Channels

Shared output protocol for all EVYD skills.

## Active Config

```yaml
destination: feishu      # feishu | obsidian | local-markdown
executor: lark-cli       # lark-cli | openclaw | local-fs
```

改这两行即可切换全部 skill 的输出方式。
- `destination` — 写到哪里
- `executor` — 用什么工具写

## Channel map

Read the Active Config above, then load the matching reference file only.

| destination | executor | Reference |
|---|---|---|
| `feishu` | `lark-cli` | `references/feishu-lark-cli.md` |
| `feishu` | `openclaw` | `references/feishu-openclaw.md` |
| `obsidian` | `local-fs` | `references/obsidian-local-fs.md` |
| `local-markdown` | `local-fs` | `references/local-markdown-local-fs.md` |

Do not load all four. Load only the one that matches.
