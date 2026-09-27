---
name: relatorio-mensal
description: Use quando a Ana pedir o relatório mensal de vendas da livraria. Monta o texto a partir das semanas do painel de vendas, no formato que a diretoria lê. Exemplo fictício.
---

# Relatório mensal de vendas

Exemplo fictício do Nexaya OS.

## Quando usar

No começo de cada mês, quando a Ana pedir o relatório do mês anterior.

## Como

1. Leia o `PROXIMO.md` do painel de vendas (`Trabalho/painel-vendas/`) e a
   memória `painel-vendas-regras`: semana fecha no domingo, receita líquida,
   devoluções à parte.
2. Some as semanas que caem no mês pelo domingo de fechamento.
3. Escreva uma página: três números no topo (receita líquida, variação contra
   o mês anterior, devoluções), uma tabela por loja e três observações.

## Regras

- Nenhum número sai da pasta `Trabalho/`.
- Se uma semana do mês não tem exportação, diga isso no topo em vez de estimar.
