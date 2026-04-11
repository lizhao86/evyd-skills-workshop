---
name: evyd-env-clone
description: |-
  Clone and replicate the EVYD team Claude Code environment on a new machine.
  Self-diagnoses installed vs missing components, auto-installs what it can, gives manual instructions for the rest.
  Supports both macOS and Windows. Idempotent — safe to run multiple times.

  Prerequisites: Claude Code installed, evyd-skills-workshop repo already cloned.

  Examples:
  - user: "/evyd-env-clone" → full environment setup wizard
  - user: "帮我配置 Claude Code 环境" → run environment clone
  - user: "检查我的环境" → audit-only mode, report what's missing
  - user: "onboard new team member" → environment replication
---

# EVYD Environment Clone

Replicate the EVYD team Claude Code environment on a new machine. Runs self-diagnosis, auto-installs what it can, and provides manual instructions for the rest.

## Prerequisites

- Claude Code is installed and running (`claude --version` works)
- This repo (evyd-skills-workshop) is already cloned locally
- User knows the local path to this repo

## Step 0: Platform Detection & Prerequisite Check

Detect the operating system and check for required tools.

### Detect OS

```bash
# macOS/Linux
OS_TYPE=$(uname -s 2>/dev/null)
```

If `uname` fails or returns `MINGW*`/`MSYS*`/`CYGWIN*`, or if running in PowerShell where `$env:OS` equals `Windows_NT`, set platform to **Windows**.

Set platform variable:
- `PLATFORM=macos` if Darwin
- `PLATFORM=windows` if Windows_NT / MINGW / MSYS
- `PLATFORM=linux` if Linux

### Check Required Tools

Check each tool and report status:

| Tool | Check Command | macOS Install | Windows Install |
|------|--------------|---------------|-----------------|
| git | `git --version` | `brew install git` | `winget install Git.Git` |
| node | `node --version` | `brew install node` | `winget install OpenJS.NodeJS.LTS` |
| python3 | `python3 --version` (mac) / `python --version` (win) | `brew install python@3` | `winget install Python.Python.3.13` |
| pip | `pip3 --version` (mac) / `pip --version` (win) | comes with python | comes with python |
| brew | `brew --version` | [brew.sh](https://brew.sh) | N/A |
| winget | `winget --version` | N/A | built-in on Windows 10/11 |

If git is missing, **stop** — it's required for everything else. Display install command and wait.

For other missing tools, collect them into a list and install in later steps as needed.

Report format:
```
=== Platform Detection ===
  OS: macOS (Darwin arm64) / Windows 11 / Linux
  
=== Tool Check ===
  [OK] git 2.50.1
  [OK] node v22.14.0
  [OK] python3 3.9.6
  [OK] pip3 21.2.4
  [OK] brew 4.x (macOS only)
  [MISSING] gh — will install in Step 3
```

## Step 1: Create Skill Symlinks

Dynamically discover all `evyd-*` directories in this repo that contain a `SKILL.md`, and create symlinks from `~/.claude/skills/` to each.

### macOS / Linux

```bash
REPO_DIR="<path-to-evyd-skills-workshop>"
SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$SKILLS_DIR"

for skill_dir in "$REPO_DIR"/evyd-*/; do
  skill_name=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    target="$SKILLS_DIR/$skill_name"
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$(cd "$skill_dir" && pwd)" ]; then
      echo "  [SKIP] $skill_name (already linked)"
    else
      rm -f "$target"
      ln -s "$(cd "$skill_dir" && pwd)" "$target"
      echo "  [LINK] $skill_name → $target"
    fi
  fi
done
```

### Windows (PowerShell)

Windows symlinks require **Developer Mode** enabled or **Administrator** privileges.

First, test if symlinks work:
```powershell
$testLink = "$env:TEMP\symlink_test_" + (Get-Random)
$testTarget = $env:TEMP
try {
    New-Item -ItemType SymbolicLink -Path $testLink -Target $testTarget -ErrorAction Stop | Out-Null
    Remove-Item $testLink
    Write-Host "[OK] Symlinks are available"
} catch {
    Write-Host "[ERROR] Symlinks not available. Please enable Developer Mode:"
    Write-Host "  Settings → System → For developers → Developer Mode → ON"
    Write-Host "  Then restart your terminal and re-run this skill."
}
```

If symlinks work, create them:
```powershell
$RepoDir = "<path-to-evyd-skills-workshop>"
$SkillsDir = "$env:USERPROFILE\.claude\skills"
if (!(Test-Path $SkillsDir)) { New-Item -ItemType Directory -Path $SkillsDir | Out-Null }

Get-ChildItem -Path $RepoDir -Directory -Filter "evyd-*" | ForEach-Object {
    $skillName = $_.Name
    $skillMd = Join-Path $_.FullName "SKILL.md"
    $linkPath = Join-Path $SkillsDir $skillName
    if (Test-Path $skillMd) {
        if ((Test-Path $linkPath) -and ((Get-Item $linkPath).Target -eq $_.FullName)) {
            Write-Host "  [SKIP] $skillName (already linked)"
        } else {
            if (Test-Path $linkPath) { Remove-Item $linkPath -Force -Recurse }
            New-Item -ItemType SymbolicLink -Path $linkPath -Target $_.FullName | Out-Null
            Write-Host "  [LINK] $skillName"
        }
    }
}
```

Report the count: `Created X symlinks, skipped Y (already existed)`

## Step 2: Install Python Packages

Install packages from `references/requirements.txt` in this skill directory.

### macOS / Linux
```bash
pip3 install -r "$REPO_DIR/evyd-env-clone/references/requirements.txt"
```

### Windows
```powershell
pip install -r "$RepoDir\evyd-env-clone\references\requirements.txt"
```

Before installing, check which packages are already present:
```bash
# For each package in requirements.txt, check:
pip3 show <package_name> 2>/dev/null && echo "[SKIP] <package_name>" || echo "[INSTALL] <package_name>"
```

Report installed vs skipped counts.

## Step 3: Install GitHub CLI (gh)

Check if `gh` is installed:
```bash
gh --version 2>/dev/null
```

If missing:

### macOS
```bash
brew install gh
```

### Windows
```powershell
winget install GitHub.cli
```

If brew/winget is unavailable, provide manual download link: https://cli.github.com/

## Step 4: Claude Code Plugin Configuration

Check if `~/.claude/settings.json` exists and contains the required plugin configuration.

Required entries in settings.json:
```json
{
  "enabledPlugins": {
    "superpowers@superpowers-marketplace": true,
    "vercel-plugin@vercel": true
  },
  "extraKnownMarketplaces": {
    "superpowers-marketplace": {
      "source": {
        "source": "github",
        "repo": "obra/superpowers-marketplace"
      }
    }
  }
}
```

### Logic

1. Read existing `~/.claude/settings.json` (or `$env:USERPROFILE\.claude\settings.json` on Windows)
2. Check if `enabledPlugins` already contains both plugins
3. If missing, **merge** the required fields into the existing JSON — do NOT overwrite the entire file
4. If settings.json doesn't exist at all, create it with the plugin config only (other settings handled in Step 8)

Report:
```
  [SKIP] superpowers@superpowers-marketplace (already enabled)
  [ADD] vercel-plugin@vercel
  [ADD] extraKnownMarketplaces.superpowers-marketplace
```

## Step 5: Git Global Config

Check current git config:
```bash
git config --global user.name
git config --global user.email
```

If either is empty, **ask the user** for their name and email, then set:
```bash
git config --global user.name "User Name"
git config --global user.email "user@example.com"
```

If both are already set, display current values and ask user to confirm they're correct.

## Step 6: GitHub CLI Authentication

Check auth status:
```bash
gh auth status
```

If not authenticated, instruct the user:

> You need to authenticate with GitHub. Run the following command and follow the interactive prompts:
> ```bash
> gh auth login
> ```
> Select:
> - GitHub.com
> - HTTPS (recommended) or SSH
> - Authenticate via browser

This step is interactive — Claude cannot complete it automatically. Wait for user confirmation before proceeding.

## Step 7: SSH Key Setup

Check for existing SSH keys:

### macOS / Linux
```bash
ls ~/.ssh/id_ed25519.pub ~/.ssh/id_rsa.pub 2>/dev/null
```

### Windows
```powershell
Test-Path "$env:USERPROFILE\.ssh\id_ed25519.pub", "$env:USERPROFILE\.ssh\id_rsa.pub"
```

If no key exists, offer to generate:
```bash
ssh-keygen -t ed25519 -C "user@example.com"
```

Then add to GitHub:
```bash
gh ssh-key add ~/.ssh/id_ed25519.pub --title "EVYD-$(hostname)"
```

If keys already exist, report `[SKIP] SSH key found` and verify it's added to GitHub:
```bash
gh ssh-key list
```

## Step 8: Settings.json Template (Manual)

Display the settings template from `references/settings-template.json` to the user.

**Do NOT auto-write this file** if it already contains content beyond what Step 4 added. The user must manually fill in sensitive fields.

Tell the user:
> Here is the EVYD standard settings.json template. Key fields you need to fill in:
>
> 1. **AWS_BEARER_TOKEN_BEDROCK** — Get this from your team lead
> 2. **AWS_REGION** — Default: us-east-1
> 3. **permissions.defaultMode** — Recommended: bypassPermissions
>
> The file location is:
> - macOS/Linux: `~/.claude/settings.json`
> - Windows: `%USERPROFILE%\.claude\settings.json`

Then ask: **"你是否在中国办公，需要配置代理？"** (Are you based in China and need proxy settings?)

If yes, also display `references/settings-china-proxy.json` and explain how to add the proxy env vars to the `env` block in settings.json.

## Step 9: MCP Connections & Final Audit

### MCP Connections

Display the checklist from `references/mcp-connections-checklist.md`. These are all OAuth-based and must be connected manually by the user through Claude Code UI.

Tell the user:
> The following MCP connections need to be set up manually. In Claude Code, use the MCP connection UI or `/mcp` command:

List each connection with brief instructions (detailed in the reference file).

### Final Environment Audit

Run a comprehensive audit and display a summary table:

```
╔══════════════════════════════════════════════════════════════╗
║                  EVYD Environment Audit                      ║
╠══════════════════════════╦════════════╦═══════════════════════╣
║ Component                ║ Status     ║ Notes                 ║
╠══════════════════════════╬════════════╬═══════════════════════╣
║ Claude Code              ║ ✓ OK       ║ v1.x.x                ║
║ Git                      ║ ✓ OK       ║ 2.50.1                ║
║ Node.js                  ║ ✓ OK       ║ v22.14.0              ║
║ Python                   ║ ✓ OK       ║ 3.9.6                 ║
║ pip packages             ║ ✓ OK       ║ 11/11 installed       ║
║ GitHub CLI (gh)          ║ ✓ OK       ║ authenticated         ║
║ SSH Key                  ║ ✓ OK       ║ ed25519, on GitHub    ║
║ Skill symlinks           ║ ✓ OK       ║ 13/13 linked          ║
║ Plugins (superpowers)    ║ ✓ OK       ║ v5.0.7                ║
║ Plugins (vercel)         ║ ✓ OK       ║ v0.32.4               ║
║ Git config               ║ ✓ OK       ║ name + email set      ║
║ settings.json            ║ ⚠ MANUAL   ║ Needs Bedrock token   ║
║ MCP: Gmail               ║ ⚠ MANUAL   ║ Connect via OAuth     ║
║ MCP: Atlassian           ║ ⚠ MANUAL   ║ Connect via OAuth     ║
║ MCP: Granola             ║ ⚠ MANUAL   ║ Connect via OAuth     ║
║ MCP: Figma               ║ ⚠ MANUAL   ║ Connect via OAuth     ║
╠══════════════════════════╬════════════╬═══════════════════════╣
║ Auto-completed           ║ X items    ║                       ║
║ Needs manual action      ║ Y items    ║                       ║
╚══════════════════════════╩════════════╩═══════════════════════╝
```

## Common Issues

- **Windows symlink fails**: Enable Developer Mode in Settings → System → For developers → Developer Mode → ON. Restart terminal.
- **pip3 not found on Windows**: Use `pip` instead of `pip3`. If still missing, reinstall Python and check "Add to PATH" during installation.
- **brew not found on macOS**: Install from https://brew.sh with `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- **gh auth fails**: If behind corporate firewall, try `gh auth login --web` and use browser-based auth.
- **Claude Code plugins not loading after settings.json edit**: Restart Claude Code (`claude` exit and relaunch).
- **Python packages fail to install**: Try `pip3 install --user -r requirements.txt` if permission denied. On Windows, try running terminal as Administrator.
- **SSH key permission denied**: On macOS/Linux, ensure `chmod 600 ~/.ssh/id_ed25519`. On Windows, check file properties → Security tab.
- **settings.json merge conflict**: If the file already has custom content, manually merge the template fields rather than overwriting.
- **中国网络问题**: Use proxy settings from `references/settings-china-proxy.json`. Also consider setting pip mirror: `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
