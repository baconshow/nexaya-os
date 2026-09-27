# Memory

The M of ARMS. Claude Code writes auto memory as small markdown files plus an
index, `MEMORY.md`, that is loaded at the start of every session. The OS does
not replace that mechanism: it decides where the folder lives and indexes it
by department.

## Where the memory lives (interview question 4)

By default Claude Code keeps auto memory per project, under
`~/.claude/projects/<project>/memory/`. The `autoMemoryDirectory` setting in
`~/.claude/settings.json` points every session to one folder instead. Check
the documentation of the user's Claude Code version before changing it.

| Option | What happens | Good for | Watch out |
|---|---|---|---|
| **Keep** | The OS indexes the existing folder(s) and does not touch settings | Users with one machine, or memory already organized | Several per-project folders mean several indexes; the OS routers link to each |
| **Point to the OS** | `autoMemoryDirectory` = `<OS root>/Sistema/memoria`; every session shares one memory, synced with the OS | Users with more than one machine, or who want one memory for everything | Everything in memory travels to every synced machine, including a work computer. Private memories must stay out, or, with Nexaya OS Pro, be listed in `memorias_privadas` of the panel config so the panel never serves them |

Changing `~/.claude/settings.json` is a global change: show the exact edit
(one key added, nothing else touched) and apply only after a clear yes. If
the user already has memories elsewhere, do not move them in this step;
offer it as a separate task.

## Memory file format

One fact per file. Frontmatter as Claude Code writes it:

```markdown
---
name: painel-vendas-regras
description: Regras de negócio do painel de vendas — semana fecha no domingo, receita líquida sem devoluções
metadata:
  type: project
---

Texto curto: o fato, por que ele importa e como aplicar.
Links para memórias relacionadas: [[fonte-dados-vendas]].
```

Types: `user` (who the user is, preferences), `feedback` (corrections that
became rules), `project` (decisions and facts of a project), `reference`
(where something is, how a tool works). Dates are absolute ("em 18/09/2026"),
never "yesterday".

## The two indexes

- **`MEMORY.md`** (in the memory folder): one `##` section per department,
  with the department name exactly as the folder, so the cleanup script (and
  the Pro panel, which colors each memory) knows whose it is. Facts valid for
  everything go under `## Sistema`. One line per memory:
  `- [Title](file.md) — one-line hook`. Keep it under ~200 lines: it is
  loaded in every session.
- **`<Depto>/MEMORIA.md`**: the same memories of that department grouped by
  project. A `##` title equal to a project name in the router links those
  memories to the project in the graph. Links are relative to the department
  folder (`../Sistema/memoria/file.md`).

New memory = file + line in `MEMORY.md` + line in the department `MEMORIA.md`.
Put that rule in the hub.

## Migrating existing memories

- Do not rewrite memory files during setup. Only regroup `MEMORY.md` by
  department (same lines, reordered) after showing the diff.
- Record problems as a hygiene list in `Sistema/MEMORIA.md`: stale paths,
  files over ~10 KB that became changelogs, memories that mix departments,
  broken `[[links]]`, index lines without a file, files without an index line,
  sync conflict copies (`MEMORY-<machine>.md` and similar).
- Write the problem file names without links in that list, so the graph does
  not duplicate nodes.

## Never in memory

- Secrets, tokens, keys, passwords, connection strings with credentials.
- Health, financial or legal details about anyone.
- Personal data of third parties. Use a role ("the client", "the advisor").
- Anything the user asked to keep private. If such a memory already exists,
  list it in `SEGURANCA.md` with the action "reduce to the rule, or move out of
  the synced folder" and let the user decide.
