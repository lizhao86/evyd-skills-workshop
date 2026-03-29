---
name: evyd-competitor-research
description: |-
  Healthcare competitive research for EVYD. Outputs structured reports to Feishu docs.
  Use when researching a specific healthcare competitor, generating a competitive landscape summary, or following up with deeper analysis on a previous report.
  Trigger on 竞品调研, competitor research, 竞品分析, competitive analysis, 竞品汇总, competitive landscape.
  Two modes: (1) Single competitor deep dive with 5 parallel sub-agents, (2) Competitive landscape summary across multiple competitors.

  Examples:
  - user: "竞品调研 Epic Systems" → Mode 1, deep dive on Epic Systems across all research dimensions
  - user: "帮我调研一下 Cerner 的交付运营" → Mode 1, scoped to delivery & operations slice
  - user: "竞品汇总" → Mode 2, read all existing reports in Feishu folder and generate landscape summary
  - user: "Research Oracle Health for the Singapore market" → Mode 1, market-scoped deep dive
  - user: "继续问第2个问题" → Follow-up mode, append deeper analysis to the existing Feishu doc
---

# 竞品调研技能

医疗健康（Healthcare）解决方案竞品分析，输出到飞书云盘。

## 背景

- **我方**：EVYD（医疗软件解决方案）
- **目标市场**：美国、新加坡、泛东南亚
- **买单方**：MOH/公共卫生机构 或 大型医疗集团
- **交付形态**：交付 + 集成 + 运营为主
- **飞书输出文件夹**：`folder_token = G1tGfI3wFldgE3d2JKscrj1InHc`
- **命名规则补充**：`For {User昵称}` 中的 `{User昵称}` 应优先使用当前对话对象在 Feishu 中的可读昵称 / 显示名；不要直接使用 open_id、user_id、系统用户名或技术标识。若工具链暂时拿不到更精确昵称，才 fallback 到消息上下文中的可读显示名。

## 硬规则

1. 只用 `web_search` 检索，不额外安装工具
2. 所有结论标注：【来源：链接】/【待核实】/【推断：基于…】
3. 不编造数字
4. 优先高可信来源：政府采购/招标、医院新闻稿、竞品官网、第三方认证
5. **输出格式：使用列表和段落，不要用 Markdown 表格**（飞书文档不支持表格渲染）

---

## Mode 1: 单个竞品深度调研

**触发词**：竞品调研 / competitor research + 竞品名

**参数**：竞品名称（必填）、切片/模块（可选）、目标市场（默认 US/SG/SEA）

### 执行流程

1. 确认竞品名称和调研范围
2. 读取 `references/single-prompt.md` 获取 5 个 Agent 的 prompt 模板
3. 并行 spawn 5 个 sub-agents（`sessions_spawn`, `mode="run"`），替换 `{COMPETITOR}` 和 `{SLICE}`：
   - **Agent A**：产品定位 & 核心能力 & 商业模式
   - **Agent B**：合规安全
   - **Agent C**：互操作集成
   - **Agent D**：交付运营
   - **Agent E**：市场足迹 & 调研背景
4. 等待全部完成，合并输出 + 生成 Normalized Summary
5. 读取 `references/report-template.md` 获取文档结构模板
6. 读取 `references/taxonomy.md` 确定 System/Module 归类
7. 按 `../evyd-output-channels/SKILL.md` 中 active channel 的协议输出文档，目标文件夹 `G1tGfI3wFldgE3d2JKscrj1InHc`
   - 文件名：`For {User昵称} - 👊「Research」{System} - {Company_ProductName} - {Module} {date}`
8. 进入追问模式：读取 `references/followup-prompt.md`，生成 3 个深挖问题

### 文件名示例

调用者「张三」调研 Epic Systems：
`For 张三 - 👊「Research」ElectronicHealthRecord - Epic Systems - InteroperabilityLayer 2026-03-12`

---

## Mode 2: 竞品全景汇总

**触发词**：竞品汇总 / 竞品全景 / competitive landscape

**参数**：切片/模块（可选）、EVYD 卖点（可选）、EVYD 短板（可选）

### 执行流程

1. 使用 `feishu_drive` 列出文件夹 `G1tGfI3wFldgE3d2JKscrj1InHc` 内所有 `For` 开头的文档
2. 逐个读取，提取 Normalized Summary + Evidence Table + Links
3. 读取 `references/landscape-prompt.md` 获取全景分析输出模板
4. 综合生成全景报告
5. 按 `../evyd-output-channels/SKILL.md` 中 active channel 的协议输出文档
   - 文件名：`For {User昵称} - 👊「Landscape」{System} - 全景分析 - {date}`

---

## 追问模式

**触发词**：继续问 / 追问 / 深入分析 / 补充调研

详细流程见 `references/followup-prompt.md`，核心规则：

1. 调研完成后主动提 3 个深挖问题（商业模式/技术细节/竞争策略）
2. 用户提问后用 `web_search` 深挖，询问是否追加到原文档
3. 追加时在原文档末尾创建一级标题追问章节，标记时间戳
4. **不新建文档**，追问内容必须追加到原文档

---

## References 索引

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| `references/single-prompt.md` | 5 个 Agent 的完整 prompt 模板 | Mode 1 启动时 |
| `references/report-template.md` | 飞书文档输出结构模板 | Mode 1 合并输出时 |
| `references/landscape-prompt.md` | 全景汇总输出模板 | Mode 2 启动时 |
| `references/followup-prompt.md` | 追问模式详细流程 | 调研完成后 / 用户追问时 |
| `references/taxonomy.md` | System & Module 归类指南 | 生成文件名时 |

## 快速示例

```
竞品调研 Epic Systems 交付运营     # Mode 1
竞品汇总                           # Mode 2
继续问 / 深挖第2个问题              # 追问模式
```
