---
name: evyd-complains-extractor
description: |
  Extract and structure user complaints/feedback from raw media files (video, audio, images).
  Process recordings from focus groups, user testing, or complaint sessions into formatted bug/issue tables.
  Supports output to Confluence comments, Excel, Markdown, or other platforms.
  Trigger: 投诉提取, feedback extraction, complains extractor, bug extraction from video,
  focus group analysis, user testing feedback, 用户反馈整理, 录屏分析, 投诉整理
---

# EVYD Complains Extractor

## Purpose
Process raw media files (videos, audio recordings, screenshots) from user testing sessions,
focus groups, or complaint channels, and convert them into structured bug/issue tables.
Optionally generate a Summary Analysis report on demand.

## Prerequisites Check
Before starting, verify these tools are available on the user's Mac:
1. **ffmpeg** — run `which ffmpeg` via Desktop Commander
2. **whisper** — run `which whisper` via Desktop Commander (installed via `pipx install openai-whisper`)
If either is missing, guide the user to install:
- ffmpeg: `brew install ffmpeg`
- whisper: `pipx install openai-whisper`

## Startup Flow
Every time this skill is activated, ask the user THREE questions before processing:

### Q1: Output Destination
Ask: "Where should I write the extracted issues?"
Options:
  a. **Confluence comment** — append as a comment on a Confluence page (safe, additive)
  b. **Excel (.xlsx)** — create a structured spreadsheet
  c. **Markdown (.md)** — create a local Markdown file
  d. **Other** — let user specify (e.g., Feishu, Notion, etc.)

### Q2: Moderator / Reporter Name
Ask: "Who is the moderator or reporter? (I'll use your profile name if you skip)"
- If the user has a known name (from user profile), pre-fill it
- Otherwise, require an answer

### Q3: Whisper Language
Ask: "What language is spoken in the recordings?"
- Default: `en` (English)
- Common options: `en`, `ms` (Malay), `zh` (Chinese), `id` (Indonesian)

## Supported File Types
| Category | Extensions |
|----------|-----------|
| Video    | .mov, .mp4, .avi, .mkv, .webm, .m4v, .flv, .wmv |
| Audio    | .mp3, .wav, .m4a, .aac, .ogg, .flac, .wma |
| Image    | .png, .jpg, .jpeg, .gif, .bmp, .webp, .heic, .tiff |

## Processing Pipeline

### Step 1: Scan Input Folder
- List all media files in the user-selected folder
- Group by type (video/audio/image)
- Report: "Found X videos, Y audio files, Z images. Proceed?"

### Step 2: Batch Extract (via Desktop Commander on Mac)
**For video files — use these EXACT ffmpeg commands:**
- Extract audio: `ffmpeg -i INPUT -vn -acodec pcm_s16le -ar 16000 -ac 1 OUTPUT.wav`
- Extract keyframes (1 frame per 5 seconds): `ffmpeg -i INPUT -vf "fps=1/5,scale=640:-1" OUTPUT_%03d.jpg`
- Use `nohup ... &` with marker files for long-running tasks (Desktop Commander has 60s timeout)
- Poll completion with marker files (e.g., `/tmp/extract_done_FILENAME`)

**For audio files:**
- Convert to wav if needed: `ffmpeg -i INPUT -acodec pcm_s16le -ar 16000 -ac 1 OUTPUT.wav`

**Transcribe all audio:**
- Run: `whisper INPUT.wav --model base --language LANG --output_format txt`
- Use background execution with marker files for batches

**For image files:**
- Read directly using Claude's multimodal vision capability
- Extract visible screen content, error messages, UI state

### Step 3: Analyze & Structure
For each media file, combine transcript + keyframe analysis to fill EXACTLY the 5 columns
defined in the Output Table Schema section below. Do not invent additional fields.

For each issue found, extract:
1. **Issue / Problems Reported** — what the user encountered (1-2 sentences max)
2. **What was expectation by the user?** — what they expected (1 sentence)
3. **Screenshots** — source file reference (e.g., `IMG_6241.MOV frame at 0:15`)
4. **Reporter (MOH)** — extracted from speech or context (e.g., "MOH tester")
5. **Moderator (EVYD)** — the name collected at startup

Deduplicate across files: if multiple files describe the same bug, merge into one entry.
Keep descriptions concise — this is a bug table, not a detailed analysis.

### Step 4: Write Output
Write results based on the chosen destination:

**Confluence comment:**
- Use `createConfluenceFooterComment` (Atlassian MCP)
- ⚠️ **NEVER use `updateConfluencePage`** — it replaces the entire page body
- Format as a horizontal 5-column table using the EXACT Output Table Schema
- Batch into groups of ~5-6 entries per comment if many issues
- Include header row in EVERY comment so each is self-contained and copy-pasteable
- Example Confluence comment body (markdown format):

```
**Batch 1/3 — Extracted from IMG_6241.MOV ~ IMG_6245.MOV | 2026-04-10 | 6 issues**

| Issue / Problems Reported | What was expectation by the user? | Screenshots | Reporter (MOH) | Moderator (EVYD) |
|---|---|---|---|---|
| App crashes on nutrition log submit | Meal should save successfully | IMG_6241.MOV 0:12 | Tester A | ZhaoLi |
| Step count stuck at 0 | Accurate step sync from phone | IMG_6243.MOV 0:08 | Tester B | ZhaoLi |
```

**Excel (.xlsx):**
- Create workbook with columns matching the output schema
- One row per issue, auto-sized columns

**Markdown (.md):**
- Write a Markdown table with the same columns
- Save to the workspace output folder

**Other:**
- Ask user for the target format and API/tool available
- Adapt the table structure accordingly

## Output Table Schema — MANDATORY FORMAT
Use EXACTLY these 5 columns. Do NOT add extra columns (no Severity, no Confidence, no Category, no Module).
Do NOT use vertical per-issue layouts. Always output a single horizontal table with one header row and one row per issue.

| Issue / Problems Reported | What was expectation by the user? | Screenshots | Reporter (MOH) | Moderator (EVYD) |
|---|---|---|---|---|
| App crashes when clicking "Submit" on nutrition log | Expected the meal to be saved successfully | IMG_6241.MOV frame at 0:12 | Tester A | ZhaoLi |
| Step count shows 0 despite walking 5000+ steps | Expected accurate step tracking synced from phone | IMG_6243.MOV frame at 0:08, screenshot_01.png | Tester B | ZhaoLi |

Column definitions:
- **Issue / Problems Reported** — concise description of the bug or friction point (1-2 sentences)
- **What was expectation by the user?** — what the user expected to happen (1 sentence)
- **Screenshots** — source file reference with timestamp if from video (e.g., `IMG_6241.MOV frame at 0:15`)
- **Reporter (MOH)** — who reported it, extracted from speech context or "Unknown"
- **Moderator (EVYD)** — the moderator name collected at startup

## Summary Classification (On-Demand Only)

**⚠️ This feature is triggered ONLY when the user explicitly asks for it.**
Do NOT auto-generate a summary after extraction. Wait for the user to say something like:
"summarize", "classify", "generate summary", "总结", "分类汇总"

### Summary Output Structure
The Summary report follows this exact structure (based on the EVYD Feedback Analysis template):

#### Section 1. Key Take Away
- **Overall takeaway**: 1-2 sentence executive summary of the main finding
- **Biggest improvement opportunities**: bulleted list of top 3-5 areas

#### Section 2. Statistics
- **2.1 Dataset Overview**
  - Total feedback records reviewed: [count]
  - Source: [table/file name]
  - Module / category covered: [if applicable]
  - Page / feature covered: [if applicable]
- **2.2 Satisfaction Summary** (if satisfaction data exists)
  - Like: [count]
  - Dislike: [count]
  - Neutral / No rating: [count]
- **2.3 High-Level Interpretation**
  - Narrative paragraph explaining the gap between surface sentiment and actual friction
  - Separate: (a) Emotional satisfaction vs (b) Operational friction / product issues

#### Section 3. Analysis of User Feedback
- **3.1 First-Level Summary by Feedback Intent**
  Categorize all feedback into intent layers:
  1. Positive appreciation — users who liked the experience
  2. Usability appreciation — users who found it easy/clear
  3. Product friction hidden inside positive sentiment — complaints masked as praise

- **3.2 Secondary Category Summary from Labels and Comments**
  1. Positive-oriented secondary themes (e.g., Clear instructions, Easy to follow, Useful info)
  2. Negative-oriented secondary themes (e.g., Step sync failure, Reward threshold unclear, 
     Nutrition logging difficulty, Mode confusion, Challenge burden)
  - List each theme as a bold bullet

- **3.3 Theme-Based Summary with Original Comments**
  For each negative theme, create a subsection:

  **Theme N: [Theme Name]**
  - **Summary of findings**: 1 paragraph describing the issue pattern, severity, and product impact
  - **Evidence table**:
    | Satisfaction | User selected label(s) | Original comment |
    |---|---|---|
    | Like/Dislike | label1 / label2 | verbatim user comment |
    - Include ALL original comments that belong to this theme
  - **Product insight and recommendation**: 1 paragraph with specific, actionable product suggestions

#### Section 4. Prioritized Recommendations (optional)
If enough themes exist, provide a numbered priority list:
1. [Top priority action] — with sub-bullets for specific steps
2. [Second priority] — with sub-bullets
3. ...continue as needed
Each recommendation should reference which theme(s) it addresses.

#### Section 5. Reference to the Original Source
- **Original source**: [name of Bitable / Confluence page / Excel file]
- **Reference URL**: [link if available]

### Summary Input Requirements
The Summary can work from TWO types of input:
1. **Structured data** — a Bitable, Excel, or table with columns like:
   Feedback ID, Module, Page Name, Satisfaction Status, Comment Label, Comment, Timestamp
2. **Previously extracted issues** — the bug table generated by Step 1-4 of this skill

### Summary Output Destination
Ask the user where to write the Summary:
- Confluence page (new page or comment)
- Markdown file
- Feishu Doc
- Excel with multiple sheets (Summary + Raw Data)

## Error Handling
- If ffmpeg/whisper fails on a file, log the error and skip to next file
- Report skipped files at the end: "Processed X/Y files. Skipped: [list]"
- If a video has no audio track, rely solely on keyframe analysis
- If an image is unreadable, report and skip

## Cleanup
After processing is complete:
- Remove temporary .wav files created during extraction
- Remove temporary keyframe .jpg files
- Keep original media files untouched

## Important Safety Rules
- **NEVER use `updateConfluencePage`** — it replaces the entire page body and will destroy existing content
- **ALWAYS use `createConfluenceFooterComment`** for Confluence output — it's safe and additive
- **NEVER delete or modify the user's original media files**
- **Desktop Commander timeout**: commands >60s must use `nohup ... &` with marker files
  - Pattern: `nohup bash -c 'COMMAND && touch /tmp/MARKER' &`
  - Poll: check for marker file existence every 5-10 seconds

## Language
- All output (issues, summaries) should be in **English** unless the user specifies otherwise
- Timestamps in output: use ISO format (YYYY-MM-DD)
- Tag output with: total issues extracted, extraction date, source file count
