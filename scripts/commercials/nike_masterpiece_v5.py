# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: nike_masterpiece_v5.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   THE GLOBAL CREATIVE ARCHITECT — Felipe Gouveia Studio     ║
║   Script: nike_masterpiece_v5.py                            ║
║   Standard: Nike Global Elite (PHOTOREAL / CYCLES / AgX)    ║
║   Versão: 5.0.0 (Masterpiece Protocol)                      ║
╚══════════════════════════════════════════════════════════════╝

Este script é o resultado da revisão completa por todos os agentes.
Abandona o EEVEE para usar o motor CYCLES (Padrão Cinema).
Implementa materiais PBR avançados, iluminação de estúdio física
e um roteiro cinematográfico de 180 frames.
"""

import bpy
import os
import sys
import math
from mathutils import Vector, Color

# --- 1. CONFIGURAÇÃO DE AMBIENTE (Architect) ---
BASE_DIR = r"D:\Blender\blenderscripts"
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders", "finals")

os.makedirs(OUTPUT_DIR, exist_ok=True)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from materials_library import MaterialLibrary
from render_manager import RenderManager

# --- 2. PROTOCOLO DE LIMPEZA E ESTÉTICA (Director) ---
def setup_masterpiece_world():
    print("🌍 [Architect/Director] Configurando Mundo para Realismo Absoluto...")
    scene = bpy.context.scene
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'
    
    # Mundo Escuro Premium com IBL (Image Based Lighting) simulado
    world = bpy.data.worlds.new("FGS_Elite_World")
    scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    bg = nodes.get("Background")
    bg.inputs['Color'].default_value = (0.015, 0.015, 0.02, 1)
    bg.inputs['Strength'].default_value = 0.2

def clear_all():
    if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# --- 3. SELEÇÃO DO PRODUTO (Smart Hero) ---
def get_hero(path):
    print(f"📦 [Architect] Caçando o Herói (Nike) em {path}")
    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.objects = data_from.objects

    hero = None
    for obj in data_to.objects:
        if obj is not None and obj.type == 'MESH':
            if "Plane" in obj.name or "Sun" in obj.name or "Camera" in obj.name:
                continue
            bpy.context.collection.objects.link(obj)
            hero = obj
            break
    
    if not hero:
        raise ValueError("Nike não encontrado.")

    bpy.context.view_layer.objects.active = hero
    hero.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    hero.location = (0, 0, 0)
    
    # Ajustar materiais para PBR Realista
    lib = MaterialLibrary()
    mat_nike = lib.metal(cor=(0.8, 0.8, 0.9), roughness=0.1, variacao="nike_premium")
    # Tentar aplicar materiais baseados em partes (se houver slots)
    if hero.data.materials:
        hero.data.materials[0] = mat_nike
    else:
        hero.data.materials.append(mat_nike)
        
    return hero

# --- 4. CENÁRIO DE ESTÚDIO (Lighting Specialist) ---
def setup_surreal_studio():
    print("✨ [Lighting] Construindo Estúdio Cinematográfico...")
    
    # Chão de Reflexo Molhado
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0,0,-0.02))
    floor = bpy.context.active_object
    floor.name = "Hero_Stage"
    mat_floor = bpy.data.materials.new("FGS_Polished_Asphalt")
    mat_floor.use_nodes = True
    bsdf = mat_floor.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.005, 0.005, 0.005, 1)
    bsdf.inputs['Roughness'].default_value = 0.08
    bsdf.inputs['Metallic'].default_value = 0.5
    floor.data.materials.append(mat_floor)

    # Iluminação de 3 Pontos FÍSICA (Cycles)
    # 1. Key Light (Softbox Gigante)
    bpy.ops.object.light_add(type='AREA', location=(-4, -4, 5))
    key = bpy.context.active_object
    key.data.energy = 2000 # Watts reais
    key.data.size = 3
    key.rotation_euler = (math.radians(35), 0, math.radians(-45))

    # 2. Rim Light (Delineador de Silhueta Blue Tech)
    bpy.ops.object.light_add(type='AREA', location=(4, 4, 3))
    rim = bpy.context.active_object
    rim.data.energy = 3000
    rim.data.size = 2
    rim.data.color = (0.4, 0.6, 1.0)
    rim.rotation_euler = (math.radians(45), 0, math.radians(135))

    # 3. Fill Light (Suavizador Orange Warm)
    bpy.ops.object.light_add(type='AREA', location=(0, 6, 2))
    fill = bpy.context.active_object
    fill.data.energy = 800
    fill.data.size = 5
    fill.data.color = (1.0, 0.8, 0.6)

# --- 5. ROTEIRO E ANIMAÇÃO (Animation Choreographer / Director) ---
def animate_scene(target):
    print("🎥 [Animation/Director] Executando Roteiro Cinematográfico...")
    
    cam_data = bpy.data.cameras.new("MasterCam")
    cam_data.lens = 100 # Macro Prime
    cam_data.dof.use_dof = True
    cam_data.dof.aperture_fstop = 2.0
    cam_data.dof.focus_object = target
    
    cam_obj = bpy.data.objects.new("MasterCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 120 # 5 segundos de pura qualidade
    
    # Roteiro: Movimento de "Dolly Zoom" Heroico
    # Frame 1: Close Macro
    cam_obj.location = (2, -4, 0.5)
    cam_obj.keyframe_insert(data_path="location", frame=1)
    
    # Frame 120: Revelação Total
    cam_obj.location = (6, -8, 1.5)
    cam_obj.keyframe_insert(data_path="location", frame=120)

    # Constraints de Direção
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

# --- 6. GESTÃO DE RENDER (Render Manager / Architect) ---
def execute_render():
    print("🚀 [RenderManager] Iniciando Motor CYCLES (Padrão Masterpiece)...")
    rm = RenderManager()
    
    output_file = os.path.join(OUTPUT_DIR, "nike_masterpiece_v5.mp4")
    
    # Preset Comercial (Cycles + Denoise)
    rm.preset("comercial", output=output_file, frame_inicio=1, frame_fim=120)
    
    # Ativar Pós-Produção Ninja
    rm.ativar_compositing(estilo="cinematico")
    rm.ativar_motion_blur(shutter=0.5)
    
    print(f"\n🎬 Iniciando Renderização Final: {output_file}")
    print("   Prepare o café. Qualidade cinema exige tempo...")
    bpy.ops.render.render(animation=True, write_still=True)

# --- 7. ORQUESTRAÇÃO FINAL ---
def produce():
    try:
        clear_all()
        setup_masterpiece_world()
        
        nike = get_hero(os.path.join(ASSETS_DIR, "nike.blend"))
        
        setup_surreal_studio()
        animate_scene(nike)
        
        execute_render()
        
    except Exception as e:
        print(f"❌ [Masterpiece Fail] Erro: {e}")

if __name__ == "__main__":
    produce()
