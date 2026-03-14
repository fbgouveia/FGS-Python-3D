# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: logo_reveal.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Template TN14: Logo Reveal Cinematográfico                ║
║                                                              ║
║   Descrição: Reveal dramático de logo construído com        ║
║              fragmentos/partículas que se unem, ou material  ║
║              emergindo do chão com forte iluminação de aro.  ║
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
from animation_engine import AnimationEngine
from render_manager import RenderManager

CONFIG = {
    "project_name": "fgs_logo_reveal",
    "theme": "premium_metal", # 'premium_metal', 'holographic', 'fire_forge'
    "duration_sec": 7.0,
    "fps": 30,
    "render": {
        "engine": "CYCLES",
        "resolution": "YOUTUBE_4K", 
        "quality": "STANDARD" 
    }
}

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in [bpy.data.materials, bpy.data.cameras, bpy.data.lights]:
        for item in coll:
            coll.remove(item)

def create_logo_mockup():
    """Gera um texto placeholder para o Logo."""
    bpy.ops.object.text_add(location=(-2.5, 0, 0))
    logo = bpy.context.active_object
    logo.name = "Logo_Main"
    
    # Propriedades do Texto 3D
    txt = logo.data
    txt.body = "FGS"
    txt.extrude = 0.2
    txt.bevel_depth = 0.02
    txt.bevel_resolution = 4
    txt.align_x = 'CENTER'
    txt.align_y = 'CENTER'
    
    # Escala e Posicionamento
    logo.scale = (2.0, 2.0, 2.0)
    logo.rotation_euler[0] = math.radians(90) # Em pé
    
    return logo

def build_scene():
    print(f"\\n💫 INICIANDO TEMPLATE: LOGO REVEAL")
    clean_scene()
    
    total_frames = int(CONFIG['duration_sec'] * CONFIG['fps'])
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_frames
    
    # Piso Refletivo
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1.0))
    piso = bpy.context.active_object
    piso.name = "Floor"
    
    mat_lib = MaterialsLibrary()
    mat_piso = bpy.data.materials.new("Mat_Floor_Reflect")
    mat_piso.use_nodes = True
    bsdf_piso = mat_piso.node_tree.nodes.get("Principled BSDF")
    if bsdf_piso:
        bsdf_piso.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
        bsdf_piso.inputs['Roughness'].default_value = 0.05 # Espelhado
    piso.data.materials.append(mat_piso)
    
    # Iluminação Dramática
    ls = LightingSystem()
    if CONFIG["theme"] == "holographic":
        ls.ponto_focado("Luz_Back", cor=(0, 0.8, 1), intensidade=10.0, raio=0.1, posicao=(0, 3, 0)) # Fundo pra frente
    elif CONFIG["theme"] == "fire_forge":
        ls.ponto_focado("Luz_Back", cor=(1, 0.3, 0), intensidade=15.0, raio=0.1, posicao=(0, 3, 0))
    else:    
        ls.aplicar_preset("LUXO") # Luz de recorte forte (Rim Light)

    # Logo
    logo = create_logo_mockup()
    
    if CONFIG["theme"] == "premium_metal":
        mat_logo = mat_lib.get_material("Titanio Escovado")
    elif CONFIG["theme"] == "holographic":
        vfx = VFXEngine()
        mat_logo = vfx._criar_material_emission("Mat_Holo", cor=(0,1,1), intensidade=5.0)
    elif CONFIG["theme"] == "fire_forge":
        mat_logo = mat_lib.get_material("Ouro")
    
    logo.data.materials.append(mat_logo)
    
    # ================= ANIMAÇÃO DE REVEAL =================
    # Usando o modificador Build para montar o logo polígono a polígono
    # Como texto não suporta build perfeitamente sem converter, vamos coverter para mesh
    bpy.context.view_layer.objects.active = logo
    bpy.ops.object.convert(target='MESH')
    
    bpy.ops.object.modifier_add(type='BUILD')
    build_mod = logo.modifiers["Build"]
    build_mod.frame_start = int(total_frames * 0.1) # Começa aos 10% do vídeo
    build_mod.frame_duration = int(total_frames * 0.5) # Demora metade do vídeo pra montar
    
    # Efeito extra: Logo sai do chão
    bpy.context.scene.frame_set(1)
    logo.location[2] = -2.0
    logo.keyframe_insert(data_path="location", index=2)
    
    bpy.context.scene.frame_set(int(total_frames * 0.7))
    logo.location[2] = 0.0
    logo.keyframe_insert(data_path="location", index=2)
    
    # Múltiplas Faíscas/Partículas "soldando" o logo
    if CONFIG["theme"] in ["premium_metal", "fire_forge"]:
        vfx = VFXEngine()
        ps = vfx.faiscas(logo, quantidade=5000, velocidade=3.0, cor=(1,0.5,0))
        ps.settings.frame_end = build_mod.frame_start + build_mod.frame_duration

    # ================= CAMERA =================
    cam_sys = CameraSystem()
    cam, target = cam_sys.adicionar_camera("Cam_Main", tipo="DOLLY", pos_inicial=(0, -8, 1), alvo=(0,0,0), lentes=75)
    
    # Dolly In dramático
    cam_sys.animar_dolly(cam, inicio=(0, -8, -0.5), fim=(0, -4, 0), start_frame=1, end_frame=total_frames)

    print("✅ Logo Reveal configurado.")

def render_project():
    rm = RenderManager()
    rm.setup_engine(CONFIG['render']['engine'])
    rm.setup_resolution(CONFIG['render']['resolution'])
    rm.setup_quality(CONFIG['render']['quality'])
    out = rm.render_animation(CONFIG['project_name'])
    print(f"🎬 RENDER COMPLETO: {out}")

if __name__ == "__main__":
    build_scene()
    
    if "--render" in sys.argv:
        render_project()
    else:
        renders_dir = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "renders", CONFIG["project_name"])
        os.makedirs(renders_dir, exist_ok=True)
        blend_path = os.path.join(renders_dir, f"{CONFIG['project_name']}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"💾 Arquivo .blend salvo em: {blend_path}")
