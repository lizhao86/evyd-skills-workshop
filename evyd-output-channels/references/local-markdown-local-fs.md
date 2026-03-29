# Channel: local-markdown + local-fs

> 场景：输出到本地 Markdown 文件。

## Config

```yaml
local_output_path: /Users/Li.ZHAO/Desktop
```

## Write Protocol

1. 拼接完整路径：`{local_output_path}/{filename}.md`
2. 用 Write 工具一次性写入全部正文
3. 用 Read 工具验证文件存在且非空

## Format Constraints

- ✅ 完整 Markdown，**包括表格**
- 无渲染器限制

## File Naming Convention

```
For {User昵称} - {Type} - {Title} - {YYYYMMDD}.md
```
