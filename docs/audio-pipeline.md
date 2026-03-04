# 🎙️ PIPELINE DE ÁUDIO — Felipe Gouveia Studio Python 3D
## Sistema de Voz IA + Lip Sync Automático

> **Resultado final:** Você escreve o diálogo → pipeline executa → personagens
> no Blender falam com sincronização labial perfeita, automaticamente.

---

## 🗺️ VISÃO GERAL DO PIPELINE

```
VOCÊ ESCREVE O DIÁLOGO
         │
         ▼
┌─────────────────────┐
│   ELEVENLABS API    │  → Gera WAV por personagem
│  (Voz IA de elite)  │     boomer_ep01.wav
└─────────────────────┘     kev_ep01.wav
         │
         ▼
┌─────────────────────┐
│  RHUBARB LIP SYNC   │  → Analisa o áudio
│  (Software gratuito)│  → Mapeia fonemas por frame
└─────────────────────┘     boomer_ep01.json
         │                  kev_ep01.json
         ▼
┌─────────────────────┐
│   BLENDER PYTHON    │  → Importa áudio no VSE
│   (lipsync_blender) │  → Cria Shape Keys na boca
└─────────────────────┘  → Aplica valores por frame
         │
         ▼
   🎬 PERSONAGEM FALA
   com lip sync perfeito
```

---

## 📦 FERRAMENTAS NECESSÁRIAS

### 1. ElevenLabs (Voz IA)
- **Site:** https://elevenlabs.io
- **Plano:** Free (10k chars/mês) ou Starter ($5/mês)
- **Como usar:** API key → script Python gera WAV automaticamente
- **Formato output:** WAV 44100Hz mono (ideal para Rhubarb)

### 2. Rhubarb Lip Sync (Análise de fonemas)
- **Site:** https://github.com/DanielSWolf/rhubarb-lip-sync
- **Custo:** 100% GRATUITO e open source
- **Download:** Baixar executável Windows: `rhubarb.exe`
- **Instalar em:** `D:\Blender\blenderscripts\tools\rhubarb\rhubarb.exe`
- **Input:** arquivo .WAV + texto opcional
- **Output:** JSON com timestamps de fonemas

### 3. Python externo (para rodar fora do Blender)
- O pipeline de geração de voz e Rhubarb roda **fora** do Blender
- O script de aplicação do lip sync roda **dentro** do Blender

---

## 🔤 SISTEMA DE FONEMAS (Rhubarb → Shape Keys)

O Rhubarb identifica **9 posições de boca** (baseado no sistema de Cathy Preston):

| Código | Fonemas | Posição da Boca | Shape Key no Blender |
|--------|---------|----------------|---------------------|
| **A** | M, B, P | Fechada | `mouth_closed` |
| **B** | Ee, I | Sorriso largo | `mouth_smile_open` |
| **C** | E, Eh | Aberta média | `mouth_medium` |
| **D** | Ai, I | Aberta com sorriso | `mouth_open_smile` |
| **E** | L, Th, K, S | Dentes visíveis | `mouth_teeth` |
| **F** | F, V | Labio inferior abaixado | `mouth_fv` |
| **G** | Oo, Q | Boca arredondada | `mouth_oo` |
| **H** | Ah, Oh | Muito aberta | `mouth_open_wide` |
| **X** | Neutro/Silêncio | Levemente aberta | `mouth_rest` |

### Para personagens estilizados (Boomer & Kev):
Usaremos **versão simplificada com 5 posições** (funciona perfeitamente para cartoon):

| Shape Key | Quando usar | Fonemas |
|-----------|-------------|---------|
| `mouth_closed` | Silêncio, M, B, P | A |
| `mouth_open_small` | Fala suave | C, E, F |
| `mouth_open_wide` | Fala aberta, risada | H, D |
| `mouth_oo` | Sons arredondados | G |
| `mouth_smile` | "Ee", sorriso | B |

---

## 🏗️ ESTRUTURA DE PASTAS DO PIPELINE DE ÁUDIO

```
D:\Blender\blenderscripts\
│
├── tools\
│   └── rhubarb\
│       └── rhubarb.exe          ← BAIXAR AQUI
│
├── audio\
│   ├── scripts\                 ← Diálogos dos episódios (TXT)
│   │   └── ep01_dialogo.txt
│   ├── raw\                     ← WAVs gerados pelo ElevenLabs
│   │   ├── boomer_ep01.wav
│   │   └── kev_ep01.wav
│   ├── lipsync\                 ← JSONs gerados pelo Rhubarb
│   │   ├── boomer_ep01.json
│   │   └── kev_ep01.json
│   └── final\                   ← Áudio mixado final do episódio
│       └── ep01_final.wav
│
└── scripts\
    └── utils\
        ├── elevenlabs_voice_gen.py   ← Gera vozes via API
        ├── rhubarb_runner.py          ← Processa áudio com Rhubarb
        └── lipsync_blender.py         ← Aplica lip sync no Blender
```

---

## 🎭 VOZES DOS PERSONAGENS

### Boomer — Características de Voz
```
Personalidade sonora: Voz grave, pausada, com sotaque ligeiramente regional
Tom: Autoritário mas casual, como um tio experiente
ElevenLabs Voice: Escolher voz masculina grave, 40-55 anos
Configurações recomendadas:
  - Stability: 0.75 (mais consistente, menos variação)
  - Clarity: 0.65
  - Style: 0.30 (natural, não exagerado)
  - Speed: 0.90 (ligeiramente mais lento que o normal)
```

### Kev — Características de Voz
```
Personalidade sonora: Voz média-alta, rápida, energética, jovem
Tom: Animado, expressivo, gírias, ritmo acelerado
ElevenLabs Voice: Escolher voz masculina jovem, 20-28 anos
Configurações recomendadas:
  - Stability: 0.45 (mais variação — ele é expressivo)
  - Clarity: 0.75
  - Style: 0.55 (mais estilizado, personalidade marcante)
  - Speed: 1.10 (ligeiramente mais rápido)
```

---

## 📝 FORMATO DO DIÁLOGO

### Como escrever o script para o pipeline:

```
# ep01_dialogo.txt
# Formato: PERSONAGEM: fala | [pausa em segundos]

BOOMER: Cara, tô te falando... esse negócio de inteligência artificial tá me deixando doido. | [1.5]
KEV: Doido como, Boomer? É a melhor coisa que aconteceu na humanidade! | [0.8]
BOOMER: Melhor coisa? Meu filho, na minha época, a gente consultava PESSOAS. Sabe o que é uma pessoa? | [1.2]
KEV: [risos] Boomer, você usa GPS ou não usa? | [0.5]
BOOMER: GPS é diferente... | [0.3]
KEV: Não é diferente! É IA! | [0.8]
BOOMER: [pausa longa] ...Então tô usando IA faz 20 anos e não sabia? | [1.0]
[AMBOS: risada] | [2.0]
KEV: [para câmera] E é exatamente ASS IM que começa toda conversa com o Boomer. | [1.0]
```

### Regras do formato:
- `PERSONAGEM:` — indica quem fala
- `| [X.X]` — pausa em segundos após a fala
- `[ação]` — indicadores de som/reação (não são falas)
- Uma linha = uma cena de fala = um arquivo WAV separado

---

## ⚙️ CONFIGURAÇÃO INICIAL (ONCE — Fazer apenas uma vez)

### Passo 1: Baixar o Rhubarb
1. Acessar: https://github.com/DanielSWolf/rhubarb-lip-sync/releases
2. Baixar: `rhubarb-lip-sync-VERSION-windows.zip`
3. Extrair em: `D:\Blender\blenderscripts\tools\rhubarb\`
4. Verificar: `D:\Blender\blenderscripts\tools\rhubarb\rhubarb.exe` existe

### Passo 2: Configurar ElevenLabs
1. Criar conta em: https://elevenlabs.io
2. Copiar API Key: Profile → API Key
3. Adicionar no arquivo `.env` do projeto (criado automaticamente pelo script)

### Passo 3: Executar setup
```powershell
# No PowerShell, na pasta do projeto:
cd D:\Blender\blenderscripts
python scripts\utils\elevenlabs_voice_gen.py --setup
```

---

## 🔄 WORKFLOW POR EPISÓDIO

### Para cada novo episódio:

```
PASSO 1: Escrever diálogo
  → Criar: audio/scripts/ep0X_dialogo.txt

PASSO 2: Gerar vozes (fora do Blender, no terminal)
  → python scripts/utils/elevenlabs_voice_gen.py --ep 01
  → Resultado: audio/raw/boomer_ep01.wav + kev_ep01.wav

PASSO 3: Gerar dados de lip sync (no terminal)
  → python scripts/utils/rhubarb_runner.py --ep 01
  → Resultado: audio/lipsync/boomer_ep01.json + kev_ep01.json

PASSO 4: Aplicar no Blender (dentro do Blender)
  → Abrir script: scripts/youtube/boomer_kev_ep01.py
  → Ele importa automaticamente os WAVs e os JSONs
  → Lip sync aplicado como shape keys nos personagens

PASSO 5: Renderizar
  → Ctrl+F12 → render com áudio sincronizado
```

---

## 📊 QUALIDADE DE OUTPUT ESPERADA

| Componente | Qualidade |
|-----------|----------|
| Voz ElevenLabs | ⭐⭐⭐⭐⭐ Ultra-realista |
| Análise Rhubarb | ⭐⭐⭐⭐ Muito precisa |
| Shape Keys cartoon | ⭐⭐⭐⭐ Excelente para o estilo |
| Sincronização total | ⭐⭐⭐⭐ Profissional |
| Resultado final | 🏆 Nível de estúdio de animação |

---

## 💡 DICA — Voices do ElevenLabs para os Personagens

### Vozes recomendadas (testar e escolher):
**Para Boomer (grave/velho):**
- `Charlie` — voz masculina grave e casual
- `George` — ton mais sério e authoritative
- `Brian` — americano, grave

**Para Kev (jovem/energético):**
- `Liam` — jovem e expressivo
- `Will` — casual e animado
- `Josh` — energético

> 💡 Dica: Você pode criar vozes CUSTOMIZADAS no ElevenLabs fazendo upload
> de 1-3 minutos de áudio com a voz que você quer clonar.
> Isso garante que o Boomer e o Kev tenham vozes únicas e exclusivas.

---

*Pipeline de Áudio v1.0 | Felipe Gouveia Studio Python 3D*
