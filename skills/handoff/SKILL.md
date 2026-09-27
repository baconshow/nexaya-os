---
name: handoff
description: Use when opening a session in a project (read its PROXIMO.md), when ending a relevant session, near the usage or context limit, and when asked for a handoff or a prompt for another session. Writes the dated handoff and rewrites PROXIMO.md.
---

# Handoff: PROXIMO.md and the continuation prompt

Sessions end all the time: the usage limit hits, the context fills up, the
user switches machines or hands the task to another session. The handoff is
what keeps the next session from rediscovering everything. This skill says
where it lives, what it contains and how to write the continuation prompt.

**Write in the user's language.** The headings below are a model; translate
them (in Portuguese: "Estado atual", "Próximo passo", "Handoffs anteriores").

## Find the OS

The OS root is in the user's `~/.claude/CLAUDE.md` (block between
`nexaya-os:inicio` and `nexaya-os:fim`). The hub is `<root>/CLAUDE.md`; each
department has a router at `<root>/<Depto>/CLAUDE.md`. If there is no OS,
use the project folder itself and say so.

## Where it lives

The department router decides. When it says nothing:

| What | Where |
|---|---|
| Project inside the OS | `<project>/PROXIMO.md` and `<project>/handoffs/AAAA-MM-DD.md` |
| Project outside the OS (a repository elsewhere) | In the OS, not in the repository: `<root>/<Depto>/<project>/PROXIMO.md` and its `handoffs/`, and the router item points there. Write inside the repository only if the user wants it versioned |
| Department-level state | `<root>/<Depto>/PROXIMO.md`, with the OS frontmatter (`os: referencia`, `depto`, `resumo`) so the cleanup and the Pro panel see it |

The project item in the router carries "Ler primeiro:" with a link to the
`PROXIMO.md`. If you create a `PROXIMO.md` in a new place, add that link.

## When opening a session in a project

1. Read the hub and the department router.
2. Read the project's `PROXIMO.md` before anything else. For detail, follow
   its link to the latest dated handoff.
3. Check what it claims against the disk: `git status --short --branch`,
   `git log --oneline -5`, the dates of the files it cites. If it is stale, say
   so in your first reply.
4. If the project has no `PROXIMO.md`, say so and follow the router.

## When ending a session

Write the handoff at the end of every relevant session, when asked, and at any
sign of an end: context near the limit, a usage-limit warning, a machine
switch. If the limit is close, write the handoff first and continue after.

1. Write the dated handoff `handoffs/AAAA-MM-DD.md`. If one exists for the
   same day, use `AAAA-MM-DD_topic.md`. Never overwrite another session's
   dated handoff.
2. Rewrite `PROXIMO.md` whole. It is the latest picture of the project, not a
   diary: current state, next step, link to today's handoff, list of the
   previous ones.
3. Durable facts (a decision of the user, a trap that cost time) go to memory
   too, not only to the handoff: memory file, line in `MEMORY.md` under the
   department, line in the department `MEMORIA.md`.
4. End your reply with the continuation prompt (model below).

### Dated handoff

```markdown
# <Project> — handoff AAAA-MM-DD

## State
One to three sentences: where the work is, on which branch, what is live.

## Done
- Concrete item, with the commit, file or number that proves it.

## Next steps
1. The next step, small enough to start without asking.

## Files touched
- `path` — what changed, and whether it is committed or only on disk.

## Risks and open items
- What may break, what depends on someone else, what was not verified.
```

### PROXIMO.md

```markdown
# PROXIMO — <Project>

Read this first when opening a session in this project.

## Current state (AAAA-MM-DD)
Five to ten lines. Detail in the [handoff of AAAA-MM-DD](handoffs/AAAA-MM-DD.md).

## Next step
1. ...

## Previous handoffs
- [AAAA-MM-DD](handoffs/AAAA-MM-DD.md)
```

### Content rules

- Every claim is verifiable: command run, commit, file. Separate what was
  done, what was not verified and what is pending.
- No secrets (passwords, tokens, `.env` contents), not even partially.
- No health, financial or legal detail about anyone. Third parties appear by
  role ("the client", "the reviewer").

## Continuation prompt

The block the user pastes into another session, another machine or another
assistant. That session has not seen this conversation, so the prompt must
stand alone. Keep it under about 30 lines.

```text
You will continue a piece of work for <how to address the user>. Reply in <language>.
Project: <project>, department <department>. Machine: <which one>.

Before anything, read in this order:
1. <absolute path of the OS root>/CLAUDE.md
2. <absolute path>/<Depto>/CLAUDE.md
3. <absolute path of PROXIMO.md> and <absolute path of the dated handoff>

State in one sentence: <...>
Your task now: <the concrete next step, with its done criterion>
Do not: <commit, push or deploy without being asked; touch ...>
When done: update PROXIMO.md (skill handoff) and say what is still pending.
```

- Use absolute paths. If the destination machine has another user profile,
  write the paths as they are on that machine (the hub's `## Máquinas`
  section says how they differ).
- A long or reusable prompt goes to a file next to the handoff
  (`handoffs/prompt-<topic>.md`), and the reply points to it.
