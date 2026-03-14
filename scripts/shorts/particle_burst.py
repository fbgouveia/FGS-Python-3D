# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: particle_burst.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Template: particle_burst.py                               ║
║   Nicho: Viral Shorts / TikTok / Reels (9:16)               ║
║                                                              ║
║   Descrição: Gera um looping ou explosão hipnotizante de     ║
║              partículas com núcleo emissivo e efeitos de     ║
║              lente, focado no aspecto estético e chamativo.  ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os
import math

# Garantir acesso aos utilitários core
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from camera_system import CameraSystem
from lighting_system import LightingSystem
from materials_library import MaterialsLibrary
from vfx_engine import VFXEngine
from render_manager import RenderManager

# ==============================================================================
# 🎯 CONFIGURAÇÕES DO TEMPLATE (Personalizável pelo Usuário/API)
# ==============================================================================
CONFIG = {
    "project_name": "particle_burst_viral",
    "theme": "nebula",  # Opções: 'nebula', 'cyberpunk', 'gold_rush', 'matrix'
    "duration_sec": 5.0,
    "fps": 30,
    "render": {
        "engine": "CYCLES",  # Cycles para volumetria irrestrita e bloom
        "resolution": "YOUTUBE_SHORTS", # 1080x1920
        "quality": "STANDARD" # 128 samples, Denoise
    }
}

# Temas de Cores Mapeados
THEMES = {
    "nebula":     {"core": (0.2, 0.0, 1.0), "particles": (1.0, 0.1, 0.5), "bg": "LUXO"},
    "cyberpunk":  {"core": (0.0, 1.0, 1.0), "particles": (1.0, 0.0, 0.8), "bg": "TECNOLOGIA"},
    "gold_rush":  {"core": (1.0, 0.8, 0.1), "particles": (1.0, 0.5, 0.0), "bg": "CALIDO"},
    "matrix":     {"core": (0.0, 1.0, 0.0), "particles": (0.1, 0.8, 0.2), "bg": "TECNOLOGIA"}
}

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in [bpy.data.materials, bpy.data.cameras, bpy.data.lights]:
        for item in coll:
            coll.remove(item)

def build_scene():
    print(f"\\n🚀 INICIANDO TEMPLATE VIRAL: {CONFIG['project_name'].upper()}")
    clean_scene()
    
    total_frames = int(CONFIG['duration_sec'] * CONFIG['fps'])
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_frames
    bpy.context.scene.render.fps = CONFIG['fps']

    # Inicializar sistemas
    cam_sys = CameraSystem()
    light_sys = LightingSystem()
    vfx_sys = VFXEngine()

    theme = THEMES.get(CONFIG["theme"], THEMES["nebula"])

    # 1. ILUMINAÇÃO BASE
    print("💡 Configurando Iluminação...")
    light_sys.aplicar_preset(theme["bg"])
    
    # 2. CÂMERA VERTICAL (9:16)
    print("🎥 Configurando Câmera Dinâmica...")
    # Câmera afasta lentamente do núcleo
    cam, target = cam_sys.adicionar_camera("Cam_Main", tipo="DOLLY", 
                                           pos_inicial=(0, -4, 0),
                                           alvo=(0, 0, 0),
                                           lentes=35)
    
    # Animação da câmera (afastar e rotacionar levemente)
    cam_sys.animar_dolly(cam, (0, -4, 0), (0, -7, 2), start_frame=1, end_frame=total_frames)

    # 3. VFX MAIN (Core Pulsante + Explosão Partículas)
    print("✨ Gerando Sistemas de Partículas...")
    
    # Núcleo 
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=0.5, location=(0, 0, 0))
    core = bpy.context.active_object
    core.name = "EnergyCore"
    core_mat = vfx_sys._criar_material_emission("Mat_Core", theme["core"], intensidade=15.0)
    core.data.materials.append(core_mat)
    
    # Animar pulsação do núcleo
    for frame in range(1, total_frames + 1, 15):
        bpy.context.scene.frame_set(frame)
        s = 0.5 + 0.1 * math.sin(frame * 0.2)
        core.scale = (s, s, s)
        core.keyframe_insert(data_path="scale")

    # Explosão de partículas
    # Utilizando faíscas que saem do centro para fora
    spark_ps = vfx_sys.faiscas(objeto=core, quantidade=15000, velocidade=10.0, cor=theme["particles"], nome="Burst_Sparks")
    # Forçar gravidade 0 para expandirem como num vácuo
    spark_ps.settings.gravity = 0.0 
    spark_ps.settings.lifetime = total_frames
    spark_ps.settings.frame_end = int(total_frames * 0.2) # Explode nos primeiros 20% do vídeo
    
    # Adicionar glitter lento para preencher o vazio
    glitter_ps = vfx_sys.glitter(objeto=core, quantidade=5000, cor=(1,1,1), tamanho=0.01, velocidade=2.0)
    glitter_ps.settings.gravity = -0.1 # Levitação leve
    glitter_ps.settings.frame_end = total_frames

    print("✅ Cena construída com sucesso!")

def render_project():
    print("\\n🎬 INICIANDO ENGINE DE RENDER...")
    rm = RenderManager()
    
    rm.setup_engine(CONFIG['render']['engine'])
    rm.setup_resolution(CONFIG['render']['resolution'])
    rm.setup_quality(CONFIG['render']['quality'])
    
    # Adicionar bloom/glow pesado no Compositor
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    
    # Limpa nodes padrão
    for node in tree.nodes:
        tree.nodes.remove(node)
        
    render_layers = tree.nodes.new('CompositorNodeRLayers')
    
    # Glare node para o Bloom
    glare = tree.nodes.new('CompositorNodeGlare')
    glare.glare_type = 'FOG_GLOW'
    glare.quality = 'HIGH'
    glare.threshold = 1.0 # Pega as luzes emissivas
    
    # Correção de cor / saturação
    color_bal = tree.nodes.new('CompositorNodeColorBalance')
    color_bal.lift = [1.0, 1.0, 1.0] 
    color_bal.gamma = [1.1, 1.1, 1.1] 
    color_bal.gain = [1.2, 1.2, 1.2] 
    
    out_node = tree.nodes.new('CompositorNodeComposite')
    
    tree.links.new(render_layers.outputs[0], glare.inputs[0])
    tree.links.new(glare.outputs[0], color_bal.inputs[1]) # Imagem
    tree.links.new(color_bal.outputs[0], out_node.inputs[0])
    
    out_dir = rm.render_animation(CONFIG['project_name'])
    print(f"\\n🎉 RENDER CONCLUÍDO! Salvo em: {out_dir}")

if __name__ == "__main__":
    build_scene()
    
    # Se passado o argumento --render, renderizar automaticamente
    if "--render" in sys.argv:
        render_project()
    else:
        # Apenas salvar o .blend
        renders_dir = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "renders", CONFIG["project_name"])
        os.makedirs(renders_dir, exist_ok=True)
        blend_path = os.path.join(renders_dir, f"{CONFIG['project_name']}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"💾 Arquivo .blend salvo em: {blend_path}")
        print("ℹ️ Dica: rode 'blender -b -P scripts/shorts/particle_burst.py -- --render' para renderizar headless.")
