# Nexaya OS Pro — the panel

Step 5 of the setup, optional in any scope. Nexaya OS itself (this plugin) is
free and complete without it: hub, routers, memory, handoff, cleanup, the apps
and routines registries. **Nexaya OS Pro** is the paid add-on that shows the
OS live. This plugin does not contain the panel's code, and the setup never
downloads it: the Pro is installed only from a package the user already has.

## What the Pro brings

- **The live 3D panel**, a local web page that draws the OS as a graph (hub,
  departments, projects, memories, skills, apps, routines) built from the
  routers, so it follows `Sistema/CONVENCOES.md` to the letter.
- **Claude's activity in real time**, read from the local Claude Code session
  transcripts of the machine: active sessions and subagents, and a feed that
  shows the description Claude wrote for each step, never the Bash command.
- **A deck of `claude -p` jobs**: prompt, allowed tools, permission mode and
  budget cap come from its configuration file; the page only picks the job,
  the model and the effort.
- **Local app control**: which apps of `Sistema/apps.json` are up, start one
  or a batch, stop what the user asks, behind the safety locks below.
- **The galaxy adjustments**: pure black background by default; nebulae,
  halos, bloom and stars tuned by each viewer and saved in their browser.
- **An installer** and an `INSTALAR.md` with the steps.
- **Phone access** inside the user's own Tailscale network (below).

## How it is sold

Through the Supporter tier of the Nexaya Design System (ds.nexaya.com.br), a
one-time payment of US$ 4.99, **coming soon**. Until the Design System is live there is no way to
buy it: say "coming soon", do not describe a checkout and do not promise a
date.

## Installing from the package

1. Ask where the package is: a folder or a `.zip` on this machine. Never look
   for it on the internet.
2. A `.zip` is extracted only with a yes, into the folder that holds the
   `.zip` (outside the OS root). The zip already carries a top folder
   `nexaya-os-pro-<version>`.
3. Find the package root: the folder with `INSTALAR.md`. Windows "Extract
   All" often nests the top folder inside one of the same name; if the path
   the user gave lacks `INSTALAR.md` but has a single `nexaya-os-pro-*`
   subfolder with it, use that subfolder. If neither has it, the package is
   incomplete: stop and say so.
4. Read `INSTALAR.md` and follow it. Show the user each step before running
   it; anything outside the OS root still needs its own yes.
5. After it, check what the core relies on:
   - `<root>/Sistema/painel/config.json` has `nome_os` equal to the OS name
     from the interview (a JSON string, escaped);
   - `Sistema/apps.json` has one entry with the id `painel-os`, depto
     `Sistema`, pasta `{OS_ROOT}/Sistema/painel` and the `porta` of
     `config.json` (the exact entry is in `INSTALAR.md`), and the
     `## Apps` of `Sistema/CLAUDE.md` cites `painel-os`;
   - the hub has a `## Painel` section saying how to open it;
   - the `faxina-os` checks report nothing about `painel-os`.
6. Start it once with the user watching, check that the hub's departments
   appear, and tell them how to stop it.

## What the core expects from the panel's config

The full list of keys is in the Pro's `INSTALAR.md`. The core refers to these:

| Key | Why the core cares |
|---|---|
| `nome_os` | The OS name, shown in the panel header and tab; the rename mode updates it |
| `porta` | The local port; the hub's `## Painel` section and `apps.json` cite it |
| `perfil_origem` | Home-folder prefix used in the routers when the OS syncs between profiles; the `faxina-os` script also reads it from here |
| `memorias_privadas` | Memory file names the panel never shows or serves |
| `maquinas_rede_interna` | Host names of machines with a private network; `apps.json` entries marked `rede-interna` show only there |

## How the panel finds things (same order as `faxina-os`)

- **OS root:** the environment variable `AGENTIC_OS_ROOT` if set; otherwise
  the folder two levels above the panel (`<root>/Sistema/painel/`).
- **Departments:** the links of the hub's `## Departamentos` section, in order.
- **Memory folder:** `AGENTIC_OS_MEMORY_DIR` if set; otherwise
  `autoMemoryDirectory` from `~/.claude/settings.json`; otherwise
  `<root>/Sistema/memoria/`.
- **Apps and routines:** `Sistema/apps.json` and `Sistema/rotinas.json`.

## Security (explain it to the user in plain words)

- It listens only on `127.0.0.1`. Never change that to `0.0.0.0`.
- Every request must carry an expected `Host`; the API needs a per-run token
  embedded in the page, and actions also need a local `Origin`. Other sites
  open in the browser cannot drive it.
- The page has a strict Content-Security-Policy; generated HTML is previewed in
  a sandbox. Sensitive-looking file names and `memorias_privadas` are never
  served.
- **`apps.json` is a root of trust.** Apps start only from it, with a closed
  list of executables and no shell metacharacters, but whoever edits it
  decides what the panel may run. Keep the OS folder private.
- The deck spends the user's Claude usage, with a budget cap per job;
  `bypassPermissions` is refused.

## Opening it on the phone (Tailscale serve, tailnet only)

The Pro's `INSTALAR.md` has the exact steps. The idea, to explain to the user:

- The panel keeps listening on `127.0.0.1`. `tailscale serve` on the same
  computer publishes it **only to the devices of the user's own tailnet**
  (their phone, their other computers), at the machine's tailnet address. The
  default in `INSTALAR.md` is plain `http://` on port 80: traffic between
  tailnet devices is already encrypted by Tailscale (WireGuard). If the
  tailnet has HTTPS certificates enabled, `https://` works too (also in
  `INSTALAR.md`).
- **Never `tailscale funnel`**: Funnel puts the panel on the public internet.
  Never another tunnel, reverse proxy or port forward either.
- Anyone in the tailnet who can open the page can drive the panel (start
  apps, run deck jobs). Keep the tailnet to the user's own devices; on a
  tailnet shared with other people, do not serve it unless Tailscale ACLs
  restrict who reaches this machine.
- Serving is a change outside the OS root: ask before turning it on, and show
  how to turn it off (the command is in `INSTALAR.md`).

## Updating

A new Pro package comes with its own `INSTALAR.md` and changelog; follow them.
The panel's `config.json` and `deck.json` are the user's and are kept: the
package never ships them inside `painel/`, only as models in `templates/`, so
copying the new `painel/` over the old one cannot overwrite them. New keys or
deck items from the models are added only with a yes.
