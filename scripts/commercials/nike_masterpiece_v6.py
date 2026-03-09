"""
╔══════════════════════════════════════════════════════════════╗
║   THE GLOBAL CREATIVE ARCHITECT — Felipe Gouveia Studio     ║
║   Script: nike_masterpiece_v6.py                            ║
║   Concept: "Meshy-Vision" Cinematic Direction               ║
║   Standard: Nike International Elite (CYCLES / AgX / PBR)   ║
║   Versão: 6.0.0 (The Perfect Scene Protocol)                ║
╚══════════════════════════════════════════════════════════════╝

Este script é o ápice da automação FGS. Ele não apenas importa de 
forma inteligente, mas atua como um 'AI Texture Artist', analisando
material slots e injetando Shaders PBR procedurais de altíssimo nível.
"""

import bpy
import os
import sys
import math
from mathutils import Vector, Color

# --- 1. INFRAESTRUTURA FGS ---
BASE_DIR = r"D:\Blender\blenderscripts"
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders", "finals")

os.makedirs(OUTPUT_DIR, exist_ok=True)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from materials_library import MaterialLibrary
from render_manager import RenderManager

# --- 2. PROTOCOLO DE DIRETOR (Reset & World) ---
def setup_director_world():
    print("🌍 [Architect/Neuro] Configurando Universo AgX Realista...")
    scene = bpy.context.scene
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'
    
    # Render Engine: CYCLES Master
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    scene.cycles.adaptive_threshold = 0.01

    # Mundo Profundo
    world = bpy.data.worlds.new("FGS_Masterpiece_World")
    scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    nodes.clear()
    
    node_bg = nodes.new('ShaderNodeBackground')
    node_bg.inputs['Color'].default_value = (0.005, 0.005, 0.01, 1)
    node_bg.inputs['Strength'].default_value = 0.1
    
    node_out = nodes.new('ShaderNodeOutputWorld')
    world.node_tree.links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

def reset_all():
    print("🧹 [Architect] Purificando Cena para Produção...")
    if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Limpar dados órfãos agressivamente
    for b in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.images]:
        for i in b: b.remove(i)

# --- 3. AI MATERIAL ARTIST (The Meshy Layer) ---
def apply_ai_pbr_materials(obj):
    """Analisa slots de materiais e injeta shaders realistas procedurais."""
    print(f"🎨 [Neuro-Aesthetics] Analisando Shaders do Herói: '{obj.name}'")
    lib = MaterialLibrary()
    
    # Mapeamento Inteligente (Desejo de Posse / Tato Visual)
    # Se o objeto não tiver slots, criamos um padrão Elite
    if not obj.data.materials:
        print("   ⚠️ Nenhum slot encontrado. Injetando Material 'Elite Nike Fiber'...")
        mat = lib.metal(cor=(0.8, 0.8, 0.9), roughness=0.1, variacao="nike_fiber_elite")
        obj.data.materials.append(mat)
    else:
        for i, slot in enumerate(obj.data.materials):
            mat_name = slot.name.lower() if slot else f"item_{i}"
            print(f"   🔹 Processando Slot: '{mat_name}'")
            
            # Lógica de Decisão AI
            if any(x in mat_name for x in ["sole", "rubber", "sola", "borracha"]):
                new_mat = lib.borracha(cor=(0.02, 0.02, 0.02), variacao="meshy_rubber")
            elif any(x in mat_name for x in ["logo", "swoosh", "metal", "gloss"]):
                new_mat = lib.metal(cor=(0.9, 0.7, 0.2), roughness=0.05, variacao="meshy_gold_logo")
            elif any(x in mat_name for x in ["fabric", "cloth", "tecido", "mesh"]):
                new_mat = lib.plastico(cor=(0.8, 0.1, 0.05), roughness=0.7, variacao="meshy_fabric")
            else:
                # Default Premium
                new_mat = lib.metal(cor=(0.7, 0.7, 0.75), roughness=0.15, variacao="meshy_default_premium")
            
            obj.data.materials[i] = new_mat

# --- 4. PRODUÇÃO DA CENA (Cinematic Standards) ---
def build_surreal_studio(target):
    print("✨ [Lighting] Construindo Estúdio de Reflexo Molhado...")
    
    # Chão de Porcelanato Negro (Reflexo AgX)
    bpy.ops.mesh.primitive_plane_add(size=50, location=(0,0,-0.01))
    floor = bpy.context.active_object
    floor.name = "Infinity_Mirror_Floor"
    mat = bpy.data.materials.new("FGS_Studio_Mirror")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0, 0, 0, 1)
    bsdf.inputs['Roughness'].default_value = 0.02
    bsdf.inputs['Specular IOR Level'].default_value = 0.8
    floor.data.materials.append(mat)

    # Iluminação de Roteiro (Architect of Desire)
    # 1. Rim Light Blue (O Mistério)
    bpy.ops.object.light_add(type='AREA', location=(4, 5, 2))
    rim = bpy.context.active_object
    rim.data.energy = 5000
    rim.data.size = 5
    rim.data.color = (0.3, 0.6, 1.0)
    rim.rotation_euler = (math.radians(60), 0, math.radians(135))

    # 2. Key Light Warm (O Desejo)
    bpy.ops.object.light_add(type='AREA', location=(-4, -3, 3))
    key = bpy.context.active_object
    key.data.energy = 4000
    key.data.color = (1.0, 0.8, 0.6)
    
    # 3. Top Spot (A Autoridade)
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, 5))
    top = bpy.context.active_object
    top.data.energy = 8000
    top.data.spot_size = math.radians(25)

def setup_cinema_camera(target):
    print("🎥 [Director] Orquestrando Câmera 100mm Macro...")
    bpy.ops.object.camera_add(location=(1.5, -6, 1.2))
    cam = bpy.context.active_object
    cam.data.lens = 100
    cam.data.dof.use_dof = True
    cam.data.dof.focus_object = target
    cam.data.dof.aperture_fstop = 2.0
    
    # Animação em Curva (Feeling)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 180 # 7.5 segundos @ 24fps
    
    # Keyframe 1: Início Sutil
    cam.location = (2, -7, 0.8)
    cam.keyframe_insert("location", frame=1)
    
    # Keyframe 180: Revelação Final
    cam.location = (4, -10, 2.5)
    cam.keyframe_insert("location", frame=180)
    
    # Track To Constrain
    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    scene.camera = cam
    return cam

# --- 5. EXECUÇÃO MASTERPIECE (The Meshy-Vision Build) ---
def run_v6_production():
    try:
        reset_all()
        setup_director_world()
        
        # Smart Hero Import
        blend_path = os.path.join(ASSETS_DIR, "nike.blend")
        with bpy.data.libraries.load(blend_path) as (data_from, data_to):
            data_to.objects = data_from.objects

        nike = None
        for obj in data_to.objects:
            if obj and obj.type == 'MESH':
                if "Plane" in obj.name: continue
                bpy.context.collection.objects.link(obj)
                nike = obj
                break
        
        if not nike: raise ValueError("Herói Nike não encontrado.")
        
        # Normalização Anti-Erro
        bpy.context.view_layer.objects.active = nike
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        nike.location = (0, 0, 0.2) # Flutuando levemente (Appealing)
        
        # A Mágica Meshy: Aplicação Automática de Materiais PBR
        apply_ai_pbr_materials(nike)
        
        build_surreal_studio(nike)
        setup_cinema_camera(nike)
        
        # Config de Render (Render Manager Layer)
        scene = bpy.context.scene
        output_file = os.path.join(OUTPUT_DIR, "nike_masterpiece_v6.mp4")
        
        rm = RenderManager()
        rm.preset("comercial", output=output_file)
        rm.ativar_compositing(estilo="cinematico")
        rm.ativar_motion_blur(shutter=0.5)
        
        print(f"\n🚀 [MASTER V6] Iniciando Renderização Cinematográfica Completa...")
        print(f"📍 Output: {output_file}")
        bpy.ops.render.render(animation=True, write_still=True)
        print("\n✨ [MASTER V6] Missão Cumprida. O Realismo Absoluto foi atingido.")

    except Exception as e:
        print(f"❌ [MASTER V6 FAIL] Erro: {e}")

if __name__ == "__main__":
    run_v6_production()
