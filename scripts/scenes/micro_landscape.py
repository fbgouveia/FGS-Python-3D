# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: micro_landscape.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import math
import random
import os

# ==============================================================================
# FELIPE GOUVEIA STUDIO - PYTHON 3D
# Projeto: Macro Landscape Miniature
# Versão: 1.0 (WOW Factor Hero)
# Descrição: Um mundo miniatura revelado por uma lente macro, focando em 
#            detalhes de cristais e vegetação abstrata.
# ==============================================================================

def setup_macro_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.frame_end = 120
    
    # --- TERRENO ABSTRATO ---
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=50, y_subdivisions=50, size=10)
    terrain = bpy.context.active_object
    
    # Deformar o terreno (procedural displacement via script)
    for v in terrain.data.vertices:
        v.co[2] = random.random() * 0.5
    
    mat_terrain = bpy.data.materials.new(name="MossTerrain")
    mat_terrain.use_nodes = True
    bsdf = mat_terrain.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.01, 0.05, 0.02, 1) # Dark green
    bsdf.inputs['Roughness'].default_value = 0.8
    terrain.data.materials.append(mat_terrain)

    # --- CRISTAIS EM MINIATURA ---
    for i in range(20):
        x = (random.random() - 0.5) * 5
        y = (random.random() - 0.5) * 5
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, subdivisions=1, location=(x, y, 0.2))
        crystal = bpy.context.active_object
        crystal.scale[2] = 2 + random.random() * 2
        
        mat_c = bpy.data.materials.new(name=f"Crystal_{i}")
        mat_c.use_nodes = True
        bsdf_c = mat_c.node_tree.nodes.get('Principled BSDF')
        bsdf_c.inputs['Base Color'].default_value = (0, 0.8, 1, 1) # Cyan
        bsdf_c.inputs['Transmission Weight'].default_value = 1.0
        bsdf_c.inputs['IOR'].default_value = 1.45
        bsdf_c.inputs['Emission Color'].default_value = (0, 0.5, 1, 1)
        bsdf_c.inputs['Emission Strength'].default_value = 0.5
        crystal.data.materials.append(mat_c)

    # --- CÂMERA MACRO (Extreme DoF) ---
    bpy.ops.object.camera_add(location=(0, -2, 1))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(70), 0, 0)
    bpy.context.scene.camera = cam
    cam.data.lens = 100 # Lente Macro
    
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 2.1
    cam.data.dof.aperture_fstop = 0.5 # Extremamente raso
    
    # Animação de Foco (Rack Focus de um cristal para outro)
    cam.data.dof.keyframe_insert(data_path="focus_distance", frame=1)
    cam.data.dof.focus_distance = 2.5
    cam.data.dof.keyframe_insert(data_path="focus_distance", frame=100)

    # Output
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "renders", "finals")
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    scene.render.filepath = os.path.join(out_dir, "macro_landscape_wow.mp4")
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'

    print(f"FGS Studio: Cena Macro configurada. Renderizando para: {scene.render.filepath}")
    bpy.ops.render.render(animation=True)
    print("FGS Studio: Render Concluído!")

if __name__ == "__main__":
    setup_macro_scene()
