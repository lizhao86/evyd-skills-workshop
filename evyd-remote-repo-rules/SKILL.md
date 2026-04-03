---
name: evyd-remote-repo-rules
description: Manage the EVYD skills GitHub-backed repository workflow for creating, updating, linking, and publishing skills. Use when asked to create a new EVYD/Ned skill, update evydskills from GitHub, fix workspace/skills structure, maintain symlink exposure from workspace/skills to the repo, or commit/push EVYD skills changes back to GitHub.
---

# EVYD Remote Repo Rules

Use this skill to keep EVYD/Ned skills consistent across the Git repository and `workspace/skills/` runtime exposure.

## Canonical locations

- Git source of truth: `/root/.openclaw/repos/evyd-skills-made-by-Ned`
- Runtime exposure: `/root/.openclaw/workspace/skills`

## Non-negotiable rules

1. Treat `/root/.openclaw/repos/evyd-skills-made-by-Ned` as the only Git working repository.
2. Ensure EVYD/Ned skills appear at `workspace/skills/<skill-name>`.
3. Do not leave nested paths like `workspace/skills/evyd-skills-made-by-Ned/<skill-name>`.
4. Expose repo-managed EVYD/Ned skills in `workspace/skills/` via symlinks, not copied duplicates.
5. Run Git operations (`status`, `diff`, `add`, `commit`, `push`, `pull`) against the repo path, not against `workspace/skills`.

## When creating a new EVYD/Ned skill

1. Create the skill folder inside `/root/.openclaw/repos/evyd-skills-made-by-Ned/<skill-name>`.
2. Add the required `SKILL.md` and any needed `references/`, `scripts/`, or `assets/`.
3. Ensure the skill name uses lowercase letters, digits, and hyphens only.
4. Replace any existing `workspace/skills/<skill-name>` directory with a symlink to the repo folder.
5. Verify `workspace/skills/<skill-name>/SKILL.md` resolves correctly.
6. If asked to publish, commit and push from the repo.

## When the user says "evydskills 更新了，git" or similar

1. Update `/root/.openclaw/repos/evyd-skills-made-by-Ned` from GitHub.
2. Scan repo subdirectories and treat folders containing `SKILL.md` as managed skills.
3. For each managed skill, ensure `workspace/skills/<skill-name>` is a symlink to the repo folder.
4. Remove stale nested exposure patterns under `workspace/skills/evyd-skills-made-by-Ned` if they appear.
5. Report the new HEAD commit and any added/removed skills.
6. Do not touch the main workspace repository unless the user explicitly asks.

## When editing and publishing EVYD/Ned skills

1. Edit either through the repo path or through `workspace/skills/<skill-name>`; they should resolve to the same repo files.
2. Before committing, review `git status` and `git diff` in `/root/.openclaw/repos/evyd-skills-made-by-Ned`.
3. Commit only the intended skill changes.
4. Push to the repo's configured GitHub remote when the user asks to sync/publish.

## Validation checklist

- The skill folder exists in the repo.
- `workspace/skills/<skill-name>` is a symlink.
- `workspace/skills/<skill-name>/SKILL.md` is readable.
- No unwanted nested repo directory remains under `workspace/skills/`.
- Git status in the repo matches the intended state.
