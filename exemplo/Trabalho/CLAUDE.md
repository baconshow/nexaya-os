---
os: departamento
depto: Trabalho
resumo: A Livraria Horizonte (fictícia) — painel de vendas semanal e migração do estoque
---

# Trabalho

Roteador do trabalho da Ana como analista de dados na Livraria Horizonte, uma
rede fictícia de seis lojas. Numa sessão sobre um projeto, leia primeiro o
`PROXIMO.md` dele e depois o que o item do projeto indica. Não varra as
pastas: o que não está aqui mora no arquivo apontado.

## Ler primeiro

- [Memórias do Trabalho](MEMORIA.md) — regras do painel de vendas e de onde vêm os dados
- [Regras do painel de vendas](../Sistema/memoria/painel-vendas-regras.md) — semana, receita líquida e devoluções; consulte antes de mexer em número

## Projetos

- [Painel de vendas](painel-vendas/) — painel semanal de vendas por loja e por categoria, em HTML estático gerado a partir da exportação de segunda-feira. Status: ativo (último handoff em 25/09). Máquina: qualquer uma para o painel; a exportação só sai do computador do trabalho. Porta 5510 (`painel-vendas-web`). Ler primeiro: [PROXIMO.md](painel-vendas/PROXIMO.md), depois o [README](painel-vendas/README.md)
- [Migração do estoque](migracao-estoque/) — mapeamento das planilhas de estoque para o sistema novo da livraria. Status: parado desde 12/09, esperando o fornecedor do sistema. Ler primeiro: [PROXIMO.md](migracao-estoque/PROXIMO.md)

## Skills

- `relatorio-mensal` — monta o relatório do mês a partir do painel de vendas, no formato que a diretoria lê
- `nexaya-os:handoff` — ler o `PROXIMO.md` ao abrir sessão e reescrevê-lo ao encerrar

## Apps

- `painel-vendas-web` — o painel de vendas servido localmente, porta 5510

## Regras

- Número por loja não sai da empresa: nada de colar tabela de vendas em
  serviço externo nem em arquivo fora de `Trabalho/`.
- A exportação de vendas só roda no computador do trabalho (rede interna). Em
  casa, trabalhe com a última exportação que já está na pasta do projeto.
- Mudança de regra de negócio (o que conta como venda, devolução, semana)
  entra na memória antes de entrar no código.

## Referências

- [README do painel](painel-vendas/README.md) — como o painel é gerado e o que cada página mostra
- [Handoff de 18/09](painel-vendas/handoffs/2026-09-18.md) — a decisão de separar devoluções

## Pendências

- A migração do estoque depende do dicionário de campos que o fornecedor
  prometeu para o fim de setembro; confirmar com a Ana se chegou.
