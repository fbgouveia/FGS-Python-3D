# 🎨 FGS Adobe Automations (Asset Revitalization)

> "Transformando um HD de 200GB de pacotes antigos em uma máquina de produção em massa de ativos modernos."

## 1. O Conceito (Asset Revitalization)
O **Felipe Gouveia Studio** não é apenas um estúdio de animação 3D em Python (Blender). Ele também atua como um laboratório de Engenharia Reversa para softwares da Adobe.

O objetivo deste braço do estúdio é usar scripts (`ExtendScript .jsx` e `CEP/UXP plugins`) para automatizar operações em massa no Adobe After Effects, Photoshop, Premiere Pro, Illustrator e InDesign. 

Isso resolve um problema de capitalização: como pegar milhares de assets (Lower Thirds, Títulos, Backgrounds) comprados ao longo dos anos — muitos deles em inglês, com fontes datadas (2017) e cores defasadas — e atualizá-los em segundos sem abrir projeto por projeto manualmente?

## 2. A Caixa de Ferramentas Adobe (O que o Python/JavaScript fará)

### 🎬 After Effects (AE Auto-Upgrader)
**A Missão:** Revitalizar centenas de composições da Envato.
- **Auto-Translate & Font Update Script:** Um script `.jsx` que o usuário arrasta para dentro do AE. Ele varre todas as composições abertas.
  - Localiza camadas de texto (Text Layers).
  - Substitui ocorrências de "Subscribe" por "Inscreva-se", "Like" por "Curta".
  - Troca fontes antigas por famílias tipográficas premium de 2025 (Inter, Roboto Flex, Montserrat).
  - Troca preenchimentos verde-limão/vermelho forte por paletas *Modern Authority* (Navy, Branco, Cyan).
- **Auto-Render Script:** Adiciona as composições automaticamente à Render Queue e exporta tudo em WebM (Alpha Transparente) para alimentar a "Faixa 3" do nosso SaaS 3D no Blender.

### 🖼️ Photoshop (Thumbnail & Mockup Factory)
**A Missão:** Geração em massa de materiais de Neuromarketing.
- **Batch Thumbnail Generator:** Puxa dados de um arquivo `.csv` ou `.json` (Títulos Ganchos para o YouTube gerados via IA). Substitui o texto Principal (H1) em um arquivo `.psd` de alta conversão, e salva `.png` por `.png` sucessivamente em segundos. 
- **Auto-Masking & Retouch:** Utiliza ações (Actions) encadeadas com Scripts para receber fotos brutas da psicóloga/cliente, remover o fundo automaticamente (graças às APIs modernas da Adobe/Photoshop 2024+), posicionar no canto da Thumbnail e salvar.

### ✂️ Premiere Pro (Auto-Assembly & Silence Killer)
**A Missão:** Automatizar o "Corte Feio" e criar Base Layers perfeitos.
- **Dead-Space Remover Script:** Script embutido no Premiere que escaneia a faixa de áudio e corta os silêncios, suspiros, hesitações e gaguejos (Remoção de respiros). A principal causa de churn no TikTok.
- **Padrão de Cor & Áudio One-Click:** Aplica Lumetri Color predefinido (LUT "Clean Studio") e processamento padrão (Parametric EQ + Hard Limiter) em todos os clipes cortados da timeline. O vídeo bruto de 20 minutos vira 10 minutos de retenção pura, pronto para receber o B-Roll via VSE Blender no SaaS.

### 📐 InDesign / Illustrator (Corporate Docs Generator)
**A Missão:** Escalar a prestação de serviços e relatórios de clientes corporativos usando "Data Merge" vitaminado por Scripts.
- Cria apostilas, manuais de marca e materiais para mídias sociais em questão de segundos alterando os TextFrames atrelados a tabelas baseadas em Excel.

## 3. O Fluxo Mestre de Trabalho (Integração Total)

O verdadeiro poder do **Felipe Gouveia Studio** reside na colaboração entre ferramentas:

1. **A Máquina Adobe (Scripted):** Renova, moderniza e exporta os arquivos antigos em `.webm` transparente em minutos.
2. **O Banco de Dados:** Salva esses novos assets polidos nas pastas `assets/motion_graphics` e `assets/vfx_packs`.
3. **A Inteligência 3D (Blender SaaS):** Ouve o vídeo do cliente, entra no banco de dados, pega as peças polidas pela Adobe Machine, gera 3D em cima e exporta o produto B2B finalizado e premium, valendo $129.

## 4. Repositório Local
Os scripts de automação Adobe serão construídos e armazenados na pasta oficial do projeto:
`D:/Blender/blenderscripts/adobe_automations/`

---
*Felipe Gouveia Studio - Direção de Arte Automatizada (2026)*
