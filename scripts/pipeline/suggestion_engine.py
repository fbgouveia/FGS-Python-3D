"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: suggestion_engine.py (Pré-Produção)                ║
║   Função: Motor de Sugestão de Retenção Visual (Análise)     ║
║           Ouve o upload (Áudio ou Vídeo), decodifica a       ║
║           intensidade e sugere a estratégia visual ideal:    ║
║           B-Roll Tela Cheia, VFX Overlay ou Mixado.          ║
╚══════════════════════════════════════════════════════════════╝

USO (Fora do Blender, roda como backend Python puro):
  from suggestion_engine import RetentionSuggestionEngine
  engine = RetentionSuggestionEngine()

  sugestao = engine.analisar_upload(
      tipo_upload="video_talking_head", 
      densidade_texto="alta", 
      emocao_predominante="ansiedade"
  )
  print(sugestao)
"""

class RetentionSuggestionEngine:
    """
    O cérebro de análise pré-script. Ele roda antes do Blender abrir.
    Ele analisa o briefing/upload do usuário e propõe a melhor estratégia
    de neuromarketing para o projeto.
    """

    def __init__(self):
        self.estrategias = {
            "FULL_BROLL": "B-Rolls 3D em Tela Cheia",
            "VFX_OVERLAY": "Efeitos VFX Overlay sobre o Vídeo Real",
            "MIXADO": "Mix Dinâmico (Corte Seco B-Roll + VFX Flutuante)"
        }

    def analisar_upload(self, tipo_upload: str, densidade_texto: str, emocao_predominante: str) -> dict:
        """
        Calcula a melhor estratégia com base em como o cérebro humano
        processa informações (Neuromarketing FGS).
        
        tipo_upload: "audio_only" | "video_talking_head" | "acao_real"
        densidade_texto: "alta" (muita fala, conceitos chatos) | "baixa" (pausas, lentidão)
        emocao_predominante: "tristeza", "tensao", "motivacao", "educativo", "alerta"
        """
        print("\n🧠 Analisando Upload: Motor de Neuromarketing Ativado...\n")
        
        sugestao = "MIXADO"
        justificativa = ""
        acao_blender = ""

        # REGRA 1: Uploads de Áudio exigem invenção total de tela
        if tipo_upload == "audio_only":
            sugestao = "FULL_BROLL"
            justificativa = "Como temos apenas o áudio (ex: Locução off ou Podcast), precisamos cobrir 100% da tela para prender a atenção. Sugiro B-Rolls metafóricos em Tela Cheia."
            acao_blender = "Usar template `TN21 (broll_generator.py)` em série."

        # REGRA 2: Vídeos "Talking Head" (Pessoa falando para a câmera)
        elif tipo_upload == "video_talking_head":
            
            # Se o texto é muito denso ou "chato", não podemos tirar muito a 
            # pessoa da tela para não perder a autoridade humana (Eye-Contact).
            if densidade_texto == "alta":
                if emocao_predominante in ["alerta", "tensao", "motivacao"]:
                    sugestao = "MIXADO"
                    justificativa = "TEXTO DENSO + TENSÃO: Manter o rosto do locutor para prender a atenção pelos olhos, mas intercalar com Cortes Secos de B-Rolls a cada 3 segundos para resetar o padrão mental do usuário. Além disso, adicionar Partículas (VFX Overlay) saltando da tela para ancorar os pontos altos."
                    acao_blender = "Cortes para `broll_generator.py` + Sobreposição de Alpha VFX `vfx_engine.py` (faíscas/flame no fundo)."
                
                else: 
                    # Exemplo: vídeo longo e calmo da psicóloga explicando Depressão
                    sugestao = "VFX_OVERLAY"
                    justificativa = "TEXTO DENSO + CALMA: Não podemos cortar a tela cheia abruptamente para B-Rolls pesados. Vamos manter o rosto amigável da Psicóloga, mas 'invocar' hologramas 3D suaves e partículas flutuando O LADO dela (VFX Overlay no Blender com fundo transparente)."
                    acao_blender = "Motor gerar objetos com material transparente flutuando e renderizar em vídeo transparente (.webm ou PNG Sequence) para sobrepor no editor."

            # Se o texto é lento, podemos criar clipes lindos
            elif densidade_texto == "baixa":
                sugestao = "FULL_BROLL"
                justificativa = "FALAS LENTAS: Cérebro do usuário do TikTok perde o foco em 2 segundos se não houver movimento. A Psicóloga fala devagar. Solução: Inserir B-Rolls 3D pesados e lindos tomando a tela toda enquanto ela fala para estimular os olhos."
                acao_blender = "Usar fortemente cenas do `scene_factory.py` (Ex: Laboratório ou Surreal)."

        # REGRA 3: Vídeos de Ação/Movimento Real (Ex: Mãe caminhando no parque gravando)
        elif tipo_upload == "acao_real":
            sugestao = "VFX_OVERLAY"
            justificativa = "O usuário já tem estímulo visual real (cenários, luz natural do vídeo). Adicionar mais B-Rolls em 3D seria poluir. Sugiro apenas 'VFX Overlay' (textos flutuantes, partículas sutis) para modernizar o que ela gravou."
            acao_blender = "Render de `vfx_engine.py` (Rains, Sparkles, UI Elements) em Alpha."

        else:
            justificativa = "Análise padrão para formato híbrido dinâmico."

        # --- Formulação do Retorno (Output para a Interface Visual) ---
        resultado = {
            "Upload Detectado": tipo_upload.upper().replace("_", " "),
            "Estratégia Recomendada": self.estrategias[sugestao],
            "Por Que Funciona (Neuromarketing)": justificativa,
            "Plano de Ação para o Blender": acao_blender
        }

        self._imprimir_tabela(resultado)
        return resultado

    def _imprimir_tabela(self, res: dict):
        print("+" + "-"*78 + "+")
        for k, v in res.items():
            print(f"| {k.ljust(76)} |")
            # Divide o valor longo em várias linhas
            palavras = v.split()
            linha_atual = ""
            for p in palavras:
                if len(linha_atual) + len(p) + 1 > 74:
                    print(f"|   {linha_atual.ljust(74)} |")
                    linha_atual = p
                else:
                    linha_atual += " " + p if linha_atual else p
            print(f"|   {linha_atual.ljust(74)} |")
            print("+" + "-"*78 + "+")

# Teste local automático quando chamarmos por python directly
if __name__ == "__main__":
    engine = RetentionSuggestionEngine()
    
    # Simulação: A mãe do Felipe (Psicóloga) gravou um reels no consultório sentada 
    # Ela fala termos técnicos e densos sobre bloqueio emocional (Tensão/Alerta).
    
    engine.analisar_upload(
        tipo_upload="video_talking_head",
        densidade_texto="alta",
        emocao_predominante="alerta"
    )

    print("\n")
    # Simulação 2: Locução de Áudio de fundo sobre Paz Interior (Lento)
    engine.analisar_upload(
        tipo_upload="audio_only",
        densidade_texto="baixa",
        emocao_predominante="terapia"
    )
