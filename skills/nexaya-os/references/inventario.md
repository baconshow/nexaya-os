# Read-only inventory

Step 2 of the setup. Goal: learn what exists, so the routers are faithful to
the disk. Nothing is created, moved, renamed or deleted in this step.

## How to run it

1. From the interview you have: the OS root, the departments and, for each
   one, the folders the user named. Add the cross-cutting areas below.
2. Launch **one subagent per area, all in the same message**, so they run in
   parallel. Use the general-purpose agent type. Five to eight areas is typical.
3. Wait for every subagent to return. Never end your turn while one is still
   running: a spawned task is not a finished task.
4. Keep the reports in the session (or in a temporary folder outside the OS).
   They contain paths and names the user may not want in a synced folder. Only
   the distilled routers and the security findings (path plus action) go into
   the OS.
5. Merge: projects per department, entry files, status, machines, ports, skills
   in use, memory problems, risks. Show the user a short summary and the list
   of items marked "to confirm", and ask before step 3.

## Areas

| Area | What the subagent reads |
|---|---|
| One per department | The folders the user named for it: project list, entry files, git state, apps and ports, what looks active or abandoned |
| Claude Code config and skills | `~/.claude/` (skills, agents, commands, rules, hooks in `settings.json`, `launch.json` files). Top-level settings keys only, never values of env vars or tokens. Count skills and their description sizes |
| Memory | The memory folder(s): every memory file, the `MEMORY.md` index, broken `[[links]]`, files without an index line, index lines without a file, stale paths, oversized files, sync conflict copies |
| Apps and routines | `launch.json` files, start scripts (`*.bat`, `*.ps1`, `*.sh`, `package.json` scripts, `Makefile`), ports that are listening now, existing scheduled tasks, repeated requests in the prompt history that could become routines |
| Big document folders (optional) | Folders like `Documents/` or a clients folder: one line per subfolder, category, period, file count. Names only for anything personal |

## Prompt model

Fill the placeholders and send one prompt per area. Keep the COMMON block
verbatim (translate it only if you must).

```text
You are a READ-ONLY inventory reader for the user's agentic OS setup.
Do not create, move, rename or delete anything. Do not run commands that write
to disk. Allowed commands: listing, reading small text files, `git -C <dir>
log --oneline -8`, `git -C <dir> status --short --branch`, `git -C <dir>
remote -v`, and listing listening ports.

PRIVACY AND SECURITY (mandatory)
- NEVER open files that may hold credentials: .env*, *.pfx, *.p12, *.key,
  *.pem, *.jks, *.kdbx, id_rsa*, and any file whose name contains key, password,
  passwd, secret, token, credential, vault, login, account, or the same words
  in the user's language (e.g. chave, senha, conta, credencial). Record only
  that the file exists and mark it [SENSITIVE].
- NEVER open personal, financial, legal or medical documents: payslips, tax
  forms, bank statements, receipts, contracts, NDAs, IDs, medical records,
  personal photos, or folders the user flagged as private ({{PRIVATE_FOLDERS}}).
  Describe them at folder or file-name level and mark [PERSONAL].
- NEVER copy a secret value into your answer, even partially.
- Cloud-synced folders may hold online-only placeholders. Opening a binary
  downloads it. Do not open binaries (office files, PDFs, archives, images,
  video, BI files). For text files (.md, .txt, small .json configs, README,
  CLAUDE.md, HANDOFF, PROXIMO.md, package.json) read only what you need,
  about the first 80 lines.
- Skip node_modules, .git, .venv, venv, __pycache__, dist, build, .cache,
  .next, target.
- Do not write down health information about anyone.

OUTPUT: plain markdown, no filler. Absolute paths. For each project or
relevant folder: path; what it is (1-2 lines); status (active, paused,
archive) with the most recent modification date you saw; entry files (CLAUDE.md,
README, HANDOFF, PROXIMO.md); machine-specific needs (network, venv, local
data); app and port if any. End with a section "Findings for the OS":
duplicates, things in the wrong place, broken or stale references, risks
([SENSITIVE] and [PERSONAL] by path only), and suggestions. Mark anything you
could not verify as "to confirm".

AREA: {{AREA_NAME}}
Folders: {{FOLDERS}}
What the user said about it: {{USER_CONTEXT}}
Specific questions: {{QUESTIONS}}
```

## Area recipes

Paste the matching block into `{{QUESTIONS}}`.

**Department.** Group by project. For each project, which file a new session
should read first. Git state of each repository. Local apps: command, port,
where the port is defined. SOPs, runbooks and repeated prompts written as
files (`INSTRUCTIONS*`, `*RUNBOOK*`, `*PROMPT*`): list with one line each,
they are candidates for skills.

**Claude Code config and skills.** Every skill (`~/.claude/skills/*/SKILL.md`
and plugin skills): name, origin, lines, description length. Usage: count
invocations in `~/.claude/history.jsonl` with grep, never read it whole, and
never copy lines that contain keys or tokens. Hooks: what each does. Settings:
top-level keys and permission patterns that allow arbitrary execution.
Estimate the fixed context cost of all skill descriptions.

**Memory.** Table: file, department, project, type, modified date, one-line
hook, flags [STALE?] (cites a path that no longer exists, check with ls),
[BIG] (over ~10 KB), [MIXED] (more than one department). Index problems.
A proposed `MEMORY.md` regrouped by department: same lines, only reordered.

**Apps and routines.** Every app with name, folder, command, port and machine;
port conflicts; which ports are listening now. Existing scheduled tasks (read
only). Candidate routines with evidence (how often the request appears, short
examples of at most 12 words). Where Claude's generated files pile up.

**Big document folders.** One line per subfolder: what it seems to be, period,
content type, file count, category (one of the departments or "archive").
Proposed organization as text only. Risks by path.

## Merging the reports

- Resolve conflicts by checking the disk yourself, briefly.
- Everything uncertain stays "to confirm" in the router, in the user's
  language. Do not guess statuses or ports.
- Findings of risk go to `Sistema/SEGURANCA.md` (see `seguranca.md`), never
  with values.
- Candidate skills and routines go to the Sistema router `## Pendências`
  until the user approves them.
