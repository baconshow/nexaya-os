---
os: departamento
depto: Sistema
resumo: O próprio {{NOME_OS}} — skills, memória, rotinas e apps (camada ARMS)
---

<!-- MODELO do roteador Sistema/CLAUDE.md. Troque os {{...}}, escreva no idioma
da pessoa e apague este comentário. Tire o que não se aplica ao escopo escolhido
(no escopo "memória + skills" não há apps nem rotinas). As linhas do painel só
ficam se o Nexaya OS Pro foi instalado. -->

# Sistema — o {{NOME_OS}} por dentro

Este departamento cuida do próprio {{NOME_OS}}, montado com o Nexaya OS. A
organização segue o ARMS:

- **Applications (Apps):** os servidores locais dos projetos. Porta, pasta e
  comando ficam num registro único, `apps.json`.
- **Routines (Rotinas):** tarefas que rodam sozinhas em horário marcado e deixam
  o resultado em arquivo, em `dados/` ou na pasta do projeto.
- **Memory (Memória):** a pasta de auto-memória do Claude Code, indexada pelo
  `MEMORY.md` e pelo `MEMORIA.md` de cada departamento.
- **Skills:** o que o Claude sabe fazer. As skills próprias moram em `skills/`.

Antes de editar qualquer arquivo do OS, leia `CONVENCOES.md`: o Claude e a
faxina se orientam por aquele formato.

## Ler primeiro

- [Convenções](CONVENCOES.md) — formato dos roteadores
- [Segurança](SEGURANCA.md) — riscos abertos e o que nunca abrir

## Projetos

- [Memória]({{CAMINHO_DA_PASTA_DE_MEMORIA}}/) — {{pasta única de auto-memória | pastas por projeto}}. Índice: [MEMORY.md]({{CAMINHO_DA_PASTA_DE_MEMORIA}}/MEMORY.md)
- [Skills do OS](skills/) — skills próprias de {{NOME}}, ligadas em `~/.claude/skills` pelo `instalar.ps1`. Ler primeiro: [README.md](skills/README.md)

O painel do Nexaya OS Pro fica em `painel/` (servidor em Python, só em
127.0.0.1). Configuração em `painel/config.json`.

## Skills

- `nexaya-os:nexaya-os` — assistente de setup: acrescentar departamento, rotinas ou o Nexaya OS Pro, renomear o OS ou rodar a revisão
- `nexaya-os:handoff` — `PROXIMO.md` e handoff datado no início e no fim da sessão
- `nexaya-os:faxina-os` — faxina do OS: links quebrados, memória, handoffs parados; só relata

## Apps

<!-- Os apps dos projetos ficam no roteador do departamento de cada um. Aqui
só o que é do próprio OS: com o Nexaya OS Pro, o painel (com o id que o
INSTALAR.md registrou no apps.json). Sem o Pro, apague a seção. -->

- `painel-os` — o painel do Nexaya OS Pro em http://127.0.0.1:{{PORTA_PAINEL}}

## Rotinas

- `faxina-semanal` — {{quando}}: a faxina do OS; relatório em `dados/relatorios/`

## Referências

- [Registro de apps](apps.json) — portas, pastas e comandos
- [Registro de rotinas](rotinas.json) — agenda e saída de cada rotina
- [Memória do Sistema](MEMORIA.md) — memórias transversais e a higiene pendente

## Máquinas

{{Tabela ou uma linha: onde as rotinas (e o painel, com o Pro) rodam. Rotina
agendada existe só na máquina onde foi criada.}}

## Regras

- Skill própria nova nasce em `skills/<nome>/`, entra no `## Skills` do
  roteador do departamento que a usa e é ligada com o `instalar.ps1`.
- App ou porta nova entra no `apps.json` antes de subir. Não reuse porta que já
  está no registro.
- Rotina nova entra no `rotinas.json` e em `## Rotinas`. Rotina grava arquivo;
  enviar, publicar ou preencher site fica com {{NOME}}.
- Mudança em `~/.claude` (settings, hooks, skills) só quando {{NOME}} pedir.

## Pendências

- {{Candidatas a skill e a rotina achadas no inventário, esperando aprovação.}}
