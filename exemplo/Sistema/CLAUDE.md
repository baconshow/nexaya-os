---
os: departamento
depto: Sistema
resumo: O próprio Ana OS — skills, memória, rotinas e apps (camada ARMS)
---

# Sistema — o Ana OS por dentro

Este departamento cuida do próprio Ana OS, montado com o Nexaya OS. A
organização segue o ARMS:

- **Applications (Apps):** os servidores locais dos projetos. Porta, pasta e
  comando ficam num registro único, `apps.json`.
- **Routines (Rotinas):** tarefas que rodam sozinhas em horário marcado e deixam
  o resultado em arquivo, em `dados/relatorios/`.
- **Memory (Memória):** uma pasta única de auto-memória, `memoria/`, indexada
  pelo `MEMORY.md` e pelo `MEMORIA.md` de cada departamento.
- **Skills:** o que o Claude sabe fazer. As skills próprias da Ana moram em
  `skills/`; as do plugin vêm com o prefixo `nexaya-os:`.

Antes de editar qualquer arquivo do OS, leia `CONVENCOES.md`: o Claude e a
faxina se orientam por aquele formato.

## Ler primeiro

- [Convenções](CONVENCOES.md) — formato dos roteadores
- [Segurança](SEGURANCA.md) — riscos abertos e o que nunca abrir
- [Estado do OS](PROXIMO.md) — o que ficou pendente na montagem

## Projetos

- [Memória](memoria/) — pasta única de auto-memória, apontada pelo `autoMemoryDirectory` do `settings.json` nas duas máquinas. Índice: [MEMORY.md](memoria/MEMORY.md)
- [Skills do OS](skills/) — as três skills próprias da Ana, sincronizadas com o OS e ligadas em `~/.claude/skills` por junction. Ler primeiro: [README.md](skills/README.md)

A Ana usa só o núcleo gratuito do Nexaya OS, sem painel. Com o Nexaya OS Pro,
o painel ficaria em `painel/` e entraria no `apps.json`; o README do exemplo
mostra como abrir o painel do Pro contra esta pasta.

## Skills

- `nexaya-os:nexaya-os` — assistente de setup: acrescentar departamento, rotinas ou o Nexaya OS Pro, renomear o OS ou rodar a revisão
- `nexaya-os:handoff` — `PROXIMO.md` e handoff datado no início e no fim da sessão
- `nexaya-os:faxina-os` — faxina do OS: links quebrados, memória, handoffs parados; só relata

## Rotinas

- `faxina-semanal` — sexta, 17:30: a faxina do OS; relatório em `dados/relatorios/`
- `resumo-semana` — sexta, 18:00: o que andou na semana, por departamento; relatório em `dados/relatorios/`

## Referências

- [Registro de apps](apps.json) — portas, pastas e comandos
- [Registro de rotinas](rotinas.json) — agenda e saída de cada rotina
- [Memória do Sistema](MEMORIA.md) — memórias transversais e a higiene pendente

## Máquinas

As rotinas agendadas existem só no notebook de casa, onde foram criadas. O
computador do trabalho tem as skills ligadas e a memória compartilhada, mas
nenhuma rotina.

## Regras

- Skill própria nova nasce em `skills/<nome>/`, entra no `## Skills` do
  roteador do departamento que a usa e é ligada com o `instalar.ps1` nas duas
  máquinas.
- App ou porta nova entra no `apps.json` antes de subir. Não reuse porta que já
  está no registro.
- Rotina nova entra no `rotinas.json` e em `## Rotinas`. Rotina grava arquivo;
  enviar, publicar ou preencher site fica com a Ana.
- Mudança em `~/.claude` (settings, hooks, skills) só quando a Ana pedir.

## Pendências

- Candidata a rotina: briefing de e-mail pela manhã. Fica de fora até a Ana
  ligar o conector de e-mail.
