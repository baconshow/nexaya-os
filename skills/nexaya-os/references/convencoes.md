---
os: referencia
depto: Sistema
resumo: Formato dos arquivos-roteador do OS — o Claude se orienta por eles e o painel monta o grafo a partir deles
---

# Convenções do OS

> **English:** this is the contract every file of the OS follows. The reserved
> `##` headings and the frontmatter values are in Portuguese on purpose, because
> the cleanup script and the Nexaya OS Pro panel parse them. Keep them exactly as written here even if the rest of
> the OS is in another language. The setup copies this file to
> `Sistema/CONVENCOES.md`.

O OS é feito de arquivos-roteador em markdown. O Claude lê esses arquivos para
achar as coisas, a faxina (`faxina-os`) confere os links e os registros, e o
painel do Nexaya OS Pro (`Sistema/painel/`, quando instalado) monta o grafo a
partir deles. Por isso o formato é fixo: o que foge dele não aparece no grafo
e obriga a próxima sessão a varrer pastas. Sem o painel, o formato vale do
mesmo jeito.

O princípio: **roteador aponta, não copia, e não reorganiza.** As pastas dos
projetos ficam onde estão. O OS é uma camada fina de arquivos que diz onde cada
coisa mora e o que ler primeiro.

## Onde fica cada coisa

| Arquivo | Papel |
|---|---|
| `CLAUDE.md` (raiz) | Hub. Quem é a pessoa, os departamentos, as regras globais |
| `<Depto>/CLAUDE.md` | Roteador do departamento: projetos, skills, apps, regras, referências |
| `<Depto>/MEMORIA.md` | Índice das memórias do departamento, agrupado por projeto |
| `<Depto>/*.md` com frontmatter `os:` | Índices e referências do departamento (aparecem no grafo) |
| `<projeto>/PROXIMO.md` | Estado atual do projeto; a primeira leitura de uma sessão nele |
| `<projeto>/handoffs/AAAA-MM-DD.md` | Handoffs datados; o `PROXIMO.md` aponta o mais recente |
| `Sistema/CONVENCOES.md` | Este arquivo |
| `Sistema/SEGURANCA.md` | Riscos abertos (só caminho e ação, nunca valor) e o que nunca abrir |
| `Sistema/apps.json` | Registro único de apps locais: porta, pasta, comando |
| `Sistema/rotinas.json` | Registro das rotinas agendadas e de onde cada uma grava |
| `Sistema/memoria/` | Pasta de memória, quando ela mora dentro do OS, com o índice `MEMORY.md` |
| `Sistema/skills/` | Skills próprias da pessoa, uma pasta por skill com `SKILL.md` |
| `Sistema/painel/` | O painel do Nexaya OS Pro (servidor e interface), quando instalado |
| `Sistema/dados/` | Saídas de rotinas e do painel; é local, não se versiona |

## Departamentos

- Um departamento é uma pasta de primeiro nível da raiz com um `CLAUDE.md`
  dentro. O nome do departamento é o nome da pasta.
- A lista oficial é a seção `## Departamentos` do hub, na ordem em que aparece.
  O painel dá uma cor a cada departamento nessa ordem.
- `Sistema` existe sempre e tem esse nome em qualquer idioma: a faxina e o
  painel procuram `Sistema/apps.json` e `Sistema/rotinas.json`, e o painel
  mora em `Sistema/painel/`.
- Prefira nomes curtos, sem espaço. Acento funciona, mas complica caminho em
  linha de comando.

## Frontmatter

Todo arquivo do OS começa com:

```yaml
---
os: hub | departamento | memoria | indice | referencia
depto: <nome do departamento>
resumo: uma linha que aparece no painel
---
```

O hub usa `os: hub` e `depto: Sistema`. As memórias em si seguem o formato de
memória do Claude Code (`name`, `description`, `metadata.type`), não este.

## Seções reservadas (títulos `##`)

O painel reconhece estes títulos sem diferenciar maiúsculas e ignorando acento:

| Título | O que vira no grafo |
|---|---|
| `## Departamentos` | só no hub: cada link vira um departamento |
| `## Ler primeiro` | referências prioritárias |
| `## Projetos` | cada item vira um projeto |
| `## Skills` | cada item vira uma skill |
| `## Referências` | cada link vira uma referência |
| `## Apps` | cada item vira um app |
| `## Rotinas` | cada item vira uma rotina |
| `## Regras`, `## Pendências`, `## Máquinas` | texto; não gera nó |

Qualquer outro título `##` vira um **grupo** (nó intermediário), desde que tenha
pelo menos um item com link. No `MEMORIA.md`, um título igual ao nome de um
projeto do roteador liga as memórias daquela seção ao projeto.

## Itens de lista

Um item por linha, começando com `- `. Continuação de item vai recuada.

- **Projeto, referência, memória:** o primeiro link do item é o nó. Os links
  seguintes no mesmo item viram referências penduradas nele.

  ```markdown
  - [Painel de vendas](painel-vendas/) — painel semanal da loja. Status: ativo. Ler primeiro: [PROXIMO.md](painel-vendas/PROXIMO.md)
  ```

- **Skill:** o primeiro nome entre crases é a skill. Skill de plugin leva o
  prefixo do plugin (`plugin:skill`).

  ```markdown
  - `relatorio-mensal` — monta o relatório do mês a partir do painel
  ```

- **App:** o primeiro nome entre crases é o `id` em `Sistema/apps.json`.
- **Rotina:** o primeiro nome entre crases é o `id` em `Sistema/rotinas.json`.

Trecho entre crases nunca vira link. Use crases para citar um caminho sem criar
nó no grafo (é o jeito certo de citar arquivo sensível em `SEGURANCA.md`).

## Memória

- O índice `MEMORY.md` da pasta de memória tem uma seção `##` por departamento,
  com o nome **exato** do departamento. É assim que o painel sabe de quem é cada
  memória. Memória que vale para todos fica em `## Sistema`.
- Uma linha por memória: `- [Título](arquivo.md) — gancho de uma linha`.
- O `MEMORIA.md` de cada departamento repete as memórias dele, agrupadas por
  projeto, com link relativo para o arquivo na pasta de memória.
- Memória nova entra nos dois lugares: `MEMORY.md` e `MEMORIA.md` do departamento.
- Memórias se ligam entre si com `[[nome-do-arquivo]]` (sem `.md`).

## Caminhos

- Link relativo é relativo ao arquivo onde está. Prefira a barra `/`: funciona
  em Windows, macOS e Linux, no GitHub e no Obsidian.
- Pasta termina com `/`. Caminho com espaço vai entre `<` e `>`:
  `[Notas da banca](<mestrado/notas da banca/>)`.
- Caminho absoluto só para o que mora fora da raiz do OS (um repositório em
  `Documents`, por exemplo). Se o OS roda em máquinas com perfis diferentes,
  escreva sempre com o perfil de uma delas e declare esse prefixo na seção
  `## Máquinas` do hub. Com o Nexaya OS Pro, declare-o também em
  `perfil_origem` no `config.json` do painel, que troca pelo perfil da máquina
  onde roda.
- Nos registros JSON (`apps.json`, `rotinas.json`, `config.json` do painel),
  use os marcadores `{OS_ROOT}` e `{HOME}` em vez de caminho fixo.

## Handoff

- Cada projeto ativo tem um `PROXIMO.md`: o estado atual e o próximo passo.
  Fica na raiz da pasta do projeto, a menos que o roteador diga outro lugar.
- Os handoffs datados ficam em `handoffs/AAAA-MM-DD.md` dentro do projeto.
- O item do projeto no roteador aponta o `PROXIMO.md` com "Ler primeiro:".

## Tamanho

Roteador aponta, não copia. Um `CLAUDE.md` de departamento fica abaixo de umas
150 linhas e o `MEMORY.md` abaixo de umas 200 (ele entra no contexto de toda
sessão). Detalhe mora no arquivo apontado.

## Nunca

- Nunca registrar segredo, senha, token, chave ou dado de saúde num arquivo do OS.
- Nunca apontar o grafo para arquivo sensível: `.env*`, `*.pfx`, `*.p12`,
  `*.key`, `*.pem`, nomes com chave, senha, token, secret ou credencial,
  contratos, holerites, extratos e documentos médicos. Cite com crases, sem link.
- Nunca mover, renomear ou apagar pasta de projeto para "arrumar" o OS. Se a
  organização incomoda, registre a proposta nas `## Pendências` e deixe a
  decisão com a pessoa.
