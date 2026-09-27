---
os: hub
depto: Sistema
resumo: {{NOME_OS}} — ponto de partida de toda sessão
---

<!-- MODELO do hub (CLAUDE.md na raiz do OS). Troque os {{...}}, escreva no
idioma da pessoa e apague este comentário. {{NOME_OS}} é o nome que a pessoa
deu ao OS na entrevista (ex.: "Ana OS"). Mantenha os títulos ## reservados
como estão: a faxina e o painel leem "Departamentos", "Ler primeiro", "Regras"
e "Máquinas". -->

# {{NOME_OS}} — Agentic System

Esta pasta (`{{RAIZ_OS}}`) é a raiz do **{{NOME_OS}}**, o sistema de agentes de
{{NOME}}, montado com o Nexaya OS. {{UMA FRASE SOBRE A SINCRONIZAÇÃO, ex.: "Ela
sincroniza pelo Dropbox entre o notebook e o computador do trabalho."}} Tudo o
que o Claude precisa para se orientar começa aqui.

**Toda sessão:** leia este arquivo, depois o `CLAUDE.md` do departamento da
tarefa. O roteador do departamento diz o que ler em seguida. Não saia varrendo
pastas: o roteador existe para evitar isso.

## Quem é {{NOME}}

- Chame de **{{COMO_CHAMAR}}**. Responda em {{IDIOMA}}.
- {{UMA OU DUAS LINHAS DE CONTEXTO: trabalho, empresa, estudos}}.
- Perfil completo: [{{TITULO_DA_MEMORIA_DE_PERFIL}}]({{CAMINHO_DA_MEMORIA_DE_PERFIL}}).

## Departamentos

- [{{DEPTO_1}}]({{DEPTO_1}}/CLAUDE.md) — {{uma linha: o que mora ali}}
- [{{DEPTO_2}}]({{DEPTO_2}}/CLAUDE.md) — {{uma linha}}
- [Sistema](Sistema/CLAUDE.md) — o próprio OS: skills, memória, rotinas e apps{{, e o painel, com o Nexaya OS Pro}}

## Ler primeiro

- [Convenções do OS](Sistema/CONVENCOES.md) — formato dos roteadores; siga antes de editar um
- [Índice de memória]({{CAMINHO_DO_MEMORY_MD}}) — fatos e decisões entre sessões, por departamento
- [Segurança](Sistema/SEGURANCA.md) — riscos abertos e o que nunca abrir

## Regras

- **Antes de criar arquivo ou pasta,** ache o destino no roteador do
  departamento. Sem destino claro, pergunte a {{NOME}}.
- **Entregáveis** ficam no projeto a que pertencem, nunca soltos na raiz do OS
  nem em `~/.claude`.
- **Handoff:** ao fim de uma sessão relevante, atualize o `PROXIMO.md` do
  projeto (skill `handoff`). Sessão nova num projeto lê o `PROXIMO.md` antes de tudo.
- **Memória:** memória nova entra na pasta de memória, no `MEMORY.md` (seção do
  departamento) e no `MEMORIA.md` do departamento.
- **Segredo nunca:** não abra nem copie `.env*`, chaves, certificados, arquivos
  com senha, token ou credencial, contratos e documentos pessoais. Não registre
  dado de saúde de ninguém em arquivo do OS.
- **Não mova nem apague** pasta de projeto sem {{NOME}} pedir. Apps, repositórios
  e arquivos com caminho fixo quebram com mudança de lugar.
- **Git:** commit e push só quando {{NOME}} pedir.

## Máquinas

<!-- Só se o OS roda em mais de um computador. Senão, apague a seção. -->

| Máquina | Perfil | Rede | O que só roda nela |
|---|---|---|---|
| {{MAQUINA_1}} | `{{HOME_1}}` | {{rede}} | {{o que só roda nela}} |
| {{MAQUINA_2}} | `{{HOME_2}}` | {{rede}} | {{o que só roda nela}} |

Caminhos absolutos nos roteadores usam `{{HOME_1}}`; em {{MAQUINA_2}}, leia como `{{HOME_2}}`.

## Painel

<!-- Só com o Nexaya OS Pro instalado. Sem ele, apague a seção. -->

O painel do Nexaya OS Pro mostra o grafo do OS e a atividade do Claude ao
vivo. Abra com `Sistema/painel/abrir-painel.bat` (Windows) ou
`python Sistema/painel/servir.py --abrir`, ou acesse
`http://127.0.0.1:{{PORTA_PAINEL}}` se já estiver rodando.
