# Output Channel Config

## Active Config

```yaml
destination: feishu      # feishu | obsidian | local-markdown
executor: lark-cli       # lark-cli | openclaw | local-fs
```

改这两行即可切换全部 skill 的输出方式。
- `destination` — 写到哪里
- `executor` — 用什么工具写

完整协议（Write Protocol / Format Constraints / File Naming）→ `output-channels/SKILL.md`
