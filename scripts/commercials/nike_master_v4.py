"""
╔══════════════════════════════════════════════════════════════╗
║   THE GLOBAL CREATIVE ARCHITECT — Felipe Gouveia Studio     ║
║   Script: nike_unlimited_standard_v4.py                     ║
║   Standard: Nike Global (Surreal/Heroic/AgX High-End)        ║
║   Versão: 4.0.0 (Master Production Protocol)                ║
╚══════════════════════════════════════════════════════════════╝

Este script implementa o ápice da automação FGS. Resolve o erro 
de importação de 'Planes' genéricos e cria um ambiente surreal
de estúdio high-end com volumetria e reflexos Apple-standard.
"""

import bpy
import os
import sys
import math
from mathutils import Vector, Color

# --- 1. CONFIGURAÇÃO DE INFRAESTRUTURA ---
BASE_DIR = r"D:\Blender\blenderscripts"
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders", "finals")

os.makedirs(OUTPUT_DIR, exist_ok=True)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# --- 2. PROTOCOLO DE LIMPEZA E ESTÉTICA ---
def setup_world_elite():
    """Configura o mundo AgX com profundidade espacial."""
    print("🌍 [Architect] Configurando Mundo AgX Deep Space...")
    bpy.context.scene.display_settings.display_device = 'sRGB'
    bpy.context.scene.view_settings.view_transform = 'AgX'
    bpy.context.scene.view_settings.look = 'AgX - High Contrast'
    
    # Mundo Escuro Premium
    world = bpy.data.worlds.new("FGS_Global_World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs['Color'].default_value = (0.01, 0.01, 0.012, 1) # Azul escuro profundo
    bg.inputs['Strength'].default_value = 0.5

def clear_orphan_data():
    """Limpeza total para garantir integridade."""
    if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights]:
        for item in block: block.remove(item)

# --- 3. SMART IMPORT (Nike Hero Selection) ---
def import_nike_hero(path):
    print(f"📦 [Architect] Executando Smart Import: {path}")
    if not os.path.exists(path): raise FileNotFoundError(path)

    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.objects = data_from.objects

    hero_obj = None
    possible_heroes = []

    for obj in data_to.objects:
        if obj is not None and obj.type == 'MESH':
            # Ignorar planos genéricos que costumam ser backgrounds do próprio arquivo
            if "Plane" in obj.name or "Ground" in obj.name:
                continue
            bpy.context.collection.objects.link(obj)
            possible_heroes.append(obj)

    # Escolher o objeto com maior volume (Geralmente o produto)
    if possible_heroes:
        possible_heroes.sort(key=lambda o: o.dimensions.length, reverse=True)
        hero_obj = possible_heroes[0]
        # Deletar os outros que foram linkados por engano
        for o in possible_heroes[1:]:
            bpy.data.objects.remove(o, do_unlink=True)
    else:
        # Fallback: Se só sobrou o Plane ou nada, importar o que tiver com 'model' no nome
        with bpy.data.libraries.load(path) as (data_from, data_to):
            for name in data_from.objects:
                if "model" in name.lower() or "nike" in name.lower():
                    data_to.objects = [name]
                    break
        if data_to.objects:
            obj = data_to.objects[0]
            bpy.context.collection.objects.link(obj)
            hero_obj = obj

    if not hero_obj: raise ValueError("Nenhum Herói (Nike) encontrado.")

    # Normalização
    bpy.context.view_layer.objects.active = hero_obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    hero_obj.location = (0, 0, 0)
    hero_obj.scale = (1, 1, 1)
    
    print(f"✨ [Architect] Herói Identificado: '{hero_obj.name}'")
    return hero_obj

# --- 4. AMBIENTE SURREAL (Floating Podium + Atmosphere) ---
def create_surreal_podium():
    """Cria uma base de reflexo infinita e atmosfera volumétrica."""
    print("✨ [Architect] Criando Atmosfera Surreal (Reflections + Volume)...")
    
    # Chão de Reflexo Infinito
    bpy.ops.mesh.primitive_circle_add(radius=10, fill_type='NGON', location=(0,0,-0.05))
    floor = bpy.context.active_object
    floor.name = "Infinity_Floor"
    
    mat = bpy.data.materials.new("FGS_HighGloss_Floor")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1)
    bsdf.inputs['Roughness'].default_value = 0.05
    bsdf.inputs['Specular IOR Level'].default_value = 1.0
    floor.data.materials.append(mat)

    # Cubo de Volume (Atmosfera / God Rays)
    bpy.ops.mesh.primitive_cube_add(size=50, location=(0,0,0))
    volume_box = bpy.context.active_object
    volume_box.name = "Atmosphere_Volume"
    
    v_mat = bpy.data.materials.new("FGS_Atmosphere")
    v_mat.use_nodes = True
    nodes = v_mat.node_tree.nodes
    nodes.clear()
    
    v_node = nodes.new('ShaderNodeVolumePrincipled')
    v_node.inputs['Density'].default_value = 0.015
    v_node.inputs['Anisotropy'].default_value = 0.7
    
    v_out = nodes.new('ShaderNodeOutputMaterial')
    v_mat.node_tree.links.new(v_node.outputs['Volume'], v_out.inputs['Volume'])
    volume_box.data.materials.append(v_mat)

# --- 5. ILUMINAÇÃO INTERNATIONAL STANDARD (High Power) ---
def setup_hero_lighting():
    print("💡 [Architect] Calibrando Iluminação Heróica Direcional...")
    
    # Top Spot (Hero Highlight)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 4))
    top = bpy.context.active_object
    top.data.energy = 5000 # EEVEE Next precisa de valores altos
    top.data.size = 2
    top.data.color = (1, 1, 1)
    
    # Rim Back (Silhouette)
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 1))
    rim = bpy.context.active_object
    rim.data.energy = 8000
    rim.data.size = 5
    rim.data.color = (0.2, 0.5, 1) # Azul Tech
    rim.rotation_euler = (math.radians(-90), 0, 0)

    # Side Key (Texture Detail)
    bpy.ops.object.light_add(type='AREA', location=(-3, 2, 2))
    key = bpy.context.active_object
    key.data.energy = 3000
    key.data.color = (1, 0.4, 0.1) # Laranja Contraste

# --- 6. CÂMERA E ANIMAÇÃO (Newtonian Flow) ---
def animate_production(target):
    print("🎥 [Architect] Orquestrando Movimento de Câmera 85mm...")
    
    cam_data = bpy.data.cameras.new("ProductionCam")
    cam_data.lens = 85
    cam_data.dof.use_dof = True
    cam_data.dof.focus_distance = 5.0
    cam_data.dof.aperture_fstop = 1.8
    
    cam_obj = bpy.data.objects.new("ProductionCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Animação Orbital de Elite
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 240
    
    for f in range(1, 241):
        angle = math.radians((f / 240) * 360)
        dist = 7.0
        cam_obj.location = (dist * math.sin(angle), -dist * math.cos(angle), 1.5)
        # Apontar para o centro
        cam_obj.rotation_euler = (math.radians(80), 0, angle)
        cam_obj.keyframe_insert(data_path="location", frame=f)
        cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)

# --- 7. RENDER FINAL OTIMIZADO ---
def run_master_production():
    try:
        clear_orphan_data()
        setup_world_elite()
        
        # O Coração do Problema: Importar APENAS o Tênis
        nike = import_nike_hero(os.path.join(ASSETS_DIR, "nike.blend"))
        
        create_surreal_podium()
        setup_hero_lighting()
        animate_production(nike)
        
        # Engine Config
        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
        scene.render.resolution_x = 1080
        scene.render.resolution_y = 1920
        scene.render.filepath = os.path.join(OUTPUT_DIR, "nike_master_v4.mp4")
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = 'MPEG4'
        scene.render.ffmpeg.codec = 'H264'
        scene.render.ffmpeg.constant_rate_factor = 'HIGH'
        
        # FX e Compositing
        scene.use_nodes = True
        nodes = scene.node_tree.nodes
        links = scene.node_tree.links
        nodes.clear()
        
        rl = nodes.new('CompositorNodeRLayers')
        glare = nodes.new('CompositorNodeGlare')
        glare.glare_type = 'FOG_GLOW'
        glare.threshold = 0.5
        
        comp = nodes.new('CompositorNodeComposite')
        links.new(rl.outputs['Image'], glare.inputs['Image'])
        links.new(glare.outputs['Image'], comp.inputs['Image'])

        print(f"\n🎬 [Architect] Renderizando Produção de Elite: {scene.render.filepath}")
        bpy.ops.render.render(animation=True, write_still=True)
        print("\n🏆 [Architect] Missão Cumprida.")

    except Exception as e:
        print(f"❌ [Architect] Erro Crítico: {e}")

if __name__ == "__main__":
    run_master_production()
