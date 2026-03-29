---
name: output-channels
description: Output channel protocols for writing skill results to Feishu, Obsidian, or local Markdown. Use when a skill needs to write output and must follow the correct write protocol, format constraints, and file naming convention for the active channel.
---

# Output Channels

Shared output protocol for all EVYD skills.

Active channel is set in `../OUTPUT_CHANNELS.md`.
Read it first to determine which channel applies, then load the corresponding reference.

## Channel map

| destination | executor | Reference |
|---|---|---|
| `feishu` | `lark-cli` | `references/feishu-lark-cli.md` |
| `feishu` | `openclaw` | `references/feishu-openclaw.md` |
| `obsidian` | `local-fs` | `references/obsidian-local-fs.md` |
| `local-markdown` | `local-fs` | `references/local-markdown-local-fs.md` |

Load only the reference that matches the active config.
Do not load all four.
