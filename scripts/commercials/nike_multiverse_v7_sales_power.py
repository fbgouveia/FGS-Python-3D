"""
╔══════════════════════════════════════════════════════════════╗
║   THE GLOBAL CREATIVE ARCHITECT — Felipe Gouveia Studio     ║
║   Script: nike_multiverse_v7_sales_power.py                  ║
║   Concept: "Spider-Verse Multiverse" + High-End Sales Power ║
║   Standard: Nike Global Elite (CYCLES / AgX / PBR)          ║
║   Versão: 7.0.0 (The Ultimate Sales Machine)                ║
╚══════════════════════════════════════════════════════════════╝

ESTRATÉGIA DE VENDA (Arquitetura do Desejo):
1. HOOK (0-2s): Caos geométrico e luzes pulsantes (Ativa a Amígdala).
2. DESIRE (2-4s): Close-up macro no material PBR (Tato Visual).
3. STATUS (4-6s): Revelação heróica sob luz de ouro (Efeito Posse).
"""

import bpy
import os
import sys
import math
import random
from mathutils import Vector, Color

# --- 1. CONFIGURAÇÃO DE AMBIENTE ---
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
def setup_multiverse_world():
    print("🌍 [Architect/Neuro] Criando Vácuo Energético Multiverso...")
    scene = bpy.context.scene
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'
    
    # Render Engine: CYCLES Master (Realismo é Venda)
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    
    # Mundo Escuro com Nebulosa Procedural sutil
    world = bpy.data.worlds.new("FGS_Multiverse_World")
    scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    nodes.clear()
    
    node_out = nodes.new('ShaderNodeOutputWorld')
    node_bg = nodes.new('ShaderNodeBackground')
    node_bg.inputs['Color'].default_value = (0.002, 0.002, 0.005, 1)
    world.node_tree.links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

def reset_scene():
    if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for b in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights]:
        for i in b: b.remove(i)

# --- 3. AI MATERIAL ARTIST (Sales Focus) ---
def apply_premium_materials(obj):
    print("🎨 [Neuro-Aesthetics] Injetando Materiais que VENDEM...")
    lib = MaterialLibrary()
    
    # Material de Luxo para o Logo (Ouro/Cromo)
    mat_logo = lib.metal(cor=(0.9, 0.7, 0.1), roughness=0.05, variacao="sales_gold")
    # Material Tátil para o Corpo (Fibra/Tecido)
    mat_body = lib.metal(cor=(0.1, 0.1, 0.12), roughness=0.3, variacao="sales_tactile")
    
    if not obj.data.materials:
        obj.data.materials.append(mat_body)
    else:
        for i, slot in enumerate(obj.data.materials):
            if any(x in slot.name.lower() for x in ["logo", "swoosh"]):
                obj.data.materials[i] = mat_logo
            else:
                obj.data.materials[i] = mat_body

# --- 4. ELEMENTOS DO MULTIVERSO (Geometric Chaos) ---
def create_multiverse_elements():
    print("✨ [Director] Gerando Fragmentos Dimensionais...")
    fragments = []
    lib = MaterialLibrary()
    mat_neon = lib.neon(cor=(0.0, 0.8, 1.0), intensidade=10.0, variacao="portal_blue")
    mat_magenta = lib.neon(cor=(1.0, 0.0, 0.5), intensidade=10.0, variacao="portal_pink")

    for i in range(15):
        # Cubos e Pirâmides Flutuantes
        shape = random.choice(['CUBE', 'STYLIZED'])
        if shape == 'CUBE':
            bpy.ops.mesh.primitive_cube_add(size=random.uniform(0.1, 0.5))
        else:
            bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.3)
        
        frag = bpy.context.active_object
        frag.location = (random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-2, 4))
        frag.rotation_euler = (random.random(), random.random(), random.random())
        frag.data.materials.append(random.choice([mat_neon, mat_magenta]))
        
        # Animação de Flutuação
        frag.keyframe_insert("location", frame=1)
        frag.location.z += 1.0
        frag.rotation_euler.z += math.radians(90)
        frag.keyframe_insert("location", frame=144)
        frag.keyframe_insert("rotation_euler", frame=144)
        fragments.append(frag)
    return fragments

# --- 5. CÂMERA DRAMÁTICA (Spider-Verse Movement) ---
def setup_sales_camera(target):
    print("🎥 [Choreographer] Orquestrando Câmera de Alto Impacto...")
    cam_data = bpy.data.cameras.new("DiscoveryCam")
    cam_data.lens = 85
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = target
    cam_data.dof.aperture_fstop = 1.4
    
    cam_obj = bpy.data.objects.new("DiscoveryCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Roteiro: 0-60 (Macro Curiosidade) | 60-144 (Revelação Heróica)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 144
    
    # Pos 1: Macro Sola
    cam_obj.location = (1.5, -2, 0.2)
    cam_obj.keyframe_insert("location", frame=1)
    
    # Pos 2: Zoom Out Rápido (The Snap)
    cam_obj.location = (5, -8, 2)
    cam_obj.keyframe_insert("location", frame=60)
    
    # Pos 3: Hero Orbit (Desejo)
    cam_obj.location = (6, -10, 3)
    cam_obj.keyframe_insert("location", frame=144)
    
    track = cam_obj.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

# --- 6. ILUMINAÇÃO DE VENDA (Emotional Triggers) ---
def setup_sales_lighting():
    print("💡 [Lighting] Calibrando Luzes de Conversão...")
    # Luz Heróica (Ouro)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
    top = bpy.context.active_object
    top.data.energy = 6000
    top.data.color = (1.0, 0.85, 0.5)
    
    # Back Light de Estrela (Rim)
    bpy.ops.object.light_add(type='AREA', location=(0, 5, 2))
    back = bpy.context.active_object
    back.data.energy = 8000
    back.data.color = (0.5, 0.8, 1.0)
    back.rotation_euler = (math.radians(90), 0, 0)

# --- 7. EXECUÇÃO MASTERPIECE V7 ---
def produce_v7():
    try:
        reset_scene()
        setup_multiverse_world()
        
        # Importar Herói
        blend_path = os.path.join(ASSETS_DIR, "nike.blend")
        with bpy.data.libraries.load(blend_path) as (data_from, data_to):
            data_to.objects = data_from.objects
        
        hero = None
        for obj in data_to.objects:
            if obj and obj.type == 'MESH' and "Plane" not in obj.name:
                bpy.context.collection.objects.link(obj)
                hero = obj
                break
        
        if not hero: raise ValueError("Nike não encontrado.")
        
        # Setup Hero
        hero.location = (0, 0, 0)
        bpy.context.view_layer.objects.active = hero
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        apply_premium_materials(hero)
        
        # Multiverso Assets
        create_multiverse_elements()
        
        # Direção
        setup_sales_camera(hero)
        setup_sales_lighting()
        
        # Render Config
        output_file = os.path.join(OUTPUT_DIR, "nike_v7_spiderverse_sales.mp4")
        rm = RenderManager()
        rm.preset("comercial", output=output_file)
        rm.ativar_compositing(estilo="cinematico")
        rm.ativar_motion_blur(shutter=0.5)
        
        print(f"\n🚀 [MASTER V7] PRODUZINDO COMERCIAL MULTIVERSO...")
        bpy.ops.render.render(animation=True, write_still=True)
        print("\n✨ [MASTER V7] SUCESSO. Venda garantida.")

    except Exception as e:
        print(f"❌ [MASTER V7 FAIL] Erro: {e}")

if __name__ == "__main__":
    produce_v7()
