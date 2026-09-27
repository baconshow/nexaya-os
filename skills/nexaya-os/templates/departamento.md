---
os: departamento
depto: {{DEPTO}}
resumo: {{uma linha que aparece no painel: o que este departamento cobre}}
---

<!-- MODELO de roteador de departamento (<Depto>/CLAUDE.md). Troque os {{...}},
escreva no idioma da pessoa, apague este comentário e as seções vazias.
Fique abaixo de ~150 linhas. Roteador aponta, não copia. -->

# {{DEPTO}}

Roteador de {{o que é o departamento, em uma frase}}. Numa sessão sobre um
projeto, leia primeiro o `PROXIMO.md` dele e depois o que o item do projeto
indica. Não varra as pastas: o que não está aqui mora no arquivo apontado.

## Ler primeiro

- [Memórias de {{DEPTO}}](MEMORIA.md) — índice das memórias do departamento, por projeto
- [{{ARQUIVO_DE_REGRAS_OU_DECISOES}}]({{caminho}}) — {{por que ler antes de tudo}}

## Projetos

- [{{PROJETO}}]({{pasta-do-projeto}}/) — {{o que é, em uma frase}}. Status: {{ativo | parado desde DD/MM | arquivo}}. Máquina: {{qualquer uma | nome}}{{; porta NNNN (`id-do-app`)}}. Ler primeiro: [PROXIMO.md]({{pasta-do-projeto}}/PROXIMO.md)
- [{{PROJETO_FORA_DO_OS}}]({{caminho absoluto da pasta}}/) — {{o que é}}. Status: {{...}}. Ler primeiro: [README.md]({{caminho absoluto}}/README.md)

## Skills

- `{{skill-do-departamento}}` — {{quando usar}}
- `nexaya-os:handoff` — ler o `PROXIMO.md` ao abrir sessão e reescrevê-lo ao encerrar

## Apps

- `{{id-no-apps.json}}` — {{o que é}}, porta {{NNNN}}

## Regras

- {{Regra específica deste departamento, com o motivo quando não for óbvio.}}

## Referências

- [{{Documento de apoio}}]({{caminho}}) — {{o que ensina}}

## Pendências

- {{Problema achado no inventário ou decisão que espera a pessoa. Uma linha cada.}}
