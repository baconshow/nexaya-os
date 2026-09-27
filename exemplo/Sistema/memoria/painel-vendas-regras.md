---
name: painel-vendas-regras
description: Regras de negócio do painel de vendas — semana fecha no domingo, receita líquida, devoluções numa linha à parte
metadata:
  type: project
---

Regras do painel de vendas da livraria, decididas pela Ana com a gerência:

- **Semana:** segunda a domingo. A semana 1 é a que contém o primeiro domingo
  do ano.
- **Receita:** líquida de descontos. Devolução **não** é abatida da receita:
  vira uma linha e uma página à parte (decisão de 18/09/2026, porque a
  gerência quer ver o volume de devoluções por loja).
- **Loja Online:** entra como sétima coluna só nos totais da rede; nas
  comparações entre lojas físicas ela fica de fora.

**Por quê:** antes de 18/09 cada relatório da livraria abatia as devoluções de
um jeito, e os números não batiam entre áreas.

De onde vêm os dados: [[fonte-dados-vendas]].
