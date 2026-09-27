# More than one machine

Many users run Claude Code on two or more computers (home and work, desktop
and laptop). The OS is designed for that, with three rules.

## 1. The OS root lives in a synced folder

Recommend in the interview a folder synced by the cloud the user already
has: OneDrive, iCloud Drive, Dropbox, Google Drive, or a private git
repository if they prefer explicit syncs. Everything in the OS root travels:
hub, routers, `PROXIMO.md` files, memory (if it lives in `Sistema/memoria/`),
the user's own skills in `Sistema/skills/`, and the Nexaya OS Pro panel with
its config when it is installed.

Watch out:

- **Sync conflict copies.** Two machines editing the same file at once
  produce copies like `MEMORY-<machine>.md` or `file (1).md`. The weekly
  `faxina-os` lists them; merging is a manual decision.
- **Online-only placeholders.** On the second machine, files may exist only as
  placeholders until opened. Reading a small text file is fine; scanning
  binaries triggers downloads.
- **What must not travel.** A work computer receives everything in the OS.
  Personal memories, client data or anything the employer should not host
  must stay out of the synced root (see `memoria.md` and `seguranca.md`).

## 2. `~/.claude` does not sync, and should not

Settings, hooks, scheduled tasks, `launch.json`, installed plugins and
`~/.claude/skills/` are per machine. On each machine:

1. Install the plugin (`/plugin marketplace add baconshow/nexaya-os`, then
   `/plugin install nexaya-os@nexaya`).
2. Write the short `~/.claude/CLAUDE.md` pointer (`templates/claude-global.md`)
   with that machine's path to the OS root.
3. If the memory is shared, set `autoMemoryDirectory` on that machine too.
4. Link the user's own skills (below).
5. Recreate the scheduled tasks that should run there. Routines that need a
   resource only one machine has (a private network, a local database) are
   created only on that machine; say so in `rotinas.json` and in the router.

## 3. Different user profiles, same routers

If the home folder differs between machines (`C:\Users\ana` at home,
`C:\Users\ana.silva` at work), prefer relative links inside the OS. For the
few absolute paths outside it, write them with one profile everywhere and
tell Claude how to translate: add a line to the hub's `## Máquinas` section,
such as "absolute paths use `C:\Users\ana`; at work read them as
`C:\Users\ana.silva`". The `faxina-os` script takes the same prefix with
`--perfil-origem`. With Nexaya OS Pro, set `perfil_origem` in the panel's
`config.json` to that prefix: the panel swaps it for the current machine's
home, and the cleanup script reads it from there too.

In `apps.json`, use `{OS_ROOT}` and `{HOME}` in `pasta`, and the `maquina`
field so each machine knows which apps it can run: `ambas` (any machine),
`rede-interna` (only the hosts listed in `maquinas_rede_interna` of the Pro
panel config), `externa` (only the others), or one machine's hostname.

## Linking the user's own skills

The user's skills live in `<OS root>/Sistema/skills/<name>/SKILL.md`, so they
sync with the OS. Claude Code reads skills from `~/.claude/skills/`, which does
not sync. The bridge is a link per skill.

**Windows** (junctions, no admin needed): copy `templates/instalar-skills.ps1`
to `<OS root>/Sistema/skills/instalar.ps1` and run it on each machine, and
again whenever a new skill folder appears:

```powershell
pwsh -NoProfile -File "<OS root>\Sistema\skills\instalar.ps1"
# without PowerShell 7:
powershell -NoProfile -ExecutionPolicy Bypass -File "<OS root>\Sistema\skills\instalar.ps1"
```

It creates `~/.claude/skills/<name>` as a junction for every subfolder with a
`SKILL.md`, skips (and reports) anything that already exists and is not a
junction to the same place, and never deletes. It can run any number of times.

**macOS/Linux** (symlinks):

```bash
for d in "<OS root>"/Sistema/skills/*/; do
  n=$(basename "$d"); [ -f "$d/SKILL.md" ] || continue
  [ -e ~/.claude/skills/"$n" ] && { echo "skip $n"; continue; }
  ln -s "$d" ~/.claude/skills/"$n" && echo "linked $n"
done
```

Ask before running either one: it changes `~/.claude/skills/`. A new session
is needed for Claude Code to load the linked skills.

The plugin's own skills (`nexaya-os:handoff`, `nexaya-os:faxina-os`) do not need
linking: installing the plugin on the machine is enough. Copy them into
`Sistema/skills/` only if the user wants to customize them; the copy then
shows up without the plugin prefix.

## The hub's `## Máquinas` section

One table: machine, user profile, network, what only runs there. It saves
every session from trying to reach a database from the wrong computer.
