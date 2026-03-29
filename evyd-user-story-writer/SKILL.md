---
name: evyd-user-story-writer
description: |-
  Write structured User Story documents with Acceptance Criteria from product requirements.
  Use when writing user stories, decomposing features into stories, or creating sprint backlog items.
  Use proactively when user mentions a new feature, requirement detail, or asks to write/improve user stories.

  Examples:
  - user: "帮我写权限管理的 User Story" → clarify [Platform][System][Module] then generate story
  - user: "这个需求帮我拆成几个 User Story" → split into separate independent stories each with AC
  - user: "Write a user story for the login feature" → generate with Given-When-Then-And AC
  - user: "我有个新功能想法" → guide through requirement clarification then write story
  - user: "User Story 的 AC 帮我补全" → generate scenarios covering all path types with Coverage Checklist
---

# User Story Writer

Write high-quality User Story documents. Apply senior product manager judgment — healthcare internet industry context.

## Step 1: Clarify Requirements

If the requirement is not specific enough, ask clarifying questions **in Chinese**. Collect:

- `[Platform]` — e.g., App, Web, Admin Portal
- `[System]` — e.g., Routines, Health Records, Permissions
- `[Module]` — e.g., Logging, Assignment, Notifications
- Requirement detail — target user, goal, core functionality

**Clarification rules:**
- Only ask questions that will materially affect the output (scope, business logic, permission/role, UI behavior, acceptance criteria)
- Group questions by topic
- Do not ask about content that can be reasonably inferred from context
- Do not fabricate business rules unless they are explicitly stated or strongly implied by the requirement

Skip this step if the user has already provided sufficient detail.

## Step 2: Writing Guidelines

Apply these perspectives when generating or refining stories:

- **Healthcare management**: health behaviour tracking, adherence, health goal achievement, medication safety boundaries
- **Product / UX**: interaction flow clarity, user mental model alignment, notification effectiveness, personalisation
- **System / technical**: system state transitions, data storage and updates, role/permission enforcement, failure scenarios
- **UI behaviour**: button states, input fields, selectors, toggle states, modal/drawer/page navigation, hover/disabled/read-only/editable states

## Step 3: Story Separation Rule

Separate different functionalities into **individual user stories**. Each story MUST:

- Focus on a single, cohesive capability that delivers specific value
- Be independently implementable and testable
- Address one clear user need or functionality
- Have its own title, description, and acceptance criteria
- Not mix unrelated UI, business logic, notification, or data logic unless they are inseparable

## Output Format

Output in **English with markdown** regardless of the input language.

### Available Templates

| Template | When to Use |
|----------|-------------|
| @EVYD-User-Story-Template.md | Default — EVYD platform, healthcare context |

### Mandatory Template Compliance (Do Not Skip)

When using a template:
1) **Open and follow the template file verbatim** (read it from the skill folder) before drafting.
2) **Render every required section heading** in the final output (do not omit sections such as **Figma Section Link(s)**).
3) Keep placeholders exactly as the template specifies (e.g., `N/A _(Remove if Applicable)_`).
4) If splitting into multiple stories, **each story must be a full template instance** (Title + Description + Figma links + Acceptance Criteria).

### Acceptance Criteria Rules

- Use Given-When-Then-And for every scenario
- Write as many scenarios as the feature genuinely requires — do not pad to hit a fixed number
- Every scenario must be verifiable by QA — no interpretation required
- **Forbidden phrases**: "should work properly", "should be user-friendly", "should be clear", "should be intuitive"
- After all scenarios, fill in the **Coverage Checklist** in the template. Mark each category as `✅ Scenario N` or `N/A`. N/A is an explicit decision, not an omission.
- The Coverage Checklist sits after `<!-- ai-context-end -->` — it is for human review only and must not be included when passing the story to downstream AI tools

### Output Channel

When the user requests writing output to a doc / cloud storage, read `../evyd-output-channels/SKILL.md` for the active channel's write protocol, format constraints, and naming convention.

- File type: `「UserStory」`
- Default folder: ask the user if not specified

Select the appropriate template based on user context or explicit request. Default to EVYD format unless the user specifies otherwise.
