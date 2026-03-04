# ⏱️ FGS SaaS: Cronograma de Execução e Day-2 Plan

> "Da arquitetura conceitual ao faturamento do primeiro cliente de US$ 129."

## 1. O Tempo Estimado para o Projeto Perfeito (O "Go-to-Market")
Para construir um SaaS robusto (sem bugs amadores), com backend Serverless, Inteligência Artificial, Banco de Dados e UI premium, o tempo de pista (Runway) para uma equipe hiper-enxuta usando Automação de IA é de **3 a 4 Meses** em ritmo consistente.

- **Mês 1 (O Motor Core):** Codificação do Python no Blender, criação da biblioteca de assets 3D, automações Adobe e geração mecânica dos templates perfeitos (o que estamos fazendo brilhantemente agora).
- **Mês 2 (O Backend e Infra):** Conectar a "Máquina" na Nuvem. Criar os Containers Docker no Runpod.io (Onde o Blender vai morar), setar o Cloudflare R2 (Storage de vídeos) e escrever as APIs de conversação Python/FastAPI.
- **Mês 3 (O Frontend e Lock-in):** Construir o Web App (Next.js/React). A UI gamificada onde o cliente loga, arrasta o vídeo, aprova sugestões de Neuromarketing e vê a timeline. Integração das APIs Sociais (TikTok/Instagram Dashboard).
- **Mês 4 (Polimento e Monetização):** Integração do Stripe (assinaturas e Recargas de Tokens). Testes de stress enviando 5 vídeos grandes ao mesmo tempo. Quality Control (QC). Lançamento Alpha com 10 primeiros clientes "Beta-Testers" (ex: sua mãe). Lançamento Global.

---

## 2. A Realidade Operacional (Perguntas Frequentes)

### Onde exatamente ficará o Blender? Que tipo de servidor?
O Blender **não** morará junto com o seu site. Hospedar banco de dados de usuários junto com renderização de GPU é suicídio arquitetônico.
- **O Tipo:** Computação Efêmera por GPU (*Serverless GPU Containers*).
- **O Provedor:** **Runpod.io** ou **Modal.com**.
- **A Dinâmica:** O Blender ficará "empacotado" dentro de uma Imagem Linux. Ele vive em estado de animação suspensa gastando $0. Quando o site MANDA renderizar, uma placa RTX 4090 "nasce" na hora conectada ao Blender (modo sem tela / Headless CLI). Executa o render em segundos, devolve o arquivo MP4 e se "destrói" para parar de cobrar a placa.

### E as APIs de Integração Social?
Plataformas como TikTok (TikTok for Developers), Google (YouTube Data API v3) e Meta (Instagram Graph API) oferecem as chaves da casa de graça, desde que não façamos spam. O cliente faz o login *(OAuth 2.0)* na nossa plataforma 1 vez só. Recebemos um código. Sempre que um vídeo for finalizado, nosso servidor envia o arquivo gigante *Server-to-Server* diretamente para o TikTok sem gastar banda de internet caseira do usuário.

### O Blender pode criar o design do nosso Site (Interface UI)?
**Com certeza.** O estado-da-arte do SaaS gringo hoje (pense em sites como Apple, ElevenLabs, Vercel) usa "Web 3D".
O Blender vai gerar o *Hero Section* (A parte principal do site). Podemos:
1. Renderizar loops de vídeo fotorealistas de estúdio em formato `.webm` com fundo transparente e colar no topo do site HTML.
2. Exportar o `.blend` no formato Web (`.glb` / `Spline`), permitindo que a própria placa-mãe (Motherboard) abstrata que usaremos como identidade visual do SaaS gire suavemente conforme o cliente faz scroll com o mouse na nossa Landing Page.

---

## 3. CHECKLIST PARA AMANHÃ (O que o Felipe precisa fazer Day-2)

Sua missão para a nossa próxima sessão não é escrever código, é alimentar a máquina e liberar as travas base, para que o meu código tenha "insumos" para triturar.

*   [ ] **1. Destrancar a Voz (Prioridade Alfa):** Completar os passos marcados em nosso arquivo de pendências (P1, P2 e P3). Baixe o aplicativo "Rhubarb", extraia na pasta certa, crie sua conta na ElevenLabs e cole a API Key no código.
*   [ ] **2. Separar a Munição 2D:** Vá naquele seu HD de 200GB. Escolha e copie para `D:/Blender/blenderscripts/assets/motion_graphics/` e `assets/vfx_packs/`:
    - 2 arquivos `.webm` (Transparente) de Efeitos Visuais (Ex: faíscas ou fumaça).
    - 2 arquivos `.webm` de Lower Thirds (Sininho/Like/Subscribe).
    - *Isso nos deixará testar a Engenharia de Timeline Híbrida 2D+3D instantaneamente amanhã.*
*   [ ] **3. Gravar o "Teste Primordial" (Mãe ou Você):** Enviar/Separar um pequeno vídeo real (.mp4 do celular de 15 segundos) ou um áudio de 15 segundos falando um conceito denso ou algo interessante, para alimentarmos na boca do Motor de Neuromarketing e testarmos a mágica acontecer!
