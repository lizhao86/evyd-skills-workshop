# 技能 Skills 作坊

基于 Claude Code Skills 框架构建的 AI 技能工具包，分两个系列：
- **evyd-** 系列：面向 EVYD 产品团队，覆盖竞品调研、需求定义、设计落地到文档交付的完整产品流程
- **ned-** 系列：Ned 个人效率工具，从 Obsidian 知识库自动生成日报和周报

## 项目简介

本项目整合了产品开发流程中最耗时的几个环节，让产品经理、设计师和工程师通过 AI 快速生成高质量工作产出。

团队工具主链路：

```
市场/竞品 → 竞品调研报告（飞书）
                  ↓
产品需求 → 用户故事 + AC → Figma 线框图脚本 → 低保真原型
                              ↓
                        User Manual（用户手册）
医疗 AI 概念 → 意图分类 → 范围边界规范
产品路线图想法 → 飞书多维表沉淀 → 重复检查 → startMonth 排期 → JSON 导出
```

个人效率工具（独立使用）：

```
Obsidian 会议纪要 + 日记 → [日报生成器] → Obsidian 日报
Obsidian 日报 + 工作思考 + 会议纪要 → [周报生成器] → Obsidian 周报
```

## 技能列表

### evyd- 系列（团队工具）

### 1. 竞品调研 (Competitor Research)

**目录**：`evyd-competitor-research/`

医疗健康解决方案竞品分析，输出到飞书云盘。支持两种模式：

- **Mode 1 — 单个竞品深度调研**：并行召唤 5 个子 Agent，分别调研产品定位、合规安全、互操作集成、交付运营、市场足迹，合并输出结构化报告
- **Mode 2 — 竞品全景汇总**：读取飞书文件夹内已有调研文档，综合生成全景分析报告
- **追问模式**：调研完成后主动提 3 个深挖问题，用户追问后追加到原文档

**触发词**：`竞品调研`、`competitor research`、`竞品汇总`、`competitive landscape`

**输出**：飞书云文档，文件夹 `G1tGfI3wFldgE3d2JKscrj1InHc`

---

### 2. 用户故事编写器 (User Story Writer)

**目录**：`evyd-user-story-writer/`

将产品需求描述转换为结构化的用户故事文档，包含完整的验收标准。

**适用场景**：需求拆分、Sprint 规划、验收标准制定

**输入**：产品需求描述（平台、系统模块、功能目标）

**输出**：
- 标准格式的用户故事，Description 包含五节结构：Business Objective / User Value / Scope / Out of Scope / Assumptions
- 使用 Given-When-Then-And 格式的验收标准，按实际需要覆盖所有适用场景类别（不凑固定数量）
- AC 末尾附 Coverage Checklist（`<!-- ai-context-end -->` 之后），仅供人工自检，不进入 AI 评审上下文
- 可选输出到飞书云文档

---

### 3. 低保真 Figma 脚本生成器 (LoFi Figma Maker)

**目录**：`evyd-lofi-figma-maker/`

将用户故事自动转换为可直接粘贴到 Figma Make 的线框图提示词。

**适用场景**：UI/UX 设计启动、快速原型制作

**输入**：用户故事文档（含验收标准）

**输出**：
- 针对每个 AC 场景生成对应屏幕的 Figma Make 提示词
- 使用标准化组件词汇表，确保 Figma AI 准确识别
- 可选输出到飞书云文档

---

### 4. 用户手册生成器 (User Manual)

**目录**：`evyd-user-manual/`

根据用户故事和验收标准，自动生成结构清晰、面向终端用户的操作手册。

**适用场景**：功能交付文档、帮助中心内容、产品培训材料

**输入**：用户故事 + 验收标准（AC），或功能描述

**输出**：
- 标准 Markdown 格式的 User Manual 章节
- 按任务分节，使用编号步骤和 UI 元素标注
- 包含常见问题 / Troubleshooting 部分
- 可选输出到飞书云文档

---

### 5. 医疗 AI 意图架构师 (AI Intention Brainstorm)

**目录**：`evyd-ai-intention-brainstorm/`

将医疗 AI 产品概念转换为结构化的意图分类和范围边界规范文档，含评估维度与权重打分逻辑。

**适用场景**：AI 产品规划、合规性设计、跨团队对齐、QA 测试用例设计

**输入**：AI 功能概念和使用场景描述（中英文均可）

**输出**：英文结构化规范文档，包含三层范围定义：
- **IS（范围内）**：AI 可以处理的意图，含知识库要求、判定标准、回复结构
- **HOOS（硬性范围外）**：绝对禁止的场景，含拒绝话术结构
- **SOOS（软性范围外）**：需转介医生的场景，遵循 Empathy → Education → Boundary → Referral → Disclaimer 模型
- **每个场景均包含 Scoring Dimensions & Weights**：基于"失败代价"框架，使用 6 个评估维度（Clinical Safety / Medical Accuracy / Information Clarity / Patient Guidance / Empathy & Support / Context Awareness）推导权重，供 AI 评测使用

**核心文件**：
- `SKILL.md` — 技能主流程
- `Scope-Layer-Templates.md` — 三层表格格式规范与示例行
- `Scoring-Framework.md` — 评分维度定义、层级基准权重、权重推导协议（3步）

---

### 6. PD 路线图作业台 (PD Roadmap Workbench)

**目录**：`evyd-pd-roadmap/`

围绕 EVYD PD roadmap 的多维表维护与导出工作流技能。不是泛用 JSON 转换器，而是专门服务于：
- 路线图想法收集与写入
- 重复项检查
- 字段补全（Problem / Function / Value / Resource）
- `startMonth` 排期
- 固定 JSON 导出

**适用场景**：
- PM/产品负责人在对话中发散需求，再沉淀进飞书多维表
- 对路线图条目做去重与人工决策
- 为下游 roadmap 呈现系统导出固定 JSON

**模块化能力**：
- **Collect + Write**：对话收集场景，并写回指定 Feishu Bitable
- **Duplicate Check**：检查重复/近重复条目，要求人工判断保留、更新或合并

**已内置辅助脚本**：
- `scripts/detect_duplicates.py` — 做候选重复项扫描（辅助判定，不自动裁决）

**核心文件**：
- `SKILL.md` — 主流程与模块入口
- `references/schema.md` — Bitable 字段规范、Resource 映射、startMonth 规划 canon
- `references/collection-write.md`
- `references/dedup-check.md`
- `scripts/detect_duplicates.py`

---

### ned- 系列（个人效率工具）

> 以下技能绑定 Ned 的 Obsidian 本地知识库路径，不适用于其他用户直接使用。

#### 7. 每日工作报告生成器 (Daily Working Report)

**目录**：`ned-daily-working-report/`

每天下班后，从 Obsidian 自动汇总当天的会议纪要和个人日记，生成简洁的工作日报。

**输入来源**：
- 当天会议纪要：`/21-Work-会议纪要 💼/`（文件名含当天日期）
- 当天个人日记：`/10-Notes-晨夕日记 📝/YYYY/MM/`（跳过 Todo 部分）

**输出**：`/24-Work-周报汇总/YYYY-MM-DD EVYD 日报.md`，含工作流水账、下一步汇总、来源索引

**触发词**：`daily-report`、`日报`、`生成日报`

**核心文件**：
- `SKILL.md` — 主流程与格式规则
- `assets/template.md` — 日报模板
- `scripts/generate_daily_report.py` — 自动化脚本

---

#### 8. 每周工作报告生成器 (Weekly Report)

**目录**：`ned-weekly-report/`

每周自动汇总本周日报、工作思考和会议纪要，生成按业务板块分组的结构化周报，体现产品团队负责人视角。

**输入来源**：
- 本周日报：`/24-Work-周报汇总/`
- 工作思考：`/22-Work-工作思考 🤔/`
- 会议纪要：`/21-Work-会议纪要 💼/`

**输出**：`/24-Work-周报汇总/YYYY-MM-DD~YYYY-MM-DD EVYD周报.md`，按业务板块分组，含下周重点和来源索引

**触发词**：`weekly-report`、`周报`、`生成周报`

**核心文件**：
- `SKILL.md` — 主流程与去重精简规则
- `assets/template.md` — 周报模板
- `scripts/generate_weekly_report.py` — 自动化脚本

---

## 完整工作流

```
1. [竞品调研] 了解市场格局
        ↓
2. 描述产品需求
        ↓
3. [用户故事编写器] 生成用户故事 + 验收标准
        ↓
4. [Figma 脚本生成器] 生成 Figma Make 提示词   →  [用户手册生成器] 生成 User Manual
        ↓
5. 设计师粘贴提示词，在 Figma Make 生成低保真线框图
        ↓
6. 进入视觉设计和开发阶段

[医疗 AI 意图架构师] — 独立使用，AI 产品规划阶段
[PD 路线图作业台] — 独立使用，路线图维护 / 去重 / 排期 / JSON 导出
```

## 项目结构

```
技能 skills 作坊/
├── README.md
├── evyd-output-channels/           # 输出渠道 skill（Active Config + 4 个渠道协议）
│   ├── SKILL.md
│   └── references/
├── evyd-ai-intention-brainstorm/   # 医疗 AI 意图架构师
│   ├── SKILL.md
│   ├── Scope-Layer-Templates.md
│   └── Scoring-Framework.md
├── evyd-competitor-research/       # 竞品调研
│   ├── SKILL.md
│   └── references/
├── evyd-lofi-figma-maker/          # 低保真 Figma 脚本生成器
│   ├── SKILL.md
│   └── Figma-Make-Prompt-Template.md
├── evyd-user-manual/               # 用户手册生成器
│   └── SKILL.md
├── evyd-user-story-writer/         # 用户故事编写器
│   ├── SKILL.md
│   └── EVYD-User-Story-Template.md
├── evyd-pd-roadmap/               # PD 路线图作业台
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── ned-daily-working-report/       # 每日工作报告生成器（个人）
│   ├── SKILL.md
│   ├── assets/template.md
│   └── scripts/generate_daily_report.py
└── ned-weekly-report/              # 每周工作报告生成器（个人）
    ├── SKILL.md
    ├── assets/template.md
    └── scripts/generate_weekly_report.py
```

## 输出渠道

`evyd-output-channels/SKILL.md` 包含 Active Config 和 4 个渠道的完整协议，改两行即可切换所有 skill 的输出方式。

| 渠道 | Reference |
|---|---|
| feishu + lark-cli | `evyd-output-channels/references/feishu-lark-cli.md` |
| feishu + openclaw | `evyd-output-channels/references/feishu-openclaw.md` |
| obsidian + local-fs | `evyd-output-channels/references/obsidian-local-fs.md` |
| local-markdown + local-fs | `evyd-output-channels/references/local-markdown-local-fs.md` |

## 技术栈

- **框架**：[Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- **输出集成**：可配置（默认飞书云文档，支持 Obsidian / 本地 Markdown / 聊天附件 fallback）

## 使用方式

在 Claude Code 中，直接通过对话触发对应技能。每个技能的 `SKILL.md` 描述了详细的触发词和工作流程。技能安装后，Claude Code 会自动识别触发条件并调用对应技能。
