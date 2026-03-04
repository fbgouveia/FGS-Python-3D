# 🌍 Motor de Localização e Edição Dinâmica de Textos

> "A mágica de transformar ativos globais (Envato/AE) em peças locais customizadas via UI."

## 1. O Problema
O usuário faz o upload de vídeos e a IA sugere um *Lower Third* bonito do pacote Envato (ex: um botão animado do YouTube). O problema é que o arquivo de vídeo (.webm ou .mp4 com Alpha) vem com a palavra fixa em inglês: **"SUBSCRIBE"**. Se o cliente é do Brasil ou Espanha, aquilo quebra a imersão.

Como permitir que o usuário da plataforma edite o texto na web e o Blender renda isso perfeitamente colado na animação gringa?

## 2. A Solução (A Arquitetura Frontend / Backend)

O sistema "SaaS" não editará o pixel do vídeo pre-renderizado. Ele usará a tática do **Corte Camada-Base (Base-Layering)** aliado à **Geração Dinâmica de Texto**.

### Passo A: O Tratamento do Banco de Assets (Única Vez)
Os seus 200GB da Envato possuem os arquivos de projeto (Ex: `.aep` do After Effects) ou versões em branco estruturadas.
1. Nós exportamos os "Lower Thirds" e botões **SEM TEXTO NENHUM**, apenas as caixas, faíscas e animações em vídeo transparente (WebM Alpha). Serão os *Blank Assets*.
2. Armazenamos no nosso servidor.

### Passo B: A Interface Web (O que o Cliente Vê)
Quando o Motor de Neuromarketing sugerir um B-Roll com Call-to-Action (CTA):
1. A interface exibe a Timeline e um "Bloco" visual.
2. O sistema detecta a linguagem do vídeo (pela transcrição do Whisper) e apresenta **Sugestões Clicáveis Automáticas**.
   - *Se áudio em PT-BR:* Mostra botões "Inscreva-se", "Curta", "Siga o Perfil".
   - *Se áudio em EN:* Mostra "Subscribe", "Like", "Follow".
3. **Poder de Edição:** Se o cliente clicar na sugestão, abre um campo de texto (Input Field). Ele pode digitar "Agende sua Consulta" (no caso da Psicóloga). Ele vê o preview na hora usando CSS/React rodando por cima do vídeo em branco.

### Passo C: O Casamento no Blender (O que o Python Faz)
Quando o cliente clica em "Renderizar", o Frontend envia para nossa API Python a String do usuário: `"Agende sua Consulta"`.

Como o Blender processa:
1. Puxa a Faixa 1 (Vídeo do Paciente).
2. Puxa a Faixa 2 (Animação Envato "Blank" em WebM transparente).
3. **Invoca o Motor de Texto (Pillow/PIL ou VSE Text Strip):** O nosso código Python (que faremos futuramente chamado `text_overlay_engine.py`) pega a palavra do usuário, escolhe a fonte premium (Inter, Roboto, Montserrat) que combina com o pacote Envato, transforma em uma imagem PNG transparente em 0.1 milissegundos e sobrepõe na Faixa 3.
4. O VSE do Blender junta o vídeo da Envato com a placa de texto do Python que se move perfeitamente sincronizada em conjunto.

## 3. O Copiloto de Textos (IA Generativa Ativa)
Se o usuário estiver sem criatividade, a interface não apenas traduz. Ela sugere baseada no **Contexto**.

*   **Exemplo:** A Psicóloga fala sobre "Dependência Emocional".
*   O Motor capta o tema. Na hora de sugerir o texto pro B-Roll, a UI exibe 3 caixas clicáveis que fogem do "Inscreva-se" padrão:
    *   *Sugestão 1:* `Liberte-se Hoje`
    *   *Sugestão 2:* `Entenda os Sinais`
    *   *Sugestão 3:* `Agende uma Avaliação`

O usuário clica. O texto é alterado em tempo real no Web App (React). Ele aprova. O Servidor renderiza via Python + Asset Blank + Texto Dinâmico.

## 4. O Sistema HTML 5 (A Carta na Manga)
O usuário relatou ter templates HTML5 maravilhosos. O Frontend (React/Playwright) pode perfeitamente abrir esses HTMLs em um servidor *Headless* invisível (sem tela), injetar o texto alterado pelo usuário via JavaScript nativo, e extrair (renderizar) aquilo em vídeo Alpha só o pedaço animado antes mesmo de mandar pro Blender. Absolutamente vanguardista!
