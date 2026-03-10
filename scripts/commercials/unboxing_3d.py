"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Template TN4: Unboxing 3D Reveal                          ║
║                                                              ║
║   Descrição: Caixa elegante se abrindo dramaticamente para   ║
║              revelar um produto no interior com iluminação   ║
║              premium volumétrica.                            ║
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
    "project_name": "unboxing_premium",
    "box_color": (0.02, 0.02, 0.02),
    "product_color": (1.0, 0.84, 0.0), # Dourado 
    "light_preset": "LUXO", 
    "duration_sec": 6.0,
    "fps": 30
}

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in [bpy.data.materials, bpy.data.cameras, bpy.data.lights]:
        for item in coll:
            coll.remove(item)

def build_box(mat_box):
    # Base da Caixa
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 1.0))
    box_base = bpy.context.active_object
    box_base.name = "Box_Base"
    box_base.data.materials.append(mat_box)

    # O cubo do Blender normal é fechado. Para ser uma caixa que abre, 
    # o jeito mais simples procedural é ter paredes soltas ou usar boolean.
    # Mas para o template rápido: vamos transformar a tampa.
    
    # Tampa da caixa (Pivot deslocado pra quina)
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(0, 0, 2.01))
    tampa = bpy.context.active_object
    tampa.name = "Box_Tampa"
    tampa.data.materials.append(mat_box)
    
    # Mover a origem (pivot) para a borda Y, para ela girar como uma dobradiça
    me = tampa.data
    for v in me.vertices:
        v.co.y -= 1.0  # Desloca a malha 1 unidade pra frente
    tampa.location.y += 1.0 # E desloca o objeto 1 unidade pra trás. Pivot agora é na borda.
    
    return box_base, tampa

def build_scene():
    print(f"\\n📦 INICIANDO TEMPLATE: UNBOXING REVEAL")
    clean_scene()
    
    total_frames = int(CONFIG['duration_sec'] * CONFIG['fps'])
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = total_frames
    
    ls = LightingSystem()
    ls.aplicar_preset(CONFIG["light_preset"])

    mat_lib = MaterialsLibrary()
    
    mat_box = bpy.data.materials.new("Mat_Box")
    mat_box.use_nodes = True
    bsdf = mat_box.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*CONFIG['box_color'], 1)
        bsdf.inputs['Roughness'].default_value = 0.2
        bsdf.inputs['Metallic'].default_value = 0.8
        
    base, tampa = build_box(mat_box)
    
    # Produto (Mockup de Perfume/Garrafa no interior)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.2, location=(0, 0, 1.6))
    produto = bpy.context.active_object
    produto.name = "Produto_Mockup"
    mat_produto = mat_lib.get_material("Ouro")
    produto.data.materials.append(mat_produto)
    
    # Tampa debaixo = fazer a tampa e o produto "brotar" de dentro da escuridão (ou box aberto)
    
    # ================= ANIMAÇÃO =================
    anim = AnimationEngine()
    
    # 1. Tampa abrindo (de frame 30 até 90)
    bpy.context.scene.frame_set(1)
    tampa.rotation_euler[0] = 0
    tampa.keyframe_insert(data_path="rotation_euler", index=0)
    
    bpy.context.scene.frame_set(30)
    tampa.rotation_euler[0] = 0
    tampa.keyframe_insert(data_path="rotation_euler", index=0)
    
    bpy.context.scene.frame_set(90)
    tampa.rotation_euler[0] = math.radians(110) # Abre para trás
    tampa.keyframe_insert(data_path="rotation_euler", index=0)
    
    # 2. Produto sobe (levitação premium da base)
    bpy.context.scene.frame_set(60) # Começa a subir quando a tampa já abriu um pouco
    produto.location[2] = 0.0  # Escondido
    produto.keyframe_insert(data_path="location", index=2)
    
    bpy.context.scene.frame_set(120)
    produto.location[2] = 1.6  # Altura final (foco)
    produto.keyframe_insert(data_path="location", index=2)
    
    anim.rotacionar_continuamente(produto, (0, 0, 1), velocidade=0.5)

    # ================= VFX =================
    vfx = VFXEngine()
    # Poeira de luz / sparkles soltando de dentro
    ps = vfx.faiscas(objeto=produto, quantidade=500, velocidade=1.0, cor=(1.0, 0.9, 0.5), nome="Unbox_Magic")
    ps.settings.frame_start = 60
    ps.settings.frame_end = 120
    ps.settings.gravity = -0.5 # Sobem em levitação

    # ================= CAMERA =================
    cam_sys = CameraSystem()
    cam, target = cam_sys.adicionar_camera("Cam_Main", tipo="ORBIT", pos_inicial=(0, -4, 3), alvo=(0,0,1.5), lentes=50)
    # Orbita leve do frame 1 ao final
    cam_sys.animar_orbita(cam, (0,0,1.5), raio=4.0, angulo_inicial=-90, voltas=0.5, frames_totais=total_frames)

    print("✅ Unboxing 3D construído.")

def render_project():
    rm = RenderManager()
    rm.setup_engine("CYCLES")
    rm.setup_resolution("INSTAGRAM_SQUARE") # 1080x1080
    rm.setup_quality("DRAFT")
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
