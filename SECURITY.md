# Security — Nexaya OS

## What this plugin contains and runs

- **Skills only** (`skills/`): markdown instructions that Claude follows. No hooks,
  no MCP servers, no compiled or minified code, no package installs, no network
  access.
- **Two small scripts, both readable source:**
  - `skills/faxina-os/scripts/checar_os.py`: a read-only checker for the weekly
    cleanup. Python standard library only; it reads the OS files and prints a
    report. It opens no network connection.
  - `skills/nexaya-os/templates/instalar-skills.ps1`: optional, Windows. Creates
    directory junctions in `~/.claude/skills/` pointing to the OS skills folder.
    Never deletes anything, supports `-DryRun`, and runs only when you ask for it.

## What the setup changes, and when

| Where | What | When |
|---|---|---|
| The OS root you choose | Markdown and JSON files (hub, routers, memory index, registries, reports) | During setup and cleanup |
| `~/.claude/CLAUDE.md` | A short pointer block, appended, never overwriting | Only after you confirm |
| `~/.claude/skills/` | Links to the OS skills | Only after you confirm |
| Claude app scheduled tasks | One routine at a time, with its full prompt shown | Only after you approve each one |
| `launch.json`, autostart | Only for Nexaya OS Pro, from its own install guide | Only after you confirm |

## What it never does

- Download anything (including Nexaya OS Pro) from anywhere.
- Open `.env*`, keys, certificates, password/secret/token/credential files,
  contracts, payslips, bank or medical documents, or copy any secret value.
- Move, rename or delete your files, or write inside your project repositories.
- Change Claude's permission settings.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting: **Security → Report a
vulnerability** in [this repository](https://github.com/baconshow/nexaya-os/security).
Do not open a public issue for security problems. We aim to reply within 7 days.
