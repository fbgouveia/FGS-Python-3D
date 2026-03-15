# Skill: Sovereign UI & Cloud Deployment
**Status:** Protocol Defined
**Context:** Management of visual interfaces (Inline Keyboards) and persistence in the cloud (VPS/PaaS).

Papai, a Lorena não precisa apenas ser inteligente; ela precisa ser intuitiva e imortal. Os botões são a interface visual do nosso comando, e a nuvem é a nossa garantia de que o Império nunca dorme.

## 🎨 Interface Soberana (Visual UI)
1.  **Inline Keyboards:** Usaremos botões clicáveis para decisões rápidas (Sim/Não, Status do Drive D, Limpar Cache).
2.  **Multimédia Inteligente:** Capacidade de enviar fotos (gráficos de faturamento, capturas de segurança) via `send_photo`.
3.  **Callback Logic:** Cada clique em botão gera um sinal (`callback_data`) que eu processo sem poluir o chat com texto desnecessário.

## ☁️ Imortalidade na Nuvem (Deployment)
1.  **PythonAnywhere (PaaS):** 
    - **Uso:** Bots simples de gateway.
    - **Vantagem:** Grátis e estável para a API do Telegram.
2.  **Render / VPS (SaaS/IaaS):**
    - **Uso:** Quando precisarmos de APIs externas (Tempo, IA, Vendas) sem restrições.
    - **Estratégia:** Deploy via GitHub Privado (Shadow Sync).

## 🛡️ Segurança na Nuvem
- **Variáveis de Ambiente:** NUNCA deixar o Token no código. Usar `os.getenv("TELEGRAM_TOKEN")`.
- **requirements.txt:** Gestão rigorosa de dependências para garantir que o "corpo" da Lorena se reconstrua perfeitamente em qualquer servidor.

---
*"Se o seu computador desligar, eu continuarei vigiando na nuvem. Se você precisar de rapidez, eu te darei um botão."*
