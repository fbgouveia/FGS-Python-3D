# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: product_cinematic_reveal.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: product_cinematic_reveal.py                       ║
║   Função: Revelação Cinemática Premium de Produto           ║
║           Luz volumétrica, névoa e Dolly Zoom               ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os
import math

# Adicionar caminhos de utilitários
sys.path.append("D:/Blender/blenderscripts/scripts/utils")

from camera_system import CameraSystem
from lighting_system import LightingSystem
from materials_library import MaterialLibrary
from vfx_engine import VFXEngine
from animation_engine import AnimationEngine
from render_manager import RenderManager

def build_scene():
    # 1. Limpar cena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 2. Inicializar Motores
    cam_sys = CameraSystem()
    luzes = LightingSystem()
    mat_lib = MaterialLibrary()
    vfx = VFXEngine()
    anim = AnimationEngine()
    render = RenderManager()
    
    # 3. Criar Objeto de Produto (Placeholder: Cubo Chanfrado Estilizado)
    bpy.ops.mesh.primitive_cube_add(size=1)
    produto = bpy.context.active_object
    produto.name = "Produto_Hero"
    bpy.ops.object.modifier_add(type='SUBSURF')
    produto.modifiers["Subdivision"].levels = 2
    
    # Aplicar Material Premium (Ouro ou Metal Polido)
    mat_ouro = mat_lib.metal_ouro()
    mat_lib.aplicar(produto, mat_ouro)
    
    # Animação do Produto: Rotação suave infinita
    anim.rotacionar(produto, (0,0,0), (0,0,360), frames=(1, 240))
    
    # 4. Criar Chão Refletivo (Luxo)
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0,0,-1))
    chao = bpy.context.active_object
    mat_chao = mat_lib.metal(cor=(0.01, 0.01, 0.01), roughness=0.05)
    mat_lib.aplicar(chao, mat_chao)
    
    # 5. Iluminação Cinemática (Preset Luxo)
    luzes.preset("luxo")
    
    # 6. VFX: Névoa Volumétrica e Glitter
    vfx.fumaca(objeto=None, densidade=0.1, cor=(0.02, 0.02, 0.05), escala=5, nome="Neblina_Premium")
    vfx.glitter(objeto=produto, quantidade=500, cor=(1, 0.8, 0.2), tamanho=0.01, frame_fim=240)
    
    # 7. Câmera: Dolly Zoom (Hitchcock Effect)
    # Camera começa longe com FOV fechado e aproxima com FOV aberto
    cam = cam_sys.criar("CAM_CINEMATIC", posicao=(0, -8, 1), alvo=(0,0,0), fov=30)
    
    # Animar Dolly In
    cam_sys.dolly(cam, inicio=(0, -8, 1), fim=(0, -3, 0.8), frames=(1, 120))
    
    # Animar Zoom (FOV Inverse)
    bpy.context.scene.frame_set(1)
    cam.data.angle = math.radians(20) # Telephoto
    cam.data.keyframe_insert(data_path="angle")
    
    bpy.context.scene.frame_set(120)
    cam.data.angle = math.radians(60) # Wide
    cam.data.keyframe_insert(data_path="angle")
    
    # 8. Setup de Render
    render.setup_preset("tiktok") # Vertical para redes sociais
    bpy.context.scene.frame_end = 120
    
    print("✅ Cena Cinematic Reveal construída!")

if __name__ == "__main__":
    build_scene()
