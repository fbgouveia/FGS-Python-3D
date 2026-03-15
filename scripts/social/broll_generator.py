# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: broll_generator.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Template TN21: Gerador de B-Rolls Concretos               ║
║                                                              ║
║   Descrição: Gera cenas curtas (3s) em loop traduzindo       ║
║   termos subjetivos em objetos físicos usando metáforas.     ║
║   Formato vertical (9:16) ideal para TikTok/Reels.           ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import pathlib as _pathlib
import bpy

# Path resolution dinâmica — sem hardcode, funciona em qualquer máquina
_utils = str(_pathlib.Path(__file__).resolve().parents[1] / "utils")
if _utils not in sys.path:
    sys.path.insert(0, _utils)

from materials_library import MaterialLibrary
from character_factory import CharacterFactory
from camera_system import CameraSystem
from lighting_system import LightingSystem
from render_manager import RenderManager
from scene_factory import SceneFactory
from vfx_engine import VFXEngine
from animation_engine import AnimationEngine
from transitions_engine import TransitionsEngine
import audio_manager as audio

# ==============================================================================
# CONFIGURAÇÕES DO B-ROLL (A serem preenchidas pelo usuário ou via LLM)
# ==============================================================================

CONCEITO = "ansiedade" 
# Exemplos: "ansiedade", "burnout", "dependencia_emocional", "clareza", "bloqueio_criativo"

# ==============================================================================

def limpar_cena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def criar_broll_concreto(conceito: str):
    """
    Traduz um conceito psicológico/abstrato em uma cena 3D literal (Eixo 3).
    """
    print(f"\n🎬 INICIANDO GERAÇÃO DE B-ROLL: Conceito '{conceito.upper()}'")
    
    limpar_cena()

    # 1. Carregar Motores Universais
    lib = MaterialLibrary()
    cameras = CameraSystem()
    luzes = LightingSystem()
    scene_f = SceneFactory(lib)
    vfx = VFXEngine(fps=24)
    anim = AnimationEngine(fps=24)
    trans = TransitionsEngine(fps=24)
    renderer = RenderManager(fps=24)

    # 2. Setup Base (Fundo Preto para total foco no objeto/mensagem)
    scene_f.criar("abstract_dark")

    # 3. Metáforas e Regras (The B-Roll Engine Core)
    if conceito == "ansiedade":
        # Ansiedade = Panela de pressão tremendo no escuro + luz instável
        
        # Prop: Um cilindro com 'tampa' simulando uma panela de ferro
        panela = scene_f._cilindro("Panela_Pressao", posicao=(0, 0, 0.5), raio=0.3, altura=0.6)
        lib.aplicar(panela, lib.metal("titanio"))
        
        # Animação
        anim.tremer(panela, intensidade=0.15, eixos=(0, 1, 2)) # Tremendo
        
        # Efeitos: Fumaça saindo violentamente de cima
        vfx.fumaca(panela, densidade=0.8, cor=(0.8, 0.8, 0.8), escala=0.5, nome="VFX_Vapor")
        
        # Iluminação de Alerta
        luzes.ponto_emissivo("Luz_Alerta", cor=(1.0, 0.1, 0.0), intensidade=10.0, posicao=(1, 0, 1))
        luzes.ring_light(posicao=(0, -2, 1), raio=0.8)

        # Audio
        # audio.sfx("audio/sfx/teacup_rattle.wav", frame=1)
        # audio.sfx("audio/sfx/steam_hiss.wav", frame=1)

    elif conceito == "burnout":
        # Burnout = Objeto elétrico pegando fogo e quebrando
        
        # Prop: Uma lâmpada superdimensionada
        lampada = scene_f.prop("garrafa", posicao=(0, 0, 0.5), escala=2.0)
        lampada.name = "Corpo_Burnout"
        lib.aplicar(lampada, lib.vidro())
        
        # Animação/VFX
        vfx.faiscas(lampada, quantidade=150, velocidade=5.0)
        vfx.fogo(lampada, escala=0.5, intensidade=1.5)
        
        luzes.preset("horror")  # Luz focada e dramática de baixo

    elif conceito == "bloqueio_criativo":
        # Bloqueio Criativo = Um peso/corrente de ferro numa engrenagem que não gira
        
        # Prop: Um bloco maciço de aço
        bloco = scene_f._cubo("Bloqueio", posicao=(0,0,1.5), escala=(0.8, 0.8, 0.8))
        lib.aplicar(bloco, lib.metal("chumbo"))
        
        # Física: Bloco cai pesadamente e não sai mais do chão
        anim.cair_kikando(bloco, altura_inicial=5.0, chao_z=0.4, quiques=1)

        luzes.preset("drama")

    else:
        # Padrão: Uma esfera branca limpa flutuando (ideia neutra)
        esfera = scene_f._cubo("Ideia", posicao=(0,0,1), escala=(0.4, 0.4, 0.4))
        anim.flutuar(esfera, amplitude=0.4)
        luzes.preset("produto_comercial")


    # 4. Cinematic Camera Setup (Vertical 9:16)
    cam = cameras.criar_camera("Broll_Cam", (0, -4, 1.2), (90, 0, 0), lente_mm=50)
    anim.mover(cam, inicio=(0, -4, 1.2), fim=(0, -3, 1.2), frames=(1, 72))

    # 5. Sistema de Transição Consciente de Clima (Context-Aware Transition)
    # Detecta o peso emocional do tema e aplica a entrada e saída ideais e subconscientes
    luz_primaria = bpy.data.objects.get("Luz_Alerta") # Exemplo pegando luz principal

    if conceito in ["ansiedade", "burnout", "panico"]:
        trans.aplicar_saida("alerta", cam, luz_principal=luz_primaria, frame_inicio=60, frame_fim=72)
    elif conceito in ["bloqueio_criativo", "luto", "depressao"]:
        trans.aplicar_saida("reflexivo", cam, luz_principal=luz_primaria, frame_inicio=60, frame_fim=72)
    else:
        trans.aplicar_saida("solucao", cam, luz_principal=luz_primaria, frame_inicio=60, frame_fim=72)

    # 6. Render Settings (Para Shorts/TikTok)
    renderer.aplicar_preset("short_reel")
    renderer.configurar_saida(
        caminho=f"D:/Blender/blenderscripts/renders/BROLL_{conceito.upper()}.mp4",
        frame_fim=72 # 3 segundos perfeitos de B-Roll 
    )

    print(f"\n✅ Setup Completo do B-Roll: {conceito.upper()}")
    print("   Para renderizar execute: python scripts/social/broll_generator.py no Blender")
    
# ==============================================================================

if __name__ == "__main__":
    # Suporte para execução via CLI (Orquestrador Ghost)
    # Formato: blender -b -P script.py -- conceito
    if "--" in sys.argv:
        idx = sys.argv.index("--")
        args = sys.argv[idx + 1:]
        if len(args) > 0:
            CONCEITO = args[0]
            
    criar_broll_concreto(CONCEITO)
    print("✨ Sistema rodou com sucesso!")
