---
name: fonte-dados-vendas
description: Os dados do painel de vendas vêm da exportação de segunda-feira, que só sai do computador do trabalho; colunas e o código novo da categoria Infantil
metadata:
  type: reference
---

O painel de vendas lê uma exportação em CSV que o sistema da livraria gera
toda segunda-feira de manhã, com a semana anterior. A exportação só sai do
computador do trabalho, porque o sistema fica na rede interna.

Colunas usadas: data, loja, categoria, quantidade, valor bruto, desconto,
devolução.

Armadilha: a categoria Infantil mudou de código em agosto de 2026. Para séries
que atravessam agosto, some os dois códigos antes de comparar.

Se a exportação atrasar, não gere o painel com a semana incompleta: registre
no `PROXIMO.md` do projeto e espere.

Regras de negócio: [[painel-vendas-regras]].
