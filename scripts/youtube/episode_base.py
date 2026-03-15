# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: episode_base.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Template: episode_base.py                                 ║
║   Nicho: Podcast & Entrevistas 3D (YouTube, Spotify)        ║
║                                                              ║
║   Descrição: Template base genérico para séries de podcast   ║
║              com mesa redonda, multi-câmera dinâmica e       ║
║              importação de sons automatizada.               ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from camera_system import CameraSystem
from lighting_system import LightingSystem
from materials_library import MaterialLibrary
from render_manager import RenderManager

# ==============================================================================
# 🎯 CONFIGURAÇÕES DO PODCAST
# ==============================================================================
CONFIG = {
    "show_name": "podcast_generic_ep1",
    "theme": "modern_dark", # 'modern_dark', 'neon_synth', 'warm_wood'
    "guests": 2,            # Número de convidados (máx 3)
    "duration_sec": 10.0,
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

def build_studio():
    # Mesa
    bpy.ops.mesh.primitive_cylinder_add(radius=2.0, depth=0.1, location=(0, 0, 0.8))
    table = bpy.context.active_object
    table.name = "Table_Main"
    
    mat_lib = MaterialLibrary()
    mat_table = mat_lib.get_material("Madera Escura" if CONFIG["theme"] == "warm_wood" else "Metal Escovado")
    table.data.materials.append(mat_table)
    
    # Cadeiras e Marcações de Personagem (Mocks de Posicionamento)
    angles = [math.radians(a) for a in [0, 180, 90, 270]][:CONFIG["guests"]]
    
    for i, angle in enumerate(angles):
        r = 1.8 # raio da cadeira
        x = math.cos(angle) * r
        y = math.sin(angle) * r
        
        # Cadeira
        bpy.ops.mesh.primitive_cube_add(size=0.6, location=(x, y, 0.3))
        chair = bpy.context.active_object
        chair.name = f"Chair_{i+1}"
        
        # Microfone
        mic_x = math.cos(angle) * (r - 0.6)
        mic_y = math.sin(angle) * (r - 0.6)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.3, location=(mic_x, mic_y, 1.0))
        mic = bpy.context.active_object
        mic.name = f"Mic_{i+1}"
        mic.data.materials.append(mat_table) # reusar metal

def build_camera_system():
    cam_sys = CameraSystem()
    
    # Câmera Master (Abre a cena)
    cam_master, _ = cam_sys.adicionar_camera("Cam_Master", pos_inicial=(0, -5, 2.5), alvo=(0,0,1))
    
    # Câmeras de Cada Host/Convidado (Over the shoulder)
    cams = [cam_master]
    angles = [math.radians(a) for a in [0, 180, 90, 270]][:CONFIG["guests"]]
    
    for i, angle in enumerate(angles):
        r_cam = 2.5
        # Câmera olhando para o participante oposto
        x = math.cos(angle - math.pi) * r_cam
        y = math.sin(angle - math.pi) * r_cam
        
        tx = math.cos(angle) * 1.5
        ty = math.sin(angle) * 1.5
        
        cam_guest, _ = cam_sys.adicionar_camera(f"Cam_Focus_{i+1}", pos_inicial=(x, y, 1.6), alvo=(tx, ty, 1.2), lentes=85)
        cams.append(cam_guest)
        
    return cam_sys, cams

def build_scene():
    print(f"\\n🎙️ CONSTRUINDO ESTÚDIO: {CONFIG['show_name'].upper()}")
    clean_scene()
    
    total_frames = int(CONFIG['duration_sec'] * CONFIG['fps'])
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_frames
    
    # Iluminação
    ls = LightingSystem()
    preset = "LUXO" if CONFIG["theme"] == "modern_dark" else "TECNOLOGIA" if CONFIG["theme"] == "neon_synth" else "CALIDO"
    ls.aplicar_preset(preset)
    
    # Estúdio e Móveis
    build_studio()
    
    # Sistema de Câmeras multi-cam
    cam_sys, cameras = build_camera_system()
    
    # Criação da Master Track de edição (cortes automáticos)
    # Ex: troca de câmera a cada 3 segundos
    print("🎬 Programando Cortes de Câmera Automáticos (Multi-Cam)...")
    
    cut_frames = range(1, total_frames, int(CONFIG['fps'] * 3))
    for frame in cut_frames:
        chosen_cam = random.choice(cameras)
        # O Blender permite marcar as câmeras ao longo do timeline (Bind Camera to Markers)
        marker = bpy.context.scene.timeline_markers.new(name=f"Cut_{chosen_cam.name}", frame=frame)
        marker.camera = chosen_cam
    
    print("✅ Podcast Studio pronto!")


def render_project():
    print("\\n🎬 INICIANDO RENDER DO EPISÓDIO...")
    rm = RenderManager()
    rm.setup_engine(CONFIG['render']['engine'])
    rm.setup_resolution(CONFIG['render']['resolution'])
    rm.setup_quality(CONFIG['render']['quality'])
    
    out_dir = rm.render_animation(CONFIG['show_name'])
    print(f"\\n🎉 RENDER CONCLUÍDO! Salvo em: {out_dir}")

if __name__ == "__main__":
    build_scene()
    
    if "--render" in sys.argv:
        render_project()
    else:
        renders_dir = os.path.join(os.path.dirname(os.path.dirname(SCRIPT_DIR)), "renders", CONFIG["show_name"])
        os.makedirs(renders_dir, exist_ok=True)
        blend_path = os.path.join(renders_dir, f"{CONFIG['show_name']}.blend")
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"💾 Arquivo .blend salvo em: {blend_path}")
