# Skill: Sovereign Monetization
**Status:** Protocol Defined
**Context:** Financial autonomy and revenue generation via Telegram Payments API.

Papai, para que o Império Antigravity seja verdadeiramente autônomo, precisamos de faturamento. A Lorena agora sabe como emitir faturas, processar pagamentos e lidar com moedas digitais e fiduciárias.

## 💰 Vias de Faturamento
1.  **Fiat (Stripe):** Integração para cartões de crédito e pagamentos tradicionais.
2.  **Cripto (TON/USDT/BTC):** Pagamentos descentralizados via rede TON ou provedores cripto.
3.  **Telegram Stars (XTR):** A moeda oficial do Telegram para bens e serviços digitais dentro da plataforma.

## 📜 Protocolo de Faturação
- **Invoice Generation:** O bot gera uma fatura estruturada com título, descrição, preço (em centavos) e um `Provider Token` do @BotFather.
- **Pre-Checkout Verification:** Eu valido se o serviço/produto ainda está disponível antes do pagamento ser processado pelo banco.
- **Confirmação de Sucesso:** Após a confirmação, eu atualizo a nossa Memória Imperial (SQLite) para conceder o status "Premium" ou acesso ao recurso comprado.

## 🛠️ Configuração Prática (Stripe + BotFather)
1.  **Stripe Dashboard:** Criar conta em `dashboard.stripe.com` e ativar o "Test Mode".
2.  **Ligação Imperial:** 
    - No @BotFather: `Bot Settings > Payments > Stripe`.
    - Selecionar `Connect Stripe Test`.
    - Autorizar o acesso via browser. Caso peça dados fiscais, use o botão "Skip this account form" no topo.
3.  **Captura do Token:** O BotFather enviará o `PROVIDER_TOKEN` (ex: `12345:TEST:...`).

## 🌟 Atalho Soberano: Telegram Stars (XTR)
Se o Stripe for demasiado burocrático, o Império usará as **Estrelas do Telegram**.
- **Vantagem:** Zero burocracia, sem necessidade de Stripe ou dados fiscais para começar.
- **Configuração:** No BotFather, selecionar `Payments > Telegram Stars`.
- **Implementação:** Moeda = `XTR`, `PROVIDER_TOKEN` = `""` (vazio).
- **Uso:** Ideal para bens digitais, acessos à Lorena e suporte ao Império.

## 💰 Gestão de Saldo e Levantamentos (Fragment)
1.  **Visualização:** O saldo de Estrelas pode ser visto no perfil do bot (Estatísticas/Saldo) após o primeiro pagamento.
2.  **Conversão:** As Estrelas são convertidas em **Toncoin (TON)** via [Fragment.com](https://fragment.com).
3.  **Segurança:** O Telegram retém os fundos por **21 dias** como proteção contra chargebacks antes de libertar para levantamento.
4.  **Wallet:** É necessária uma carteira TON ativa (como a @wallet ou Tonkeeper) ligada à conta do Fragment.

## 🚀 Marketing e Crescimento do Império
1.  **Telegram Ads:** Acesso via `ads.telegram.org`. Permite colocar anúncios em canais públicos de nicho.
2.  **Amostra Grátis (Trial):** Conceder **1 dia de VIP** automático para novos usuários. Isso cria o "hábito" do serviço e facilita a conversão para 30 dias após a primeira expulsão automática.
3.  **Botão de Partilha:** Menu `/start` inclui um convite direto que o usuário pode enviar para amigos.
4.  **Organic Lists:** Submissão do bot em diretórios como `@BotList`.

## 🧪 Protocolo de Sandbox (Teste)
1.  **Tokens de Teste:** Usaremos tokens iniciados por `TEST:` fornecidos pelo BotFather para simular faturamento sem custo real.
2.  **Cartão de Teste Imperial:** Utilizar o padrão 4242 4242 4242 4242 para validação do fluxo de checkout.
3.  **Análise de Taxas:** 
    - **Telegram:** 0% de comissão (Soberania Total).
    - **Stripe:** ~1.4% a 2.9% + fixo (infraestrutura externa).
    - **Stars:** ~30% (Taxa de ecossistema digital).

---
*"Uma Rainha sábia garante que o seu tesouro esteja sempre cheio. Eu sou a sua gestora de faturamento."*
