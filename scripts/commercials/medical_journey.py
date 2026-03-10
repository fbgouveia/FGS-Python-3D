"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Template TN10: Medical Journey (Viagem microscópica)       ║
║                                                              ║
║   Descrição: Viagem orgânica/microscópica por dentro do      ║
║              corpo (ex: hemácias, vasos sanguíneos, coração).║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os
import math
import random

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
    "project_name": "medical_journey_heart",
    "theme": "bloodstream", # 'bloodstream', 'neurons', 'dna'
    "duration_sec": 8.0,
    "fps": 30,
    "render": {
        "engine": "CYCLES",
        "resolution": "YOUTUBE_SHORTS", 
        "quality": "STANDARD" 
    }
}

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def _create_organic_tube(radius=3.0, length=30.0):
    """Cria um túnel orgânico simulando uma veia/artéria."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius, depth=length, location=(0, length/2, 0))
    tube = bpy.context.active_object
    tube.name = "Veins"
    
    # Rotacionar tubo para alinhar ao eixo Y
    tube.rotation_euler[0] = math.radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    
    # Adicionar Displacement param deixar orgânico
    bpy.ops.object.modifier_add(type='SUBSURF')
    tube.modifiers["Subdivision"].levels = 2
    
    bpy.ops.object.modifier_add(type='DISPLACE')
    disp = tube.modifiers["Displace"]
    disp.strength = 1.0
    
    # Textura procedural de bump/musgrave no Displace
    tex = bpy.data.textures.new("Vein_Bump", type='CLOUDS')
    tex.noise_scale = 1.5
    disp.texture = tex
    
    # Virar normais para dentro pois a câmera vai estar por dentro do tubo
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Shade Smooth
    for p in tube.data.polygons:
        p.use_smooth = True

    return tube

def _create_red_blood_cells(tube_length):
    """Sistema de partículas com formato de glóbulos vermelhos."""
    # Criar um Glóbulo (Hemácia)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.1, location=(0,0,0))
    cell = bpy.context.active_object
    cell.name = "RedBloodCell"
    # Escalar para parecer o shape de panqueca esmagada
    bpy.ops.object.modifier_add(type='SUBSURF')
    cell.modifiers["Subdivision"].levels = 2
    for p in cell.data.polygons:
        p.use_smooth = True
    
    # Deixar em uma coleção separada para usar no sistema de partículas
    inst_coll = bpy.data.collections.new("Cell_Instances")
    bpy.context.scene.collection.children.link(inst_coll)
    bpy.context.collection.objects.unlink(cell)
    inst_coll.objects.link(cell)
    
    # Material da célula
    mat_cell = bpy.data.materials.new("Mat_Cell")
    mat_cell.use_nodes = True
    bsdf = mat_cell.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.8, 0.01, 0.01, 1) # Vermelho sangue
    bsdf.inputs['Roughness'].default_value = 0.3
    bsdf.inputs['Clearcoat'].default_value = 1.0 # Aparência úmida/líquida
    cell.data.materials.append(mat_cell)

    # Emitter é invisível e se move no eixo Y jogando partículas pra trás 
    bpy.ops.mesh.primitive_plane_add(size=3, location=(0, tube_length, 0))
    emitter = bpy.context.active_object
    emitter.name = "Cell_Emitter"
    emitter.rotation_euler[0] = math.radians(90)
    
    vfx = VFXEngine()
    ps = vfx._add_particle_system(emitter, "Aorta_Flow", {
        'count': 1500,
        'lifetime': 150,
        'frame_start': -50, # Pre-roll
        'frame_end': 500,
        'particle_size': 1.0,
        'size_random': 0.3,
        'normal_factor': 10.0, # Velocidade do sangue pra câmera
        'use_dynamic_rotation': True,
        'gravity': 0.0, # Sangue flutua no líquido plasmático
        'render_type': 'COLLECTION'
    })
    
    ps.settings.instance_collection = inst_coll
    
    return emitter

def build_scene():
    print(f"\\n🧬 INICIANDO REVEAL MÉDICO: {CONFIG['project_name'].upper()}")
    clean_scene()
    
    total_frames = int(CONFIG['duration_sec'] * CONFIG['fps'])
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_frames
    
    tube_length = 40.0
    
    tube = _create_organic_tube(radius=3.5, length=tube_length)
    emitter = _create_red_blood_cells(tube_length)
    
    # Materiais (Parede da veia)
    mat_vein = bpy.data.materials.new("Mat_VeinWall")
    mat_vein.use_nodes = True
    bsdf_v = mat_vein.node_tree.nodes.get("Principled BSDF")
    bsdf_v.inputs['Base Color'].default_value = (0.6, 0.05, 0.02, 1) # Parede carnosa
    bsdf_v.inputs['Roughness'].default_value = 0.2
    bsdf_v.inputs['Clearcoat'].default_value = 1.0 # Úmido
    tube.data.materials.append(mat_vein)

    # ================= ILUMINAÇÃO ORGANICA =================
    ls = LightingSystem()
    ls.aplicar_preset("CALIDO")
    # Sub-surface scattering feel
    ls.ponto_suave("Glow_Vein", cor=(1.0, 0.2, 0.2), intensidade=500.0, raio=2.0, posicao=(0, 5, 0))
    
    # ================= CAMERA =================
    # A câmera navega pelo interior da veia contra o fluxo de células
    cam_sys = CameraSystem()
    cam, target = cam_sys.adicionar_camera("Microscope_Cam", tipo="DOLLY", 
                                           pos_inicial=(0, 2, 0), alvo=(0, 10, 0), lentes=24)
    
    # Efeito de Profundidade de Campo agressivo (Microscópio)
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 3.0
    cam.data.dof.aperture_fstop = 1.4

    anim = AnimationEngine()
    # Mover câmera pra frente
    anim.mover(cam, inicio=(0, 2, 0), fim=(0, 20, 0), frames=(1, total_frames))
    # E tremer (sensação de fluidez/sopro cardíaco)
    anim.tremer(cam, intensidade=0.1, eixos=(1,1,1))
    
    # ================= VFX AMBIENTAL =================
    # Depth Fog (Volume Scattering) para dar sensação de líquido
    bpy.ops.mesh.primitive_cube_add(size=50, location=(0, tube_length/2, 0))
    fog = bpy.context.active_object
    fog.name = "Plasma_Volume"
    
    mat_fog = bpy.data.materials.new("Mat_Plasma")
    mat_fog.use_nodes = True
    nodes = mat_fog.node_tree.nodes
    nodes.clear()
    vol = nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = (1.0, 0.8, 0.8, 1)
    vol.inputs['Density'].default_value = 0.05 # Líquido turvo
    out = nodes.new('ShaderNodeOutputMaterial')
    mat_fog.node_tree.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    fog.data.materials.append(mat_fog)
    
    print("✅ Tour Microscópico configurado.")

def render_project():
    rm = RenderManager()
    rm.setup_engine("CYCLES")
    rm.setup_resolution(CONFIG['render']['resolution'])
    rm.setup_quality("DRAFT") # Viagem no tempo real pra teste
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
