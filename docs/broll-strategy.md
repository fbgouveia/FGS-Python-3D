# 🎥 FGS B-Roll Engine: Estratégia e Implementação

> Este documento define a lógica do Módulo Criador de B-Rolls para vídeos de "Talking Head" (câmera única).
> Foco no nicho de conteúdo complexo (Psicologia, Medicina, Advocacia, Educação).

## 1. O Problema
Criadores de conteúdo sem equipe multicâmera sofrem com **baixa retenção** devido à monotonia visual. 
Quando recorrem a bancos de imagem genéricos ou IAs geradoras de vídeo, esbarram no **"Efeito Abstrato"**: as IAs tentam ilustrar sentimentos (ansiedade, trauma, direito contratual) com metáforas etéreas, hiper-subjetivas ou psicodélicas que o público leigo (scrolling no shorts/reels) não consegue decodificar em 1 segundo.

## 2. A Solução: The FGS B-Roll Engine
Um pipeline que converte conceitos complexos em **Metáforas Concretas de Objeto 3D**.
A regra visual de ouro do B-Roll Engine é a **Ancoragem Literal**.

### Comparativo Módulo de Decisão (LLM)
| Áudio / Conceito | IA Genérica (Subjetivo ❌) | FGS B-Roll Engine (Concreto ✅) | Componentes do Eixo 1 Utilizados |
| :--- | :--- | :--- | :--- |
| **"Efeito Burnout"** | Humanoide de luz derretendo em um salão infinito | Uma lâmpada queimando com um estalo e fumaça | `prop("lampada") + vfx.faiscas() + anim.escalar()` |
| **"Ansiedade Acumulada"** | Redemoinho de cores frenéticas | Uma panela de pressão tremendo violentamente | `prop("panela") + anim.tremer()` |
| **"Trauma de Infância"** | Boneca rachada num fundo musical sombrio | Um bloco de montar (Lego) faltando na base | `prop("bloco_brinquedo")` |
| **"Dependência Emocional"**| Correntes se dissolvendo | Dois ímãs tentando ser separados e soltando faíscas | `prop("ima") + anim.mover() + vfx.faiscas()` |

## 3. O Fluxo de Funcionamento (Pipeline)

1. **Ingestão Auditiva**: 
   - Usuário faz upload do trecho do vídeo ou áudio (ex: 5-10 segundos da psicóloga falando).
   - O sistema transcreve usando OpenAI Whisper.
2. **LLM Concept Simplifier**:
   - Um prompt do GPT/Claude altamente treinado analisa a frase.
   - *Prompt interno:* "Você é um diretor de arte popular. Transforme o conceito X num objeto cotidiano único isolado num fundo escuro sendo afetado pelas leis da física."
3. **Conversão para Código Python (Blender)**:
   - A resposta da LLM é passada para o gerador de scripts (baseado nos templates).
   - O código invoca os scripts do **Eixo 1**: `scene_factory.py`, `vfx_engine.py` e `animation_engine.py`.
4. **Renderização VSE**:
   - O Blender renderiza a cena.
   - O `audio_manager.py` pode incluir efeitos sonoros impactantes (*tick-tock* para ansiedade, vidro quebrando, *woosh*).

## 4. O Sistema "Loop 3 Segundos"
B-Rolls não precisam de direção de arte de longa-metragem. Eles precisam ser cirúrgicos.
O template de B-Roll gerará um arquivo de 72 frames (3 segundos a 24fps) desenhado para ser repetido em loop pelo editor se necessário. Tudo renderizado pelo `render_manager` no preset "tiktok" ou "youtube".

## 5. Passos de Desenvolvimento Necessários
Para viabilizar isso, precisamos adicionar na nossa `Biblioteca de Assets` (Eixo 2):
1. **Coleção de Props Universais:** Lâmpada, Cérebro de brinquedo, Balão, Imã, Corrente, Ampulheta, Engrenagens, Copo de Água.
2. **Template TN21 - `broll_generator.py`:** Um script que serve de base para o LLM injetar as animações e objetos nele.
