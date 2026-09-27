# Routines

The R of ARMS. A routine is a Claude task that runs on a schedule and **writes
a file, then stops**. Sending email, publishing, committing, filling a website
or touching a calendar stays with the user. A routine that needs one of those
produces a proposal file the user acts on.

## Where a routine can run

### Level 1 — scheduled tasks of the desktop app

- Created with the `scheduled-tasks` MCP (`create_scheduled_task`: `taskId`,
  `title`, `description`, `prompt`, `cronExpression` in **local** time).
- They see the local disk and the account's connectors, like a normal session.
- They run only while the desktop app is open on that machine. A run missed
  because the app was closed runs at the next launch. Tell the user this.
- Stored per machine in `~/.claude/scheduled-tasks/<taskId>/SKILL.md`. That
  folder does not sync: a task exists only on the machine where it was
  created.
- This is the default level for OS routines, because they read and write the
  OS folder.

### Level 2 — cloud routines

- Created with `/schedule` or on claude.ai. They run with the computer off.
- They **do not see the local disk**: no OS folder, no local repositories, no
  private network. They only reach connectors (email, calendar) and remote
  repositories.
- Useful for a routine whose input and output both live in connectors. Not
  for anything that must write into the OS.

### Level 3 — headless `claude -p` from the OS scheduler

Windows Task Scheduler, cron or launchd run the CLI with no app open, as long
as the machine is on. Flags that exist and matter for a routine:

| Flag | Use in a routine |
|---|---|
| `-p` / `--print` | non-interactive mode; the prompt can call a skill: `-p "/skill-name args"` |
| `--model` | `sonnet` as the routine default; `opus` only with a reason; `haiku` for trivial checks |
| `--effort` | `low` or `medium` for routines |
| `--permission-mode` | `dontAsk` with a closed tool list, or `acceptEdits` when it must write the report |
| `--allowedTools` | only what the routine needs, e.g. `Read,Glob,Grep,Write` |
| `--output-format` | `json` when something (a script, the Pro panel) reads the result |
| `--max-budget-usd` | spending cap per run; the main safety limit available |
| `--no-session-persistence` | do not keep the routine as a resumable session |

There is **no `--max-turns`** flag; do not rely on it. Check `claude --help`
on the user's version before writing the scheduler entry. Other cautions:

- Call `claude` by absolute path; a machine can have more than one install and
  the scheduler's PATH is not the user's.
- Hooks configured in `settings.json` also fire in `-p` mode. If they inject
  text or slow things down, pass `--settings` with a routine-specific file.
- In `-p` mode the trust dialog is skipped and invalid settings may be ignored
  silently. Check the first run's output by hand.
- Headless runs use the same account and limits as interactive sessions.

Model call (adapt paths; test once by hand, with the user watching):

```text
"<absolute path to claude>" -p "/nexaya-os:faxina-os" --model sonnet --effort medium --permission-mode acceptEdits --allowedTools "Read,Glob,Grep,Write" --output-format json --max-budget-usd 1 --no-session-persistence --add-dir "<OS root>"
```

## The routines to propose (step 6)

Propose two or three, all read-only except for their own report. Before
creating each one, show the user: id, schedule in plain words and cron, the
full prompt, the output path, and the level. Create only after a clear yes,
one at a time. Then add it to `Sistema/rotinas.json` and to the `## Rotinas`
section of `Sistema/CLAUDE.md`.

| id | When | What | Output |
|---|---|---|---|
| `faxina-semanal` | Friday late afternoon (`30 17 * * 5`) | The OS cleanup (skill `faxina-os`): broken links, memory index against files, stale `PROXIMO.md`, loose files | `Sistema/dados/relatorios/faxina-AAAA-MM-DD.md` |
| `resumo-semana` | Friday or Monday morning | What moved in the last 7 days: `PROXIMO.md` files, dated handoffs, memories modified in the week, by department | `Sistema/dados/relatorios/semana-AAAA-MM-DD.md` |
| `briefing-email` | Weekday mornings | Only if an email connector is connected: highlights of the last 24 h, read-only | `Sistema/dados/briefing.md` (and `.json` if the Pro panel shows it) |

Scheduled prompts start with no memory of the conversation, so they must be
self-contained: absolute OS root, what to read, what never to open, the exact
output path and format.

### Prompt model: faxina-semanal

```text
You are the "faxina-semanal" routine of {{NOME_OS}}. Write in {{LANGUAGE}}.
The OS root is {{OS_ROOT}}. Today's date goes in the report name.
If the skill nexaya-os:faxina-os is available, follow it. Otherwise:
read {{OS_ROOT}}/CLAUDE.md and {{OS_ROOT}}/Sistema/CONVENCOES.md, then check,
READ-ONLY: broken links in the hub, in every department CLAUDE.md and MEMORIA.md;
convention problems (missing "os:" frontmatter, router over ~150 lines);
{{MEMORY_DIR}}/MEMORY.md against the files in that folder (missing lines,
lines without file, broken [[links]], sync conflict copies);
PROXIMO.md files not modified for more than 7 days; new loose files in the OS
root in the last 7 days.
Never open .env*, *.pfx, *.key, *.pem, or files whose names contain key,
password, secret, token, credential, contract, payslip.
Write only {{OS_ROOT}}/Sistema/dados/relatorios/faxina-AAAA-MM-DD.md (create
the folder if needed) with sections: Summary, Broken links, Conventions,
Memory, Handoffs, Loose files, Suggestions. Fix nothing.
```

### Prompt model: resumo-semana

```text
You are the "resumo-semana" routine of {{NOME_OS}}. Write in {{LANGUAGE}}.
The OS root is {{OS_ROOT}}. Read, without changing anything: the hub, the
department list in its "## Departamentos" section, every PROXIMO.md under the
OS root, the dated handoffs (handoffs/AAAA-MM-DD*.md) of the last 7 days, and
the memories in {{MEMORY_DIR}} modified in the last 7 days.
Never open sensitive files (.env*, keys, certificates, contracts, payslips)
and never write health data about anyone.
Write only {{OS_ROOT}}/Sistema/dados/relatorios/semana-AAAA-MM-DD.md: one
section per department with what moved, what is pending and the decisions
recorded; a department with no movement gets one line saying so.
```

### Prompt model: briefing-email (only with an email connector)

```text
You are the "briefing-email" routine of {{NOME_OS}}. Write in {{LANGUAGE}}.
Use the {{EMAIL_CONNECTOR}} connector READ-ONLY: never send, reply, archive,
label, mark as read or create drafts. Look at inbox threads of the last 24
hours, skip promotions and automatic notifications, and pick at most 8
highlights: direct requests, deadlines, replies someone is waiting for,
{{PRIORITY_SENDERS_OR_TOPICS}}.
Never copy message bodies, verification codes, passwords, login links, bank
data or health information. Keep only sender, subject and one sentence on why
it matters.
Write {{OS_ROOT}}/Sistema/dados/briefing.md, and
{{OS_ROOT}}/Sistema/dados/briefing.json as
{"gerado_em": ISO date, "resumo": text, "destaques": [{"de", "assunto", "por_que"}]}.
If the connector is unavailable, write the JSON with an empty list and a
summary explaining why. Do not try another way.
```

## `rotinas.json`

```json
{
  "rotinas": [
    {
      "id": "faxina-semanal",
      "depto": "Sistema",
      "titulo": "Faxina semanal do OS",
      "agenda": "Sexta, 17:30 (cron 30 17 * * 5)",
      "descricao": "Links quebrados, índice de memória e PROXIMO.md parados. Só relata.",
      "saida": "Sistema/dados/relatorios/faxina-*.md"
    }
  ]
}
```

`saida` is relative to the OS root (or absolute) and may be a glob; the newest
match is the routine's last report (the Pro panel shows it).

## Candidates that stay out

Write them in the Sistema router `## Pendências` instead of creating them:
anything that sends or publishes; anything that needs a network only one
machine has (it would fail on the others); a handoff hook on session stop
(changes global settings; ask separately).
