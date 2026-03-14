# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: integration_test_lorena.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: integration_test_lorena.py                        ║
║   Função: Teste de Integração com Avatar Lorena             ║
║           Valida o stack completo com personagem animado     ║
╚══════════════════════════════════════════════════════════════╝

NVIDIA RECOMMENDATION:
"Integrate LorenaAvatar into integration_test — create the avatar,
generate a 30-frame sequence and launch a headless render."

ACCEPTANCE CRITERIA:
✅ Lorena aparece na cena com rig e material holográfico
✅ Idle animations ativas (flutuar, respirar, piscar)
✅ Wave hello nos primeiros frames
✅ Pipeline de render produz MP4 válido
"""

import os
import sys
import bpy
from datetime import datetime
from pathlib import Path

try:
    from paths import BASE_DIR, UTILS_DIR, RENDERS_DRAFTS, ensure_structure
    from logger import get_logger
    
    log = get_logger("INTEGRATION_TEST")
    ensure_structure()
    FGS_ROOT = BASE_DIR
    if str(UTILS_DIR) not in sys.path:
        sys.path.append(str(UTILS_DIR))
    # Character dir is also needed
    CHAR_DIR = BASE_DIR / "scripts" / "characters"
    if str(CHAR_DIR) not in sys.path:
        sys.path.append(str(CHAR_DIR))
except ImportError:
    FGS_ROOT = Path(__file__).resolve().parents[2]
    sys.path.append(str(FGS_ROOT / "scripts" / "utils"))
    sys.path.append(str(FGS_ROOT / "scripts" / "characters"))
    log = None

from scene_setup import limpar_cena
from camera_system import CameraSystem
from lighting_system import LightingSystem
from animation_engine import AnimationEngine
from render_manager import RenderManager
from render_pipeline import RenderPipeline
from lorena_avatar import LorenaAvatar


def build_lorena_scene():
    """
    Constrói a cena de teste com a Lorena.
    
    Módulos utilizados:
    - CameraSystem    → câmera cinemática
    - LightingSystem  → iluminação 3-pontos
    - LorenaAvatar    → avatar completo
    - AnimationEngine → idle + wave
    """
    if log: log.info("🏗️ Building Lorena scene...")

    # 1. Limpa e configura cena
    limpar_cena()
    scene = bpy.context.scene
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 96  # 4 segundos

    # 2. Render Manager
    rm = RenderManager()
    rm.preset("youtube", frame_inicio=1, frame_fim=96)
    rm.ativar_compositing(estilo="cinematico")

    # 3. Chão com material escuro premium
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    mat_floor = bpy.data.materials.new("Mat_Floor")
    mat_floor.use_nodes = True
    bsdf = mat_floor.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.015, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.1
    floor.data.materials.append(mat_floor)

    # 4. Avatar Lorena
    lorena = LorenaAvatar(nome="Lorena", posicao=(0, 0, 0))
    lorena.build()
    lorena.apply_idle_animations()

    # Expressão e gesto de saudação
    lorena.set_expression("smile", intensidade=0.7, frame=12)
    lorena.wave_hello(frame_inicio=12)

    # 5. Iluminação cinemática para holograma
    ls = LightingSystem()
    ls.preset("produto")
    # Luz ciano suave para reforçar o efeito holográfico
    ls.ponto_emissivo(
        nome="Holo_Rim",
        cor=(0.0, 0.7, 1.0),
        energia=15.0,
        posicao=(-2.5, -1.5, 2.0)
    )
    ls.ponto_emissivo(
        nome="Holo_Fill",
        cor=(0.0, 0.5, 0.8),
        energia=8.0,
        posicao=(2.5, 1.5, 1.5)
    )

    # 6. Câmera
    cam_sys = CameraSystem()
    cam = cam_sys.criar_camera(
        nome="Lorena_Cam",
        posicao=(0, -4.5, 1.4),
        alvo=lorena.mesh_obj,
        fov=35,
        use_dof=True,
        foco_dist=4.5,
        fstop=1.4
    )
    bpy.context.scene.camera = cam

    # Câmera move sutilmente (parallax)
    anim = AnimationEngine(fps=24)
    anim.mover(cam, inicio=(0, -4.5, 1.4), fim=(-0.3, -4.2, 1.5), frames=(1, 96))

    print("✅ Cena Lorena construída com sucesso!")
    print(f"   Frames: 1-96 @ 24fps = 4 segundos")
    print(f"   Lorena mesh: {lorena.mesh_obj.name}")
    print(f"   Lorena rig:  {lorena.armature_obj.name}")


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Use localized renders/drafts for tests
    try:
        from paths import RENDERS_DRAFTS
        out_dir = RENDERS_DRAFTS
    except ImportError:
        out_dir = FGS_ROOT / "renders" / "tests"
        
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = str(out_dir / f"integration_lorena_{ts}.mp4")

    pipeline = RenderPipeline(
        output_path=out_path,
        engine="BLENDER_EEVEE_NEXT",
        frame_start=1,
        frame_end=96,
        resolution=(1920, 1080),
        fps=24
    )

    result = pipeline.run(build_fn=build_lorena_scene, preview=False)

    if result.get("status") == "PASS":
        if log: log.info(f"🎬 RENDER COMPLETE: {out_path}")
        try:
            from notify_user import notify
            notify(f"Lorena renderizada! {ts}", "FGS Studio")
        except ImportError:
            pass
        sys.exit(0)
    else:
        print(f"\n❌ FALHA NO RENDER. Verifique os logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
