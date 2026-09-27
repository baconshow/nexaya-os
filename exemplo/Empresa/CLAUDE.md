---
os: departamento
depto: Empresa
resumo: O ateliê da Ana (fictício) — painéis para pequenos negócios; site e propostas
---

# Empresa

Roteador do ateliê da Ana, um negócio pequeno e fictício que faz painéis de
dados para pequenos negócios (padarias, academias, escolas de idiomas). É
trabalho de fim de semana: dois ou três clientes por vez. Numa sessão sobre um
projeto, leia primeiro o `PROXIMO.md` dele.

## Ler primeiro

- [Memórias da Empresa](MEMORIA.md) — o tom das propostas e o que já foi decidido com clientes
- [Tom das propostas](../Sistema/memoria/tom-das-propostas.md) — escopo fechado, sem jargão; leia antes de escrever para cliente

## Projetos

- [Site do ateliê](site/) — site de uma página com portfólio e contato, HTML puro. Status: ativo (22/09). Porta 5520 (`site-atelie`). Ler primeiro: [PROXIMO.md](site/PROXIMO.md)
- [Propostas](propostas/) — propostas comerciais, uma por cliente, a partir de um modelo. Status: ativo (24/09), uma proposta em revisão. Ler primeiro: [PROXIMO.md](propostas/PROXIMO.md), depois o [modelo](propostas/modelo-proposta.md)

## Skills

- `proposta-comercial` — escreve a proposta a partir do modelo e das regras de tom
- `nexaya-os:handoff` — ler o `PROXIMO.md` ao abrir sessão e reescrevê-lo ao encerrar

## Apps

- `site-atelie` — o site servido localmente para revisão, porta 5520

## Regras

- Cliente aparece pelo tipo de negócio ("a padaria", "a academia"), nunca pelo
  nome de pessoa, em qualquer arquivo do OS.
- Preço e prazo só entram numa proposta depois que a Ana confirmar.
- Nada é enviado a cliente pelo Claude: a Ana revisa e envia.

## Referências

- [Modelo de proposta](propostas/modelo-proposta.md) — estrutura e frases-padrão

## Pendências

- O site ainda não tem domínio; a Ana decide o nome em outubro.
