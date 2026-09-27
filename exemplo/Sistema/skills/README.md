---
os: referencia
depto: Sistema
resumo: Skills próprias da Ana — roteadores curtos, sincronizados com o OS e ligados ao Claude Code por junction
---

# Skills do OS

Estas são as skills escritas para o trabalho da Ana. Cada uma é curta: diz
quando usar, as regras que não se negociam e aponta para o arquivo onde o
detalhe mora, sem copiá-lo.

A fonte é esta pasta, que sincroniza com o OS. O Claude Code lê as skills por
junctions em `~/.claude/skills/<nome>`, criadas pelo `instalar.ps1` que o setup
copia para cá. Editar aqui já vale nas duas máquinas depois de uma sessão nova.

## Skills

- `relatorio-mensal` — relatório do mês da livraria a partir do painel de vendas
- `proposta-comercial` — proposta do ateliê a partir do modelo e do tom combinado
- `fichamento` — fichamento de artigo no formato da dissertação

As skills do plugin (`nexaya-os:handoff`, `nexaya-os:faxina-os`) não moram aqui:
vêm com o plugin instalado em cada máquina.

## Criar uma skill nova

1. Crie `<nome>/SKILL.md` com o frontmatter `name` e `description` (até uns
   250 caracteres, dizendo quando usar).
2. Escreva um roteador: quando usar, regras centrais, caminhos para o que já
   existe.
3. Rode o `instalar.ps1` nas duas máquinas e liste a skill no `## Skills` do
   roteador do departamento que a usa.

> Exemplo fictício: não ligue estas skills no seu Claude Code. Elas existem
> para a faxina (e o painel do Nexaya OS Pro) terem o que mostrar.
