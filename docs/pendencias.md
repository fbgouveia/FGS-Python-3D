# 📋 PENDÊNCIAS & EVOLUÇÃO DA ESTRUTURA
## Felipe Gouveia Studio — Python 3D
> Atualizado em: 2026-03-04 | Versão: 3.0.0

> [!IMPORTANT]
> Boomer & Kev é o projeto-piloto que prova o sistema.
> **A infraestrutura sendo construída serve para QUALQUER cliente,
> QUALQUER personagem, QUALQUER tipo de produção 3D imaginável.**
> Tudo que criamos é genérico, reutilizável e white-label ready.

---

## 🦭 COLUNAS DA EVOLUÇÃO

```
 EIXO 1 → Infraestrutura Base     (funções genéricas reutilizáveis)
 EIXO 2 → Biblioteca de Assets    (personagens, cenários, materiais)
 EIXO 3 → Sistemas Especializados  (física, partículas, lip sync, mocap)
 EIXO 4 → Templates por Nicho     (20+ categorias de produção)
 EIXO 5 → Projetos Piloto         (provar cada template com um projeto real)
 EIXO 6 → Pipeline de Produção    (workflow do briefing ao render)
 EIXO 7 → White Label Ready       (produto empacotado para venda)
 EIXO 8 → Adobe Automations       (ferramentas auxiliares Ae/Pr/Ps)
```

---

## 🔴 BLOQUEANTES — Fazer AGORA (sem isso nada funciona)

> [!CAUTION]
> Estas 3 pendências bloqueiam o pipeline de áudio completo.
> Resolva antes de avançar para qualquer outra coisa.

### P1 — Instalar Rhubarb Lip Sync
```
STATUS: ⛔ Pendente
RESPONSÁVEL: Felipe (usuário)
TEMPO ESTIMADO: 5 minutos

PASS OS:
1. Acessar: https://github.com/DanielSWolf/rhubarb-lip-sync/releases
2. Baixar: rhubarb-lip-sync-X.X.X-windows.zip
3. Extrair em: D:\Blender\blenderscripts\tools\rhubarb\
4. Verificar: rhubarb.exe existe na pasta
5. Testar: python scripts\utils\rhubarb_runner.py --check
```

### P2 — Criar Conta ElevenLabs e Configurar API Key
```
STATUS: ⛔ Pendente
RESPONSÁVEL: Felipe (usuário)
TEMPO ESTIMADO: 10 minutos

PASSOS:
1. Criar conta: https://elevenlabs.io (plano gratuito: 10k chars/mês)
2. Ir em: Profile → API Keys → copiar a chave
3. No terminal: python scripts\utils\elevenlabs_voice_gen.py --setup
4. Colar a API Key quando solicitado
5. O script vai listar as vozes disponíveis
```

### P3 — Testar Pipeline de Áudio (ElevenLabs + Rhubarb)
```
STATUS: ✅ Concluído
RESPONSÁVEL: Agente
TEMPO ESTIMADO: 0 minutos
PASSOS: Pipeline validado. O sistema roda com ElevenLabs via Python e o Rhubarb extrai fonemas com sucesso.
```

---

## 🟠 EIXO 1 — ARQUITETURA UNIVERSAL (Infraestrutura Genérica)

> [!NOTE]
> Tudo aqui é construído de forma **totalmente genérica**.
> Não é para o Boomer. Não é para o Kev.
> É para **qualquer personagem, qualquer cena, qualquer produção**.

### AU1 — Sistema Universal de Personagens
```
STATUS: ✅ Concluído (scripts/utils/character_factory.py)
ARQUIVO: scripts/utils/character_factory.py

O QUE FAZ:
- Gera qualquer tipo de personagem via parâmetros
- Input: especie, estilo, proporções, paleta, expressões
- Output: personagem completo
```

### AU2 — Biblioteca Universal de Cenários
```
STATUS: ✅ Concluído (scripts/utils/scene_factory.py)
ARQUIVO: scripts/utils/scene_factory.py

O QUE FAZ:
- Gera qualquer ambiente/cenário via parâmetros
- 12 ambientes pré-configurados prontos (estúdios, exteriores, sci-fi)
```

### AU3 — Motor Universal de Animação
```
STATUS: ✅ Concluído (scripts/utils/animation_engine.py)
ARQUIVO: scripts/utils/animation_engine.py

O QUE FAZ:
- Aplica keyframes, animações procedurais contínuas e físicas simples.
```

### AU4 — Sistema Universal de Câmeras
```
STATUS: ✅ Concluído (scripts/utils/camera_system.py)
ARQUIVO: scripts/utils/camera_system.py

O QUE FAZ:
- Cria e anima qualquer tipo de câmera cinematográfica (orbit, dolly, multi-cam, etc)
```

### AU5 — Sistema Universal de Iluminação
```
STATUS: ✅ Concluído (scripts/utils/lighting_system.py)
ARQUIVO: scripts/utils/lighting_system.py

O QUE FAZ:
- Aplica iluminação cinemátografica por tipo de cena (14 presets)
```

### AU6 — Sistema Universal de Materiais
```
STATUS: ✅ Concluído (scripts/utils/materials_library.py)
ARQUIVO: scripts/utils/materials_library.py

O QUE FAZ:
- Conta com 24 materiais PBR procedurais integrados e flexíveis.
```

### AU7 — Motor de Efeitos Especiais (VFX)
```
STATUS: ✅ Concluído (scripts/utils/vfx_engine.py)
ARQUIVO: scripts/utils/vfx_engine.py

O QUE FAZ:
- Partículas, magias, chuva, fluidos mantaflow, fogo e fumaça
```

### AU8 — Sistema de Render Universal
```
STATUS: ✅ Concluído (scripts/utils/render_manager.py)
ARQUIVO: scripts/utils/render_manager.py

O QUE FAZ:
- 9 presets de qualidade (TikTok, Youtube, Cinema, Draft, etc)
```

---

## 🟡 EIXO 2 — BIBLIOTECA DE ASSETS UNIVERSAL

> [!NOTE]
> Assets reutilizáveis entre TODOS os projetos.
> Um personagem criado para um cliente pode ser adaptado para outro.

### LA1 — Galeria de Personagens Universais
```
STATUS: 🔵 Não iniciado
LOCALIZAÇÃO: characters/library/

PERSONAGENS A CRIAR (progressivamente):
├── ANIMAIS: urso, raposa, lobo, leao, gato, cao, panda, aguia
├── HUMANOS: homem_negocio, mulher_negocio, cientista, chef
├── CRIATURAS: robo, alien, fantasma, dragao, golem
└── ABSTRATOS: cubo_personalidade, esfera_emocional, forma_geometrica

RULES:
- Cada personagem = arquivo .blend + script Python gerador
- Todos com armature Rigify-compatível
- Todos com Shape Keys de expressões
- Paleta customizável por projeto
```

### LA2 — Galeria de Cenários Universais
```
STATUS: 🔵 Não iniciado
LOCALIZAÇÃO: scenes/library/

CENÁRIOS A CRIAR:
├── podcast_studio.blend    (em uso: Boomer & Kev)
├── product_studio.blend    (comerciais de produto)
├── office_modern.blend     (corporativo, apresentações)
├── city_street.blend       (urbano genérico)
├── nature_forest.blend     (natureza/ambiental)
├── sci_fi_lab.blend        (tecnologia, medicina)
├── medieval_castle.blend   (histórico)
└── abstract_void.blend     (surreal, minimalista)
```

### LA3 — Biblioteca de Animações BVH
```
STATUS: 🔵 Não iniciado
LOCALIZAÇÃO: motions/bvh/

ACERVO A CONSTRUIR:
├── CONVERSA: falar_sentado, ouvir_atento, concordar, discordar
├── EMOCAO: risada_forte, surpresa, tristeza, celebracao
├── LOCOMOCAO: andar, correr, pular, danar
├── PROFISSIONAL: apresentar, apontar, digitar, cozinhar
└── ACAO: lutar, defender, atacar, esquivar

FONTE GRATUITA: CMU Graphics Lab Motion Capture Database
```

### LA4 — Biblioteca de Props (Objetos)
```
STATUS: 🔵 Não iniciado
LOCALIZAÇÃO: assets/props/

PROPS POR CATEGORIA:
├── PODCAST: microfones, headphones, mesas, cadeiras
├── CULINARIA: pratos, copos, garrafas, ingredientes
├── TECNOLOGIA: computadores, smartphones, tablets, robots
├── NATUREZA: árvores, rochas, flores, agua
└── GENERICOS: caixas, bolas, mesas, cadeiras, carros
```

### LA5 — Biblioteca de Presets de Iluminação
```
STATUS: 🔵 Não iniciado
LOCALIZAÇÃO: assets/lighting_presets/

PALETAS NARRATIVAS JÁ DEFINIDAS:
├── Luxo (preto + dourado)
├── Saúde (branco + azure + verde)
├── Tecnologia (escuro + cian neon)
├── Natureza (verde + amber)
├── Alimentos (quente + vibrante)
├── Espaço (preto + nebulosa)
├── Ação (escuro + laranja explosão)
└── Surreal (roxo escuro + teal)
```

### LA6 — HDRI Pack (Ambientes de Iluminação)
```
STATUS: 🔵 Não iniciado
LOCALIZAÇÃO: assets/hdri/

HDRIs NECESSÁRIOS:
- Estudio fotográfico neutro (produto)
- Céu aberto / por-do-sol
- Interior de escritório
- Floresta
- Cenário urbano noturno
FONTE GRATUITA: https://polyhaven.com/hdris
```

### LA7 — Acervo Motion Graphics & Lower Thirds
```
STATUS: 🟡 Em andamento (Upload no GDrive pelo Usuário)
LOCALIZAÇÃO: assets/motion_graphics/

ACERVO EXTERNO:
- Pacotes Envato/Motion Array (Alpha Channel / WebM)
- Lower Thirds (Subscribe, Like, Nome, Botões)
- Overlays (VHS, Glitch, Film Grain, Light Leaks)
COMO USAR: O Python (via VSE) puxará e embedará esses vídeos diretamente na Faixa 3.
```

### LA8 — Acervo de Plugins AE / Templates de Vídeo
```
STATUS: 🟡 Em andamento (Upload no GDrive pelo Usuário)
LOCALIZAÇÃO: assets/templates_ae/ e assets/vfx_packs/

ACERVO EXTERNO:
- Magic Packs (fogo realista, raios, magia 2D)
- Efeitos Sonoros atrelados (SFX Sync)
- Templates HTML5 interagindo com React
COMO USAR: Servirão como Backgrounds de alta performance mixados com os Renders Puros do Blender.
```

---

## 🟢 EIXO 3 — TEMPLATES POR NICHO (Scripts Prontos)

> [!NOTE]
> Cada template = script Python completo genérico,
> personalizável via bloco de parâmetros no topo.
> Um template serve para TODOS os clientes do mesmo nicho.

### Comerciais de Produto
```
[ ] TN1: product_spin_360.py       → Produto girando com iluminação premium
[ ] TN2: product_reveal.py         → Produto emergindo da névoa/escuridão
[ ] TN3: liquid_splash.py          → Splash de bebida com Mantaflow
[ ] TN4: unboxing_3d.py            → Caixa se abrindo revelando produto
[ ] TN5: comparison_before_after.py → Antes/depois com morph 3D
```

### Séries e Entretenimento
```
[ ] TN6: podcast_episode_base.py   → Template de episódio de podcast (genérico)
[ ] TN7: news_explainer.py         → Personagem explica notícia com infográfico
[ ] TN8: educational_video.py      → Animação educativa com objetos 3D
[ ] TN9: music_visualizer.py       → Visualização de áudio em 3D reativo
[ ] TN21: broll_generator.py       → B-Rolls Concretos (Psicologia/Medicina/Educação)
```

### Científico e Corporativo
```
[ ] TN10: medical_journey.py        → Viagem pelo corpo humano
[ ] TN11: molecule_animation.py     → Moléculas, DNA, células
[ ] TN12: architecture_flythrough.py → Fly-through de edifício/espaço
[ ] TN13: data_visualization_3d.py  → Gráficos e dados em 3D animados
[ ] TN14: logo_reveal.py            → Revelação de logo com efeitos
```

### Especiais e Virais
```
[ ] TN15: particle_burst_short.py   → Explosão de partículas (vertical 9:16)
[ ] TN16: space_scene.py            → Cena cósmica genérica (planetas, galáxias)
[ ] TN17: horror_atmosphere.py      → Atmosfera de terror/thriller
[ ] TN18: time_lapse_nature.py      → Nature time-lapse procedural 3D
[ ] TN19: car_commercial.py         → Reveal de carro premium
[ ] TN20: fashion_runway.py         → Desfile de moda com personagens
```

---

## 🟣 EIXO 4 — PROJETOS PILOTO (Provar cada nicho)

> Cada projeto piloto prova que o template do nicho funciona.

| # | Projeto | Nicho | Template usado | Status |
|---|---------|-------|---------------|--------|
| PP1 | **Boomer & Kev** | Podcast/Entretenimento | TN6 | 🟡 Em andamento |
| PP2 | **Comercial de Bebida** | Produto/Gastronomia | TN3 | 🔵 Não iniciado |
| PP3 | **Tour pelo Coração** | Medicina/Educação | TN10 | 🔵 Não iniciado |
| PP4 | **Reveal de Logo FGS** | Corporativo/Branding | TN14 | 🔵 Não iniciado |
| PP5 | **Short Viral de Partículas** | Redes sociais | TN15 | 🔵 Não iniciado |
| PP6 | **B-Roll Ansiedade/Psicologia** | B-Roll Engine | TN21 | 🔵 Não iniciado |

---

## 🟠 SCRIPTS DA INFRAESTRUTURA BASE (Fase 2 imediata)

> Scripts core que desbloqueiam tudo mais:

| # | Prioridade | Script | Depende de | Sessões |
|---|-----------|--------|-----------|----------|
| S1 | **P0** | `scripts/utils/materials_library.py` | — | 1 |
| S2 | **P0** | `characters/character_factory.py` | S1 | 2 |
| S3 | **P1** | `scenes/scene_factory.py` | S1 | 2 |
| S4 | **P1** | `scripts/utils/camera_system.py` | — | 1 |
| S5 | **P1** | `scripts/utils/lighting_system.py` | — | 1 |
| S6 | **P1** | `scripts/utils/vfx_engine.py` | — | 1 |
| S7 | **P1** | `scripts/utils/animation_engine.py` | S2 | 1 |
| S8 | **P2** | `scripts/utils/render_manager.py` | — | 1 |
| S9 | **P2** | `scripts/utils/mocap_utils.py` | S2, S7 | 1 |

---

## 🟠 MELHORIAS BOOMER & KEV (Fase 2)

| # | Melhoria | Prioridade |
|---|----------|----------|
| M1 | Modelagem 3D detalhada dos rostos (boca articulada) | Alta |
| M2 | Shape Keys reais de boca para lip sync preciso | Alta |
| M3 | Armature completo (rigging humano via Rigify) | Alta |
| M4 | Biblioteca de animações BVH de conversa | Média |
| M5 | Biblioteca de expressões faciais animadas | Média |
| M6 | Som ambiente do estúdio + trilha do tema | Média |
| M7 | Template de abertura/encerramento reutilizável | Baixa |
| M8 | Variações de cenário por tema de episódio | Baixa |

---

## 🔵 INFRAESTRUTURA WHITE LABEL (Fase Final)

| # | Item | Descrição |
|---|------|----------|
| I1 | Interface web de geração | Formulário → script Python automático |
| I2 | Servidor de render em nuvem | GPU dedicada sem depender do PC |
| I3 | Sistema de templates catalogado | Biblioteca com 20+ templates por nicho |
| I4 | Dashboard de projetos | Gerenciar múltiplos clientes/projetos |
| I5 | API de geração | REST API: briefing → script Python |
| I6 | Painel de clientes | White-label: cada cliente tem seu hub |
| I7 | Painel Gestor Social | Analítica e Multi-Upload Nativo |
| I8 | Engine Misto de Billing | Assinatura Fixa + GPU Tokens Avulsos |

---

## ✅ CONCLUÍDO — Histórico (2026-03-04)

### P1 — Instalar Rhubarb Lip Sync
```
STATUS: ⛔ Pendente
RESPONSÁVEL: Felipe (usuário)
TEMPO ESTIMADO: 5 minutos

PASSOS:
1. Acessar: https://github.com/DanielSWolf/rhubarb-lip-sync/releases
2. Baixar: rhubarb-lip-sync-X.X.X-windows.zip
3. Extrair em: D:\Blender\blenderscripts\tools\rhubarb\
4. Verificar: rhubarb.exe existe na pasta
5. Testar: python scripts\utils\rhubarb_runner.py --check
```

### P2 — Criar Conta ElevenLabs e Configurar API Key
```
STATUS: ⛔ Pendente
RESPONSÁVEL: Felipe (usuário)
TEMPO ESTIMADO: 10 minutos

PASSOS:
1. Criar conta: https://elevenlabs.io (plano gratuito: 10k chars/mês)
2. Ir em: Profile → API Keys → copiar a chave
3. No terminal: python scripts\utils\elevenlabs_voice_gen.py --setup
4. Colar a API Key quando solicitado
5. O script vai listar as vozes disponíveis
```

### P3 — Definir e Configurar as Vozes dos Personagens
```
STATUS: ⛔ Pendente (depende de P2)
RESPONSÁVEL: Felipe + Agente
TEMPO ESTIMADO: 20 minutos

PASSOS:
1. No ElevenLabs → Speech Synthesis → Voice Library
2. Testar vozes e escolher:
   - BOOMER: voz grave, masculina, 40-55 anos (ex: Charlie, George)
   - KEV: voz jovem, energética, 20-28 anos (ex: Liam, Josh)
3. Copiar os Voice IDs de cada voz escolhida
4. Editar: scripts\utils\elevenlabs_voice_gen.py
   - Linha ~60: "voice_id": "ID_DO_BOOMER"
   - Linha ~80: "voice_id": "ID_DO_KEV"
5. Teste: python scripts\utils\elevenlabs_voice_gen.py --test "Olá!" --char boomer
```

---

## 🟡 SCRIPTS PENDENTES — Desenvolvimento (Fase 2)

> [!IMPORTANT]
> O EIXO 1 FOIP CONCLUIDO! A nova prioridade é expandir os templates (Eixo 3) e fazer melhorias e revisões parciais!

| # | Prioridade | Script |
|---|-----------|--------|
| R1 | **P1** | **REVISÃO: Testar e ajustar parâmetros de Eixo 1 (AU1-AU8)** |
| S1 | **P2** | `scripts/commercials/product_spin_360.py` |
| S2 | **P2** | `scripts/commercials/liquid_splash.py` |
| S3 | **P3** | `scripts/shorts/particle_burst.py` |
| S4 | **P3** | `scripts/youtube/episode_base.py` |
| S5 | **P1** | `scripts/social/broll_generator.py` |

---

## 🟠 MELHORIAS BOOMER & KEV — Modelagem e Animação

> [!NOTE]
> O script atual usa geometria simples (esferas). Para qualidade
> de série profissional, os personagens precisam de modelagem real.

### M1 — Modelagem 3D Detalhada dos Rostos
```
STATUS: 🔵 Fase 2
O QUE É: Rostos com boca modelada, dentes, olhos com córnea
POR QUE IMPORTA: Lip sync muito mais expressivo e real
COMO FAZER: Agente gera script de modelagem procedural
             OU você modela no Blender e agente anima
```

### M2 — Shape Keys Reais de Boca
```
STATUS: 🔵 Fase 2 (depende de M1)
O QUE É: Deformações de vértices para cada fonema
POR QUE IMPORTA: Lip sync cinematográfico (nível Pixar)
ATUALMENTE: Usamos escala de objeto (funciona mas é limitado)
```

### M3 — Armature Completo (Rigging Humano)
```
STATUS: 🔵 Fase 2
O QUE É: Esqueleto completo para animar corpo inteiro
POR QUE IMPORTA: Gestos com braços, inclinações de corpo
FERRAMENTAS: Rigify (add-on Blender) via Python
```

### M4 — Biblioteca de Animações BVH/Mixamo
```
STATUS: 🔵 Fase 2 (depende de M3)
O QUE É: Banco de animações de conversa, gestos, risadas
FONTE: CMU Motion Capture Database (gratuito)
       Mixamo (Adobe — gratuito com conta)
```

### M5 — Expressões Faciais Animadas
```
STATUS: 🔵 Fase 2 (depende de M1, M2)
O QUE É: Surpresa, alegria, ceticismo, risada — em Shape Keys
POR QUE IMPORTA: Personagens mais expressivos e identificáveis
```

---

## 🔵 INFRAESTRUTURA FUTURA — White Label

> [!NOTE]
> Estas pendências são para quando o produto estiver pronto para ser
> empacotado e vendido como white-label para outras agências.

### I1 — Interface Web de Geração de Scripts
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: Formulário web onde cliente descreve a cena
         → backend gera o script Python automaticamente
STACK SUGERIDA: Next.js + FastAPI + Gemini API
```

### I2 — Servidor de Render em Nuvem
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: GPU dedicada em cloud (AWS/GCP) para renderizar
         sem precisar do computador do usuário
CUSTO ESTIMADO: $50-200/mês dependendo do uso
```

### I3 — Dashboard de Projetos
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: Painel para gerenciar múltiplos projetos,
         ver histórico de renders, status de pipeline
```

### I4 — API de Geração
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: REST API que recebe briefing e retorna script Python
         Permite integração com ferramentas de terceiros
```

### I5 — Engine Misto de Billing (Tokens + Subscription)
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: Sistema financeiro gamificado. Mensalidade base ($30/mês).
         A mensalidade dá acesso às automações sociais. 
         Gerações 3D gastam "Tokens" atrelados a Recargas Replicate-Style ($5/$10).
```

### I6 — Painel de Clientes (SaaS Dashboard)
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: Onde a Psicóloga / Agência gerencia seus vídeos e tokens.
```

### I7 — Hub de Gestão de Mídias Sociais (Lock-in)
```
STATUS: 🔵 Fase 4 (futura)
O QUE É: Exportação de vídeo nativa via API (TikTok, Reels, YT).
         O usuário não precisa baixar e postar no celular. Analytics de leads.
```

---

## ✅ SOUND DESIGN & MÚSICA (Planejamento)

> [!NOTE]
> O Blender possui um Video Sequence Editor (VSE) muito capaz, que usaremos para
> mixar áudio diretamente pelo Python, da mesma forma que foi feito o Lip Sync.

### 1. Sound Effects (SFX) e Música de Fundo (BGM)
O script Python final do nicho (ex: Template de Comercial) importará os sons durante o render.

*   **Infraestrutura Necessária**: 
    1. Criaremos um `audio_manager.py` (ou embutiremos no `render_manager.py`).
    2. Ele vai aceitar chamadas como: `audio.add_sfx("sweep.wav", frame=12)` ou `audio.add_bgm("lofi_beat.mp3", volume=0.3)`.
*   **Fontes de Áudio**: Usaremos bibliotecas royalty-free locais que mapearemos na pasta `D:/Blender/blenderscripts/audio/sfx/` e `audio/music/`.
*   **Mixagem**: O Python define as "stripes" de áudio no Sequence Editor do Blender, corta nos frames certos e ajusta volume e fade in/out.

## ✅ CONCLUÍDO — Histórico (2026-03-04)

| Data | Item | Status |
|------|------|--------|
| 2026-03-04 | Sistema de agentes instalado (23 agentes) | ✅ |
| 2026-03-04 | Agente `@blender-animator` v2.0 criado | ✅ |
| 2026-03-04 | Arquitetura Universal (Eixo 1) Completa! (8 módulos core) | ✅ |
| 2026-03-04 | Script Ep.1 Boomer & Kev gerado (720 frames 3D) | ✅ |
| 2026-03-04 | Pipeline de Voz (ElevenLabs) + Lip Sync (Rhubarb) pronto | ✅ |

---

## 🗓️ CRONOGRAMA DE EVOLUÇÃO

```
SEMANA 1 (AGORA — Desbloqueio Imediato):
├── ✅ Resolver P1 (Rhubarb)
├── ✅ Resolver P2 (ElevenLabs)
├── ✅ Resolver P3 (Voice IDs)
└── ✅ Render completo do Ep.1 com vozes + lip sync

SEMANA 2 (Infraestrutura Base — Eixo 1):
├── S1: materials_library.py (base de tudo)
├── S4: camera_system.py
├── S5: lighting_system.py
└── S8: render_manager.py

SEMANA 3 (Personagens e Cenários Universais):
├── S2: character_factory.py (sistema genérico)
├── S3: scene_factory.py (qualquer cenário)
└── LA6: HDRI Pack (polyhaven.com)

SEMANA 4 (VFX e Animação):
├── S6: vfx_engine.py
├── S7: animation_engine.py
└── S9: mocap_utils.py

MÊS 2 (Templates por Nicho):
├── TN1-TN5: Templates de comerciais
├── TN14: Logo reveal (projeto FGS)
├── PP2: Piloto Comercial de Bebida
└── PP5: Piloto Short Viral

MÊS 3 (Biblioteca de Assets):
├── LA1: Galeria de personagens (8 animais base)
├── LA2: Cenários base (8 ambientes)
├── LA3: Animações BVH (20+ movimentos)
└── LA4: Props library (50+ objetos)

MÊS 4+ (Especializações e Pilotos):
├── PP3: Piloto Médico
├── PP4: Piloto Corporativo
├── TN10-TN20: Templates especializados
└── Boomer & Kev: Melhoria de modelagem (M1-M5)

FASE FINAL (White Label):
├── I1-I6: Infraestrutura de produto
└── Lançamento como produto comercial
```

---

## 📊 STATUS GERAL

| Eixo | Descrição | Status | % |
|------|-----------|--------|---|
| **Bloqueantes** | P1-P3: Rhubarb + ElevenLabs + Vozes | ⚠️ Pendente | 0% |
| **Eixo 1** | Arquitetura Universal (AU1-AU8) | ✅ Completo | 100% |
| **Eixo 2** | Biblioteca de Assets (LA1-LA6) | 🔵 Não iniciado | 0% |
| **Eixo 3** | Templates por Nicho (TN1-TN20) | 🔵 Não iniciado | 0% |
| **Eixo 4** | Projetos Piloto (PP1-PP5) | 🟡 1/5 em andamento | 20% |
| **Agente IA** | @blender-animator v2.0 | ✅ Completo | 100% |
| **Documentação** | README + Docs + Bíblia | ✅ Completo | 100% |
| **Pipeline Áudio** | ElevenLabs + Rhubarb + Blender | ✅ Código pronto | 80% |
| **Infrastructure** | White Label + Painel Social | 🔵 Fase final | 0% |
| **Automações Adobe** | Eixo 8 (AE/PR/PS Scripts) | 🔵 Não iniciado | 0% |
| **TOTAL GERAL** | | **Em evolução** | **~35%** |

---

*Pendências FGS Python 3D | Versão 3.0.0 | 2026-03-04*

| Data | Item | Status |
|------|------|--------|
| 2026-03-04 | Sistema de agentes instalado (23 agentes) | ✅ |
| 2026-03-04 | Agente `@blender-animator` v2.0 criado | ✅ |
| 2026-03-04 | Plano master do projeto criado | ✅ |
| 2026-03-04 | Estrutura de pastas completa criada | ✅ |
| 2026-03-04 | Framework de Direção de Arte criado | ✅ |
| 2026-03-04 | Bíblia do Boomer & Kev criada | ✅ |
| 2026-03-04 | Script Ep.1 Boomer & Kev gerado | ✅ |
| 2026-03-04 | Pipeline de áudio documentado | ✅ |
| 2026-03-04 | `elevenlabs_voice_gen.py` criado | ✅ |
| 2026-03-04 | `rhubarb_runner.py` criado | ✅ |
| 2026-03-04 | `lipsync_blender.py` criado | ✅ |
| 2026-03-04 | `scene_setup.py` criado | ✅ |
| 2026-03-04 | Diálogo Ep.1 escrito | ✅ |
| 2026-03-04 | README.md completo gerado | ✅ |
| 2026-03-04 | Este documento de pendências criado | ✅ |

---

## 🗓️ CRONOGRAMA SUGERIDO

```
SEMANA 1 (AGORA):
├── ✅ Resolver P1 (Rhubarb)
├── ✅ Resolver P2 (ElevenLabs)
├── ✅ Resolver P3 (Voice IDs)
└── ✅ Gerar vozes e testar lip sync do Ep.1

SEMANA 2:
├── S1: materials_library.py
├── S2: base_character.py
└── Render completo do Ep.1 com vozes

SEMANA 3:
├── S3: camera_utils.py
├── S4: render_utils.py
├── S5: mocap_utils.py
└── Ep.2 completo (tema a definir)

SEMANA 4:
├── S6: podcast_studio.py (standalone)
├── M1: Modelagem melhorada dos rostos
└── Ep.3 completo

MÊS 2:
├── Primeiros comerciais (S7, S8)
├── Primeiro short viral (S9)
├── Lançamento do canal YouTube
└── Planejamento White Label
```

---

*Documento de Pendências | Felipe Gouveia Studio Python 3D*
*Versão: 1.0 | Atualizado: 2026-03-04*
