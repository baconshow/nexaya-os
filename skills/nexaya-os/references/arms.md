# ARMS and the router principle

Read this before step 0. It is what you explain to the user, and the frame for
every decision later in the setup.

## The four layers

| Layer | What it is in Claude Code | Where it lives in the OS | Registry |
|---|---|---|---|
| **Applications** | Local servers the user runs for their projects (dashboards, dev servers, static previews), plus, with Nexaya OS Pro, the live panel of the OS | The project folders, wherever they are | `Sistema/apps.json` (one entry per app: id, folder, command, port, machine) |
| **Routines** | Claude tasks that run on a schedule and leave a file behind | Scheduled tasks of the desktop app, cloud routines, or `claude -p` from the OS scheduler | `Sistema/rotinas.json` and the `## Rotinas` section of the Sistema router |
| **Memory** | Claude Code auto memory: one fact per file, plus the `MEMORY.md` index loaded in every session | Default per-project folder, or one shared folder (`Sistema/memoria/`) | `MEMORY.md` (by department) and `<Depto>/MEMORIA.md` (by project) |
| **Skills** | `SKILL.md` folders Claude loads on demand | `~/.claude/skills/`, plugins, and the user's own skills in `Sistema/skills/` | `## Skills` section of each department router |

Around the four layers sits the **hub** (`CLAUDE.md` at the OS root) and one
**router** per department (`<Depto>/CLAUDE.md`). A session reads the hub, then
the router of the task's department, then the project's `PROXIMO.md`, and only
then opens detail files. Three hops, no folder scanning.

## Routers, not folder reorganization

The OS never moves the user's files. It adds a thin layer of markdown that
says where things already are.

Why this matters, in the order users usually feel it:

- **Moving breaks things.** Local apps have hard-coded paths, git repos have
  remotes and hooks, BI and office files keep absolute links, IDEs keep
  workspace paths, cloud-synced folders re-upload everything that moves.
- **Moving is irreversible in practice.** Nobody remembers the old layout a
  week later. A router can be deleted with zero consequences.
- **Routers age well.** When a project moves, one link changes. The weekly
  cleanup (`faxina-os`) finds the broken link.
- **Other people and tools keep working.** Colleagues, scripts and scheduled
  jobs never notice the OS exists.

If the inventory shows a real mess (duplicates, a project in the wrong
department folder), write it as a proposal in the router's `## Pendências` and
let the user decide. Never "fix" it during setup.

## What the OS is not

- Not a copy of the user's notes. A router line is one sentence and a link.
- Not a task manager. `PROXIMO.md` holds the next step of a project, not a backlog.
- Not a place for secrets. Security findings are recorded as path plus action.

## The 5-line pitch for step 0

Say it in the user's language, in your own words, roughly:

1. Your OS is a folder of short markdown files that tell Claude where your things are and what to read first.
2. It is organized by department (your areas of work and life) and by the four ARMS layers: Applications, Routines, Memory, Skills.
3. Nothing of yours moves: the OS points to your folders as they are.
4. I start with an interview and a read-only inventory, then write the routers, and you review before anything global changes.
5. At the end you get a hub, one router per department, a memory index, handoff and cleanup skills, registries of your local apps and, if you want, scheduled routines. The live 3D panel is Nexaya OS Pro, an optional paid add-on (coming soon).

Offer to show the fictional example at `${CLAUDE_PLUGIN_ROOT}/exemplo/` if
the user wants to see the result first.
