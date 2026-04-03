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
                              ↓                        ↓
                        User Manual（用户手册）   设计评审（用户视角反馈 + Heuristic 评分）
产品内容 → PPT 内容 JSON → EVYD Aptos 幻灯片（可编辑 .pptx）
医疗 AI 概念 → 意图分类 → 范围边界规范
产品路线图想法 → 飞书多维表沉淀 → 重复检查 → startMonth 排期
```

个人效率工具（独立使用）：

```
Obsidian 会议纪要 + 日记 → [日报生成器] → Obsidian 日报
Obsidian 日报 + 工作思考 + 会议纪要 → [周报生成器] → Obsidian 周报
```

## 技能列表

### evyd- 系列（团队工具）

### Repo Workflow. EVYD 远程仓库规则 (Remote Repo Rules)

**目录**：`evyd-remote-repo-rules/`

约束 EVYD/Ned skills 的 GitHub 仓库工作流：真仓库放在独立 repo，`workspace/skills/` 只暴露各 skill 入口，不允许出现嵌套仓库目录。用于新建 skill、同步 GitHub 更新、修正软链接暴露、以及把本地 skill 修改提交回 GitHub。

**适用场景**：
- 新建一个 EVYD/Ned skill
- 说“evydskills 更新了，git”
- 修复 `workspace/skills/` 目录结构
- 把 skill 改动提交/推送到 GitHub

**核心规则**：
- Git 真仓库：`/root/.openclaw/repos/evyd-skills-made-by-Ned`
- 运行时暴露：`/root/.openclaw/workspace/skills/<skill-name>`
- `workspace/skills/` 下 EVYD/Ned skill 应为指向 repo 的软链接，而不是副本
- Git 操作一律在 repo 目录执行

---

### 0. EVYD PPT 生成器 (PPT Generator)

**目录**：`evyd-ppt-generator/`

将内容 JSON 文件渲染为原生可编辑的 EVYD 品牌 PPTX 演示文稿。所有幻灯片均为真实形状和文本框（可在 PowerPoint 中编辑），非截图。

**架构**：内容（JSON）/ 风格（预设）/ 渲染器（固定代码）三层分离——模型只需生成 content.json（约 400 tokens/15 张幻灯片），换风格改一行字，无需重新生成代码。

**触发词**：`生成PPT`、`做幻灯片`、`演示文稿`、`ppt generator`、`EVYD ppt`

**可用幻灯片类型**：`cover` / `agenda` / `section_divider` / `bullets_with_panel` / `two_column_check` / `cards_grid` / `criteria_rows` / `scope_tiers` / `two_panel` / `two_column_steps` / `scenario_cards` / `survey` / `ending`

**可用风格预设**：`evyd_blue`（默认）/ `evyd_white`（适合打印）/ `evyd_teal`（高对比度）

**用法**：
```bash
cd "evyd-ppt-generator"
python gen_pptx.py content.json --output output.pptx
```

**示例文件**：`examples/bruai-focusgroup.json`（MOH BruAI Focus Group 完整 15 张幻灯片）

**核心文件**：
- `SKILL.md` — 完整 JSON schema 文档 + 扩展指南
- `gen_pptx.py` — 通用渲染器（固定，不重新生成）
- `styles.py` — 风格预设（添加新风格只需新增一个 dict）
- `examples/` — 示例 content.json 文件

---


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

围绕 EVYD PD roadmap 的多维表维护工作流技能，专门服务于：
- 路线图想法收集与写入
- 重复项检查
- 字段补全（Problem / Function / Value / Resource）
- `startMonth` 排期

**适用场景**：
- PM/产品负责人在对话中发散需求，再沉淀进飞书多维表
- 对路线图条目做去重与人工决策

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

---

### 7. 设计评审 (Design Review)

**目录**：`evyd-design-review/`

以非技术普通用户视角评审 Figma 设计，输出第一人称用户反馈报告，并对照 EVYD UX & Visual Design Heuristic Rating Sheet 逐条评分。

**适用场景**：设计师完成 Figma 设计后，想在进入开发前获得真实用户会遇到的困惑和障碍

**输入**：Figma 链接（Prototype 或设计稿）或截图，指定目标用户角色

**支持角色**：医生 / 护士 / 患者 / 管理员（各有独立背景设定与思维方式）

**输出**：
- 第一人称用户反馈（口语化中文，无设计术语）：第一眼印象、任务路径、困惑点、亮点、总结
- Heuristic 评分对照：对照 10 条 EVYD UX 维度，逐条标注状态与一行观察

**触发词**：`设计评审`、`design review`、`帮我看看这个设计`、`用户视角看设计`、`站在用户角度`

**核心文件**：
- `SKILL.md` — 主流程
- `references/personas.md` — 4 个用户角色背景设定
- `references/feedback-template.md` — 反馈报告结构模板（含 Heuristic 评分对照）
- `references/heuristics.md` — EVYD UX & Visual Design Heuristic Rating Sheet（10 条维度）

---

### 8. 输出渠道配置 (Output Channels)

**目录**：`evyd-output-channels/`

所有 evyd- 技能共用的输出渠道配置与协议。在 `SKILL.md` 顶部改两行 YAML 即可全局切换输出方式。

**支持渠道**：
- **feishu + lark-cli**：通过 lark-cli 写入飞书 / Lark 文档
  - ⚠️ Cowork 模式下 lark-cli 在用户本机，必须通过 Desktop Commander 的 `start_process` 执行（不能在 sandbox 里跑）
  - ⚠️ 长内容不能直接作为 `--markdown` 参数，需先用 `write_file` 写入 `/tmp/content.md`，再用 `$(cat /tmp/content.md)` 引用
  - 支持 `feishu`（飞书国内版）和 `lark`（Lark 国际版 larksuite.com）两种 brand，通过 `lark-cli config init --brand lark` 切换
- **feishu + openclaw**：通过飞书机器人调用 OpenClaw 写入（待接入，接口细节待补充）
- **obsidian + local-fs**：写入本地 Obsidian vault，支持模板映射
- **local-markdown + local-fs**：写入本地桌面 Markdown 文件

---

### 8. PPT 生成器 (PPT Generator)

**目录**：`evyd-ppt-generator/`

从内容 JSON 生成 EVYD 品牌风格的 PPTX 演示文稿，使用 EVYD Aptos 模板，输出真实可编辑的形状和文字（非截图）。

**适用场景**：内部汇报、客户提案、MOH 演讲、焦点小组等

**架构**：
```
content.json（模型生成，约 400 tokens / 15 页）
    → gen_pptx.py + styles.py（固定渲染器，不重新生成）
    → .pptx（PowerPoint 可直接编辑）
```

**支持的幻灯片类型**：`cover` / `agenda` / `section_divider` / `bullets_with_panel` / `two_column_check` / `cards_grid` / `criteria_rows` / `scope_tiers` / `two_panel` / `two_column_steps` / `scenario_cards` / `survey` / `ending`

**内置样式**：`evyd_blue`（默认）/ `evyd_white` / `evyd_teal`

**触发词**：`生成PPT`、`做幻灯片`、`演示文稿`、`EVYD ppt`

**核心文件**：
- `SKILL.md` — 完整 JSON schema 与 workflow
- `gen_pptx.py` — 渲染器
- `styles.py` — 样式预设
- `examples/` — 示例 JSON

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
6. 视觉设计完成后 → [设计评审] 用户视角反馈 + Heuristic 评分
        ↓
7. 进入开发阶段

[医疗 AI 意图架构师] — 独立使用，AI 产品规划阶段
[PD 路线图作业台] — 独立使用，路线图维护 / 去重 / 排期
[PPT 生成器] — 独立使用，从内容 JSON 生成 EVYD 品牌 PPTX
```

## 项目结构

```
技能 skills 作坊/
├── README.md
├── evyd-ppt-generator/             # EVYD PPT 生成器（JSON → 原生可编辑 PPTX）
│   ├── SKILL.md
│   ├── gen_pptx.py
│   ├── styles.py
│   └── examples/bruai-focusgroup.json
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
├── evyd-design-review/             # 设计评审（用户视角 + Heuristic 评分）
│   ├── SKILL.md
│   └── references/
├── evyd-pd-roadmap/               # PD 路线图作业台
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── evyd-ppt-generator/            # PPT 生成器
│   ├── SKILL.md
│   ├── gen_pptx.py
│   ├── styles.py
│   └── examples/
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
