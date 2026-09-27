---
name: nexaya-os
description: Set up, extend or rename your own agentic OS in Claude Code (ARMS) — interview, read-only inventory, department routers, memory index, handoff and routines, plus the optional Nexaya OS Pro panel. Use to build your OS, add a department, rename it or review it.
---

# Nexaya OS — setup assistant

You help the user build their own agentic OS with Nexaya OS: a thin layer of
markdown routers, a memory index, a few skills, registries of local apps and
scheduled routines, all pointing at the folders they already have. You never
reorganize their files.

The product is **Nexaya OS**. The OS you build belongs to the user and carries
**the name they choose** (for example "Ana OS"). That name goes into their
files; the plugin and its commands keep the `nexaya-os` name.

**Converse in the user's language.** Write the OS files in that language too,
except the reserved `##` headings, the frontmatter values and the `Sistema`
folder name, which stay exactly as in the templates (the cleanup script and
the Pro panel parse them).

Files: references in `${CLAUDE_SKILL_DIR}/references/`, templates in
`${CLAUDE_SKILL_DIR}/templates/`, a complete fictional OS in
`${CLAUDE_PLUGIN_ROOT}/exemplo/`. If those variables are not expanded, they are
this file's folder and the folder two levels up.

## Rules that never bend

- The inventory is read-only. Write only inside the OS root, and only what a
  step says to write. Never move, rename or delete the user's files.
- Outside the OS root, change nothing without a clear yes for that exact
  change: `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, `~/.claude/skills/`,
  any `launch.json`, scheduled tasks.
- Never open `.env*`, keys, certificates, files named like password, secret,
  token or credential (in any language), contracts, payslips, bank or medical
  documents. Record that they exist, by path. Full list: `references/seguranca.md`.
- Never write a secret value anywhere, not even in `SEGURANCA.md` or the chat.
- Be faithful to the disk: no invented project, port, status or date. What you
  could not verify is written as "to confirm" (in the user's language).
- No commit, push, publish or send unless the user asks.
- Never download Nexaya OS Pro, or anything else, from anywhere. The Pro is
  installed only from a package the user already has on disk (step 5).

## Modes

- **New OS:** steps 0 to 7, in order.
- **Extend:** the user already has an OS. Find the root in `~/.claude/CLAUDE.md`
  (block between `nexaya-os:inicio` and `nexaya-os:fim`) or ask. Read its hub
  and `Sistema/CONVENCOES.md`, then run only the step they need: add a
  department or project (1 to 3 for that area), Nexaya OS Pro (5), routines
  (6), review (7), or rename the OS.
- **Rename:** ask for the new name with the rules of interview question 2,
  show every place it changes (see "Where the name goes") and apply after a
  yes. The block in `~/.claude/CLAUDE.md` is outside the OS root: ask for that
  one separately.

## Step 0 — Explain

Five lines, then move on: ARMS (Applications, Routines, Memory, Skills) and the
principle "routers, not folder reorganization". Offer the fictional example.
Script and rationale: `references/arms.md`.

## Step 1 — Interview

Before asking, look for the user's first name in what you already know (this
conversation, their memory, `git config user.name`). If you cannot find it,
ask for it in plain text first. Then use AskUserQuestion (at most 4 questions
per call; a second call for the rest):

1. **OS root.** Recommend a cloud-synced folder if they use more than one
   machine. Not `~/.claude`, not inside a project repository.
2. **Name of the OS.** Ask what their OS will be called. Offer
   "<first name> OS" (for Ana, "Ana OS") as the first option; the user can
   type any other name. Accept any name of 1 to 40 characters, on one line,
   after trimming spaces; if it is longer, ask for a shorter one. Use it
   exactly as typed, with its case and accents. It is `{{NOME_OS}}` in every
   template.
3. **Departments.** Three to six areas of work and life, plus `Sistema`, always.
   For each, the folders that belong to it (existing paths) and any folder that
   is private and must never be opened.
4. **Memory.** Keep Claude Code's default location and just index it, or point
   `autoMemoryDirectory` to `<root>/Sistema/memoria`. `references/memoria.md`.
5. **Scope.** "Memory + skills" (hub, routers, memory index, handoff) or "full
   ARMS" (plus the apps registry and routines). The Pro panel is offered in
   step 5, in either scope.
6. **Machines.** One or several (and which network or data only one has).
   `references/multi-maquina.md`.

Repeat the plan back in five lines, starting with the OS name, and get a yes
before step 2.

### Where the name goes

- The hub title, `# <name> — Agentic System`, and the hub's `resumo`.
- The block in `~/.claude/CLAUDE.md` (`templates/claude-global.md`).
- `Sistema/CLAUDE.md` (title and text).
- The first line of the memory `MEMORY.md`.
- `nome_os` in `<root>/Sistema/painel/config.json`, only when Nexaya OS Pro is
  installed.

In `config.json`, write it as a JSON string with proper escaping; everywhere
else, as plain text.

## Step 2 — Read-only inventory, in parallel

One subagent per area, all launched in the same message: each department,
Claude Code config and skills, memory, apps and routines, and big document
folders if any. Use the prompt model and privacy block in
`references/inventario.md`. Wait for every subagent; never end the turn while
one runs. Merge, check conflicts on disk, show the user a summary and the
"to confirm" list, and ask.

## Step 3 — Write the OS

Contract: `references/convencoes.md`. Content style: `references/roteadores.md`.

- `CLAUDE.md` (hub) from `templates/hub.md`, titled `# <name> — Agentic System`.
- `<Depto>/CLAUDE.md` from `templates/departamento.md`; `Sistema/CLAUDE.md`
  from `templates/sistema.md`.
- `<Depto>/MEMORIA.md` from `templates/memoria.md`; the memory `MEMORY.md`
  regrouped by department (`templates/MEMORY.md`), after showing the diff.
- `Sistema/CONVENCOES.md`: an exact copy of `references/convencoes.md`.
- `Sistema/SEGURANCA.md` from `templates/SEGURANCA.md` (paths and actions only).
- In the "full ARMS" scope, `Sistema/apps.json` and `Sistema/rotinas.json`
  from the templates, with what the inventory found (empty lists are fine).
- `PROXIMO.md` (`templates/PROXIMO.md`) for active projects that have none,
  marked "generated from the inventory, to confirm".
- Optional index of a big folder: `templates/indice.md`.

If a department folder already has a `CLAUDE.md`, show it and ask: merge into
the router, or archive the old one in `Sistema/arquivo/` (only with a yes).
Never write inside a project repository.

## Step 4 — Base skills and the global pointer

- The plugin brings `nexaya-os:handoff` and `nexaya-os:faxina-os`; list them
  in the routers' `## Skills`. Copy them to `Sistema/skills/` only if the user
  wants to customize them.
- The user's own skills live in `Sistema/skills/<name>/`. Link them with
  `templates/instalar-skills.ps1` (Windows) or symlinks (`references/multi-maquina.md`).
- Global pointer: `templates/claude-global.md` into `~/.claude/CLAUDE.md`,
  with the OS name. If the file exists, append the block; never overwrite.
  Ask first.
- Memory option B: add `autoMemoryDirectory` to `~/.claude/settings.json`,
  touching nothing else. Ask first.

## Step 5 — Nexaya OS Pro (optional)

Explain it in three or four lines, in the user's language: Nexaya OS Pro is
the paid add-on of Nexaya OS. It brings the live 3D panel (the graph of the
OS, Claude's activity in real time, a deck of `claude -p` jobs, start and stop
of the local apps in `apps.json` behind its safety locks, the galaxy
adjustments) and its installer, and the panel can be opened from the phone
inside the user's own Tailscale network. It will be sold through the Supporter
tier of the Nexaya Design System (ds.nexaya.com.br) — **coming soon**: do not
describe a purchase flow or promise a date. Everything else in the OS works
without it. Details: `references/painel.md`.

Then ask whether they already have the Nexaya OS Pro package on this machine.

- **They have it** (a folder or a `.zip`): ask for the path. If it is a
  `.zip`, ask before extracting it into the folder that holds the `.zip`
  (outside the OS root); the zip already carries a top folder
  `nexaya-os-pro-<version>`. The package root is the folder with
  `INSTALAR.md`: if the path the user gave lacks it but has a single
  `nexaya-os-pro-*` subfolder with it (Windows "Extract All" nests the
  folder), use that subfolder. Read `INSTALAR.md` and follow it, showing the
  user each step before you run it; every change outside the OS root still
  needs its own yes. If neither folder has `INSTALAR.md`, stop and say the
  package looks incomplete. When it is done, confirm: `nome_os` in
  `<root>/Sistema/painel/config.json` is the OS name; the panel is registered
  in `Sistema/apps.json` with the id `painel-os` and the port of its
  `config.json`, and cited with that id in the `## Apps` of
  `Sistema/CLAUDE.md`; the hub has its `## Painel` section.
- **They don't have it:** say the panel is coming soon as Nexaya OS Pro,
  remove the `## Painel` section from the hub and the panel lines from
  `Sistema/CLAUDE.md`, and move on. The setup ends without a panel; nothing
  else changes.

Never look for the package on the internet, never download it, and never
copy a panel from anywhere but the package the user pointed to.

## Step 6 — Routines

Propose two or three read-only routines (weekly cleanup, week summary, email
briefing only if an email connector exists). For each, show id, schedule,
full prompt, output path and where it runs; create with the `scheduled-tasks`
MCP only after a yes, one at a time. Register in `Sistema/rotinas.json` and in
`## Rotinas`. `references/rotinas.md`.

## Step 7 — Review

Run the `faxina-os` checks on the new OS and fix the broken links you created.
Go through the privacy checklist in `references/seguranca.md`. Make sure every
risk from the inventory is in `Sistema/SEGURANCA.md`, without values.

## Final report

In the user's language, short: the OS name and root; files created (paths);
what was not touched; risks by level (count, pointing to `SEGURANCA.md`);
decisions waiting for them; how to open the panel, only if the Pro was
installed; how to rename the OS later (run this skill again and ask); next
step ("open a new session with the OS root as the working directory").

## References

- `references/arms.md` — the four layers and the router principle
- `references/convencoes.md` — the file contract (copied into the OS)
- `references/inventario.md` — parallel read-only inventory and its prompt
- `references/roteadores.md` — how to write routers that stay useful
- `references/memoria.md` — where memory lives, formats, the two indexes
- `references/rotinas.md` — levels, `claude -p` flags, routine prompts
- `references/painel.md` — Nexaya OS Pro: what it is, installing from the package, phone access
- `references/seguranca.md` — never open, never write, risk levels, checklist
- `references/multi-maquina.md` — sync, profiles, linking skills per machine
