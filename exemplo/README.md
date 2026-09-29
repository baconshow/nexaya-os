# Exemplo — o Ana OS

Um OS **fictício** e completo, do jeito que o assistente `nexaya-os` monta.
A Ana deu ao OS dela o nome **Ana OS**; ela, a Livraria Horizonte, o ateliê,
os clientes e os números são inventados. Serve para ver o resultado antes de
montar o seu, para testar a faxina e para abrir o painel do Nexaya OS Pro sem
expor nenhum dado real.

## O que olhar

- [CLAUDE.md](CLAUDE.md) — o hub: quem é a Ana, os cinco departamentos, as regras.
- Um roteador de departamento: [Trabalho/CLAUDE.md](Trabalho/CLAUDE.md).
- Um projeto com `PROXIMO.md` e handoffs datados: [painel-vendas](Trabalho/painel-vendas/PROXIMO.md).
- A memória: [índice](Sistema/memoria/MEMORY.md) e o [MEMORIA.md do Trabalho](Trabalho/MEMORIA.md).
- A camada ARMS: [Sistema/CLAUDE.md](Sistema/CLAUDE.md), [apps.json](Sistema/apps.json) e [rotinas.json](Sistema/rotinas.json).
- O contrato: [Sistema/CONVENCOES.md](Sistema/CONVENCOES.md), cópia da versão genérica do plugin.

## Abrir o painel do Nexaya OS Pro contra o exemplo

O painel não faz parte deste repositório: é o Nexaya OS Pro, vendido pelo
Supporter do Nexaya Design System (em breve). Com o pacote do Pro em mãos,
da raiz deste repositório:

```bash
# Windows (Git Bash) ou macOS/Linux
AGENTIC_OS_ROOT="./exemplo" AGENTIC_OS_MEMORY_DIR="./exemplo/Sistema/memoria" \
  python "<pasta do Nexaya OS Pro>/painel/servir.py" --abrir
```

```powershell
# PowerShell
$env:AGENTIC_OS_ROOT = ".\exemplo"
$env:AGENTIC_OS_MEMORY_DIR = ".\exemplo\Sistema\memoria"
python "<pasta do Nexaya OS Pro>\painel\servir.py" --abrir
```

`AGENTIC_OS_MEMORY_DIR` evita que o painel leia a sua própria memória (a do
`autoMemoryDirectory` do seu `settings.json`). A camada ao vivo mostra a
atividade real do Claude na sua máquina. Rodando direto da pasta do pacote, o
deck fica vazio até você copiar o `templates/deck.json` do pacote para a pasta
`painel` dele. O `INSTALAR.md` do Pro traz o resto.

## Conferir os links

```bash
python skills/faxina-os/scripts/checar_os.py exemplo --memoria exemplo/Sistema/memoria --formato md --falhar-se-quebrado
```

O exemplo não tem link quebrado, problema de convenção, memória fora do
índice nem registro inconsistente. O único achado esperado é a lista de
`PROXIMO.md` parados: a faxina usa a data escrita no próprio arquivo, e as
datas do exemplo são fixas (setembro de 2026), então com o tempo todos
aparecem como parados.

## O que não está aqui

- O painel em `Sistema/painel/`: só existe com o Nexaya OS Pro instalado.
- `Sistema/dados/`: é onde as rotinas gravam, e fica fora do git.
- O `instalar.ps1` em `Sistema/skills/`: as skills da Ana são de mentira e não devem ser ligadas no seu Claude Code.
