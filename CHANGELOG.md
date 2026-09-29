# Changelog

Todas as mudanças relevantes do Nexaya OS ficam registradas aqui.
As versões seguem o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## 1.0.1 — ajustes pedidos pela checagem do diretório

### Alterado

- `plugin.json`: autor `nexaya-os` (o nome "Nexaya" era parecido demais com outro
  conector do diretório); ícone `.claude-plugin/icon.svg`.
- `exemplo/README.md`: os comandos do painel usam caminhos relativos
  (`./exemplo`) em vez de `$PWD`.

## 1.0.0 — primeira versão pública do Nexaya OS (núcleo gratuito)

Publicada pela [Nexaya](https://nexaya.com.br) sob licença MIT.

### Adicionado

- Manifesto do plugin `nexaya-os` (`.claude-plugin/plugin.json`) e o
  marketplace `nexaya` (`.claude-plugin/marketplace.json`), para instalar com
  `/plugin marketplace add baconshow/nexaya-os` e
  `/plugin install nexaya-os@nexaya`, ou pelo app, em "Adicionar de um
  repositório".
- Skill `nexaya-os`: o assistente de setup. Entrevista (com o nome que a
  pessoa dá ao próprio OS, de 1 a 40 caracteres, com "<primeiro nome> OS"
  como sugestão), inventário só de leitura em paralelo, escrita do OS (hub
  "<nome> — Agentic System", roteadores, índices de memória, `SEGURANCA.md`,
  registros de apps e de rotinas), rotinas e revisão. Também estende um OS que
  já existe e o renomeia, mostrando cada lugar que muda. Referências e modelos
  em `skills/nexaya-os/`.
- Passo opcional do Nexaya OS Pro no setup: explica o painel pago (em breve,
  pelo Supporter do Nexaya Design System) e, se a pessoa já tem o pacote do
  Pro, segue o `INSTALAR.md` dele. O setup nunca baixa nada.
- Skill `handoff`: fecha a sessão com um handoff datado, o `PROXIMO.md` do
  projeto e o prompt de continuação; a sessão seguinte começa por ele.
- Skill `faxina-os`: revisão só de leitura do OS (links quebrados nos
  roteadores, memórias fora do índice, `PROXIMO.md` parados, arquivos soltos,
  registros de apps e rotinas), com relatório, script de apoio em Python puro
  e testes em `skills/faxina-os/scripts/testes/`.
- O contrato dos roteadores (`references/convencoes.md`), copiado para o
  `Sistema/CONVENCOES.md` de cada OS.
- Um OS fictício completo em `exemplo/`, o Ana OS, para ver o formato antes de
  montar o seu.
- README em português e inglês, licença MIT.
