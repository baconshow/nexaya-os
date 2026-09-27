---
name: faxina-os
description: Use for the weekly cleanup of your agentic OS or when asked to check it — broken links in routers, memory index vs files, stale PROXIMO.md, loose files, app and routine registries. Read-only; writes only a report.
---

# Faxina do OS — report only

The OS rots quietly: a project moves and a router link breaks, a memory is
written without its index line, a `PROXIMO.md` stops being updated, files pile
up in the root. This skill finds those problems and writes a report. It
**never fixes, moves or deletes anything**; fixing is a separate step the user
asks for.

**Write the report in the user's language.**

## Find the OS

- The root is in `~/.claude/CLAUDE.md` (block between `nexaya-os:inicio` and
  `nexaya-os:fim`), or given by the user, or the environment variable
  `AGENTIC_OS_ROOT`.
- The contract is `<root>/Sistema/CONVENCOES.md`. Read it first; it is the
  ruler for every check below.
- The memory folder is the environment variable `AGENTIC_OS_MEMORY_DIR` if
  set, else `autoMemoryDirectory` in `~/.claude/settings.json`, else
  `<root>/Sistema/memoria/` (the same order the Nexaya OS Pro panel uses).

## Never open

`.env*`, `*.pfx`, `*.p12`, `*.key`, `*.pem`, and files whose names contain
key, password, secret, token, credential, contract or payslip (also in the
user's language). A link to one of them is itself a finding ("router points to
a sensitive file"); check only whether the path exists.

## The checks

Run the mechanical part with the script when Python is available:

```text
python "${CLAUDE_SKILL_DIR}/scripts/checar_os.py" "<root>" --formato json
```

Options: `--memoria <folder>`, `--dias 7`, `--perfil-origem <prefix>`,
`--formato md`. It only reads. If Python is not available (or the routine has
no Bash permission), do the same checks with Read, Glob and Grep:

1. **Links in the routers.** The hub, every `<Depto>/CLAUDE.md` listed under
   `## Departamentos`, and every first-level `.md` of a department with an
   `os:` frontmatter (`MEMORIA.md`, indexes). Every markdown link outside code
   blocks and backticks: relative to the file, or absolute (swap the profile
   prefix — `--perfil-origem`, the line in the hub's `## Máquinas`, or
   `perfil_origem` of the Pro panel config — for this machine's home). List each
   broken one with file and line.
2. **Conventions.** Frontmatter `os`, `depto`, `resumo` present and valid;
   department folder with a `CLAUDE.md` missing from the hub, or listed without
   one; `Sistema` present; a heading that looks like a reserved one but is
   misspelled (`## Projeto`, `## Referencia:`) or in another language; a
   department router over ~150 lines.
3. **Memory.** `MEMORY.md` against the folder: lines without a file, files
   without a line, `##` sections that are not department names, broken
   `[[wikilinks]]`, sync conflict copies (`MEMORY-<MACHINE>.md`, `name (1).md`,
   `name 2.md`, "conflicted copy"), files over ~10 KB, an index over ~200
   lines. Also memories missing from their department's `MEMORIA.md`.
4. **Handoffs.** Every `PROXIMO.md` under the root and those the routers point
   to outside it, with the modification date. Mark the ones older than 7 days.
   Stale is not wrong (a paused project), so report, don't judge.
5. **Loose files.** Files directly in the OS root other than `CLAUDE.md` and a
   README; mark the ones created in the last 7 days. Also new files directly
   in `~/.claude/` that are not configuration (names only).
6. **Registries.** `Sistema/apps.json` and `Sistema/rotinas.json`: valid JSON,
   repeated ports, `pasta` that does not exist, ids cited in `## Apps` or
   `## Rotinas` of a router but missing from the registry, and registered ids
   no router cites.

Then add what a script cannot judge: a router that copies content instead of
pointing, a project item without "Ler primeiro:", a `PROXIMO.md` whose claims
contradict the disk (spot-check one or two with `git log -1`).

## The report

Write `<root>/Sistema/dados/relatorios/faxina-AAAA-MM-DD.md` (create the folder
if needed; if a report for today exists, overwrite only that one). Sections:

1. **Summary** — three lines: how healthy the OS is and the top issue.
2. **Broken links** — file:line → target.
3. **Conventions**
4. **Memory**
5. **Handoffs** — table: file, modified, stale?
6. **Loose files**
7. **Registries**
8. **Suggestions** — at most ten, each one concrete ("change the link in
   `Trabalho/CLAUDE.md` line 22 to `painel-vendas/PROXIMO.md`"), ordered by
   impact. Nothing is applied.

Never copy file contents into the report beyond the minimum to locate a
problem, and never anything from a sensitive file.

In an interactive session, end with the report path and the three-line
summary, and offer to fix the suggestions one by one with the user's yes.
In a scheduled routine, just write the report and stop.
