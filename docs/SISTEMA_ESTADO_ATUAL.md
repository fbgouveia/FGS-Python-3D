# BLENDERSCRIPTS — ESTADO DO SISTEMA
**Felipe Gouveia Studio | Atualizado: 2026-03-15**

---

## 1. ARQUITETURA LÓGICA

```
┌─────────────────────────────────────────────────────────────┐
│  INTENÇÃO (Input)                                           │
│  conceito="ansiedade" | nicho="psicologia" | formato="reel" │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  ANÁLISE — suggestion_engine.py                             │
│  Analisa: tipo_upload + densidade_texto + emoção            │
│  Retorna: estratégia visual (FULL_BROLL / VFX_OVERLAY /     │
│           MIXADO) + template recomendado + ação no Blender  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  GERAÇÃO DO MANIFESTO — portfolio_builder.py                │
│  Gera JSON declarativo com: cena + personagens +            │
│  animações + engine + resolução + licença                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  ORQUESTRAÇÃO — bridge_engine.py ⚠️ QUEBRADO               │
│  Lê o JSON → executa deterministicamente:                   │
│  SceneFactory → CharacterFactory → AnimationEngine →        │
│  CameraSystem → VFXEngine → RenderManager                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  MOTORES CORE (todos funcionais)                            │
│  scene_factory    → 14 ambientes prontos                    │
│  character_factory→ 19 espécies + humano + robô             │
│  camera_system    → 8 presets + orbit/dolly/handheld        │
│  animation_engine → mover/flutuar/tremer/orbitar/quicar     │
│  vfx_engine       → partículas/fogo/fumaça/laser/portal     │
│  transitions_engine→ reflexivo/alerta/solucao               │
│  render_manager   → 9 presets de output                     │
│  materials_library→ 100+ materiais PBR procedurais          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  ASSETS — paths.py + library_config.py                      │
│  get_library("hdri")  → D:\Graphic Designer Resources\HDRI  │
│  get_library("music") → D:\...\MUSIC                        │
│  Fallback: assets/ local se GDR offline                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  OUTPUT — renders/finals/*.mp4                              │
│  → Portfolio Watcher copia para React Portfolio             │
│  → clara_funnel_trigger analisa qualidade → ação marketing  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. FLUXO DE ASSETS

```
D:\Graphic Designer Resources\ (477GB — fonte primária)
     │
     ├─ get_library("hdri")        → lighting_system.load_hdri()
     ├─ get_library("music")       → audio_manager.from_library("music")
     ├─ get_library("sfx")         → audio_manager.from_library("sfx")
     ├─ get_library("vfx")         → vfx_engine (manual por enquanto)
     ├─ get_library("motion")      → animation_engine (manual por enquanto)
     └─ get_library("luts")        → render_manager (manual por enquanto)

Fallback automático → assets/ local (leve, no git)
Mirror futuro      → G:\My Drive\FGS_LIBRARY (via rclone)
```

**O que está conectado:**
- HDRI → `lighting_system.load_hdri()` ✅
- Música/SFX → `audio_manager.from_library()` ✅

**O que ainda não está conectado:**
- VFX packs → `vfx_engine` (manual)
- Motion graphics → `animation_engine` (manual)
- LUTs → `render_manager` (manual)
- Stock video → nenhum módulo ainda

---

## 3. STATUS DE CADA ARQUIVO

### PRONTOS PARA PRODUÇÃO ✅

| Arquivo | Função | Observação |
|---------|--------|------------|
| `utils/materials_library.py` | 100+ materiais PBR | Completo |
| `utils/scene_factory.py` | 14 ambientes 3D | Completo |
| `utils/character_factory.py` | 19 espécies + humano | Completo |
| `utils/camera_system.py` | 8 presets + 7 movimentos | Completo |
| `utils/animation_engine.py` | Keyframe + procedural + física | Completo |
| `utils/vfx_engine.py` | Partículas + fluidos + sci-fi | Fluidos precisam de bake manual |
| `utils/transitions_engine.py` | 3 climas emocionais | Completo |
| `utils/render_manager.py` | 9 presets de render | Completo |
| `utils/asset_orchestrator.py` | Organiza ZIPs/arquivos por tipo | Completo |
| `utils/paths.py` | Resolução de caminhos + GDR | Completo |
| `utils/library_config.py` | 22 categorias da GDR | Completo |
| `utils/audio_manager.py` | BGM + SFX + from_library() | Completo |
| `utils/lighting_system.py` | 14 presets + load_hdri() | Completo |
| `utils/license_manager.py` | BASIC/PRO/ENTERPRISE | Mock (sem API real) |
| `pipeline/suggestion_engine.py` | Análise pré-produção neuromarketing | Completo |
| `pipeline/portfolio_builder.py` | Gera manifests JSON | Completo, caminhos hardcoded |
| `social/broll_generator.py` | Gerador de B-rolls por conceito | Completo |
| `social/broll_orchestrator.py` | Fila de B-rolls em background | Completo |
| `youtube/boomer_kev_ep01.py` | Episódio completo podcast 3D | Completo, standalone |

### QUEBRADOS — PRECISAM DE FIX ❌

| Arquivo | Problema | Severidade |
|---------|----------|------------|
| `utils/bridge_engine.py` | `factory.build()` → deveria ser `factory.criar()` | CRÍTICO |
| `utils/bridge_engine.py` | `anim_engine.apply_animation()` → não existe, métodos são `mover()`, `flutuar()` etc. | CRÍTICO |
| `utils/bridge_engine.py` | Importa `lighthouse_3d` que não existe | CRÍTICO |
| `FGS_PRODUCER_CORE.py` | Importa `render_pipeline`, `scene_setup` que não existem | CRÍTICO |
| `FGS_PRODUCER_CORE.py` | `setup_studio_lighting()` não existe em lighting_system | CRÍTICO |
| `utils/lorena_system_guardian.py` | Assume que DB existe, não inicializa | ALTO |
| `scripts/marketing/clara_funnel_trigger.py` | Não executa ações (email/WhatsApp vazio) | MÉDIO |

### INCOMPLETOS — PARCIALMENTE FUNCIONAIS ⚠️

| Arquivo | O que falta |
|---------|------------|
| `utils/vfx_engine.py` | Fluidos requerem bake manual |
| `pipeline/portfolio_builder.py` | Paths hardcoded (`D:\Blender\...`) |
| `youtube/boomer_kev_ep01.py` | Loop de pés incompleto (linha 192) |
| `utils/lorena_system_guardian.py` | Sem inicialização de DB |

---

## 4. ARQUIVOS IMPORTADOS QUE NÃO EXISTEM

Estes módulos são referenciados no código mas **não existem no repo**:

| Módulo | Quem importa | O que deve fazer |
|--------|-------------|-----------------|
| `lighthouse_3d.py` | `bridge_engine.py` | Auditoria de qualidade da cena |
| `render_pipeline.py` | `FGS_PRODUCER_CORE.py` | Wrapper de execução do render |
| `scene_setup.py` | `FGS_PRODUCER_CORE.py` | Inicialização básica de cena |

> Nota: `logger.py`, `notify_user.py` existem mas com import frágil (sem fallback robusto).

---

## 5. PENDÊNCIAS — LISTA PRIORIZADA

### PRIORIDADE 1 — Desbloqueiam o pipeline central

- [ ] **PC1** — Corrigir `bridge_engine.py`: trocar `factory.build()` → `factory.criar()` e `apply_animation()` → métodos corretos
- [ ] **PC2** — Criar `lighthouse_3d.py`: auditoria de qualidade (conta polígonos, luzes, câmeras — retorna score 0-100)
- [ ] **PC3** — Corrigir `FGS_PRODUCER_CORE.py`: remover imports de módulos inexistentes, adaptar para usar módulos reais

### PRIORIDADE 2 — Robustez e integridade

- [ ] **PR1** — Corrigir `lorena_system_guardian.py`: adicionar inicialização do DB antes de consultar
- [ ] **PR2** — `portfolio_builder.py`: substituir path hardcoded por `paths.BASE_DIR`
- [ ] **PR3** — Conectar `suggestion_engine.py` ao `broll_orchestrator.py` (hoje são independentes)

### PRIORIDADE 3 — Expansão de assets

- [ ] **PA1** — Conectar VFX packs da GDR ao `vfx_engine.py` via `get_library("vfx")`
- [ ] **PA2** — Conectar LUTs da GDR ao `render_manager.py` via `get_library("luts")`
- [ ] **PA3** — Conectar motion graphics da GDR ao `animation_engine.py`
- [ ] **PA4** — Baking automático de fluidos no `vfx_engine.py`

### PRIORIDADE 4 — Integrações externas

- [ ] **PI1** — `clara_funnel_trigger.py`: integrar com WhatsApp Business API ou e-mail
- [ ] **PI2** — `license_manager.py`: substituir validação local por chamada a API central
- [ ] **PI3** — rclone: configurar sync D:\Graphic Designer Resources → Google Drive
- [ ] **PI4** — Instalar dependências: `watchdog`, `gdown`, `duckduckgo-search`, `requests`, `beautifulsoup4`

---

## 6. APRIMORAMENTOS SUGERIDOS

### A. Camada de seleção inteligente de assets
Hoje os scripts chamam `get_library()` manualmente. O ideal é uma função que dado o `conceito` retorne o mapa de assets ideal:

```python
# Exemplo futuro
assets = AssetSelector.para_conceito("ansiedade")
# retorna: { "hdri": "dark_moody.hdr", "music": "tension_01.mp3", "lut": "desaturado.cube" }
lighting.load_hdri(assets["hdri"])
audio.from_library("music", nome=assets["music"])
```

### B. Geração de manifesto via SuggestionEngine
Hoje `suggestion_engine.py` e `portfolio_builder.py` não conversam. Conectá-los:

```
SuggestionEngine.analisar(conceito) → estratégia
PortfolioBuilder.from_estrategia(estratégia) → manifest.json
BridgeEngine(manifest.json) → cena no Blender
```

### C. `boomer_kev_ep01.py` como template reutilizável
Hoje é standalone. Deveria virar `PodcastEpisodeTemplate(personagem_a, personagem_b, tema)` consumindo `CharacterFactory` + `SceneFactory` + `CameraSystem`.

### D. Bake automático de fluidos
`vfx_engine.py` cria domínios Mantaflow mas não bake. Adicionar:
```python
bpy.ops.fluid.bake_all()
```

---

## 7. O QUE PODE SER EXECUTADO HOJE

Estes scripts funcionam **agora mesmo** no Blender:

```bash
# Episódio podcast completo (Boomer & Kev)
blender -b -P scripts/youtube/boomer_kev_ep01.py

# B-roll por conceito
blender -b -P scripts/social/broll_generator.py -- ansiedade

# Showcase de produto 360
blender -b -P scripts/commercials/product_spin_360.py
```

O pipeline via JSON manifest (`bridge_engine.py`) ainda não funciona até PC1/PC2 serem resolvidos.

---

*Documento mantido por EUvc — Felipe Gouveia Studio*
