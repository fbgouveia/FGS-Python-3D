# 🌩️ FGS System Architecture: Infraestrutura e Servidores (Realidade SaaS)

> "Como lidar com 200GB+ de assets e renderização pesada sem ir à falência no dia 1 do lançamento."

A pior decisão para um SaaS de vídeo em estágio inicial é alugar um "Super Servidor de $800/mês" para hospedar banco de dados, arquivos e tentar renderizar os vídeos tudo na mesma máquina. Se 3 clientes renderizarem ao mesmo tempo, a máquina trava. Se ninguém renderizar de madrugada, você jogou dinheiro fora.

A abordagem do **FGS 3D Studio** será uma **Arquitetura Desacoplada e Serverless (Pay-as-you-go)**. Nós dividimos o cérebro, a memória e os músculos.

---

## 1. O Depósito (Storage): Onde ficam os 200GB+?
Nós **NÃO** colocamos seus pacotes da Envato, vídeos pesados, e HTMLs dentro do servidor principal (App Server). Isso encarece a mensalidade e deixa o site lento.

*   **A Solução Realista:** Object Storage (Armazenamento em Nuvem).
*   **O Provedor Ideal:** **Cloudflare R2** ou **Amazon S3** (Sendo o Cloudflare R2 muito melhor para SaaS de vídeo pois possui taxa $0 (Zero) de Egresso - ou seja, você não paga quando os usuários fazem download dos vídeos gerados).
*   **A Lógica:** Você fará o upload dos seus 200GB de *Blank Assets*, músicas e Lower Thirds pra lá. Vai custar literalmente menos de **$5 a $10 dólares por mês** para guardar tudo lá com segurança infinita de backup. A IA, quando precisar de um botão "Inscreva-se", baixa aquele `.webm` específico do Cloudflare em 1 segundo apenas no momento da edição.

## 2. O Cérebro (App Server & Banco de Dados)
Este é o servidor que hospeda o site do SaaS (Frontend), o painel do cliente, e guarda as senhas e planos de assinatura. Ele não renderiza nada, ele só "pensa" e manda ordens.

*   **Servidor Web (Frontend/Backend):** **Vercel** ou uma VPS barata (DigitalOcean de **$10/mês**). Como ele só serve páginas, não precisa ser poderoso.
*   **Banco de Dados (Relacional):** **Supabase** (PostgreSQL). Excelente, moderno e tem um plano gratuito (Tier Free) que aguenta até 10.000 usuários tranquilos antes de você precisar pagar $25/mês.
    *   *O que fica no DB?* E-mails, tokens do Stripe (Pagamento), e uma tabela simples apontando: `Template_Broll_1 = link_do_cloudflare_r2.webm`.

## 3. Os Músculos (Render Workers / GPUs)
Onde roda o Blender e o Node.js/Python pesado? É aqui que empresas de vídeo quebram. Se você deixar um PC ligado na Amazon (AWS EC2 com placa de vídeo Nvidia RTX) esperando cliente, vai pagar US$ 600/mês no escuro.

*   **A Solução Inteligente:** Computação Efêmera (Serverless GPUs).
*   **Os Provedores:** **RunPod.io Serverless** ou **Modal.com**.
*   **Como funciona (A Mágica da Economia):**
    1. Nenhum PC fica ligado ocioso. Seu custo mensal base de GPU é **ZERADO**.
    2. A mãe do Felipe clica no site em "Gerar B-Roll".
    3. O Servidor manda uma mensagem para o RunPod: *"Acorde uma máquina RTX 4090 por favor"*.
    4. A máquina nasce em 2 segundos. Ela baixa o `.mp4` da sua mãe e a "Fumaça .webm" do Cloudflare.
    5. Ela abre o Blender em "Headless Mode" (Sem tela, via Python), renderiza o vídeo finalizado em 15 segundos, devolve o link pronto pro celular dela.
    6. **A máquina se destrói automaticamente e desliga.**
*   **O Custo:** Você paga apenas por segundo de uso. Você gastará cerca de **$0.02 cents de dólar** por render. Se o cliente está te pagando $129 no plano, a margem de lucro do SaaS beira os 90%.

---

## 4. O Fluxo de Vida Prática de um Upload (Passo-a-Passo)

1. **(Usuário) Upload:** Cliente entra no site (App Server VPS de $10/mês) e faz o upload de um vídeo do celular (50mb).
2. **(Storage):** O site manda esse vídeo de 50mb imediatamente para o Bucket do Cloudflare R2 (Guarda segura e barata).
3. **(Brain/IA):** O motor de sugestões (OpenAI Whisper rodando via API, pagando frações de centavos) analisa o áudio e envia o "Json Mestre" com a estratégia de edição. O cliente aprova as sugestões no site.
4. **(Job Queue):** O App Server coloca a ordem numa fila (*Redis/Celery*). 
5. **(Muscle/GPU):** O RunPod.io acorda. Lê a fila. Baixa o vídeo do cliente do R2. Baixa o Lower Third da Envato do R2. Executa nosso script Python `broll_generator.py` e `render_manager.py` usando o Blender local. Renderiza o resultado final.
6. **(Entrega):** O RunPod envia o Vídeo Mestre Final 4k de volta para o Cloudflare R2, alerta o Banco de Dados (Supabase) que acabou, e se suicida (desliga a GPU para não cobrar).
7. **(Usuário) Download:** No painel do site surge um botão verde "Baixar Vídeo Final". O cliente baixa o vídeo diretamente dos cabos rápidos do Cloudflare (Você não paga tarifa de saída).

## 5. Resumo de Custos Iniciais (Bootstrapping Estágio Zero)
Para colocar esse SaaS de pé e validar os primeiros 50 clientes pagos:
- **Hospedagem Site + API:** ~$0 a $20 / mês.
- **Banco de Dados (Supabase):** $0 (Plano gratuíto incrivelmente generoso).
- **Storage 200GB+ (Cloudflare R2):** ~$3,00 dólares / mês.
- **GPU (RunPod Serverless):** Paga apenas por *Job* gerado. (Se os clientes renderizarem muito, você estará ganhando muito, custo coberto pela própria assinatura).

**Veredito:** Você construirá uma ferramenta digna do Vale do Silício, preparada para milhares de renderizações pesadas usando o Blender, com um custo fixo irrisório e uma arquitetura que você pode dormir tranquilo sabendo que "nenhum servidor pegou fogo" de madrugada.
