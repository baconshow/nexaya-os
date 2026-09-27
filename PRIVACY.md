# Privacy policy — Nexaya OS

*Last updated: September 27, 2026. Português abaixo.*

This policy covers the **Nexaya OS** plugin for Claude (this repository), published
by [Nexaya](https://nexaya.com.br).

## Summary

The plugin collects nothing. It has no telemetry, no analytics, no servers of its
own and it makes no network requests. Everything it produces is plain files on
your own disk.

## What the plugin reads

- **Only the folders you point to**, during setup and only after you confirm. To
  write the routers, Claude reads file and folder names and markdown notes in
  those folders. The inventory is read-only: nothing is moved, renamed or deleted.
- **Never:** credential and secret files (`.env*`, keys, certificates, files named
  like password, secret, token or credential), contracts, payslips, bank or medical
  documents. The skills tell Claude to list those by name only and never open them,
  and to never copy a secret value anywhere.

## What the plugin writes, and where

All on your machine, and outside the OS folder only after you say yes:

- Markdown and JSON files inside the OS root you choose (hub, routers, memory
  index, registries of apps and routines, reports).
- A short block in `~/.claude/CLAUDE.md` that points new Claude sessions to your
  OS. It is appended, never overwrites the file.
- Links in `~/.claude/skills/` to the OS skills, when you choose to install them.
- Scheduled routines in the Claude app, one at a time, each only after you approve
  its full prompt.

## Data sent to third parties

None by the plugin. Content that Claude reads while you use the plugin is processed
by Anthropic as part of your normal use of Claude, under Anthropic's own terms and
privacy policy. Routines you choose to create run in your own Claude app and may use
connectors you already enabled there (for example, your email), only if you ask for
it.

## Retention

The plugin keeps nothing. The files it helps create stay on your disk until you
delete them. Deleting the OS folder and the block in `~/.claude/CLAUDE.md` removes it
entirely; your original folders are never changed.

## Children

The plugin is not intended for people under 18.

## Nexaya OS Pro

Nexaya OS Pro (the live panel) is a separate product, not part of this repository.
It also runs only on your machine and ships its own terms.

## Contact and changes

Questions: open an issue at
[github.com/baconshow/nexaya-os](https://github.com/baconshow/nexaya-os/issues).
Changes to this policy are dated at the top of this file and recorded in the
repository history.

---

# Política de privacidade — Nexaya OS

*Atualizada em 27 de setembro de 2026.*

Esta política cobre o plugin **Nexaya OS** para o Claude (este repositório),
publicado pela [Nexaya](https://nexaya.com.br).

**Resumo:** o plugin não coleta nada. Não tem telemetria, análise de uso nem
servidor próprio, e não faz nenhum acesso à rede. Tudo o que ele produz são arquivos
comuns no seu próprio disco.

- **O que ele lê:** só as pastas que você indicar, no setup e depois da sua
  confirmação: nomes de arquivos e pastas e notas em markdown, para escrever os
  roteadores. O inventário é só leitura. Arquivos de credencial, contratos,
  holerites e documentos bancários ou médicos são listados só pelo nome e nunca
  abertos; nenhum segredo é copiado.
- **O que ele escreve:** arquivos markdown e JSON na raiz do OS que você escolher.
  Fora dela, e só com o seu sim: um bloco no `~/.claude/CLAUDE.md` (acrescentado,
  nunca sobrescreve), links em `~/.claude/skills/` e rotinas agendadas no app do
  Claude, uma a uma.
- **Terceiros:** o plugin não envia nada a ninguém. O conteúdo que o Claude lê é
  processado pela Anthropic no seu uso normal do Claude, pelas regras dela. Rotinas
  que você criar rodam no seu app e só usam os seus conectores se você pedir.
- **Retenção:** o plugin não guarda nada. Os arquivos ficam no seu disco até você
  apagar.
- **Menores:** o plugin não é destinado a menores de 18 anos.
- **Nexaya OS Pro:** produto separado, fora deste repositório; também roda só na
  sua máquina e tem os próprios termos.
- **Contato:** abra uma issue em
  [github.com/baconshow/nexaya-os](https://github.com/baconshow/nexaya-os/issues).
