# 📚 Felipe Gouveia Studio — Guia do Usuário
## Como Usar os Scripts Python no Blender

> Guia completo para iniciantes. Sem enrolação, passo a passo.

---

## 🔧 O QUE VOCÊ PRECISA TER INSTALADO

1. **Blender 4.0 ou superior** — [Download gratuito em blender.org](https://www.blender.org/download/)
2. **Os scripts deste projeto** — Pasta `D:\Blender\blenderscripts\`

---

## 🚀 COMO RODAR UM SCRIPT PYTHON NO BLENDER

### Passo 1 — Abrir o Blender
- Abra o Blender normalmente
- Uma cena com cubo, câmera e luz vai aparecer (não se preocupe com isso)

### Passo 2 — Ir para a aba Scripting
- No topo da janela, clique na aba **"Scripting"**
- (É a última aba na barra superior)
- A tela vai mudar para mostrar um editor de texto

### Passo 3 — Criar um novo script
- No editor de texto (painel cinza no canto), clique em **"New"**
- Um arquivo vazio vai aparecer

### Passo 4 — Colar o script
- **Copie TODO** o script Python que eu gerei para você
- **Cole** no editor de texto do Blender (Ctrl+V)

### Passo 5 — Executar o script
- Clique no botão **▶ "Run Script"** (ou pressione Alt+P)
- Aguarde a execução (pode levar alguns segundos)
- O Blender vai processar e criar tudo automaticamente
- Uma mensagem de sucesso vai aparecer no Console

### Passo 6 — Ver o resultado
- Clique na aba **"Layout"** (primeira aba no topo)
- Você vai ver a cena criada pelo script
- Use o **botão do meio do mouse** para orbitar e ver de ângulos diferentes

---

## 🎬 COMO RENDERIZAR O VÍDEO

### Método 1 — Render Completo (vídeo final)
1. No menu superior: **Render → Render Animation** (ou pressione Ctrl+F12)
2. Aguarde o render (tempo varia: de 1 min a horas, dependendo da qualidade)
3. O arquivo MP4 vai ser salvo automaticamente na pasta configurada

### Método 2 — Render de um Frame (para testar)
1. No menu superior: **Render → Render Image** (ou pressione F12)
2. Uma janela vai abrir mostrando como ficou esse frame
3. Para salvar: na janela do render, **Image → Save As**

### Método 3 — Preview Rápido (viewport)
1. Com a cena aberta, pressione a tecla **Numpad 0** (ver pela câmera)
2. No header da viewport, clique no ícone de esfera sombreada
3. Selecione **"Rendered"** para ver preview em tempo real

---

## ⚙️ ONDE FICAM OS ARQUIVOS RENDERIZADOS

Os scripts do FGS salvam automaticamente em:
- **Drafts (testes):** `D:\Blender\blenderscripts\renders\drafts\`
- **Finals (entrega):** `D:\Blender\blenderscripts\renders\finals\`

---

## 🎯 TIPOS DE SCRIPT DISPONÍVEIS

| Pasta | Para que serve | Tempo de render |
|-------|---------------|----------------|
| `scripts/commercials/` | Comerciais de produto | 5-30 minutos |
| `scripts/youtube/` | Animações para canal | 10-60 minutos |
| `scripts/shorts/` | Reels e Shorts (vertical) | 2-10 minutos |
| `scripts/utils/` | Ferramentas base (não executar direto) | — |

---

## 🆘 PROBLEMAS COMUNS E SOLUÇÕES

### ❌ "Python: Script failed — Check console for details"
**Causa:** Erro no script.
**Solução:** 
1. Vá em **Window → Toggle System Console** (abre um terminal)
2. Leia a mensagem de erro
3. Me envie o erro e eu corrijo o script

### ❌ O render está muito lento
**Causa:** Usando CPU em vez de GPU, ou qualidade muito alta.
**Solução:**
1. Vá em **Edit → Preferences → System**
2. Em "Cycles Render Devices", selecione sua GPU (NVIDIA/AMD)
3. Marque o dispositivo como ativo
4. Feche e tente renderizar novamente

### ❌ O Blender travou durante o render
**Causa:** Memória RAM insuficiente ou cena muito pesada.
**Solução:**
1. Feche outros programas abertos
2. No script, reduza o parâmetro `QUALIDADE_RENDER = "preview"`
3. Tente renderizar um frame único primeiro (F12) para testar

### ❌ Não vejo nada na cena após rodar o script
**Causa:** O script pode ter rodado mas a visualização está errada.
**Solução:**
1. Pressione **Numpad 0** para ver pela câmera
2. Pressione **Numpad .** para centralizar na seleção
3. Pressione **A** para selecionar tudo, depois **Numpad .**

---

## 💡 DICAS PARA INICIANTES

### Navegação no Blender
| Ação | Tecla/Mouse |
|------|------------|
| Orbitar (rodar a vista) | Botão do meio do mouse + arrastar |
| Zoom | Scroll do mouse |
| Pan (mover a vista) | Shift + botão do meio + arrastar |
| Ver pela câmera | Numpad 0 |
| Centralizar a cena | Numpad . (no teclado numérico) |
| Tela cheia | Ctrl + Espaço |

### Atalhos Úteis
| Ação | Tecla |
|------|-------|
| Render imagem | F12 |
| Render animação | Ctrl+F12 |
| Executar script | Alt+P |
| Desfazer | Ctrl+Z |
| Salvar arquivo | Ctrl+S |

---

## 📂 ESTRUTURA DO PROJETO (Referência Rápida)

```
D:\Blender\blenderscripts\
│
├── scripts/            ← Scripts Python prontos para usar
│   ├── commercials/    ← Comerciais de produto
│   ├── youtube/        ← Animações para YouTube  
│   ├── shorts/         ← Reels e Shorts
│   └── utils/          ← Ferramentas (não executar direto)
│
├── renders/            ← Vídeos e imagens renderizadas
│   ├── drafts/         ← Testes e aprovações
│   └── finals/         ← Entregas finais
│
├── references/         ← Coloque aqui suas imagens/vídeos de referência
│   ├── images/
│   └── videos/
│
├── motions/            ← Arquivos de captura de movimento
│   ├── bvh/            ← Mocap .bvh
│   └── mixamo/         ← Animações do Mixamo .fbx
│
└── characters/         ← Personagens reutilizáveis
```

---

## 🔄 WORKFLOW RESUMIDO

```
1️⃣  Você tem uma ideia ou referência visual
        ↓
2️⃣  Me envia a imagem/vídeo + descreve o que quer
        ↓
3️⃣  Eu gero o script Python completo
        ↓
4️⃣  Você abre o Blender → Scripting → New → Cola → Run Script
        ↓
5️⃣  Blender cria a cena automaticamente
        ↓
6️⃣  Você revisa → Render → Render Animation
        ↓
7️⃣  ✅ Vídeo pronto na pasta /renders/
```

---

*Felipe Gouveia Studio Python 3D | Versão 1.0.0*
