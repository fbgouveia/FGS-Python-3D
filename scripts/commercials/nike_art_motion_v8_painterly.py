"""
╔══════════════════════════════════════════════════════════════╗
║   THE GLOBAL CREATIVE ARCHITECT — Felipe Gouveia Studio     ║
║   Script: nike_art_motion_v8_painterly.py                    ║
║   Concept: "Painterly Street-Art" - Da Arte para a Vida      ║
║   Standard: FGS Artistic Premium (CYCLES / AgX)             ║
║   Versão: 8.0.0 (The Living Masterpiece)                    ║
╚══════════════════════════════════════════════════════════════╝

ESTRATÉGIA DE DIREÇÃO (DNA Visual da Arte do Felipe):
1. PALETA: Azul Sky (Background), Branco Gesso (Sola), Azul Escuro/Preto (Destaques).
2. TEXTURA: "Oil Paint / Spray" - Materiais com rugosidade tátil e relevo de pincelada.
3. MOTION: O tênis "pinta" a si mesmo ou flutua em um estúdio que parece um quadro.
"""

import bpy
import os
import sys
import math
import random
from mathutils import Vector, Color

# --- 1. SETUP DE AMBIENTE ---
BASE_DIR = r"D:\Blender\blenderscripts"
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders", "finals")

os.makedirs(OUTPUT_DIR, exist_ok=True)
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from materials_library import MaterialLibrary
from render_manager import RenderManager

# --- 2. CONFIGURAÇÃO DA CENA (Inspired by the Art) ---
def setup_art_studio():
    print("🌍 [Architect/Neuro] Criando Estúdio de Arte Moderna...")
    scene = bpy.context.scene
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'
    
    # Engine: CYCLES para capturar a textura da "tinta"
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    
    # Background Azul Sky (conforme referência)
    world = bpy.data.worlds.new("FGS_Art_World")
    scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    nodes.clear()
    
    node_out = nodes.new('ShaderNodeOutputWorld')
    node_bg = nodes.new('ShaderNodeBackground')
    # Cor Azul Sky da Arte: (0.35, 0.75, 1.0)
    node_bg.inputs['Color'].default_value = (0.35, 0.75, 1.0, 1)
    world.node_tree.links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

def reset_scene():
    if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for b in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.images]:
        for i in b: b.remove(i)

# --- 3. MATERIALS: THE PAINTERLY EFFECT ---
def create_painterly_material(name, color, bump_strength=0.5):
    """Cria um material que simula pincelada de tinta óleo/acrílica."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    node_out = nodes.new('ShaderNodeOutputMaterial')
    node_bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    node_bsdf.inputs['Base Color'].default_value = (*color, 1)
    node_bsdf.inputs['Roughness'].default_value = 0.4
    
    # Textura de Ruído para simular o relevo da tinta
    node_noise = nodes.new('ShaderNodeTexNoise')
    node_noise.inputs['Scale'].default_value = 250
    node_noise.inputs['Detail'].default_value = 15
    node_noise.inputs['Distortion'].default_value = 0.5
    
    node_bump = nodes.new('ShaderNodeBump')
    node_bump.inputs['Strength'].default_value = bump_strength
    
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])
    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])
    
    return mat

def apply_art_materials(obj):
    print("🎨 [Neuro-Aesthetics] Aplicando DNA de Street-Art no Objeto...")
    # Paleta extraída da imagem do Felipe
    color_sky = (0.3, 0.7, 0.9)   # Azul predominante
    color_white = (0.9, 0.9, 0.95) # Gesso/Sola
    color_dark = (0.01, 0.02, 0.05) # Detalhes/Escuro

    mat_blue = create_painterly_material("Art_Blue", color_sky, 0.8)
    mat_white = create_painterly_material("Art_White", color_white, 1.2)
    mat_dark = create_painterly_material("Art_Dark", color_dark, 0.5)

    if not obj.data.materials:
        obj.data.materials.append(mat_blue)
    else:
        for i, slot in enumerate(obj.data.materials):
            low_name = slot.name.lower()
            if any(x in low_name for x in ["sole", "bottom", "white", "sola"]):
                obj.data.materials[i] = mat_white
            elif any(x in low_name for x in ["swoosh", "logo", "dark", "black"]):
                obj.data.materials[i] = mat_dark
            else:
                obj.data.materials[i] = mat_blue

# --- 4. ANIMATION: THE CANVAS COME TO LIFE ---
def animate_art_reveal(hero):
    print("🎬 [Choreographer] Animando a 'Arte Viva'...")
    hero.rotation_euler = (0, 0, 0)
    
    # Movimento: Flutuação Orgânica (como se estivesse no quadro)
    hero.keyframe_insert("location", frame=1)
    hero.keyframe_insert("rotation_euler", frame=1)
    
    # Meio da animação
    hero.location.y += 0.2
    hero.location.z += 0.05
    hero.rotation_euler.z = math.radians(15)
    hero.keyframe_insert("location", frame=72)
    hero.keyframe_insert("rotation_euler", frame=72)
    
    # Fim da animação (Loop suave)
    hero.location.y = 0
    hero.location.z = 0
    hero.rotation_euler.z = 0
    hero.keyframe_insert("location", frame=144)
    hero.keyframe_insert("rotation_euler", frame=144)

# --- 5. CAMERA & LIGHTS ---
def setup_art_production(target):
    # Câmera Frontal Estilo Quadro
    cam_data = bpy.data.cameras.new("ArtCam")
    cam_data.lens = 100 # Macro Portrait
    cam_obj = bpy.data.objects.new("ArtCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    cam_obj.location = (8, 0, 0.5)
    cam_obj.rotation_euler = (math.radians(85), 0, math.radians(90))
    
    # Iluminação "Top-Down" para destacar o relevo da tinta
    bpy.ops.object.light_add(type='AREA', location=(2, 0, 5))
    top_light = bpy.context.active_object
    top_light.data.energy = 5000
    top_light.data.color = (1, 0.98, 0.95)
    top_light.data.size = 3

# --- 6. PRODUÇÃO V8 ---
def produce_v8():
    try:
        reset_scene()
        setup_art_studio()
        
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
        
        if not hero: raise ValueError("Nike.blend não possui malha válida.")
        
        # Ajustar para o centro
        hero.location = (0, 0, 0)
        bpy.context.view_layer.objects.active = hero
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        
        # Aplicar Direção de Arte
        apply_art_materials(hero)
        animate_art_reveal(hero)
        setup_art_production(hero)
        
        # Render Config
        output_file = os.path.join(OUTPUT_DIR, "nike_v8_painterly_motion.mp4")
        rm = RenderManager()
        rm.preset("comercial", output=output_file)
        rm.ativar_compositing(estilo="cinematico")
        
        print("\n🚀 [MASTER V8] TRANSFORMANDO ARTE EM MOVIMENTO...")
        bpy.ops.render.render(animation=True, write_still=True)
        print("\n✨ [MASTER V8] SUCESSO. A arte ganhou vida.")

    except Exception as e:
        print(f"❌ [MASTER V8 FAIL] Erro: {e}")

if __name__ == "__main__":
    produce_v8()
