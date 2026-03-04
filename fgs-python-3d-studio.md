# Felipe Gouveia Studio — Python 3D
## Plano Master do Projeto

**Tipo:** PYTHON/BLENDER — Agência Criativa Completa via IA  
**Versão:** 2.0.0  
**Status:** IMPLEMENTATION  
**White Label:** Sim (produto futuro para venda)  
**Agente Principal:** `blender-animator` v2.0

---

## 🎯 Visão do Produto

> **"O céu não é o limite. É apenas o começo."**

**Felipe Gouveia Studio Python 3D** é uma **agência criativa completa operada por IA**, capaz de produzir qualquer conteúdo 3D imaginável — do hiper-real ao completamente surreal — usando exclusivamente Python + Blender.

### O que isso significa:
1. Você fornece **referência visual** (imagem/vídeo) + **roteiro/ideia**
2. O agente analisa, concebe a narrativa e gera o **script Python completo**
3. O script inclui storytelling cinematográfico + gatilhos de neuromarketing
4. O Blender **executa e renderiza** automaticamente
5. Entrega **MP4/PNG** prontos para publicação

### Domínios de Produção (TODOS):
| Domínio | Exemplos de Projetos |
|---------|--------------------|
| **Gastronomia** | Splash de bebida, derretimento de chocolate, pizza em câmera lenta |
| **Medicina** | Viagem pelo corpo, moléculas, DNA, cirurgia 3D |
| **Espaço** | Viagem a Marte, buracos negros, colisão de galáxias |
| **Arquitetura** | Fly-through de prédios, demolições, smart cities |
| **Automóvel** | Reveal de carro, motor explodido, crash test |
| **Moda/Luxo** | Tecido em câmera lenta, perfume, joalheria |
| **História/Conflito** | Batalhas reconstruídas, evolução de impérios |
| **Natureza** | Tempestades, florestas crescendo, oceanos |
| **Ciência** | Fractais, Big Bang, física quântica visualizada |
| **Negócios** | Infográficos 3D, logo reveals, dashboards holográficos |
| **Entretenimento** | Trailers cinematográficos, intros de games, personagens |
| **Surreal** | Qualquer universo impossível que a mente conceba |

---

## ✅ Critérios de Sucesso

- [ ] Scripts Python funcionam no Blender 4.0+ sem erros
- [ ] Personagens reutilizáveis entre projetos (biblioteca)
- [ ] Movimentos humanos via BVH/Mocap e Mixamo funcionais
- [ ] Pipeline completo: ideia → script → render ≤ 5 minutos (EEVEE)
- [ ] Código 100% comentado em português para usuário iniciante
- [ ] Estrutura de pastas organizada e versionada
- [ ] Pronto para white-label (sem dependências de terceiros exclusivas)

---

## 🛠️ Stack Tecnológico

| Componente | Tecnologia | Motivo |
|-----------|-----------|--------|
| **Scripting** | Python 3.11+ (built-in Blender) | Único suportado pelo bpy |
| **3D Engine** | Blender 4.0+ | Open source, poderoso, bpy |
| **Render Fast** | EEVEE Next | Tempo real, GPU, < 5min |
| **Render Quality** | Cycles + Denoiser AI | Foto-real para comerciais |
| **Mocap** | BVH (arquivo padrão) | Universal, gratuito |
| **Animações** | Mixamo (Adobe) | Biblioteca +2000 animações |
| **Fluidos** | Mantaflow (built-in Blender) | Splash, água, fumaça |
| **Partículas** | Blender Particle System | Glitter, poeira, fogo |
| **Output** | FFmpeg via Blender | MP4, WebM, PNG sequence |

---

## 📁 Estrutura de Pastas do Projeto

```
d:\Blender\blenderscripts\
│
├── .agent/                          # Sistema de agentes (instalado)
│
├── GEMINI.md                        # Regras do workspace
├── fgs-python-3d-studio.md          # Este plano (você está aqui)
│
├── characters/                      # Personagens reutilizáveis
│   ├── base_character.py            # Script: cria personagem base
│   ├── character_library.blend      # Biblioteca de personagens
│   └── README.md
│
├── scenes/                          # Cenas e cenários
│   ├── studio_base.py               # Estúdio fotográfico virtual
│   ├── outdoor_environment.py       # Ambiente externo
│   └── abstract_void.py             # Fundo abstrato
│
├── scripts/                         # Scripts de produção
│   ├── commercials/                 # Comerciais
│   │   ├── product_spin_360.py      # Produto girando 360
│   │   ├── liquid_splash.py         # Splash de bebida
│   │   └── product_reveal.py        # Reveal dramático
│   ├── youtube/                     # Animações YouTube
│   │   ├── episode_base.py          # Template de episódio
│   │   └── dialogue_scene.py        # Cena de diálogo
│   ├── shorts/                      # Reels/Shorts
│   │   ├── vertical_quick.py        # Template 9:16 rápido
│   │   └── particle_burst.py        # Explosão de partículas
│   └── utils/                       # Utilitários
│       ├── scene_setup.py           # Setup padrão de cena
│       ├── materials_library.py     # Biblioteca de materiais
│       ├── camera_utils.py          # Utilidades de câmera
│       ├── render_utils.py          # Utilidades de render
│       └── mocap_utils.py           # Import BVH/Mixamo
│
├── motions/                         # Dados de animação
│   ├── bvh/                         # Arquivos .bvh de mocap
│   └── mixamo/                      # FBX do Mixamo
│
├── renders/                         # Output
│   ├── drafts/                      # Previews para aprovação
│   └── finals/                      # Renders finais para entrega
│
├── references/                      # Referências visuais
│   ├── images/                      # Imagens de referência
│   └── videos/                      # Vídeos de referência
│
└── docs/                            # Documentação
    ├── how-to-use.md                # Guia do usuário iniciante
    ├── blender-basics.md            # Blender para leigos
    └── script-catalog.md            # Catálogo de scripts
```

---

## 📊 FASE 1 — FUNDAÇÃO (Utilitários Base)

### Task 1.1 — scene_setup.py
**Agente:** `blender-animator`  
**Prioridade:** P0 — Bloqueante  
**Input:** Configurações (fps, resolução, duração)  
**Output:** Função `setup_scene()` funcionando  
**Verify:** Script executa sem erros, cena limpa criada  

```
Inclui:
- Limpeza de cena
- Configuração de FPS e resolução
- World/background
- Unidades métricas
- Frame range
```

### Task 1.2 — materials_library.py
**Agente:** `blender-animator`  
**Prioridade:** P0 — Bloqueante  
**Input:** Parâmetros de cor e propriedades  
**Output:** Biblioteca de materiais reutilizáveis  
**Verify:** Materiais criados corretamente no Blender  

```
Inclui:
- PBR completo (metal, plástico, vidro, pele estilizada)
- Liquid (bebidas, água, mel)
- Emission (neon, brilho)
- Holographic/Iridescent
```

### Task 1.3 — camera_utils.py
**Agente:** `blender-animator`  
**Prioridade:** P1  
**Input:** Posição, alvo, tipo de shot  
**Output:** Câmera configurada cinematograficamente  
**Verify:** DOF funcional, composição correta  

### Task 1.4 — render_utils.py
**Agente:** `blender-animator`  
**Prioridade:** P1  
**Input:** Qualidade, formato, path de output  
**Output:** Render configurado e otimizado  
**Verify:** MP4 exportado corretamente  

### Task 1.5 — mocap_utils.py
**Agente:** `blender-animator`  
**Prioridade:** P1  
**Input:** Arquivo .bvh ou .fbx  
**Output:** Animação aplicada ao armature  
**Verify:** Personagem se move com dados de mocap  

---

## 📊 FASE 2 — PERSONAGENS

### Task 2.1 — base_character.py
**Agente:** `blender-animator`  
**Prioridade:** P0  
**Input:** Nome, posição, variações  
**Output:** Personagem estilizado com armature  
**Verify:** Personagem criado, rigged, pronto para animação  

```
Personagem do Universo FGS:
- Corpo estilizado (não fotorealista)
- Proporções humanas (1.75m, skeleton humano)
- Armature completo (head, spine, arms, legs, fingers)
- Material de pele estilizada
- Suporta BVH, Mixamo e keyframe manual
```

### Task 2.2 — character_variations.py
**Agente:** `blender-animator`  
**Prioridade:** P2  
**Input:** Tipo de personagem (herói, vilão, neutro)  
**Output:** Variações do personagem base  
**Verify:** Variações consistentes com o universo visual  

---

## 📊 FASE 3 — SCRIPTS DE PRODUÇÃO

### Task 3.1 — product_spin_360.py (Comercial)
**Agente:** `blender-animator`  
**Input:** Imagem/descrição do produto, cores, duração  
**Output:** Script de comercial produto girando  
**Verify:** Render de 10s funcional  

### Task 3.2 — liquid_splash.py (Comercial Bebida)
**Agente:** `blender-animator`  
**Input:** Tipo de bebida, cores, velocidade  
**Output:** Script de splash realista  
**Verify:** Partículas/fluido funcionando no Blender  

### Task 3.3 — particle_burst.py (Short/Reel)
**Agente:** `blender-animator`  
**Input:** Cores, densidade, duração  
**Output:** Script de explosão de partículas 9:16  
**Verify:** Render vertical 15-30s funcional  

### Task 3.4 — episode_base.py (YouTube)
**Agente:** `blender-animator`  
**Input:** Cena, personagens, ações básicas  
**Output:** Template de episódio reutilizável  
**Verify:** Personagens animados com BVH/Keyframes  

---

## 📊 FASE 4 — DOCUMENTAÇÃO (Usuário Iniciante)

### Task 4.1 — how-to-use.md
**Agente:** `documentation-writer`  
**Conteúdo:**
- Como abrir o Blender
- Como usar a aba Scripting
- Como rodar um script
- Como fazer o render
- FAQ de problemas comuns

### Task 4.2 — script-catalog.md
**Agente:** `documentation-writer`  
**Conteúdo:**
- Lista de todos os scripts disponíveis
- O que cada um faz
- Parâmetros ajustáveis
- Exemplos de uso

---

## 🔄 PIPELINE DE TRABALHO DIÁRIO

```
VOCÊ (usuário):
1. Encontra imagem/vídeo de referência → compartilha comigo
2. Descreve o roteiro/ideia
3. Especifica: tipo (comercial/youtube/short), duração, cores principais

EU (agente):
1. Analiso a referência visual
2. Decomponho em elementos 3D
3. Gero o script Python completo
4. Forneço explicação passo-a-passo
5. Forneço instruções de uso no Blender

BLENDER (execução):
1. Você abre a aba Scripting
2. Cola o script gerado
3. Clica em ▶ Run Script
4. Aguarda execução
5. Roda o render (Render → Render Animation)
6. Arquivo MP4 salvo na pasta /renders/
```

---

## ⚡ TECNOLOGIAS-CHAVE DO bpy (Blender Python API)

| Módulo | Para que serve |
|--------|---------------|
| `bpy.ops` | Operações (criar objetos, importar, renderizar) |
| `bpy.data` | Dados (materiais, meshes, armatures, cenas) |
| `bpy.context` | Contexto atual (cena ativa, objeto selecionado) |
| `bpy.types` | Tipos de dados do Blender |
| `mathutils` | Matemática 3D (Vector, Matrix, Euler, Quaternion) |

---

## 🎨 UNIVERSO VISUAL FELIPE GOUVEIA STUDIO

**Identidade Visual dos Personagens:**
- Estilo: Semi-realista estilizado (entre cartoon e realismo)
- Proporção: Humana (não super deformado)
- Paleta: Neutros com acentos de cor vibrante
- Traço: Clean, sem texturas complexas de pele

**Identidade Visual das Cenas:**
- Iluminação: Cinematográfica, dramática quando necessário
- Cores: Paletas curadas para cada tipo de produção
- Background: Variado por projeto (estúdio, natureza, abstrato)
- Qualidade: Sempre premium, independente do tipo

---

## 📅 CRONOGRAMA ESTIMADO

| Fase | Descrição | Estimativa |
|------|-----------|-----------|
| **Fase 1** | Utilitários base (5 scripts) | 1-2 sessões |
| **Fase 2** | Personagens base | 1-2 sessões |
| **Fase 3** | Scripts de produção (4 tipos) | 2-3 sessões |
| **Fase 4** | Documentação | 1 sessão |
| **Total** | Fundação completa | ~6-8 sessões |

*Cada "sessão" = uma conversa com o agente gerando 1-3 scripts*

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

- [ ] **Task 1.1** → Criar `scripts/utils/scene_setup.py`
- [ ] **Task 1.2** → Criar `scripts/utils/materials_library.py`
- [ ] **Task 2.1** → Criar `characters/base_character.py`
- [ ] **Task 3.1** → Criar primeiro comercial: `scripts/commercials/product_spin_360.py`
- [ ] Criar estrutura de pastas do projeto

**Prioridade:** Task 1.1 → 1.2 → 2.1 (em sequência, pois são dependências)

---

## 📌 NOTAS IMPORTANTES

1. **Blender 4.0+** obrigatório (API do bpy mudou significativamente)
2. **GPU recomendada** para render rápido (NVIDIA/AMD com drivers atualizados)
3. **Scripts são standalone** — não dependem de addons externos
4. **White-label**: Todos os scripts terão header padronizado do FGS
5. **Versionamento**: Cada script terá versão no header (`v1.0`, `v1.1`, etc.)

---

*Plano criado em: 2026-03-04 | Agente: @blender-animator | Status: APROVADO PARA IMPLEMENTAÇÃO*
