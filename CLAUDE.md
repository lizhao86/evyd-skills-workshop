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

独立使用：`evyd-ai-intention-brainstorm`、`evyd-pd-roadmap`、`evyd-ppt-generator`、`evyd-project-init`、`evyd-complains-extractor`、`evyd-env-clone`、`evyd-team-todo`

## 常用命令

### PPT 生成器（唯一含可执行代码的 skill）

```bash
cd evyd-ppt-generator
python3 gen_pptx.py content.json --style evyd_blue --output output.pptx
```

可用风格（10 套）：`evyd_blue`（默认）/ `evyd_white` / `evyd_teal` / `dark_navy` / `cooltech` / `morandi` / `warm` / `monochrome` / `sunrise` / `charcoal_gold`

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
