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

1. **A Fase Zero: Sugestão de Retenção (Motor de Neuromarketing)**:
   - O Python puramente analisa o upload do criador: *É "Talking Head"? A profissional fala devagar? É um assunto tenso?*. 
   - Essa fase toma a decisão executiva de Arte:
      - **"Full B-Roll"** (Corta o vídeo para tela cheia 3D, para compensar falas longas).
      - **"Mixado/Cortes Rápidos"** (Não remove o rosto do profissional de saúde porque é denso e importante o contato visual, mas interpola com B-Rolls rápidos).
      - **"VFX Overlay"** (Mantém a psicóloga no vídeo e renderiza o Blender com fundo Transparente – *Alpha Channel* – para chover partículas e objetos brilhantes literalmente do lado dela na edição).
2. **Painel Front-End (Visual Timeline)**:
   - *O pulo do gato para o produto vendável:* O sistema não apenas cospe uma lista de textos. O Front-End exibirá uma **Timeline de Vídeo Interativa**.
   - No painel, o usuário verá o vídeo original rolando e marcações (ex: `00:01:24 - Inserir VFX Ansiedade [Alpha]`).
   - *Sugestões Secundárias da IA (The Editor's Copilot):* A IA nunca dá apenas uma opção cravada em pedra. Se o usuário clicar na marcação "VFX Ansiedade", a IA sugere 3 alternativas para aquele momento exato (ex: 1. `Panela de Pressão Tremendo`, 2. `Relógio Tic-Tac Acelerado`, 3. `Termômetro Estourando`). O criador pode alterar a sugestão com um clique, e o sistema refaz a aprovação.
3. **Ingestão Auditiva e Transcrição Cênica**: 
   - O sistema usa a transcrição de áudio não apenas para a leganda, mas para mapear o *Timing Perfeito* usando os carimbos de tempo (timestamps) de cada palavra-chave falada.
4. **LLM Concept Simplifier**:
   - Um prompt do GPT/Claude altamente treinado analisa a frase.
   - *Prompt interno:* "Você é um diretor de arte popular. Transforme o conceito X num objeto cotidiano único isolado num fundo escuro sendo afetado pelas leis da física."
5. **Conversão para Código Python (Blender)**:
   - A resposta da LLM é passada para o gerador de scripts (baseado nos templates).
   - O código invoca os scripts do **Eixo 1**: `scene_factory.py`, `vfx_engine.py` e `animation_engine.py`.
6. **Auto-Compositing e Render Final VSE (A Resposta do "Vale a Pena?")**:
   - SIM, o Blender renderizará TUDO! Esse é o diferencial de um SaaS.
   - Nós não vamos obrigar a psicóloga a baixar arquivos soltos `.mp4` com Alpha transparente e abrir o Premiere.
   - O Blender possui o **Video Sequence Editor (VSE)** e o **Compositor Nodes**. 
   - **Como Funciona:** O Python vai colocar o vídeo original (`minhamae.mp4`) na Faixa 1 da timeline do Blender. Nas Faixas de cima, o Python joga e encaixa perfeitamente nos milissegundos exatos todos os VFX e B-Rolls gerados pela Fase 3.
   - **O Retorno:** O servidor devolve um ÚNICO vídeo `.mp4` 100% finalizado com o rosto da sua mãe, o fundo com faíscas renderizadas e os cortes secos em 3D e áudios SFX tudo colado.

## 4. O Sistema "Loop 3 Segundos"
B-Rolls não precisam de direção de arte de longa-metragem. Eles precisam ser cirúrgicos.
O template básico gerará arquivos que podem atuar em Background ou ser loops em tela cheia renderizados pelo `render_manager` no preset "tiktok".

## 5. Passos de Desenvolvimento Necessários
Para viabilizar isso, precisamos adicionar na nossa `Biblioteca de Assets` (Eixo 2) e Eixo 6 (Pipeline):
1. **Coleção de Props Universais:** Lâmpada, Cérebro de brinquedo, Balão, Imã, Corrente, Ampulheta.
2. **O Suggestion Engine:** O código `scripts/pipeline/suggestion_engine.py` (Criado ✅).
3. **Motor Timeline Assembly:** Um novo módulo no `render_manager` que cria canais de composição para vídeos de fundo.
4. **Template TN21 - `broll_generator.py`:** Um script que baseia a lógica e injeta os assets (Criado ✅).
