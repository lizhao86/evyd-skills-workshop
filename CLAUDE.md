# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

EVYD 产品团队的 Claude Code Skills 工具包，覆盖竞品调研 → 需求定义 → 用户故事 → 设计落地 → 文档交付的完整产品流程。每个 skill 是一个独立目录，入口文件为 `SKILL.md`。

## 架构

### Skill 结构约定

每个 skill 目录的标准结构：
- `SKILL.md` — 入口文件，定义触发词、工作流、输出格式（必须存在）
- `references/` — 可选的参考模板、schema、角色设定等
- `scripts/` — 可选的辅助脚本（如 `evyd-pd-roadmap/scripts/detect_duplicates.py`）

### 注册与暴露

- Skills 通过 symlink 暴露给 Claude Code：`~/.claude/skills/<skill-name>` → 本仓库对应目录
- `.claude-plugin/plugin.json` 定义插件元信息，`repackage-plugin.sh` 用于打包 `.plugin` 文件供 Cowork 安装

### 输出渠道系统

`evyd-output-channels/` 是所有 skill 共用的输出渠道抽象层，`destination + executor` 两层配置。支持 8 个渠道组合：飞书（lark-cli / openclaw）、Obsidian、本地 Markdown、Jira（claude-mcp / community-mcp）、Confluence（claude-mcp / community-mcp）。其中 `claude-mcp` 依赖 Claude Code 内置 Atlassian MCP（零配置），`community-mcp` 使用 sooperset/mcp-atlassian（需 API Token）。Jira/Confluence 渠道按 skill 分别路由到不同操作（创建 ticket / 创建页面 / 添加 comment），详见各 reference 文件中的路由表。

### 主链路工作流

```
evyd-competitor-research → evyd-requirement-breakdown → evyd-user-story-writer → evyd-lofi-figma-maker → evyd-design-review
                                                              ↓
                                                        evyd-user-manual
```

独立使用：`evyd-ai-intention-brainstorm`、`evyd-pd-roadmap`、`evyd-ppt-generator`、`evyd-project-init`、`evyd-complains-extractor`、`evyd-env-clone`、`evyd-team-todo`、`evyd-data-analysis`

### evyd-data-analysis 数据分析 skill

- 输入：用户提供的 Excel/CSV 数据文件
- 三层输出结构（顺序固定，严格分离）：Data Facts → Insights → Actions
- 统计计算：pandas + scipy/statsmodels，非纯 prompt，所有结论需有计算支撑
- 证据标签：`[已知]` `[推断]` `[假设]` `[风险]`，混入主观判断为违规
- PPT 联动：分析结果可自动转为 `content.json` 交给 `evyd-ppt-generator` 生成管理层汇报 PPT（Narrative Template E）
- PPT 全 freeform：所有幻灯片使用 `freeform` 类型，不用 `stat_highlight`/`chart`/`ending` 等结构化类型
- PPT 排版铁律：正文 sz ≥ 18，标题 sz ≥ 36，每个数据页底部必须有独立来源标注（sz 12, y ≥ 9.5, color text_dim），禁止将来源嵌入正文或卡片 body
- 参考材料：`references/metric-playbook.md`（指标手册）、`references/examples.md`（分析案例）、`references/analysis-frameworks.md`（统计方法）

### evyd-team-todo 数据与输出约定

- 数据文件：`todo/team-todo.md`，完成即删除，不保留 `[x]` 标记（可选扩展支持 `[~]` 进行中、`[x]+Done:` 保留、`Updated:` 更新日期、缩进子项）
- 成员映射：`todo/members.md`，userid ↔ 姓名 ↔ 角色
- Due 格式：`YYYY-MM-DD`（不是 MM-DD）
- 报告中的优先级标记（P0/P1/P2）根据 Due vs 当前日期动态计算，不存储在数据中
- 无优先级字段，不要在输出中凭空添加”高优/中优”
- **每日推送**：通过 OpenClaw cron 定时为每位成员生成待办摘要并投递，渠道解耦（企微/飞书/Telegram/webchat 等均可），详见 `references/daily-push.md`
- **身份识别三步决策树（每次对话必须先跑）：**
  - Step 1：userid 精确匹配 → 命中则直接进入操作
  - Step 2：未命中 → 问用户姓名
  - Step 3：姓名比对 members.md → 完全相同则确认绑定 / 相似则列出澄清 / 无匹配则注册新用户
  - 禁止跳过 userid 匹配直接猜测身份，禁止未经确认关联已有成员
- **五个操作的输出格式均已锁死**，各含严格模板 + 禁止清单，不允许漂移：
  - ① 布置：`✅ 已给{姓名}加了待办：{内容}`
  - ② 查看：`📋 你的待办（N条未完成）：` + 编号列表 + 固定尾句
  - ③ 更新：`✅ 已删除/已更新` 或 `❓ 匹配到N条`
  - ④ 汇总：`📊 团队待办汇总` + 严格模板
  - ⑤ 推送：`✅ 已为{姓名}开启每日推送` + cron 管理

## 常用命令

### PPT 生成器（唯一含可执行代码的 skill）

```bash
cd evyd-ppt-generator
python3 gen_pptx.py content.json --style evyd_blue --output output.pptx
```

可用风格（28 套，v2 schema）：
- business：`evyd_blue` / `evyd_white` / `evyd_teal` / `dark_navy` / `charcoal_gold` / `boardroom_slate` / `fintech_navy` / `pitch_vc` / `investor_deck`
- tech-dark：`cooltech` / `tokyo_night` / `cyberpunk_neon` / `terminal_green`
- editorial：`morandi` / `warm` / `warm_soft` / `sunrise` / `magazine_bold` / `newspaper_editorial` / `vogue_serif`
- lifestyle：`xhs_white` / `xhs_warm` / `pastel_dream` / `cafe_cream`
- minimal：`monochrome` / `nordic_minimal` / `bauhaus_primary` / `zen_mono`

主题目录 + 推荐算法见 `evyd-ppt-generator/references/theme-catalog.md`。对比度审计：`python3 gen_pptx.py --check-contrast`。

**工作流（先模板，后内容）**：

1. **先选叙事模板**（A–K，11 套）— 看受众 + 时长 + 是要决策还是要梳理，2 分钟搞定。模板**先于**内容定，因为它决定后续要去找什么数据。
2. **可选调研**（Phase 2）— 只在用户明确触发（"帮我查一下"）或素材明显不足时才跑。**默认假设用户自己有内容**，不要主动开 web search。
3. **写 content.json** — 按模板结构填，模板规定 slide 类型节奏，用户内容塞进格子里。
4. **渲染 + 对比度审计**

三种工况：
- 用户给了完整内容 → AI 是编辑/排版师，模板组织素材
- 用户给了主题 + 大纲 → AI 是 ghost-writer，模板指引调研方向
- 用户只给一句话意图 → AI 先反问受众/时长定模板，再问"你手上有素材还是要我研究"

模板是**假设**不是合同。中途如果证据指向更强结构（如数据极强→从 A 切到 E 金字塔），AI 必须**显式**提议切换并让用户拍板，不能闷头改。

### 插件打包

```bash
./repackage-plugin.sh
```

Git pull 后运行，生成 `evyd-skills.plugin` 供 Cowork 重新安装。

## 开发约定

- 新增 skill 时，必须创建 `<skill-name>/SKILL.md` 作为入口，并在 `~/.claude/skills/` 下创建 symlink
- Skill 命名统一使用 `evyd-` 前缀（团队工具）
- 所有 skill 的文本输出默认英文，对话交互使用中文
- `evyd-requirement-breakdown` 的 Feature Scope 输出（Fxx 编号）直接作为 `evyd-user-story-writer` 的输入，两者格式耦合

### 计划执行纪律（防止默默漏项）

当在 `/root/.claude/plans/*.md` 里写好了计划并进入执行阶段：

1. **每个 Phase 都要建对应的 todo**。Phase 下每个具体子项（helper、JSON 文件、CLI 标志、验证步骤）都要有独立的 pending todo——不要把"Phase N"作为一个粗颗粒度的 todo 就完事。
2. **子项落地后才能 complete 那个 Phase**。例如计划里说 "Phase 3 = header_rule_color + card_radius + drop-shadow"，三样都跑通了才能把 Phase 3 标 completed。只做一样就标 completed 是违规的 silent scope cut。
3. **验证步骤不是可选**。计划里列出的 verification 步骤（render 样例、跑 `--check-contrast`、回归测试）每一步都要建 todo 并执行。验证漏跑就是计划没完成。
4. **主动降级要明说**。如果中途发现某子项不值得做（性价比差、有技术阻塞），必须先用 AskUserQuestion 或在输出里**显式**告知用户并让对方确认，而不是静默跳过。
5. **收尾时对账**。commit 前重新打开 plan 文件对照一遍，任何偏差都要在 commit message 或对话里说明。
