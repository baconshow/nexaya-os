---
os: referencia
depto: Sistema
resumo: Riscos de segurança e privacidade abertos, por prioridade, com caminho e ação; e o que nunca abrir
---

# Segurança

Riscos achados no inventário de 26/09/2026. Aqui só entram caminho e ação:
**nenhum valor de segredo** é copiado para este arquivo. Os caminhos vão entre
crases, não como link, para o grafo do painel não apontar para eles. Quando
resolver um item, apague a linha.

## Crítico

Nenhum.

## Alto

1. **Arquivo de variáveis de ambiente do site dentro da pasta sincronizada.**
   - Onde: `Empresa/site/.env` (o inventário viu o nome; o conteúdo não foi aberto).
   - Ação: o site é HTML puro e não precisa dele. Confirmar com a Ana de onde
     veio, tirar da pasta sincronizada e, se tiver alguma chave, trocar a chave.

## Médio

2. **Memória pessoal sincronizando com o computador do trabalho.**
   - Onde: `Sistema/memoria/viagem-preferencias.md`.
   - Ação: o conteúdo é só preferência de viagem, sem dado sensível. A Ana
     decidiu manter. Reavaliar se a memória pessoal crescer.

## Nunca abrir

O Claude registra que estes arquivos existem, mas nunca lê o conteúdo:

- `.env`, `.env.*`, `*.pfx`, `*.p12`, `*.key`, `*.pem`, `*.kdbx`,
  `id_rsa*`, `*serviceAccount*.json`, `client_secret*.json`.
- Nomes com chave, senha, token, secret, credencial, conta, login ou vault.
- Contratos, holerites, extratos, recibos, documentos de identidade, exames e
  fotos pessoais.
- A pasta de documentos pessoais da Ana, fora do OS (ela sabe qual é).
- Binários em pasta de nuvem (abrir dispara o download do arquivo).
