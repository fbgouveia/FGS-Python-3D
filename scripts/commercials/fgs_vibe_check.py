# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: fgs_vibe_check.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
Script: fgs_vibe_check.py
Author: Felipe Gouveia Studio
Purpose: Demonstration commercial (15s) using the FGS Master Hero.
The script shows how to:
  1. Clean & configure a 15-second commercial scene.
  2. Add a classic 3-point light rig.
  3. Create the Master Hero character via CharacterFactory.criar_master_hero().
  4. Animate a subtle head-bob (speech-like motion).
  5. Set up a cinematic close-up camera.
  6. Choose the optimal render engine (EEVEE).
"""

import sys
import os
import math
import bpy

# Add the project root to sys.path
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.append(_PROJECT_ROOT)
    
# Utils folder
_UTILS_DIR = os.path.join(_PROJECT_ROOT, "utils")
if _UTILS_DIR not in sys.path:
    sys.path.append(_UTILS_DIR)

from character_factory import CharacterFactory, MaterialLibrary
from scene_setup import (
    limpar_cena,
    setup_scene_comercial,
    adicionar_iluminacao_3_pontos,
    configurar_camera_padrao,
)

# Constants
DURATION_SECONDS = 15
FPS = 24
TOTAL_FRAMES = DURATION_SECONDS * FPS

def _set_render_engine(engine: str = "EEVEE"):
    """Switch the active scene render engine."""
    scene = bpy.context.scene
    scene.render.engine = engine
    if engine.upper() == "EEVEE":
        eevee = scene.eevee
        eevee.use_gtao = True
        eevee.use_bloom = True
        eevee.use_motion_blur = True
        eevee.use_ssr = True  # Note: Screen Space Reflections
        print("🔧 Render engine set to EEVEE (rapid preview).")
    else:
        scene.render.engine = "CYCLES"
        print("🔧 Render engine set to CYCLES (high-quality).")

def main():
    print("\n🎬 Starting FGS Vibe Check Demo...")
    
    # 3.1 Clean the current Blender file
    limpar_cena()

    # 3.2 Configure the 15-second commercial scene
    setup_scene_comercial()

    # 3.3 3-point lighting rig
    adicionar_iluminacao_3_pontos()

    # 3.4 Build the Master Hero character
    # CharacterFactory handles its own library if not provided, 
    # but we provide it for explicit premium control
    factory = CharacterFactory(MaterialLibrary())

    # Create the hero via shortcut
    factory.criar_master_hero(posicao=(0, 0, 0), humor="feliz")

    # Get the character name
    hero_name = next(iter(factory.personagens))
    print(f"✅ Master Hero created: '{hero_name}'")

    # 3.5 Animate a subtle head-bob
    factory.head_bob(
        nome=hero_name,
        frame_inicio=1,
        frame_fim=TOTAL_FRAMES,
        amplitude=0.03,
        frequencia=8,
    )
    print("🌀 Head-bob animation applied.")

    # 3.6 Cinematic close-up camera
    CAM_POS = (0, -3.8, 1.9)
    CAM_TARGET = (0, 0, 0)
    configurar_camera_padrao(
        posicao=CAM_POS,
        alvo=CAM_TARGET,
        fov_graus=45,
    )
    print("📷 Camera positioned for cinematic close-up.")

    # 3.7 Set Render Engine
    _set_render_engine("EEVEE")

    print("\n🚀 Vibe-Check demo script finished!")
    print("    • Next: Press Space-Bar to preview or F12 to Render.")
    print("\n✅ All Imperial steps executed successfully.\n")

if __name__ == "__main__":
    main()
