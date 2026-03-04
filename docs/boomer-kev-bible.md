# 🐾 BÍBLIA DO PROJETO — BOOMER & KEV
## Série de Animação 3D | Felipe Gouveia Studio Python 3D

> **Conceito:** Dois animais estilizados com comportamento completamente humano,
> co-apresentando um podcast de papo solto, risadas e comentários sobre a vida.
> Puro entretenimento com personalidade forte e identificação imediata.

---

## 🎯 OVERVIEW DA SÉRIE

| Campo | Detalhe |
|-------|---------|
| **Nome** | Boomer & Kev |
| **Formato** | Episódios curtos (30s a 2min) + Shorts (15s) |
| **Plataforma** | YouTube + Instagram Reels + TikTok |
| **Gênero** | Comédia / Talk Show / Podcast estilizado |
| **Tom** | Descontraído, engraçado, surpreendente, relatable |
| **Público** | 18-40 anos, digitais nativos, amantes de humor inteligente |
| **Frequência** | A definir (semanal recomendado) |
| **Idioma** | Português BR (com potencial multi-idioma para white-label) |

---

## 🦁 PERSONAGEM 1 — BOOMER

### Identidade
- **Nome completo:** Boomer
- **Espécie:** Urso / Bear estilizado (definição visual: corpo de urso, postura e expressões 100% humanas)
- **Apelido:** "O velho"
- **Arquétipo:** O cara experiente que fica surpreso com o mundo atual

### Personalidade
| Traço | Expressão |
|-------|-----------|
| **Nostálgico** | Sempre traz referências "da sua época" |
| **Desconfiado de tecnologia** | Reage com confusão a coisas modernas |
| **Genuíno** | Risada aberta, sem filtro, expressivo |
| **Teimoso mas adorável** | Discorda de tudo mas com carisma |

### Aparência Física (Parâmetros para o Script Python)
```python
BOOMER = {
    "especie": "urso",
    "cor_corpo": (0.45, 0.28, 0.15),      # Marrom médio
    "cor_focinho": (0.65, 0.45, 0.28),    # Marrom claro
    "cor_orelha_interna": (0.7, 0.4, 0.3), # Rosado
    "altura_relativa": 1.0,                # Maior que o Kev
    "proporcao_corpo": "ombros_largos",    # Corpo de urso humanizado
    "tamanho_cabeca": 0.38,               # Grande (mais expressivo)
    "olhos": {
        "cor": (0.15, 0.08, 0.04),        # Castanho escuro
        "tamanho": "grande",               # Expressivos
        "sobrancelha": "grossa"            # Para expressões dramáticas
    },
    "roupa_padrao": "camisa_xadrez_aberta", # Estilo despojado/casual
    "acessorio": "copo_de_cafe"            # Sempre com café (prop recorrente)
}
```

### Maneirismos de Animação
- **Quando ri:** Corpo todo balança para trás, patas batem na mesa
- **Quando discorda:** Cruza os braços, olha de soslaio com uma sobrancelha levantada
- **Quando está confuso:** Franze o focinho, inclina a cabeça para o lado
- **Quando concorda:** Aponta para o Kev com entusiasmo, acena com a cabeça vigorosamente
- **Gesto característico:** Bate com a palma na mesa quando faz um ponto importante

### Ângulo de Câmera Padrão
- Câmera ligeiramente abaixo da linha dos olhos (autoridade, presença)
- Screen Left (lado esquerdo da tela — convenção para o personagem "estabelecido")

---

## 🦊 PERSONAGEM 2 — KEV

### Identidade
- **Nome completo:** Kev
- **Espécie:** Raposa / Fox estilizado (corpo de raposa, gestos e expressões 100% humanos)
- **Apelido:** "O moderno"
- **Arquétipo:** O jovem antenado que tenta explicar o mundo atual pro Boomer

### Personalidade
| Traço | Expressão |
|-------|-----------|
| **Hiperativo** | Fala rápido, gesta muito, se anima com tudo |
| **Antenado** | Sempre tem a referência mais atual |
| **Provocador** | Adora zoar o Boomer com carinho |
| **Impulsivo** | Reage antes de pensar, fica envergonhado depois |

### Aparência Física (Parâmetros para o Script Python)
```python
KEV = {
    "especie": "raposa",
    "cor_corpo": (0.85, 0.35, 0.08),      # Laranja raposa
    "cor_focinho": (0.95, 0.85, 0.75),    # Creme/off-white
    "cor_orelhas": (0.85, 0.35, 0.08),    # Mesmo laranja
    "ponta_orelha": (0.05, 0.05, 0.05),  # Pretas nas pontas
    "altura_relativa": 0.88,              # Mais baixo e esguio que Boomer
    "proporcao_corpo": "esbelto",         # Corpo de raposa ágil
    "tamanho_cabeca": 0.33,              # Menor, mais elegante
    "olhos": {
        "cor": (0.1, 0.55, 0.2),         # Verde vivo
        "tamanho": "amêndoa",             # Characteristic fox eyes
        "sobrancelha": "fina_expressiva"  # Ágil nas expressões
    },
    "roupa_padrao": "camiseta_hoodie",    # Estilo streetwear
    "acessorio": "fones_no_pescoco"       # Fones de ouvido pendurados (prop recorrente)
}
```

### Maneirismos de Animação
- **Quando ri:** Riso explosivo e curto, às vezes cai para o lado
- **Quando explica algo:** Gesticula com as patas para todos os lados, muito expressivo
- **Quando provoca:** Sorriso de lado, sobrancelha levantada, olha para a câmera
- **Quando se surpreende:** Orelhas vão para cima, olhos arregalados, boca aberta
- **Gesto característico:** Aponta para o próprio peito quando faz uma afirmação ousada

### Ângulo de Câmera Padrão
- Câmera na linha dos olhos (igualdade, juventude)
- Screen Right (lado direito da tela — convenção para o personagem "dinâmico")

---

## 🎙️ O CENÁRIO — PODCAST STUDIO "THE DEN"

### Descrição
Um estúdio de podcast improvisado mas aconchegante — tipo aquele cantinho que todo mundo que curte podcast tem em casa. Vibe de "começamos do zero com o que tínhamos".

### Elementos FIXOS (sempre presentes em TODOS os episódios)
- Mesa de madeira rústica no centro
- Dois microfones condensadores com braço articulado (em frente a cada personagem)
- Headphones sobre a mesa (não nos ouvidos — eles falam ao vivo)
- Luz de anel (ring light) atrás de cada personagem (efeito visual marcante)
- Backdrop: parede de tijolos aparentes com alguns objetos aleatórios
- "ON AIR" sinal luminoso vermelho na parede (light prop recorrente)
- Alguns livros empilhados, plantas, copos de bebida

### Elementos VARIÁVEIS (mudam por episódio/tema)
- Objetos temáticos na mesa (relacionados ao assunto do episódio)
- Decoração de fundo (pode ter banner de "episódio X")
- Cor da iluminação de fundo (azul padrão, mas ajustável)

### Paleta de Cores do Cenário
```python
CENARIO_PODCAST = {
    "parede_fundo": (0.18, 0.14, 0.11),     # Tijolo escuro / charcoal
    "mesa": (0.35, 0.22, 0.12),              # Madeira rústica
    "iluminacao_bg": (0.05, 0.15, 0.45),    # Azul meia-luz (mood podcast)
    "ring_light_boomer": (0.9, 0.85, 0.7),  # Luz quente
    "ring_light_kev": (0.7, 0.85, 0.9),     # Luz fria (contraste)
    "microfone": (0.05, 0.05, 0.05),        # Preto
    "sign_on_air": (0.9, 0.1, 0.05),        # Vermelho neon
    "accents": (0.7, 0.55, 0.2)             # Dourado nos detalhes
}
```

### Câmera Master (Referência para Script)
```python
CAMERAS_PODCAST = {
    # Câmera 1 — Wide (Establishing)
    "WS": {
        "posicao": (0, -6, 1.5),
        "alvo": (0, 0, 1.2),
        "fov": 60,
        "uso": "Primeira cena / resolução / reação dupla"
    },
    
    # Câmera 2 — OTS Boomer (vemos o Kev, câmera atrás do Boomer)
    "OTS_BOOMER": {
        "posicao": (-1.5, -3.5, 1.8),
        "alvo": (1.2, 0, 1.5),
        "fov": 45,
        "uso": "Quando Kev está falando"
    },
    
    # Câmera 3 — OTS Kev (vemos o Boomer, câmera atrás do Kev)
    "OTS_KEV": {
        "posicao": (1.5, -3.5, 1.8),
        "alvo": (-1.2, 0, 1.5),
        "fov": 45,
        "uso": "Quando Boomer está falando"
    },
    
    # Câmera 4 — MCU Boomer
    "MCU_BOOMER": {
        "posicao": (-1.8, -2.5, 1.8),
        "alvo": (-1.0, 0, 1.6),
        "fov": 35,
        "uso": "Reação / expressão do Boomer"
    },
    
    # Câmera 5 — MCU Kev
    "MCU_KEV": {
        "posicao": (1.8, -2.5, 1.8),
        "alvo": (1.0, 0, 1.6),
        "fov": 35,
        "uso": "Reação / expressão do Kev"
    },
    
    # Câmera 6 — Insert / Cutaway (mesa, microfone, objeto)
    "CUTAWAY": {
        "posicao": (0, -1.5, 0.8),
        "alvo": (0, 0.5, 0.5),
        "fov": 40,
        "uso": "Detalhe cômico / objeto relevante"
    }
}
```

---

## 📋 ESTRUTURA PADRÃO DE EPISÓDIO (30 SEGUNDOS)

### Shot List Template — Boomer & Kev (30s)

```
BOOMER & KEV — EPISÓDIO [X]: "[TÍTULO]"
Duração: 30 segundos | 720 frames @ 24fps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CENA 01 | WS | 0:00-0:03 (72 frames)
Câmera: Wide Shot — o estúdio completo
Ação: Sign "ON AIR" acende, câmera revela os dois sentados
Boomer: Ajustando o microfone
Kev: Fazendo sinal de "joia" para câmera
Áudio: Música de tema animada (3s)
━━━━━

CENA 02 | MCU BOOMER | 0:03-0:06 (72 frames)
Câmera: Medium Close-Up — Boomer centralizado
Ação: Boomer fala para o microfone com expressão séria
Fala: [fala inicial do episódio]
Maneirismo: Sobrancelha levantada, pata no copo de café
Áudio: Voz do Boomer + música baixa de fundo
━━━━━

CENA 03 | REACT KEV | 0:06-0:08 (48 frames)
Câmera: MCU Kev — Reaction Shot
Ação: Kev reage com expressão exagerada
Maneirismo: Orelhas disparam para cima, olhos arregalados
Áudio: Efeito sonoro de surpresa (subtil)
━━━━━

CENA 04 | OTS BOOMER | 0:08-0:12 (96 frames)
Câmera: Over The Shoulder — câmera atrás do Boomer vendo o Kev
Ação: Kev gesticula e explica algo animadamente
Maneirismo: Patas se movem muito, inclinado para frente
Áudio: Kev falando (principal)
━━━━━

CENA 05 | MCU BOOMER | 0:12-0:15 (72 frames)
Câmera: MCU Boomer
Ação: Boomer ouve cétic o, cruza os braços, balança a cabeça
Maneirismo: Sobrancelha franzida, olha de lado para a câmera
Áudio: Hmm / resmungo característico do Boomer
━━━━━

CENA 06 | OTS KEV | 0:15-0:18 (72 frames)
Câmera: Over The Shoulder — câmera atrás do Kev vendo o Boomer
Ação: Boomer faz uma observação bombástica ou absurda
Maneirismo: Se inclina para frente, apontando para o microfone
Áudio: Boomer falando (principal)
━━━━━

CENA 07 | CUTAWAY | 0:18-0:20 (48 frames)
Câmera: Insert — detalhe cômico na mesa
Ação: Objeto relevante para o episódio / Copo de café do Boomer tremendo
Áudio: Efeito sonoro exagerado (cômico)
━━━━━

CENA 08 | REACT BOOMER | 0:20-0:22 (48 frames)
Câmera: ECU Boomer — Extreme Close-Up no rosto
Ação: Boomer ri absurdamente / pisada forte na mesa
Maneirismo: Todo o corpo balança, pata na mesa
Áudio: Risada do Boomer (sincronizada com animação)
━━━━━

CENA 09 | WS DUPLO | 0:22-0:25 (72 frames)
Câmera: Wide Shot — ambos em cena juntos
Ação: Os dois rindo juntos, atmosfera relaxada
Maneirismo: Kev cai de lado, Boomer chora de rir
Áudio: Música volta mais forte
━━━━━

CENA 10 | MCU KEV | 0:25-0:27 (48 frames)
Câmera: MCU Kev — olhando para câmera
Ação: Kev diz a frase de encerramento / gancho para próximo ep
Maneirismo: Pisca para a câmera, sorriso de lado
Áudio: Kev quebrando a quarta parede com a frase final
━━━━━

CENA 11 | WS - OUTRO | 0:27-0:30 (72 frames)
Câmera: Wide Shot suave recuando
Ação: Sign "ON AIR" apaga, os dois acenam
Áudio: Tema musical sobe e fecha
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL: 11 CENAS | 30 SEGUNDOS | 720 FRAMES
```

---

## 🎨 LINGUAGEM VISUAL DA SÉRIE

### Estilo
- **Render:** EEVEE Next (velocidade para série) com toon shading suave
- **Contorno:** Linha fina de contorno (Freestyle ou Grease Pencil) para estilo cartoon/animação
- **Sombras:** Suaves, sem sombras duras — estilo animação de TV
- **Iluminação:** Ring lights criam identidade visual do podcast

### Regras de Câmera
- **NUNCA** câmera completamente estática — sempre microanimação (respira, leve oscillação)
- **SEMPRE** DOF ativo — o que não está em foco fica levemente desfocado
- **Cortes** em ritmo com a fala/música (edição musical)
- Câmera **levemente abaixo** do nível dos personagens (os torna mais imponentes e presentes)

### Assinatura Visual da Série
- Sign "ON AIR" que aparece/some em toda abertura/encerramento
- Cores dos ring lights (quente=Boomer, frio=Kev) criam identidade visual imediata
- Microfones sempre visíveis — ancoram no contexto de podcast
- Mesa de madeira como "território" compartilhado dos dois

---

## 🔄 VARIAÇÕES DE EPISÓDIO

### Tipos de episódio possíveis:

| Tipo | Descrição | Duração |
|------|-----------|---------|
| **Debate** | Os dois discutem um tema, opiniões opostas | 30s-2min |
| **Entrevista** | Um convidado (novo personagem) no estúdio | 60s-5min |
| **Top List** | "Top 5 coisas que o Boomer/Kev faz" | 30s-1min |
| **Reação** | Os dois assistem algo (tela no set) e reagem | 30s-1min |
| **Short Viral** | Um único momento cômico, cortado no pico | 15s |
| **Extended** | Papo longo, múltiplos temas | 5-10min |

---

## 📐 CONSISTÊNCIA ENTRE EPISÓDIOS (Regras Imutáveis)

1. **Boomer sempre à esquerda** na tela (screen left)
2. **Kev sempre à direita** na tela (screen right)
3. **Microfones sempre** na posição correta na frente de cada um
4. **Sign "ON AIR"** sempre na mesma posição na parede
5. **Proporção dos personagens** nunca muda (Boomer maior, Kev menor)
6. **Cores dos personagens** nunca mudam entre episódios
7. **A mesa é sempre a mesma** (objetos podem mudar, mesa não)
8. **Ring lights** sempre presentes (cores podem variar por episódio especial)

---

## 🚀 PRÓXIMOS PASSOS — PRODUÇÃO

### Fase A: Setup dos Personagens (Scripts Python)
- [ ] `boomer_character.py` — Criar o personagem Boomer completo
- [ ] `kev_character.py` — Criar o personagem Kev completo
- [ ] `podcast_studio.py` — Criar o cenário completo

### Fase B: Cenas Base
- [ ] `podcast_cameras.py` — Setup de todas as 6 câmeras
- [ ] `podcast_lighting.py` — Ring lights + iluminação ambiente
- [ ] `podcast_props.py` — Mesa, microfones, objetos fixos

### Fase C: Primeiro Episódio
- [ ] Definir tema do Episódio 1
- [ ] Gerar pré-roteiro completo
- [ ] Gerar script Python do episódio completo
- [ ] Render e revisão
- [ ] Ajustes e entrega final

---

*Projeto: Boomer & Kev | Felipe Gouveia Studio Python 3D*  
*Bíblia v1.0 — Base para toda a série*
