# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: integration_test.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: integration_test.py                                ║
║   Função: Testa integração de todos os core modules          ║
║   LAYER 1 — Task 1.4                                         ║
╚══════════════════════════════════════════════════════════════╝

Composes:
  - scene_setup
  - materials_library
  - lighting_system
  - camera_system
  - animation_engine
  - render_manager
  - render_pipeline

Produces a 3-second animation (72 frames @ 24fps)
ACCEPTANCE: Valid MP4 output from headless render.
"""

import os
import sys
import bpy
from datetime import datetime

sys.path.append("D:/Blender/blenderscripts/scripts/utils")

from scene_setup import limpar_cena, setup_scene_youtube
from materials_library import MaterialLibrary
from lighting_system import LightingSystem
from camera_system import CameraSystem
from animation_engine import AnimationEngine
from render_manager import RenderManager
from render_pipeline import RenderPipeline

def build_integration_scene():
    """Builds the scene using ALL 6 core modules."""
    
    # 1. SCENE SETUP
    limpar_cena()
    setup_scene_youtube()  # Sets fps=30, 1920x1080 (will be overridden by pipeline or we can match it)
    
    # 2. RENDER MANAGER (configure some specifics like bloom, motion blur)
    rm = RenderManager()
    rm.preset("youtube", frame_inicio=1, frame_fim=72)
    # Ativar compositing e motion blur do RenderManager
    rm.ativar_compositing(estilo="cinematico")
    rm.ativar_motion_blur(shutter=0.5)
    
    # 3. MATERIALS & OBJECT
    mat_lib = MaterialLibrary()
    
    # Floor
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    floor = bpy.context.active_object
    mat_lib.aplicar(floor, mat_lib.plastico(cor=(0.02, 0.02, 0.02), variacao="preto"))
    
    # Main Object (Suzanne)
    bpy.ops.mesh.primitive_monkey_add(size=2, location=(0, 0, 1.5))
    suzanne = bpy.context.active_object
    # Smooth shading
    for poly in suzanne.data.polygons:
        poly.use_smooth = True
    mat_lib.aplicar(suzanne, mat_lib.metal(cor=(1.0, 0.6, 0.5), variacao="ouro_rose"))
    
    # 4. LIGHTING SYSTEM
    ls = LightingSystem()
    ls.preset("produto")
    # And add a rim light manually
    ls.ponto_emissivo("Rim_Test", cor=(0.0, 0.5, 1.0), energia=10.0, posicao=(-3, 3, 2))
    
    # 5. CAMERA SYSTEM
    cam_sys = CameraSystem()
    cam = cam_sys.criar("IntegrationCam", posicao=(0, -6, 2), alvo=(0, 0, 1.5), fov=30, use_dof=True, foco_dist=4.5, fstop=1.8)
    bpy.context.scene.camera = cam
    
    # 6. ANIMATION ENGINE
    anim = AnimationEngine(fps=24) # Ensure it aligns
    anim.flutuar(suzanne, amplitude=0.3, velocidade=1.0)
    anim.rotacionar(suzanne, inicio_graus=(0,0,0), fim_graus=(0,0,360), frames=(1, 72))
    anim.mover(cam, inicio=(0, -7, 2), fim=(0, -5, 2.5), frames=(1, 72))
    
    print("✅ All Core Modules composed successfully.")

def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = f"D:/Blender/blenderscripts/renders/tests/integration_test_{ts}.mp4"
    
    # Pipeline handles the final render orchestration
    pipe = RenderPipeline(
        output_path=out_path,
        engine="BLENDER_EEVEE_NEXT",
        frame_start=1,
        frame_end=72,
        resolution=(1920, 1080),
        fps=24
    )
    
    # The pipeline step "render" will run
    result = pipe.run(build_fn=build_integration_scene, preview=False)
    sys.exit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
