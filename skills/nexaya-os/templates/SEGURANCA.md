---
os: referencia
depto: Sistema
resumo: Riscos de segurança e privacidade abertos, por prioridade, com caminho e ação; e o que nunca abrir
---

<!-- MODELO do Sistema/SEGURANCA.md. NUNCA escreva o valor de um segredo aqui,
nem parte dele. Caminhos entre crases, nunca como link (o grafo do painel não
pode apontar para arquivo sensível). Nenhum item é corrigido pelo setup: as
ações são da pessoa. Apague este comentário. -->

# Segurança

Riscos achados no inventário de {{DATA}}. Aqui só entram caminho e ação:
**nenhum valor de segredo** é copiado para este arquivo. Quando resolver um
item, apague a linha.

## Crítico

Credencial ativa exposta. Trocar primeiro, arrumar o arquivo depois.

1. **{{O que é, sem o valor}}.**
   - Onde: `{{caminho}}`
   - Ação: {{rotacionar ou revogar; depois mover para um cofre de senhas e apagar o arquivo}}

## Alto

2. **{{O que é}}.**
   - Onde: `{{caminho}}`
   - Ação: {{...}}

## Médio

3. **{{O que é}}.**
   - Onde: `{{caminho}}`
   - Ação: {{...}}

## Nunca abrir

O Claude registra que estes arquivos existem, mas nunca lê o conteúdo:

- `.env`, `.env.*`, `*.pfx`, `*.p12`, `*.key`, `*.pem`, `*.jks`, `*.kdbx`,
  `id_rsa*`, `*serviceAccount*.json`, `client_secret*.json`.
- Nomes com chave, senha, token, secret, credencial, conta, login ou vault.
- Contratos, holerites, extratos, recibos, documentos de identidade, exames e
  laudos, fotos pessoais.
- {{Pastas que a pessoa marcou como privadas na entrevista.}}
- Binários em pasta de nuvem (abrir dispara o download do arquivo).
