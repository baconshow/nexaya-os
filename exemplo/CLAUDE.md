---
os: hub
depto: Sistema
resumo: Ana OS — ponto de partida de toda sessão
---

# Ana OS — Agentic System

Esta pasta é a raiz do **Ana OS**, o sistema de agentes da Ana, montado com o
Nexaya OS. Ela sincroniza pela nuvem entre o notebook de casa e o computador
do trabalho.
Tudo o que o Claude precisa para se orientar começa aqui.

> Exemplo fictício do Nexaya OS: a Ana, a livraria, o ateliê e todos os
> projetos são inventados. Veja o [README do exemplo](README.md).

**Toda sessão:** leia este arquivo, depois o `CLAUDE.md` do departamento da
tarefa. O roteador do departamento diz o que ler em seguida. Não saia varrendo
pastas: o roteador existe para evitar isso.

## Quem é a Ana

- Chame de **Ana**. Responda em português do Brasil, com respostas curtas.
- Analista de dados na Livraria Horizonte (rede fictícia de livrarias), dona de
  um pequeno ateliê de painéis para pequenos negócios e mestranda em ciência
  de dados.
- Perfil completo: [Quem é a Ana](Sistema/memoria/quem-e-a-ana.md).

## Departamentos

- [Trabalho](Trabalho/CLAUDE.md) — a livraria: painel de vendas e migração do estoque
- [Empresa](Empresa/CLAUDE.md) — o ateliê: site, propostas e clientes
- [Estudos](Estudos/CLAUDE.md) — mestrado e curso de estatística
- [Pessoal](Pessoal/CLAUDE.md) — viagem, leituras e a vida fora do trabalho
- [Sistema](Sistema/CLAUDE.md) — o próprio OS: skills, memória, rotinas e apps

## Ler primeiro

- [Convenções do OS](Sistema/CONVENCOES.md) — formato dos roteadores; siga antes de editar um
- [Índice de memória](Sistema/memoria/MEMORY.md) — fatos e decisões entre sessões, por departamento
- [Segurança](Sistema/SEGURANCA.md) — riscos abertos e o que nunca abrir

## Regras

- **Antes de criar arquivo ou pasta,** ache o destino no roteador do
  departamento. Sem destino claro, pergunte à Ana.
- **Entregáveis** ficam no projeto a que pertencem, nunca soltos na raiz do OS
  nem em `~/.claude`.
- **Handoff:** ao fim de uma sessão relevante, atualize o `PROXIMO.md` do
  projeto (skill `handoff`). Sessão nova num projeto lê o `PROXIMO.md` antes de tudo.
- **Memória:** memória nova entra em `Sistema/memoria/`, no `MEMORY.md` (seção
  do departamento) e no `MEMORIA.md` do departamento.
- **Segredo nunca:** não abra nem copie `.env*`, chaves, certificados, arquivos
  com senha, token ou credencial, contratos e documentos pessoais. Não registre
  dado de saúde de ninguém em arquivo do OS.
- **Não mova nem apague** pasta de projeto sem a Ana pedir.
- **Git:** commit e push só quando a Ana pedir.

## Máquinas

| Máquina | Perfil | Rede | O que só roda nela |
|---|---|---|---|
| notebook (casa) | `C:/Users/ana` | internet | rotinas agendadas |
| computador do trabalho | `C:/Users/ana` | rede interna da livraria | exportação diária de vendas, que o painel de vendas consome |

Tarefa que precisa da rede interna da livraria fica para uma sessão no
computador do trabalho.
