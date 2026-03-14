# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: FGS_PRODUCER_CORE.py                               ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — FGS PRODUCER CORE v1.1             ║
║   The Central Intelligence for 3D Content Production         ║
║   Layer-0 Governance Integrated                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import bpy
import pathlib
from datetime import datetime
import shutil

# --- DESIGN TOKENS (Brutalist Neural Glass) ---
SIGNAL_ORANGE = "\033[38;5;202m"
NEURAL_WHITE = "\033[97m"
RESET = "\033[0m"

# --- LAYER-0 GOVERNANCE CHECK ---
def validate_sovereignty():
    """Valida se as Leis Universais e a autorização de Lorena/Clara estão presentes."""
    if not os.path.exists("D:/REGENCIA_UNIVERSAL/LEIS_UNIVERSAIS.md"):
        print(f"{SIGNAL_ORANGE}❌ CRITICAL: Regência Universal não detectada! Abortando...{RESET}")
        sys.exit(1)
    # print(f"{SIGNAL_ORANGE}🛡️  [LAYER-0] Soberania Digital reconhecida.{RESET}")

# 1. Dynamic Path Configuration
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(str(SCRIPT_DIR / "scripts" / "utils"))

try:
    from paths import UTILS_DIR, RENDERS_FINALS, ensure_structure, BASE_DIR
    from logger import get_logger
    
    log = get_logger("PRODUCER_CORE")
    if str(UTILS_DIR) not in sys.path:
        sys.path.append(str(UTILS_DIR))
    
    from scene_setup import setup_scene
    from materials_library import apply_material
    from lighting_system import setup_studio_lighting
    from render_pipeline import RenderPipeline
    from camera_system import CameraSystem
    
    log.info(f"{SIGNAL_ORANGE}✅ FGSS Utils & Logger loaded under Sovereignty Protocol.{RESET}")
except ImportError as e:
    print(f"❌ Error loading utils: {e}")
    sys.exit(1)

def build_fgs_production():
    """Função Master de Construção da Cena."""
    log.info(f"{SIGNAL_ORANGE}🏗️ Building Scene: FGS_HERO_ASSET...{RESET}")
    
    # A. Setup Inicial
    setup_scene(fps=24, res_x=1920, res_y=1080)
    
    # B. Criar Objeto de Prova (Exemplo de Produto)
    bpy.ops.mesh.primitive_monkey_add(size=2, location=(0, 0, 1))
    suzanne = bpy.context.active_object
    suzanne.name = "FGS_HERO_ASSET_MONKEY"
    
    # D. Iluminação Cinematográfica
    setup_studio_lighting(intensity=2.0, color_top=(1, 1, 1), color_side=(1, 0.4, 0)) # Laranja FGSS
    
    # E. Configurar Câmera Dinâmica
    cam_sys = CameraSystem()
    cam_sys.criar_camera("FGS_CAM", posicao=(7, -7, 5), alvo=(0, 0, 1), fov=45)

def perform_governance_feedback(output_path, success=True):
    """Registra o sucesso/falha na memória de Lorena e Clara."""
    hoje = datetime.now().strftime("%Y-%m-%d")
    lorena_diary = pathlib.Path(f"D:/Lorena/diario/DIARIO_LORENA_{hoje}.md")
    
    status = "SUCESSO" if success else "FALHA"
    entry = f"\n### [PRODUÇÃO] Audit Trail - {datetime.now().strftime('%H:%M:%S')}\n"
    entry += f"- **Script:** FGS_PRODUCER_CORE.py\n"
    entry += f"- **Status:** {status}\n"
    entry += f"- **Output:** {output_path}\n"
    
    try:
        # Create diary dir if missing
        lorena_diary.parent.mkdir(parents=True, exist_ok=True)
        with open(lorena_diary, "a", encoding="utf-8") as f:
            f.write(entry)
        log.info(f"{SIGNAL_ORANGE}📝 Audit feedback sent to Lorena's Diary.{RESET}")
    except Exception as e:
        log.warning(f"Could not write to Lorena's diary: {e}")

def main():
    validate_sovereignty()
    
    try:
        ensure_structure()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"FGS_CORE_PROD_{ts}.mp4"
        output = str(RENDERS_FINALS / output_name)
        
        log.info(f"{SIGNAL_ORANGE}🚀 INICIANDO PROTOCOLO DE PRODUÇÃO FGSS...{RESET}")
        log.info(f"📂 Final Output: {output}")
        
        pipe = RenderPipeline(
            output_path=output,
            engine="BLENDER_EEVEE_NEXT",
            frame_start=1,
            frame_end=60,
            resolution=(1920, 1080)
        )
        
        pipe.run(build_fn=build_fgs_production, preview=False)
        
        # Automatic Backup of the generated file
        backup_dir = BASE_DIR / "renders" / "backups"
        backup_dir.mkdir(exist_ok=True)
        shutil.copy2(output, backup_dir / output_name)
        
        perform_governance_feedback(output, success=True)
        log.info(f"{SIGNAL_ORANGE}✨ Production Completed Successfully.{RESET}")
        
    except Exception as e:
        log.error(f"❌ Critical Failure in Production Core: {e}")
        perform_governance_feedback("N/A", success=False)
        sys.exit(1)

if __name__ == "__main__":
    main()
