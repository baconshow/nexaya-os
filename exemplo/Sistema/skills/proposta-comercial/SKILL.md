---
name: proposta-comercial
description: Use quando a Ana pedir uma proposta para um cliente do ateliê. Escreve o rascunho a partir do modelo de proposta e do tom combinado; preço e prazo ficam a confirmar. Exemplo fictício.
---

# Proposta comercial do ateliê

Exemplo fictício do Nexaya OS.

## Quando usar

Quando a Ana contar o que um cliente pediu e quiser o rascunho da proposta.

## Como

1. Leia o modelo em `Empresa/propostas/modelo-proposta.md` e a memória
   `tom-das-propostas`.
2. Escreva o rascunho em `Empresa/propostas/AAAA-MM-tipo-de-negocio.md`,
   seguindo as seis partes do modelo, na ordem.
3. Marque preço e prazo como "a confirmar pela Ana".
4. Atualize o `PROXIMO.md` das propostas (skill `nexaya-os:handoff`).

## Regras

- O cliente aparece pelo tipo de negócio, nunca pelo nome de uma pessoa.
- A proposta não é enviada pelo Claude.
