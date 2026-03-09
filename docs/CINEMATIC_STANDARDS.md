# 🎬 FGS — CINEMATIC PRODUCTION STANDARDS (v1.0)

> **"Não entregamos renders. Entregamos Pixels de Poder."**

Este documento define o que é uma "Cena Perfeita" no Felipe Gouveia Studio. Todo script gerado deve ser auditado contra este padrão.

## 💎 Os 7 Pilares da Perfeição (O Checklist do Diretor)

### 1. BACKGROUND (O Universo)
- **Proporção:** 16:9 (Cinema) ou 9:16 (Social Vertical).
- **Cenário:** Deve existir um ambiente (chão infinito, estúdio, fumaça, partículas).
- **Profundidade:** Uso de névoa (Mist Pass) ou desfoque de fundo (Bokeh) para separar planos.

### 2. OBJECT (O Herói)
- **Integridade:** Escala 1.0, Rotação 0, Origem no Centro.
- **PBR Master:** Materiais procedurais que simulam física real (Anisotropia, Specularity, Clearcoat).
- **Hero Framing:** O objeto deve ocupar o "centro de atenção" áureo.

### 3. LIGHT (A Alma)
- **Espaço AgX:** Obrigatório. Nunca usar tons lavados.
- **Técnica 3-Pontos:** Key (8000W), Fill (3000W), Rim (12000W) — valores para Cycles/AgX.
- **Volumetria:** O ar deve ter "peso". Uso de Princpled Volume para raios de luz.

### 4. MOTION (A Vida)
- **Curva de Animação:** Jamais usar interpolação linear. Usar Bezier ou Inércia Física.
- **Dinamismo:** Se o objeto está parado, a câmera se move. Se o objeto se move, a câmera acompanha.
- **Motion Blur:** Obrigatório para realismo de movimento.

### 5. FEELING (A Emoção)
- **Paleta Narrativa:** Escolher cores que evoquem a marca (ex: Azul Tech, Ouro Luxo).
- **Compositing:** Glare, Lens Distortion e Vignette para esconder a "perfeição matemática" do 3D.

### 6. APPEALING (O Magnetismo)
- **Texturas Táteis:** O espectador deve sentir vontade de tocar.
- **Focal Length:** Usar lentes reais (50mm para natural, 85mm+ para classe, 24mm para drama).

### 7. DESIRE (O Gatilho)
- **Impacto Inicial:** Os primeiros 30 frames devem ser o "Hook".
- **Impressão Residual:** O frame final deve ser o "The End" que deixa o usuário querendo mais.

---

## 🛠️ Fluxo de Trabalho dos Agentes
- **Architect of Desire:** Cria o roteiro magnético.
- **Chief of Neuro-Aesthetics:** Define a estética e as sensações.
- **Global Creative Architect:** Codifica o sistema em Python/Blender.

---
*FGS Cinematic Standards | 2026*
