# 🎨 DIREÇÃO DE ARTE — Felipe Gouveia Studio Python 3D
## Framework Universal de Produção Visual

> **Regra de ouro:** Antes de qualquer script Python, existe a Direção de Arte.  
> Sem direção de arte definida → sem script gerado.

---

## HIERARQUIA DE PRODUÇÃO

```
INPUT (Você fornece)
│
├── 1. REFERÊNCIA VISUAL         → Imagem, vídeo, mood board
├── 2. CONCEITO / IDEIA          → O que é? Quem aparece? O quê acontece?
├── 3. OBJETIVO                  → Vender? Entreter? Informar? Viralizar?
└── 4. DURAÇÃO                   → 15s / 30s / 60s / 2min / episódio

            ↓

PROCESSO (Agente gera)
│
├── A. PRÉ-ROTEIRO               → Estrutura de cenas numeradas
├── B. SHOT LIST                 → Plano a plano com tipo de câmera
├── C. BÍBLIA DO PROJETO         → Personagens, cenário, paleta, regras
└── D. SCRIPT PYTHON             → Código Blender pronto para executar

            ↓

OUTPUT (Blender entrega)
│
└── MP4 / PNG SEQUENCE           → Pronto para publicação
```

---

## SISTEMA DE TIPOS DE PLANO (SHOT TYPES)

### Tipos de câmera disponíveis:

| Código | Nome | Descrição | Uso ideal |
|--------|------|-----------|-----------|
| **XWS** | Extreme Wide Shot | Cena inteira, personagens pequenos | Estabelecer ambiente grandioso |
| **WS** | Wide Shot / Establishing | Personagem completo + ambiente | Primeira cena de ambiente |
| **MS** | Medium Shot | Da cintura para cima | Diálogos, ações gerais |
| **MCU** | Medium Close-Up | Peito para cima | Conversa íntima, expressões |
| **CU** | Close-Up | Rosto/objeto principal | Emoção, detalhe importante |
| **ECU** | Extreme Close-Up | Olho, boca, detalhe específico | Tensão, ênfase dramática |
| **OTS** | Over The Shoulder | Câmera atrás de um personagem | Diálogos entre dois personagens |
| **POV** | Point of View | Visão subjetiva do personagem | Imersão, perspectiva única |
| **CUTAWAY** | Insert / Detalhe | Detalhe relevante da cena | Mostrar objeto/reação |
| **REACT** | Reaction Shot | Reação do personagem que ouve | Comédia, drama, surpresa |

---

## ESTRUTURA DE CENAS POR DURAÇÃO

### Para 30 segundos (padrão FGS):

```
TOTAL: 30 segundos | 720 frames @ 24fps

ESTRUTURA RECOMENDADA (10-12 planos):

┌─────────────────────────────────────────────────────────┐
│  CENA 1: ESTABLISHING (3-4s)                            │
│  Tipo: WS ou XWS                                        │
│  Objetivo: "Onde estamos? Quem são?"                    │
│  Câmera: Estática ou leve movimento de revelação        │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│  CENA 2: INTRODUÇÃO DOS PERSONAGENS (2-3s)              │
│  Tipo: MS ou MCU                                        │
│  Objetivo: Apresentar protagonistas                     │
│  Câmera: Suave dolly para frente                        │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│  CENAS 3-7: DESENVOLVIMENTO (12-15s)                    │
│  Tipos: Alternando OTS / MCU / REACT / CUTAWAY          │
│  Objetivo: Ação principal / diálogo / narrativa         │
│  Câmera: Variada — cria ritmo e energia                 │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│  CENAS 8-9: CLÍMAX (4-5s)                              │
│  Tipo: CU ou ECU → zoom out para WS                    │
│  Objetivo: Momento de maior impacto emocional           │
│  Câmera: Movimento dramático (crash zoom, orbit)        │
└─────────────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────────────┐
│  CENA 10: RESOLUÇÃO / LOGO (3-4s)                       │
│  Tipo: WS ou produto/logo em destaque                   │
│  Objetivo: CTA, marca, conclusão emocional              │
│  Câmera: Recuo suave ou estática com fade               │
└─────────────────────────────────────────────────────────┘
```

### Para outros formatos:

| Duração | Nº de Planos | Ritmo médio |
|---------|-------------|-------------|
| **15s Short/Reel** | 5-7 planos | 2-3s por plano |
| **30s Comercial** | 10-12 planos | 2.5-3s por plano |
| **60s Trailer** | 15-20 planos | 3-4s por plano |
| **2min YouTube** | 30-40 planos | Varia por cena |
| **Episódio 5min** | 80-120 planos | Varia dramaticamente |

---

## FORMATO DO PRÉ-ROTEIRO

### Template Padrão FGS:

```
PRÉ-ROTEIRO — [NOME DO PROJETO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tipo: [COMERCIAL / YOUTUBE / SHORT / EPISÓDIO]
Duração: [X segundos / minutos]
Personagens: [Lista]
Ambiente: [Descrição]
Objetivo: [Vender / Entreter / Educar / Viralizar]
Mood: [Cômico / Dramático / Épico / Surreal / Informativo]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CENA 01 | [TIPO DE PLANO] | [DURAÇÃO]
INT/EXT: [Interior ou exterior]
DESCRIÇÃO: [O que vemos visualmente]
AÇÃO: [O que acontece]
CÂMERA: [Tipo de movimento]
ÁUDIO: [Música, voiceover, efeito sonoro]
NOTAS DE ARTE: [Iluminação, paleta, detalhes especiais]
━━━━━

CENA 02 | [TIPO DE PLANO] | [DURAÇÃO]
[... repetir para cada cena]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: [X cenas] | [X segundos] | [X frames @ Xfps]
```

---

## BÍBLIA DO PROJETO (Project Bible)

Cada série ou projeto recorrente DEVE ter uma Bíblia com:

### 1. Personagens
- Nome e apelido
- Espécie / tipo (para projetos com animais ou criaturas)
- Personalidade (3 adjetivos principais)
- Maneirismos físicos (como ele se move, senta, gesticula)
- Paleta de cores exclusiva do personagem
- Proporções do corpo (será mantida em TODOS os scripts)

### 2. Ambiente
- Descrição do cenário principal
- Paleta de cores do ambiente
- Elementos fixos (sempre presentes)
- Elementos variáveis (mudam por episódio)
- Iluminação padrão

### 3. Linguagem Visual
- Estilo (cartoon, semi-realista, estilizado, hiper-real)
- Velocidade de câmera (lenta/rápida/mista)
- Tipo de corte dominante (corte seco / dissolve / wipe)
- Uso de close-up (frequente = intimidade, raro = drama)
- Paleta geral do projeto

### 4. Regras de Consistência
- Detalhes que NUNCA mudam entre episódios
- Ângulo padrão de câmera para cada personagem
- Assinatura visual (algo único que identifica a série)

---

## ANÁLISE DE INPUT (Como processar sua referência)

### Quando você envia uma IMAGEM:
```
O agente analisa:
1. Composição (regra dos terços, ponto focal)
2. Paleta de cores dominante
3. Estilo visual (realismo? cartoon? abstrato?)
4. Iluminação (ambiente? dura? suave? colorida?)
5. Objetos/elementos presentes
6. Mood/atmosfera emocional
→ Gera pré-roteiro baseado nessa referência
```

### Quando você envia um VÍDEO:
```
O agente analisa:
1. Tipo de planos usados (WS, CU, OTS?)
2. Ritmo de cortes (rápido? lento?)
3. Movimento de câmera (estática? dolly? handheld?)
4. Iluminação e paleta
5. Narrativa e estrutura
6. Energia e momentum
→ Reproduz ou adapta o estilo em Python 3D
```

### Quando você envia uma LOCUÇÃO (texto/áudio):
```
O agente analisa:
1. Ritmo e pausas do texto (determina timing das cenas)
2. Palavras-chave que pedem visual específico
3. Emoção do narrador (determina tipo de plano)
4. Chamadas para ação (onde enfatizar visualmente)
→ Sincroniza cenas com o ritmo da locução
```

---

## GLOSSÁRIO RÁPIDO

| Termo | Significado |
|-------|-------------|
| **Corte seco** | Transição direta sem efeito |
| **Dissolve** | Fundido cruzado entre cenas |
| **Fade In/Out** | Escurece ou clarea gradualmente |
| **B-Roll** | Imagens complementares (não o personagem principal) |
| **Blocking** | Posicionamento inicial de personagens na cena |
| **Beat** | Momento de pausa intencional na narrativa |
| **Payoff** | Resolução de uma expectativa criada antes |
| **L-Cut / J-Cut** | Som começa antes/depois do corte visual |
| **Dutch Angle** | Câmera inclinada (tensão, instabilidade) |
| **Rack Focus** | Foco muda de um plano para outro |

---

*Felipe Gouveia Studio Python 3D | Framework de Direção de Arte v1.0*
