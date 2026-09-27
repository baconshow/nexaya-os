---
os: indice
depto: {{DEPTO}}
resumo: Índice de {{PASTA}} — uma linha por subpasta, sem abrir nada pessoal
---

<!-- MODELO de índice de uma pasta grande (Documentos, clientes, arquivo morto).
Fica na pasta do departamento (<Depto>/<NOME>.md) e é apontado em "## Referências"
do roteador. Nível de pasta, nunca de arquivo pessoal. Marque [SENSÍVEL] e
[PESSOAL] sem abrir. Os títulos ## viram grupos no painel. Apague este comentário. -->

# Índice de {{PASTA}}

Índice de `{{CAMINHO_ABSOLUTO_DA_PASTA}}`, feito no inventário de {{DATA}}. Só
nomes e metadados: nenhum documento pessoal foi aberto.

## {{Categoria 1, ex.: Clientes ativos}}

- [{{Subpasta}}](<{{CAMINHO_ABSOLUTO}}/{{Subpasta}}/>) — {{o que é}}, {{período}}, {{tipo de conteúdo}}, {{N}} arquivos

## {{Categoria 2, ex.: Arquivo morto}}

- [{{Subpasta}}](<{{CAMINHO_ABSOLUTO}}/{{Subpasta}}/>) — {{o que é}} [PESSOAL]

## Proposta de organização

{{Texto, sem executar: o que poderia ser agrupado ou arquivado. A decisão é da pessoa.}}

## Riscos de segurança

{{Só caminhos entre crases e a ação recomendada. Nunca valores. Os mesmos itens
entram no Sistema/SEGURANCA.md.}}
