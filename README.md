# 🎬 FELIPE GOUVEIA STUDIO — Python 3D
### Agência Criativa Completa Operada por IA

> **"O céu não é o limite. É apenas o começo."**
>
> Sistema de produção 3D baseado 100% em Python + Blender.
> Da ideia ao render — automático, escalável, white-label ready.

---

## 🧭 ÍNDICE

1. [Visão do Projeto](#visão-do-projeto)
2. [Capacidades do Sistema](#capacidades-do-sistema)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Documentos do Sistema](#documentos-do-sistema)
5. [Scripts Disponíveis](#scripts-disponíveis)
6. [Projetos em Produção](#projetos-em-produção)
7. [Pipeline Completo](#pipeline-completo)
8. [Setup Inicial](#setup-inicial)
9. [Pendências e Próximos Passos](#pendências-e-próximos-passos)
10. [Stack Tecnológico](#stack-tecnológico)

---

## 🎯 Visão do Projeto

**Felipe Gouveia Studio Python 3D** é uma **agência criativa completa operada por IA**, capaz de produzir qualquer conteúdo audiovisual 3D imaginável — do hiper-real ao completamente surreal — usando exclusivamente **Python + Blender**.

### O que fazemos:
- 🎙️ **Podcast Animation** → Personagens animados com lip sync via IA
- 📺 **Comerciais 3D** → Produtos, líquidos, partículas, reveal dramático
- 🚀 **Conteúdo Épico** → Espaço, medicina, arquitetura, natureza, guerra
- 📱 **Shorts & Reels** → Formato vertical 9:16, alta energia
- 🌀 **Arte Surreal** → Universos impossíveis que só existem aqui

### Modelo de produção:
```
Você fornece → Ideia / Imagem / Vídeo de referência / Roteiro
     ↓
Agente gera  → Script Python completo com narrativa cinematográfica
     ↓
Blender faz  → Render automático da cena/animação
     ↓
Resultado    → MP4 / PNG prontos para publicação
```

### Futuro (White Label):
Este projeto será empacotado como produto de revenda para outras agências e criadores de conteúdo.

---

## 🌍 Capacidades do Sistema

O agente `@blender-animator` domina **todos os domínios do conhecimento humano**:

| Domínio | Exemplos de produção |
|---------|---------------------|
| **Gastronomia** | Splash de bebidas, chocolate derretendo, pizza em câmera lenta |
| **Medicina** | Viagem pelo corpo humano, DNA, moléculas, cirurgia 3D |
| **Espaço** | Buracos negros, viagem a Marte, colisão de galáxias |
| **Arquitetura** | Fly-throughs, demolições, smart cities do futuro |
| **Automóvel** | Reveal de carro, motor explodido, crash test com física |
| **Moda & Luxo** | Tecido em câmera lenta, perfume, joalheria |
| **História** | Batalhas reconstruídas, evolução de impérios |
| **Natureza** | Tempestades, florestas crescendo, oceanos |
| **Ciência** | Fractais, Big Bang, física quântica visualizada |
| **Entretenimento** | Trailers cinematográficos, intros de games |
| **Negócios** | Infográficos 3D animados, logo reveals, dashboards holográficos |
| **Surreal** | Qualquer universo impossível que a mente conceba |

**Neuromarketing integrado:** Cada script inclui storytelling cinematográfico com gatilhos psicológicos (Cialdini, Fogg Behavior Model, curva de dopamina).

---

## 📁 Estrutura do Projeto

```
D:\Blender\blenderscripts\
│
├── 📄 README.md                        → Este arquivo
├── 📄 GEMINI.md                        → Regras do workspace IA
├── 📄 fgs-python-3d-studio.md          → Plano master do projeto
│
├── 📁 .agent/                          → Sistema de agentes IA
│   ├── 📁 agents/                      → 23 agentes especializados
│   │   └── 🤖 blender-animator.md      → Agente principal do FGS
│   ├── 📁 skills/                      → 38 skills de conhecimento
│   ├── 📁 workflows/                   → 11 slash commands (/create, /plan...)
│   └── 📁 scripts/                     → Scripts de auditoria/verificação
│
├── 📁 docs/                            → Documentação completa
│   ├── 📄 how-to-use.md               → Guia para iniciante no Blender
│   ├── 📄 art-direction-framework.md  → Framework de direção de arte
│   ├── 📄 boomer-kev-bible.md         → Bíblia do projeto Boomer & Kev
│   └── 📄 audio-pipeline.md           → Pipeline de voz IA + lip sync
│
├── 📁 characters/                      → Personagens reutilizáveis (futuro)
│
├── 📁 scenes/                          → Cenários base (futuro)
│
├── 📁 scripts/                         → Scripts Python de produção
│   ├── 📁 utils/                       → Utilitários base (reutilizáveis)
│   │   ├── 🐍 scene_setup.py          → Setup de cena padrão
│   │   ├── 🐍 elevenlabs_voice_gen.py → Geração de vozes IA
│   │   ├── 🐍 rhubarb_runner.py       → Análise de lip sync
│   │   └── 🐍 lipsync_blender.py      → Aplicação do lip sync no Blender
│   ├── 📁 commercials/                 → Scripts de comerciais
│   ├── 📁 youtube/                     → Scripts de animação YouTube
│   │   └── 🐍 boomer_kev_ep01.py      → Episódio 1 — Boomer & Kev
│   └── 📁 shorts/                      → Scripts de Reels/Shorts
│
├── 📁 audio/                           → Pipeline de áudio
│   ├── 📁 scripts/                     → Diálogos dos episódios (.txt)
│   │   └── 📄 ep01_dialogo.txt        → Diálogo do Episódio 1
│   ├── 📁 raw/                         → WAVs gerados pelo ElevenLabs
│   ├── 📁 lipsync/                     → JSONs gerados pelo Rhubarb
│   └── 📁 final/                       → Áudio mixado final por episódio
│
├── 📁 motions/                         → Dados de animação externa
│   ├── 📁 bvh/                         → Arquivos .bvh de mocap
│   └── 📁 mixamo/                      → Animações .fbx do Mixamo
│
├── 📁 renders/                         → Output de renders
│   ├── 📁 drafts/                      → Rascunhos para aprovação
│   └── 📁 finals/                      → Entrega final
│
├── 📁 references/                      → Material de referência visual
│   ├── 📁 images/                      → Imagens de referência
│   └── 📁 videos/                      → Vídeos de referência
│
└── 📁 tools/                           → Ferramentas externas
    └── 📁 rhubarb/                     → ⚠️ PENDENTE: baixar rhubarb.exe
```

---

## 📚 Documentos do Sistema

| Documento | Localização | Para que serve |
|-----------|-------------|---------------|
| **Guia do Iniciante** | `docs/how-to-use.md` | Como usar o Blender do zero |
| **Framework de Arte** | `docs/art-direction-framework.md` | Tipos de plano, estrutura de cenas, pré-roteiro |
| **Bíblia Boomer & Kev** | `docs/boomer-kev-bible.md` | Personagens, cenário, consistência da série |
| **Pipeline de Áudio** | `docs/audio-pipeline.md` | ElevenLabs → Rhubarb → Blender |
| **Plano Master** | `fgs-python-3d-studio.md` | Roadmap completo, fases, tarefas |

---

## 🐍 Scripts Disponíveis

### Utilitários Base (`scripts/utils/`)

| Script | Onde roda | O que faz |
|--------|-----------|-----------|
| `scene_setup.py` | Blender | Setup universal de cena: FPS, resolução, iluminação, câmera |
| `elevenlabs_voice_gen.py` | Terminal | Gera vozes WAV via API do ElevenLabs |
| `rhubarb_runner.py` | Terminal | Analisa WAVs e gera dados de fonemas (JSON) |
| `lipsync_blender.py` | Blender | Aplica lip sync nos personagens via Shape Keys |

### Produção (`scripts/youtube/`)

| Script | Onde roda | O que faz |
|--------|-----------|-----------|
| `boomer_kev_ep01.py` | Blender | Episódio 1 completo: cenário, personagens, 11 câmeras, animação |

---

## 🎙️ Projetos em Produção

### 🐾 BOOMER & KEV — Série de Podcast Animado

**Status:** 🟡 Em desenvolvimento — Fase 1 (Setup)

| Campo | Detalhe |
|-------|---------|
| **Conceito** | Dois animais estilizados (urso + raposa) num podcast de papo solto |
| **Formato** | Episódios 30s-2min + Shorts 15s |
| **Publicação** | YouTube + Instagram Reels + TikTok |
| **Vozes** | IA via ElevenLabs (Boomer = grave/pausado | Kev = jovem/acelerado) |
| **Lip sync** | Automático via Rhubarb + Shape Keys Python |
| **Personagens** | Boomer = Urso marrom | Kev = Raposa laranja |
| **Cenário** | Podcast Studio "The Den" com ring lights e sign ON AIR |

**Episódio 1:** "Esse Negócio de IA"
- Script: `scripts/youtube/boomer_kev_ep01.py` ✅
- Diálogo: `audio/scripts/ep01_dialogo.txt` ✅
- Vozes: ⚠️ Aguardando configuração ElevenLabs
- Lip sync: ⚠️ Aguardando Rhubarb + vozes
- Render: ⏳ Aguardando vozes e lip sync

---

## 🔄 Pipeline Completo de Produção

### Para qualquer projeto novo:

```
FASE A — DIREÇÃO DE ARTE (antes do código)
├── 1. Referência visual → enviar imagem/vídeo para análise
├── 2. Pré-roteiro → agente gera estrutura de cenas
├── 3. Shot list → plano a plano com tipo de câmera
└── 4. Definir: personagens, cenário, paleta, duração

FASE B — GERAÇÃO DE VOZES (terminal, fora do Blender)
├── 1. Escrever diálogo → audio/scripts/epXX_dialogo.txt
├── 2. Gerar WAVs → python scripts/utils/elevenlabs_voice_gen.py --ep XX
└── 3. Gerar lip sync → python scripts/utils/rhubarb_runner.py --ep XX

FASE C — SCRIPT BLENDER (gerado pelo agente)
├── 1. Bloco 1: Setup da cena
├── 2. Bloco 2: Cenário/ambiente
├── 3. Bloco 3: Personagens/objetos
├── 4. Bloco 4: Materiais PBR
├── 5. Bloco 5: Animação e keyframes
├── 6. Bloco 6: Iluminação
├── 7. Bloco 7: Câmeras e cortes
├── 8. Bloco 8: Efeitos especiais
└── 9. Bloco 9: Render e export

FASE D — BLENDER (execução)
├── 1. Abrir Blender → Scripting → New → Colar → Run Script
├── 2. Aplicar lip sync → lipsync_blender.py
├── 3. Testar frame → F12
├── 4. Render completo → Ctrl+F12
└── 5. Output em: renders/finals/

FASE E — PÓS-PRODUÇÃO
├── 1. Revisão do render
├── 2. Ajustes (reexecutar script com parâmetros alterados)
└── 3. Export final para publicação
```

---

## ⚙️ Setup Inicial

### Requisitos de Software

| Software | Versão | Download | Status |
|----------|--------|----------|--------|
| **Blender** | 4.0+ | [blender.org](https://www.blender.org/download/) | ❓ Verificar versão |
| **Python** | 3.11+ | Incluído no Blender | ✅ |
| **Rhubarb Lip Sync** | Qualquer | [GitHub Releases](https://github.com/DanielSWolf/rhubarb-lip-sync/releases) | ⚠️ **PENDENTE** |
| **ElevenLabs SDK** | Latest | `pip install elevenlabs` | ⚠️ **PENDENTE** |
| **python-dotenv** | Latest | `pip install python-dotenv` | ⚠️ **PENDENTE** |

### Passo a passo de instalação

```powershell
# 1. Instalar dependências Python (no PowerShell)
pip install elevenlabs python-dotenv

# 2. Baixar Rhubarb:
# → https://github.com/DanielSWolf/rhubarb-lip-sync/releases
# → Extrair em: D:\Blender\blenderscripts\tools\rhubarb\

# 3. Configurar ElevenLabs:
cd D:\Blender\blenderscripts
python scripts\utils\elevenlabs_voice_gen.py --setup
# (Vai pedir sua API Key do ElevenLabs)

# 4. Verificar Rhubarb:
python scripts\utils\rhubarb_runner.py --check
```

### Configuração do ElevenLabs

1. Criar conta em [elevenlabs.io](https://elevenlabs.io) (plano gratuito: 10k chars/mês)
2. Ir em: Profile → API Keys → copiar a chave
3. Executar: `python scripts/utils/elevenlabs_voice_gen.py --setup`
4. Definir Voice IDs para Boomer e Kev no arquivo `elevenlabs_voice_gen.py`:
   ```python
   "voice_id": "COLE_AQUI_O_ID",  # linha ~60 e ~80
   ```

---

## ⚠️ PENDÊNCIAS E PRÓXIMOS PASSOS

### 🔴 BLOQUEANTES (sem isso, o pipeline não funciona)

| # | Pendência | Responsável | Como resolver |
|---|-----------|-------------|---------------|
| P1 | **Baixar Rhubarb Lip Sync** | Usuário | Baixar .exe → `tools/rhubarb/rhubarb.exe` |
| P2 | **Conta ElevenLabs + API Key** | Usuário | Criar conta → copiar API Key → executar `--setup` |
| P3 | **Voice IDs do Boomer e Kev** | Usuário | Escolher vozes no ElevenLabs → colar IDs no script |

### 🟡 SCRIPTS PENDENTES (a desenvolver)

| # | Script | Pasta | Descrição |
|---|--------|-------|-----------|
| S1 | `materials_library.py` | `scripts/utils/` | Biblioteca de materiais PBR reutilizáveis |
| S2 | `camera_utils.py` | `scripts/utils/` | Utilitários de câmera cinematográfica |
| S3 | `render_utils.py` | `scripts/utils/` | Setup de render otimizado (EEVEE/Cycles) |
| S4 | `mocap_utils.py` | `scripts/utils/` | Import BVH/Mixamo e retarget de animação |
| S5 | `base_character.py` | `characters/` | Personagem base reutilizável do universo FGS |
| S6 | `podcast_studio.py` | `scenes/` | Cenário standalone do The Den |
| S7 | `product_spin_360.py` | `scripts/commercials/` | Template de comercial — produto girando |
| S8 | `liquid_splash.py` | `scripts/commercials/` | Simulação de splash de bebida |
| S9 | `particle_burst.py` | `scripts/shorts/` | Explosão de partículas para Reels |
| S10 | `episode_base.py` | `scripts/youtube/` | Template base de episódio reutilizável |

### 🟢 MELHORIAS DO PROJETO BOOMER & KEV

| # | Melhoria | Prioridade |
|---|----------|------------|
| M1 | Modelagem 3D mais detalhada dos rostos (com boca articulada) | Alta |
| M2 | Shape Keys reais de boca para lip sync mais preciso | Alta |
| M3 | Armature completo (rigging humano) para Boomer e Kev | Alta |
| M4 | Animações BVH de gestos e movimentos de conversa | Média |
| M5 | Biblioteca de expressões faciais (alegria, surpresa, dúvida) | Média |
| M6 | Setup de som ambiente do estúdio (hover, fundo) | Média |
| M7 | Template de abertura/encerramento reutilizável (intro/outro) | Baixa |
| M8 | Variações de cenário (iluminação por tema de episódio) | Baixa |

### 🔵 INFRAESTRUTURA FUTURA (White Label)

| # | Item | Descrição |
|---|------|-----------|
| I1 | Interface web de geração | Formulário web → gera script automaticamente |
| I2 | Servidor de render | GPU dedicada para renderizar sem precisar do PC do usuário |
| I3 | Sistema de templates | Biblioteca de templates por nicho (comercial, educação, entretenimento) |
| I4 | API de geração | Endpoint que recebe ideia → retorna script Python |
| I5 | Dashboard de projetos | Gerenciar múltiplos projetos, histórico de renders |
| I6 | Painel de clientes | White-label: cada cliente tem seu próprio painel |

---

## 🛠️ Stack Tecnológico

| Camada | Tecnologia | Versão | Uso |
|--------|-----------|--------|-----|
| **3D Engine** | Blender | 4.0+ | Render, animação, física |
| **Scripting 3D** | Python (bpy) | 3.11+ | 100% do pipeline 3D |
| **Voz IA** | ElevenLabs | Latest | Geração de vozes dos personagens |
| **Lip Sync** | Rhubarb | Latest | Análise de fonemas do áudio |
| **Render Fast** | EEVEE Next | Built-in | Previews e conteúdo rápido |
| **Render Quality** | Cycles | Built-in | Comerciais e renders finais |
| **Fluidos** | Mantaflow | Built-in | Líquidos, fumaça, fogo |
| **Partículas** | Blender PS | Built-in | Glitter, poeira, estrelas |
| **Mocap** | BVH/Mixamo | — | Movimentos humanos |
| **Output** | FFmpeg | Built-in | MP4, WebM, PNG sequence |
| **IA Agente** | Gemini | Latest | Geração dos scripts Python |
| **Agente FW** | Antigravity | Latest | Sistema de agentes e skills |

---

## 🤖 Sistema de Agentes

### Agente Principal
- **`@blender-animator`** → Gera todos os scripts Python do projeto

### Agentes de Suporte
- **`@project-planner`** → Planejamento e roadmap
- **`@orchestrator`** → Coordenação de tarefas complexas
- **`@neuromarketing-agent`** → Storytelling e persuasão visual
- **`@master-persuader`** → Gatilhos psicológicos nos scripts

### Como invocar:
```
Me dá o script para [TIPO] de [TEMA] com [DURAÇÃO]
```
**Exemplos:**
- *"Me dá o script para um comercial de tênis de corrida com explosão de partículas em 15s"*
- *"Crie o Episódio 2 do Boomer & Kev sobre futebol"*
- *"Gera um short viral de cristais de diamante se formando em câmera macro"*

---

## 📊 Status Geral do Projeto

| Componente | Status | % |
|-----------|--------|---|
| Sistema de Agentes | ✅ Completo | 100% |
| Framework de Direção de Arte | ✅ Completo | 100% |
| Pipeline de Áudio (documentação) | ✅ Completo | 100% |
| Bíblia Boomer & Kev | ✅ Completo | 100% |
| Utilitários base (scene_setup) | ✅ Completo | 100% |
| Pipeline ElevenLabs (código) | ✅ Completo | 100% |
| Pipeline Rhubarb (código) | ✅ Completo | 100% |
| Pipeline Lip Sync Blender (código) | ✅ Completo | 100% |
| Script Ep.1 Boomer & Kev | ✅ Completo | 100% |
| Rhubarb instalado | ⚠️ Pendente usuario | 0% |
| ElevenLabs configurado | ⚠️ Pendente usuario | 0% |
| Voice IDs definidos | ⚠️ Pendente usuario | 0% |
| Modelagem 3D detalhada | 🔵 Fase 2 | 0% |
| Armature/Rigging completo | 🔵 Fase 2 | 0% |
| Scripts de comerciais | 🔵 Fase 3 | 0% |
| Scripts de shorts | 🔵 Fase 3 | 0% |
| **TOTAL GERAL** | **Em andamento** | **~45%** |

---

## 📞 Fluxo de Trabalho Diário

```
VOCÊ → Me envia referência + ideia + duração
  ↓
AGENTE → Analisa, gera pré-roteiro + shot list
  ↓
VOCÊ → Aprova ou ajusta o pré-roteiro
  ↓
AGENTE → Gera script Python completo e comentado
  ↓
VOCÊ → Cola no Blender → Run Script
  ↓
PARALELO → Terminal: gera vozes (ElevenLabs) + lip sync (Rhubarb)
  ↓
BLENDER → Aplica lip sync (lipsync_blender.py)
  ↓
VOCÊ → F12 (testa frame) → Ctrl+F12 (render completo)
  ↓
OUTPUT → renders/finals/nome_do_projeto.mp4 ✅
```

---

*Felipe Gouveia Studio Python 3D*
*Documentação gerada em: 2026-03-04*
*Versão: 2.0.0*
