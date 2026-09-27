# Painel de vendas

Painel semanal de vendas da Livraria Horizonte (rede fictícia), por loja e por
categoria. É HTML estático: um script lê a exportação de segunda-feira e gera
as páginas em `web/`.

## Como rodar

- Ver o painel: suba o app `painel-vendas-web` pelo painel (se houver o Nexaya OS
  Pro), ou rode
  `python -m http.server 5510 --bind 127.0.0.1` dentro de `web/` e abra
  `http://127.0.0.1:5510`.
- Gerar de novo: a exportação só sai do computador do trabalho; o passo a passo
  está no `PROXIMO.md`.

## Páginas

- **Resumo:** receita líquida da semana, comparação com a semana anterior e com
  a mesma semana do ano passado.
- **Lojas:** as seis lojas lado a lado.
- **Categorias:** os dez gêneros que mais venderam.
- **Devoluções:** linha própria, fora da receita (decisão de 18/09).

## Regras

As regras de negócio estão na memória `painel-vendas-regras` do OS. Mudança
de regra entra lá antes de entrar aqui.
