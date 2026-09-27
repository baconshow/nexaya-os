# Writing good routers

The format is in `convencoes.md`. This file is about content: what makes a
router useful to the next session, and what makes it rot.

## The rules

1. **Point, don't copy.** A router line is one sentence and a link. If you feel
   like pasting a runbook, link to it instead. The detail lives in one place.
2. **Stay under ~150 lines per department router.** A long router is a sign
   that a project deserves its own `PROXIMO.md` or an index file
   (`templates/indice.md`) inside the department.
3. **Start with `## Ler primeiro`.** Two to five links a new session must read
   before anything else in that department: the department's `MEMORIA.md`,
   the file with the house rules, the one decision log everybody forgets.
4. **Every active project has a "Ler primeiro:" link**, normally to its
   `PROXIMO.md`. If it has none, create one from the inventory (step 3) and
   mark it as generated.
5. **Be faithful to the disk.** No invented project, port, status or date.
   What the inventory could not verify is written as "to confirm with <name>"
   in the user's language.
6. **Write for a stranger.** The reader is a new session with no memory of
   this conversation. Full sentences, no private shorthand.
7. **Prose, not telegraph.** Even if the user likes terse chat replies, OS
   files are read months later.

## Anatomy of a project item

```markdown
- [Painel de vendas](painel-vendas/) — painel semanal de vendas das lojas, em HTML estático. Status: ativo (último handoff em 18/09). Máquina: qualquer uma; sobe na porta 5510 (`painel-vendas-web`). Ler primeiro: [PROXIMO.md](painel-vendas/PROXIMO.md), depois o [README](painel-vendas/README.md)
```

In order: link to the folder (the node), what it is, status with evidence,
machine and port when relevant, "Ler primeiro:" links. One line; the Pro panel
turns the extra links into references hanging from the project.

Bad item, and why:

```markdown
- Vendas — ver pasta
```

No link (no node, no way to open it), no status, no entry file.

## Departments with many projects

Use your own `##` headings (anything not reserved becomes a group node) to
split a crowded department: `## Clientes ativos`, `## Arquivo`. Keep
`## Projetos` for the active ones, so the panel highlights them.

A table under an item is fine for a project with several versions or parts,
but the item line above it must still carry the link and "Ler primeiro:".

## The hub

- Who the user is, in three lines, and how to address them.
- `## Departamentos`: one link per department router, one line each. The
  order here is the order (and color) in the panel.
- `## Ler primeiro`: conventions, memory index, security.
- `## Regras`: only global rules (where files go, handoff, secrets, no moving
  folders, git). Department rules go in the department router.
- `## Máquinas` if the OS runs on more than one computer.

## `## Regras` in a department

Short, specific, and each rule with its reason when it is not obvious:
"Never push to `main` in the site repository: it deploys on push." Generic
advice ("write clean code") does not belong in a router.

## `## Pendências`

Open problems the inventory found and decisions waiting for the user. One
line each. Remove the line when it is solved and, if the solution is a
durable fact, record it in memory.

## PROXIMO.md

- Rewritten whole at the end of a relevant session (skill `handoff`), never
  appended like a diary.
- State in 5 to 10 lines, the next step small enough to start without asking,
  link to the latest dated handoff, list of previous ones.
- A department-level `PROXIMO.md` (at `<Depto>/PROXIMO.md`) carries the OS
  frontmatter (`os: referencia`) so it shows in the panel.

## Keeping routers alive

- New project: add the item before creating files in it.
- Project moved or renamed: update the link in the router the same day.
- The weekly `faxina-os` routine reports broken links, oversized routers and
  stale `PROXIMO.md` files. It never fixes them; the next session does.
