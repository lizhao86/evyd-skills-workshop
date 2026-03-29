# Channel: feishu + openclaw

> 场景：通过飞书机器人调用 OpenClaw，由 OpenClaw 自带飞书 skill 写入文档。

## Write Protocol

1. 调用 OpenClaw 飞书 skill 的文档创建接口，传入 title + folder + markdown 正文
2. 验证返回的 doc_url 可访问
3. 若失败 → 拆分内容分段写入

> ⚠️ **待补充**：OpenClaw 飞书 skill 的具体调用方式、接口名、参数格式，请在实际接入后补充到此处。

## Format Constraints

与 feishu + lark-cli 相同（飞书渲染器限制不变）：

- ✅ H1/H2/H3、bullet list、有序列表
- ❌ **禁止 Markdown 表格**
- ❌ 禁止超过 2 层的复杂嵌套

## File Naming Convention

```
For {User昵称} - {Type} - {Title} - {YYYYMMDD}
```
