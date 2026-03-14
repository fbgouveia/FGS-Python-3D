# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: logo_reveal_tangible.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — BLENDER PYTHON PIPELINE            ║
║   Script: logo_reveal_tangible.py                             ║
║   Neuromarketing: Tática #91 (Tato e Tangibilidade)          ║
║   Status: PRODUCTION_READY                                   ║
╚══════════════════════════════════════════════════════════════╝

Este script cria um Reveal de Logo focado na percepção tátil.
Usa materiais metálicos escovados, profundidade de campo (DOF)
e iluminação dramática para vender "Substância".
"""

import sys
import bpy
import os

# Garantir acesso aos utilitários FGSS
UTILS_PATH = "D:/Blender/blenderscripts/scripts/utils"
if UTILS_PATH not in sys.path:
    sys.path.append(UTILS_PATH)

try:
    from render_pipeline import RenderPipeline
    from materials_library import apply_material
    from lighting_system import setup_studio_lighting
    from scene_setup import setup_scene
    print("✅ FGSS Pipeline Tools Loaded.")
except ImportError:
    print("⚠️ Utils not found. Running in standalone mode.")

def build_logo_reveal():
    """
    Constrói a cena de Reveal com foco em Tangibilidade (#91)
    """
    # 1. Configuração da Cena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 2. Criar Objeto do Logo (Texto como placeholder para o Logo FGSS)
    bpy.ops.object.text_add(location=(0, 0, 0))
    logo = bpy.context.active_object
    logo.data.body = "FGSS"
    logo.data.size = 2.0
    logo.data.extrude = 0.2
    logo.data.bevel_depth = 0.05
    logo.data.align_x = 'CENTER'
    logo.data.align_y = 'CENTER'
    logo.rotation_euler = (1.5708, 0, 0) # Virar para frente
    
    # 3. Aplicar Tática #91: Material Metálico Pesado
    # Criar material de Ouro Escovado (Brushed Gold) para tangibilidade
    mat = bpy.data.materials.new(name="FGS_TANGIBLE_GOLD")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    p = nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (1.0, 0.6, 0.1, 1.0)
    p.inputs["Metallic"].default_value = 1.0
    p.inputs["Roughness"].default_value = 0.2
    logo.data.materials.append(mat)
    
    # 4. Iluminação Dramática (Gera sombras que definem a forma/tato)
    setup_studio_lighting(intensity=5.0)
    
    # 5. Câmera com DOF (Depth of Field) para focar na "textura"
    cam_data = bpy.data.cameras.new("Revealer_Cam")
    cam_obj = bpy.data.objects.new("Revealer_Cam", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    cam_obj.location = (0, -8, 2)
    cam_obj.rotation_euler = (1.4, 0, 0)
    
    # Configurar DOF para Tática #91
    cam_data.dof.use_dof = True
    cam_data.dof.focus_object = logo
    cam_data.dof.aperture_fstop = 1.2 # Fundo borrado, foco na "matéria"
    
    # 6. Animação de Zoom (Reveal)
    cam_obj.keyframe_insert(data_path="location", frame=1)
    cam_obj.location.y = -5
    cam_obj.keyframe_insert(data_path="location", frame=120)

def main():
    output = f"D:/Blender/blenderscripts/renders/finals/LOGO_REVEAL_91.mp4"
    pipe = RenderPipeline(
        output_path=output,
        frame_start=1,
        frame_end=120,
        resolution=(1920, 1080),
        engine="BLENDER_EEVEE_NEXT"
    )
    pipe.run(build_fn=build_logo_reveal)

if __name__ == "__main__":
    main()
