# 技能 Skills 作坊

基于 Claude Code Skills 框架构建的 AI 技能工具包，面向 EVYD 产品团队，覆盖竞品调研、需求定义、设计落地到文档交付的完整产品流程。

> **公私分离**：Ned 个人效率工具（日报/周报生成器）已迁移至私有仓库，本仓库仅保留团队工具。

## 项目简介

本项目整合了产品开发流程中最耗时的几个环节，让产品经理、设计师和工程师通过 AI 快速生成高质量工作产出。

团队工具主链路：

```
市场/竞品 → 竞品调研报告（飞书）
                  ↓
产品需求（零散输入）→ [需求拆解器] Requirement Ticket（Y Model + UC + Feature Scope + Dependency）
                                              ↓
                              [用户故事编写器] → 用户故事 + AC → Figma 线框图脚本 → 低保真原型
                                                                      ↓                        ↓
                                                               User Manual（用户手册）   设计评审（用户视角反馈 + Heuristic 评分）
产品内容 → PPT 内容 JSON → EVYD Aptos 幻灯片（可编辑 .pptx）
医疗 AI 概念 → 意图分类 → 范围边界规范
产品路线图想法 → 飞书多维表沉淀 → 重复检查 → startMonth 排期
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

将内容 JSON 文件渲染为原生可编辑的 PPTX 演示文稿。所有幻灯片均为真实形状和文本框（可在 PowerPoint 中编辑），非截图。无需外部模板文件。

**架构**：内容（JSON）/ 布局（渲染器）/ 风格（JSON 预设）三层分离——模型只需生成 content.json（约 400 tokens/15 张幻灯片），**布局由 Claude 自动根据内容选择**，换风格改一行字，无需重新生成代码。渲染后自动运行溢出检测，智能缩小字号修复排版问题。

**触发词**：`生成PPT`、`做幻灯片`、`演示文稿`、`ppt generator`、`EVYD ppt`

**v2.2 能力**：7 种叙事模板、直接用户画像（问不猜）、三轮搜索 + 5 级可信度、10 种原生图表、图片搜索 + Claude 视觉审美判断、CSV/Excel 数据管道、叙事连贯性检查、交付报告、11 项视觉 QA

**可用幻灯片类型（21 种）**：
- **Chrome 框架**：`cover` / `agenda` / `section_divider` / `ending`
- **内容布局**：`bullets_with_panel` / `two_column_check` / `cards_grid` / `criteria_rows` / `scope_tiers` / `two_panel` / `two_column_steps` / `scenario_cards` / `survey`
- **数据可视化**：`stat_highlight` / `timeline` / `chart`（10 种图表类型）/ `comparison_table`
- **视觉强调**：`quote_full` / `center_focus` / `image_full`（支持图片搜索下载）
- **别名**：`key_metrics` → `stat_highlight` / `quote_highlight` → `quote_full`

**可用风格预设（10 套）**：`evyd_blue`（默认）/ `evyd_white` / `evyd_teal` / `dark_navy` / `cooltech` / `morandi` / `warm` / `monochrome` / `sunrise` / `charcoal_gold`

每套样式包含 `chart_colors`（5色图表配色）和 `best_for`（场景推荐元数据）。

**用法**：
```bash
cd "evyd-ppt-generator"
python3 gen_pptx.py content.json --style evyd_blue --output output.pptx
```

**示例文件**：`examples/fullstack-v2.json`（20 页综合示例，覆盖 radar/scatter/area 等全部新图表）

**核心文件**：
- `SKILL.md` — 完整 JSON schema + 7 种叙事模板 + 布局选型指南 + 5 阶段工作流
- `gen_pptx.py` — 统一渲染器（10 种图表 + validate_and_fix 溢出检测）
- `styles/` — 10 套风格预设（含 chart_colors + best_for 元数据）
- `scripts/data_to_chart.py` — CSV/Excel → chart JSON 转换器（pandas）
- `references/design-guidelines.md` — 排版、配色、图表设计规范
- `examples/` — 4 个示例 content.json 文件

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


---

### 2.5. 需求拆解器 (Requirement Breakdown)

**目录**：`evyd-requirement-breakdown/`

将零散的产品想法、会议纪要、客户反馈等非结构化输入，转换为规范化的 Jira Requirement Ticket，使用 Y Model 框架（WHAT / WHY / HOW）进行分析。

**适用场景**：需求启动阶段、BA 整理需求、PM 对齐跨团队依赖

**输入**：任意形式的产品需求描述（文字、会议纪要、Figma 链接、聊天记录等）

**输出**：结构化 Requirement Ticket（英文 Markdown），包含：
- **WHAT**：用户场景分析
- **WHY**：业务目标与用户动机
- **HOW**：
  - **Use Cases**：用户旅程 + 功能边界定义表格，Module Legend 内嵌在各 UC 中
  - **Feature Scope**：产品与技术功能清单（采用 Fxx 编号，直接作为 `/evyd-user-story-writer` 的输入）
  - **Dependency Scope**：跨团队协作 TODO，含时机标注（前置 / 可并行 / 上线后）
- **Clarifying Questions**：针对未确认假设的追问
- **Notes**：实现假设、边界说明、补充备注

**触发词**：`需求拆解`、`requirement breakdown`、`帮我整理需求`、`做个 requirement doc`

**工作流位置**：`evyd-user-story-writer` 的上游 skill

**核心文件**：
- `SKILL.md` — 主流程与输出格式规范

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

### 9. 项目初始化 (Project Init)

**目录**：`evyd-project-init/`

标准化 EVYD 项目脚手架工具。在 `evydProject-XXX` 目录下一键完成：创建标准目录结构（`sourcecode/`、`requirementgathering/`）、初始化 Git、创建 GitHub 私有仓库、自动邀请团队协作者（write 权限）。

**适用场景**：新建 EVYD 项目时，快速搭建标准化项目结构并配置 GitHub 仓库

**触发词**：`初始化项目`、`project init`、`帮我把这个项目标准化`

**标准协作者**：alvinbjl、lmh521571-ai、lynnwu10504、CY246588

**核心文件**：
- `SKILL.md` — 完整初始化流程

---

### 10. 投诉/反馈提取器 (Complains Extractor)

**目录**：`evyd-complains-extractor/`

从录屏、录音、截图等原始媒体文件中，批量提取用户投诉和反馈，输出为结构化 bug/issue 表格。支持 Focus Group、用户测试、投诉渠道等场景。

**适用场景**：焦点小组录屏分析、用户测试反馈整理、投诉渠道媒体批量处理

**输入**：视频（.mov/.mp4 等）、音频（.mp3/.wav 等）、截图（.png/.jpg 等）

**处理流程**：
1. 扫描文件夹，按类型分组
2. 视频：ffmpeg 提取音频 + 关键帧 → whisper 转录 → Claude 视觉分析
3. 音频：ffmpeg 转换 → whisper 转录
4. 图片：Claude 多模态直接识别
5. 结构化提取为 5 列表格（Issue / Expectation / Screenshots / Reporter / Moderator）
6. 跨文件去重合并

**输出**：
- Confluence comment（安全追加，不覆盖页面）
- Excel (.xlsx)
- Markdown (.md)
- 可选：按需生成 Summary Analysis 报告（分类汇总 + 优先建议）

**触发词**：`投诉提取`、`feedback extraction`、`complains extractor`、`录屏分析`、`用户反馈整理`

**前置依赖**：`brew install ffmpeg` + `pipx install openai-whisper`

**核心文件**：
- `SKILL.md` — 完整处理流程 + 输出格式规范 + Summary 模板

---

### 11. 环境克隆 (Environment Clone)

**目录**：`evyd-env-clone/`

一键复制 EVYD 团队 Claude Code 工作环境到新设备。自检当前环境状态，自动安装可自动化的组件（skill symlinks、Python 包、gh CLI、插件配置），对需要手动操作的部分（Bedrock 凭证、MCP OAuth 连接）给出逐步指引。

**前提**：Claude Code 已安装，evyd-skills-workshop 仓库已 clone

**完整支持**：macOS + Windows（双平台命令分支）

**适用场景**：新成员 onboarding、跨设备迁移、环境一致性审计

**触发词**：`/evyd-env-clone`、`配置环境`、`环境克隆`、`onboard`、`检查我的环境`

**10 步工作流**：
1. 平台检测 + 前置工具检查
2. 创建 skill symlinks（动态发现，幂等）
3. 安装 Python 包
4. 安装 GitHub CLI
5. Claude Code 插件配置
6. Git 全局配置
7. GitHub 认证
8. SSH Key 设置
9. settings.json 模板（含中国代理配置）
10. MCP 连接 + 环境审计汇总表

**核心文件**：
- `SKILL.md` — 完整交互式工作流
- `references/requirements.txt` — Python 包清单
- `references/settings-template.json` — settings.json 模板（凭证脱敏）
- `references/settings-china-proxy.json` — 中国代理叠加配置
- `references/mcp-connections-checklist.md` — MCP 手动连接指南

---

### 8. PPT 生成器 v2.2 (PPT Generator)

**目录**：`evyd-ppt-generator/`

从内容 JSON 生成 EVYD 品牌风格的 PPTX 演示文稿，纯程序化 free-mode 渲染，输出真实可编辑的形状和文字（非截图）。布局类型由 AI 自动选择，无需手动指定。

**v2.2 能力**：7 种叙事模板、直接用户画像、三轮搜索 + 5 级可信度、10 种原生图表、图片搜索 + 视觉审美判断、CSV/Excel 数据管道、叙事连贯性检查、交付报告、11 项视觉 QA

**架构**：
```
用户需求 → 受众分析 + 叙事模板(7种) → 可选内容研究（三轮搜索 + 5级可信度）
    → 可选图片搜索（WebSearch + 下载验证）
    → 可选数据处理（CSV/Excel → pandas → chart JSON）
    → content.json（模型生成，约 400 tokens / 15 页）
    → gen_pptx.py + styles/（固定渲染器，不重新生成）
    → .pptx（PowerPoint 可直接编辑）
    → QA 验证（soffice 转图 + 11项 checklist）→ 交付摘要
```

**可用幻灯片类型（21 种）**：
- **Chrome 框架**：`cover` / `agenda` / `section_divider` / `ending`
- **内容布局**：`bullets_with_panel` / `two_column_check` / `cards_grid` / `criteria_rows` / `scope_tiers` / `two_panel` / `two_column_steps` / `scenario_cards` / `survey`
- **数据可视化**：`stat_highlight` / `timeline` / `chart`（10 种图表） / `comparison_table`
- **视觉强调**：`quote_full` / `center_focus` / `image_full`（支持图片搜索）
- **别名**：`key_metrics` → `stat_highlight` / `quote_highlight` → `quote_full`

**可用风格预设（10 套）**：`evyd_blue`（默认）/ `evyd_white` / `evyd_teal` / `dark_navy` / `cooltech` / `morandi` / `warm` / `monochrome` / `sunrise` / `charcoal_gold`

**触发词**：`生成PPT`、`做幻灯片`、`演示文稿`、`EVYD ppt`

**核心文件**：
- `SKILL.md` — 完整 JSON schema、7 种叙事模板、布局选型指引与 5 阶段 workflow（含视觉审美 + 连贯性检查）
- `gen_pptx.py` — 渲染器（10 种图表 + validate_and_fix 溢出检测）
- `styles/` — 10 套样式预设（含 chart_colors + best_for 元数据）
- `scripts/data_to_chart.py` — CSV/Excel → chart JSON 转换器
- `references/design-guidelines.md` — 排版、配色、图表设计规范
- `examples/` — 4 个示例 JSON

---

## 完整工作流

```
1. [竞品调研] 了解市场格局
        ↓
2. 描述产品需求
        ↓
2.5 [需求拆解器] 生成 Requirement Ticket（Y Model + UC + Feature Scope + Dependency）
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
[项目初始化] — 独立使用，新项目标准化脚手架 + GitHub + 协作者
[投诉提取器] — 独立使用，从录屏/录音/截图中提取结构化 bug 表格
[环境克隆] — 独立使用，新成员跨设备环境复制 + 自检 + 自动安装
```

## 项目结构

```
技能 skills 作坊/
├── README.md
├── evyd-ppt-generator/             # EVYD PPT 生成器 v2（JSON → 原生可编辑 PPTX，21 种布局 + 图表 + 叙事模板）
│   ├── SKILL.md
│   ├── gen_pptx.py
│   ├── styles/
│   └── examples/
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
├── evyd-requirement-breakdown/     # 需求拆解器（Y Model + UC + Story Scope + Dependency）
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
├── evyd-project-init/              # 项目初始化脚手架
│   └── SKILL.md
├── evyd-complains-extractor/       # 投诉/反馈提取器（媒体文件 → 结构化 bug 表格）
│   └── SKILL.md
├── evyd-env-clone/                 # 环境克隆（跨设备环境复制 + 自检）
│   ├── SKILL.md
│   └── references/
└── evyd-remote-repo-rules/         # 远程仓库工作流规则
```

## 输出渠道

`evyd-output-channels/SKILL.md` 包含 Active Config 和 8 个渠道的完整协议，改两行即可切换所有 skill 的输出方式。

| 渠道 | Reference | 环境要求 |
|---|---|---|
| feishu + lark-cli | `references/feishu-lark-cli.md` | 需安装 lark-cli |
| feishu + openclaw | `references/feishu-openclaw.md` | 待接入 |
| obsidian + local-fs | `references/obsidian-local-fs.md` | 无 |
| local-markdown + local-fs | `references/local-markdown-local-fs.md` | 无 |
| jira + claude-mcp | `references/jira-claude-mcp.md` | Claude Code + Atlassian OAuth |
| jira + community-mcp | `references/jira-community-mcp.md` | sooperset/mcp-atlassian + API Token |
| confluence + claude-mcp | `references/confluence-claude-mcp.md` | Claude Code + Atlassian OAuth |
| confluence + community-mcp | `references/confluence-community-mcp.md` | sooperset/mcp-atlassian + API Token |

### Jira / Confluence Per-skill 路由

Jira 和 Confluence 渠道不是所有 skill 统一写到一个地方，而是按 skill 分别路由：

| Skill | Jira | Confluence |
|---|---|---|
| evyd-competitor-research | — | 页面 → EPT1 / Overall Landscape |
| evyd-requirement-breakdown | Requirement ticket → BACKLOG | — |
| evyd-user-story-writer | Story ticket → BACKLOG（link Requirement） | — |
| evyd-ai-intention-brainstorm | Story ticket → BACKLOG（link Requirement） | — |
| evyd-lofi-figma-maker | Comment → 关联 ticket | — |
| evyd-user-manual | — | 页面 → BPS / To Be Moved（可覆盖） |
| evyd-design-review | Comment → 关联 ticket | — |
| evyd-pd-roadmap | 不适用（继续飞书多维表） | — |
| evyd-ppt-generator | 不适用（本地文件） | — |
| evyd-complains-extractor | — | Comment → 关联页面 |

## 技术栈

- **框架**：[Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- **输出集成**：可配置（默认飞书云文档，支持 Obsidian / 本地 Markdown / 聊天附件 fallback）

## 使用方式

在 Claude Code 中，直接通过对话触发对应技能。每个技能的 `SKILL.md` 描述了详细的触发词和工作流程。技能安装后，Claude Code 会自动识别触发条件并调用对应技能。
