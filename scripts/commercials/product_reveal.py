# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: product_reveal.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: product_reveal.py (TN2)                           ║
║   Função: Revelação Cinematográfica de Produto              ║
╚══════════════════════════════════════════════════════════════╝

Este template cria uma cena onde um produto premium é revelado 
do escuro com luzes dramáticas e névoa (volumetrics).
"""

import bpy
import os
import sys

# Garantir importação dos utilitários
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))

try:
    from materials_library import MaterialLibrary
    from character_factory import CharacterFactory
    from scene_factory import SceneFactory
    from audio_manager import AudioManager
    from animation_engine import AnimationEngine
    from scene_setup import (
        setup_scene,
        limpar_cena,
        adicionar_luz_sol,
        configurar_camera_padrao,
    )
except ImportError:
    # Fallback se executado de outro diretório
    sys.path.append("D:/Blender/blenderscripts/scripts/utils")
    from materials_library import MaterialLibrary
    from character_factory import CharacterFactory
    from scene_setup import setup_scene, limpar_cena, adicionar_luz_sol, configurar_camera_padrao

def setup_volumetric_world():
    """Configura o mundo com volume para efeitos de luz dramáticos."""
    scene = bpy.context.scene
    scene.world.use_nodes = True
    nodes = scene.world.node_tree.nodes
    links = scene.world.node_tree.links
    
    # Limpar nós
    nodes.clear()
    
    # Criar novos nós
    node_out = nodes.new('ShaderNodeOutputWorld')
    node_vol = nodes.new('ShaderNodeVolumePrincipled')
    
    # Configurar Volume
    node_vol.inputs['Density'].default_value = 0.02
    node_vol.inputs['Anisotropy'].default_value = 0.7
    
    # Lincar
    links.new(node_vol.outputs['Volume'], node_out.inputs['Volume'])

def criar_luz_reveal(nome, posicao, cor=(1, 1, 1), energia=500):
    """Cria uma luz de destaque para o reveal."""
    light_data = bpy.data.lights.new(name=nome, type='SPOT')
    light_data.energy = energia
    light_data.color = cor
    light_data.spot_size = 0.7
    light_data.spot_blend = 1.0
    
    light_obj = bpy.data.objects.new(name=nome, object_data=light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = posicao
    return light_obj

def run_reveal():
    print("🎬 [CLARA GOUVEIA] Iniciando Template: Luxury Product Reveal (TN2) Ultra-Premium")
    
    # 1. Setup Base
    limpar_cena()
    setup_scene(fps=24, duracao_segundos=10)
    
    mat_lib = MaterialLibrary()
    factory = CharacterFactory(mat_lib)
    scene_factory = SceneFactory(mat_lib)
    audio_manager = AudioManager()
    anim_engine = AnimationEngine()
    
    # 2. Cenário Imperial (Luxury Showroom)
    # Clara: "O ambiente comunica status antes mesmo do produto ser visto."
    print("   🏙️ Building Luxury Showroom...")
    scene_factory.criar_cenario("luxury_showroom")
    
    # 3. O Protagonista (Leão Premium - O Maestre Hero)
    # Clara: "O arquétipo do soberano gera confiança imediata."
    produto = factory.criar_preset(
        "LEAO_PREMIUM", 
        posicao=(0, 0, 0.3), # No pódio
        escala=[1.2, 1.2, 1.2],
        humor="serio"
    )
    
    # 4. Iluminação de Revelação (Gaze Trigger)
    # Luz Principal (Key) - Ativada via Fade
    luz_main = criar_luz_reveal("Luz_Key", (-4, -4, 5), cor=(1, 0.95, 0.8), energia=0)
    
    # Rim Light (Contorno) - Ativada desde o início
    criar_luz_reveal("Luz_Rim", (2, 4, 3), cor=(0.7, 0.8, 1.0), energia=1200)
    
    # 5. Áudio Sincronizado (Neuromarketing: Sound Priming)
    if os.path.exists("D:/Lorena/assets/audio/bgm/luxury_loop.mp3"):
        audio_manager.adicionar_bgm("D:/Lorena/assets/audio/bgm/luxury_loop.mp3", volume=0.4)
    
    # SFX: O "Sparkle" no momento do reveal (Frame 24 - 1s)
    if os.path.exists("D:/Lorena/assets/audio/sfx/sparkle_reveal.wav"):
        audio_manager.adicionar_sfx("D:/Lorena/assets/audio/sfx/sparkle_reveal.wav", frame_inicio=24)
        
    # 6. Animação de Câmera e Revelação (Kinetic Engagement)
    # Iniciar Órbita Profissional
    cam_obj = bpy.context.scene.camera
    anim_engine.orbitar(cam_obj, alvo=(0, 0, 1), raio=7.0, altura=2.0, frame_fim=240, voltas=0.3)
    
    # Keyframe de Energia da Luz (O Reveal)
    luz_main.data.keyframe_insert(data_path="energy", frame=1)
    bpy.context.scene.frame_set(48) # 2 segundos
    luz_main.data.energy = 2500
    luz_main.data.keyframe_insert(data_path="energy", frame=48)
    
    # Bloom e Volumetrics para o "Glow" do luxo
    setup_volumetric_world()
    
    # 7. Configuração de Render (Valuation de Software)
    bpy.context.scene.render.engine = 'CYCLES'
    if hasattr(bpy.context.scene, "cycles"):
        bpy.context.scene.cycles.samples = 256 # Qualidade Cinema
        bpy.context.scene.cycles.use_denoising = True
    
    print("✅ [LORENA GOUVEIA] Cena validada e pronta para o terminal de render!")

if __name__ == "__main__":
    run_reveal()
