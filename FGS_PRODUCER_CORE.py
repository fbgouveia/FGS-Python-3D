# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: FGS_PRODUCER_CORE.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — FGS PRODUCER CORE v1.0             ║
║   The Central Intelligence for 3D Content Production         ║
╚══════════════════════════════════════════════════════════════╝

Este é o orquestrador master que integra todos os utilitários do
pipeline FGSS. Ele permite criar cenas completas chamando as
bibliotecas de materiais, luz, câmera e render.

Modo de Uso:
blender -b -P D:/Blender/blenderscripts/FGS_PRODUCER_CORE.py
"""

import sys
import os
import bpy

# 1. Dynamic Path Configuration
import pathlib
import sys

# Localize script directory to allow relative imports
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR / "scripts" / "utils"))

try:
    from paths import UTILS_DIR, RENDERS_FINALS, ensure_structure
    from logger import get_logger
    
    log = get_logger("PRODUCER_CORE")
    if str(UTILS_DIR) not in sys.path:
        sys.path.append(str(UTILS_DIR))
    
    from scene_setup import setup_scene
    from materials_library import apply_material
    from lighting_system import setup_studio_lighting
    from render_pipeline import RenderPipeline
    from camera_system import CameraSystem
    # from vfx_engine import spawn_particle_explosion
    
    log.info("✅ FGSS Utils & Logger loaded successfully.")
except ImportError as e:
    print(f"❌ Error loading utils: {e}")
    # Add fallback paths if standard detection fails
    print("Attempting manual path recovery...")
    sys.exit(1)

def build_fgs_production():
    """
    Função Master de Construção da Cena.
    Aqui é onde a 'mágica' acontece combinando todos os módulos.
    """
    # A. Setup Inicial
    setup_scene(fps=24, res_x=1920, res_y=1080)
    
    # B. Criar Objeto de Prova (Exemplo de Produto)
    bpy.ops.mesh.primitive_monkey_add(size=2, location=(0, 0, 1))
    suzanne = bpy.context.active_object
    suzanne.name = "FGS_HERO_ASSET_MONKEY"
    
    # C. Aplicar Material Premium (Tática #91: Tangibilidade)
    # Supondo que apply_material aceite o objeto e o tipo
    # apply_material(suzanne, "GOLD_PBR") 
    
    # D. Iluminação Cinematográfica
    setup_studio_lighting(intensity=2.0, color_top=(1, 1, 1), color_side=(1, 0.4, 0)) # Laranja FGSS
    
    # E. Adicionar Efeito VFX (Tática #10: Placebo da Expectativa)
    # spawn_particle_explosion(location=(0,0,0), color=(1, 0.4, 0))

    # F. Configurar Câmera Dinâmica (Uso do Sistema Cinematográfico)
    cam_sys = CameraSystem()
    cam_sys.criar_camera("FGS_CAM", posicao=(7, -7, 5), alvo=(0, 0, 1), fov=45)

def main():
    try:
        # ensure directories exist before render
        ensure_structure()
        
        # Caminho de saída baseado na data
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Use dynamic path from paths.py
        output_name = f"FGS_CORE_PROD_{ts}.mp4"
        output = str(RENDERS_FINALS / output_name)
        
        # Iniciar Pipeline de Render
        pipe = RenderPipeline(
            output_path=output,
            engine="BLENDER_EEVEE_NEXT",
            frame_start=1,
            frame_end=60, # 2.5 segundos de render
            resolution=(1920, 1080)
        )
        
        print(f"\n🚀 INICIANDO PROTOCOLO DE PRODUÇÃO FGSS...")
        print(f"📂 Output: {output}")
        pipe.run(build_fn=build_fgs_production, preview=False)
        
    except Exception as e:
        print(f"❌ Critical Failure in Production Core: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
