---
name: evyd-lofi-figma-maker
description: |-
  Generate copy-paste Figma Make prompts for LoFi wireframes from User Story documents.
  Use when converting user stories to Figma wireframe prompts, generating lofi mockup prompts, or preparing designs for Figma Make.
  Use proactively when user shares a user story and asks to generate wireframes, Figma prompts, or lofi designs — even without explicitly invoking this skill.

  Examples:
  - user: "帮我把这个 User Story 转成 Figma lofi 线框图 prompt" → parse story, generate prompts
  - user: "生成可以粘贴到 Figma Make 的脚本" → extract UI info, output ready-to-copy prompt blocks
  - user: "这个 AC 对应几个屏幕" → analyze AC scenarios, identify distinct screen states
  - user: "Generate Figma Make prompts for the login feature" → parse story, map AC to screens, output prompts
  - user: "帮我把 AC 里的错误处理也生成一个 wireframe" → generate error state prompt from AC
---

# LoFi Figma Make Prompt Generator

Generate ready-to-copy prompts for **Figma Make** (Figma's official AI design feature) from User Story documents. One prompt per screen state.

## Step 1: Parse the User Story

Extract the following fields from the provided User Story:

| Field | Source in User Story |
|-------|----------------------|
| Platform | Title `[Platform]` — e.g., App, Web, Admin Portal |
| System + Module | Title `[System] [Module]` |
| User Role | Title `As a [Role]` |
| Goal | Title `I [action/goal]` |
| Feature Context | Description section (1–2 sentences) |
| Primary Flow | AC Happy Path scenario |
| Secondary Flows | AC Alternative Path scenarios |
| Error States | AC Error Handling scenarios |
| Edge Cases | AC Edge Case scenarios |

Also capture any **supplementary description** provided by the user — layout preferences, specific components, screen dimensions, or additional context not in the user story.

## Step 2: Identify Screens

Map each AC scenario type to a screen to wireframe:

| AC Scenario Type | Screen to Generate |
|------------------|--------------------|
| Happy Path | Primary screen — default / loaded state |
| Alternative Path | Secondary screen or next step in a multi-step flow |
| Edge Case | Empty state, zero-data, or boundary condition screen |
| Error Handling | Error/validation state — inline errors, failure modal, or error screen |

**If the user story has 5+ AC scenarios**, consolidate where logical (e.g., multiple error scenarios → one error state screen).

If the user did not specify which screens to generate, generate prompts for **Happy Path + Error Handling** by default, and list the other available screens with a note that the user can request them.

## Step 3: Generate Prompts

For each identified screen, generate one Figma Make prompt using @Figma-Make-Prompt-Template.md.

Apply these judgments when building the component list:
- **Infer standard components from context** — e.g., "login" implies email input + password input + primary CTA; "list view" implies search bar + list item cards + empty state
- **Translate AC language into UI components** — e.g., "user sees a confirmation" → Modal dialog; "system shows an error" → Inline error message or Warning banner
- **Use the Component Vocabulary** from the template — exact terms matter for Figma Make recognition
- **Order components top to bottom** in the list, matching visual hierarchy
- **One prompt = one screen state** — do not mix default and error states in one prompt

## Output Format

Output each prompt as a clearly labeled, copy-paste ready block. Add a brief note explaining which AC scenario it maps to.

---

### Prompt [N]: [Screen Name]

> *Maps to: AC Scenario [N] — [Scenario Name]*

```
[full prompt content here — ready to paste into Figma Make]
```

---

Separate each prompt with `---`. After all prompts, add a **Screens Overview** table listing all identified screens, which were generated, and which are available on request.

### Available Templates

| Template | When to Use |
|----------|-------------|
| @Figma-Make-Prompt-Template.md | Default — Figma Make (Figma official AI), LoFi wireframes |

## Output Channel

When the user requests writing output to a doc / cloud storage, read `../evyd-output-channels/SKILL.md` for the active channel’s write protocol, format constraints, and naming convention.

- File type: `「LoFi」`
- Default folder: ask the user if not specified

### Document Structure (skill-specific, apply after channel protocol)

When writing multiple prompts, always use this structure regardless of channel:

- `# [Feature / Story Name]`
- `## Prompt 1: [Screen Name]`
- short note: `Maps to: [AC scenario / screen state]`
- prompt body in plain text block
- repeat for Prompt 2 / Prompt 3 if needed

Do not collapse multiple prompts into one long paragraph.
