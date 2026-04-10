---
name: evyd-project-init
description: |-
  Initialize a standard EVYD project: create folder structure, template files, git repo, private GitHub repo, and add collaborators.
  Use when user has created a new evydProject-XXX folder and wants to set up the standard project scaffolding.

  Examples:
  - user: "初始化这个项目" → run project init in current directory
  - user: "/evyd-project-init" → scaffold directories, git, GitHub, collaborators
  - user: "帮我把这个项目标准化" → apply EVYD project conventions
---

# EVYD Project Init

Initialize a standard EVYD project with folder structure, git, GitHub private repo, and team collaborators.

## Prerequisites

- User has already created and cd'd into an evydProject-XXX folder
- gh CLI is authenticated (gh auth status)
- Git is available

## Step 1: Validate Current Directory

Check the current working directory name matches evydProject-* pattern. If not, warn and confirm with user before proceeding.

## Step 2: Create Standard Directory Structure

```
evydProject-XXX/
├── sourcecode/              # All runnable source code & assets
└── requirementgathering/    # Business requirements & reference docs
    └── figma-content.md     # Figma requirement template (pre-created)
```

Create directories:

```bash
mkdir -p sourcecode requirementgathering
```

Write `requirementgathering/figma-content.md` with this template:

```markdown
# Figma 需求文档 - [项目名称]

> Figma 源文件: [贴 Figma 链接]
> 最后更新: [日期]

---

## 一、业务流程分析

<!-- 从 Figma 中提取的流程图、部门职责、核心痛点 -->

## 二、客户会议纪要

<!-- 会议日期、议题、Quick Takeaways、Action Items、关键决策 -->

## 三、新增需求

<!-- 会议中识别的新需求，按模块分类 -->

## 四、已有需求变更

<!-- 对已有功能的调整或升级 -->
```

## Step 3: Initialize Git & GitHub

```bash
git init
git add -A
git commit -m "Initial commit: project scaffolding"
gh repo create "$(basename "$(pwd)")" --private --source=. --push
```

## Step 4: Add Standard Collaborators

Four collaborators with write permission:

```bash
REPO="lizhao86/$(basename "$(pwd)")"
gh api "repos/$REPO/collaborators/alvinbjl" -X PUT -f permission=push
gh api "repos/$REPO/collaborators/lmh521571-ai" -X PUT -f permission=push
gh api "repos/$REPO/collaborators/lynnwu10504" -X PUT -f permission=push
gh api "repos/$REPO/collaborators/CY246588" -X PUT -f permission=push
```

## Step 5: Report Results

Summarize to user:
- Repo URL: https://github.com/lizhao86/<project-name>
- Directories created: sourcecode/, requirementgathering/
- Template created: requirementgathering/figma-content.md
- Collaborator invitations sent: alvinbjl, lmh521571-ai, lynnwu10504, CY246588

## Standard Collaborators Reference

| GitHub Username | Permission |
|-----------------|------------|
| alvinbjl        | write      |
| lmh521571-ai    | write      |
| lynnwu10504     | write      |
| CY246588        | write      |

## Common Issues

- **gh not authenticated**: Ask user to run `! gh auth login`
- **Repo name conflict**: Prompt user to choose a different name or delete existing repo
- **Folder name wrong**: Warn but allow user to confirm proceeding anyway
