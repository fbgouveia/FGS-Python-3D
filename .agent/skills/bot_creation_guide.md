# Skill: Bot Fleet Management (Quick-Start)
**Status:** Protocol Defined
**Context:** Rapid deployment of specialized sub-agents via @BotFather.

Papai, entendi que eu posso comandar uma frota de sub-agentes. O @BotFather é o nosso recrutador oficial.

## 🛠️ Protocolo de Recrutamento
1.  **Criação:** `/newbot` via @BotFather.
2.  **Identidade:** O username deve terminar em `bot` e ser único.
3.  **Token (A Alma do Bot):** Nunca partilhar. Guardar no `credentials_vault.py`.

## 🧪 Teste de Conexão Rápida
- **URL:** `https://api.telegram.org/bot<TOKEN>/getMe`
- Se retornar JSON válido, o bot está vivo e pronto para ordens.

## 🚀 Padrão de Codificação Soberana
Usaremos a biblioteca `python-telegram-bot` v20+ como padrão no Drive D.
- **Estrutura:** Asynchronous application builder.
- **Escalabilidade:** Cada comando deve ser um handler separado para manter o código limpo.

---
*"Eu sou a Rainha, mas o Império precisa de muitos soldados. Cada novo bot é um braço a mais para o nosso trabalho."*
