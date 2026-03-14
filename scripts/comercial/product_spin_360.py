# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: product_spin_360.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Comercial Script                  ║
║   Script: product_spin_360.py                               ║
║   Função: Gerador Automático de Showcase de Produto (360)    ║
║           Prepara cena, ilumina e anima rotação.             ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import math
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path("D:/Blender/blenderscripts")
sys.path.append(str(BASE_DIR / "scripts" / "utils"))

try:
    from camera_system import CameraSystem
    from lighting_system import LightingSystem
    from materials_library import MaterialLibrary
except ImportError as e:
    print(f"❌ Erro ao importar utilitários: {e}")

class ProductShowcase:
    def __init__(self, target_obj_name=None):
        self.target = bpy.context.active_object if not target_obj_name else bpy.data.objects.get(target_obj_name)
        self.cam_sys = CameraSystem()
        self.light_sys = LightingSystem()
        self.lib = MaterialLibrary()

    def build_scene(self, nicho="luxo"):
        """Prepara iluminação e fundo baseados no nicho."""
        if not self.target:
            print("⚠️ Nenhum objeto alvo selecionado.")
            return

        print(f"💎 Preparando showcase para: {self.target.name} (Nicho: {nicho})")
        
        # 1. Fundo Infinito
        paleta = self.lib.paleta(nicho)
        mat_fundo = self.lib.gradiente_degrade(cor_topo=paleta["principal"], cor_base=paleta["fundo"])
        
        # Criar plano de fundo curvo (estúdio)
        bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 5, 0))
        fundo = bpy.context.active_object
        fundo.name = "FGS_Showcase_Backdrop"
        fundo.rotation_euler.x = math.radians(90)
        self.lib.aplicar(fundo, mat_fundo)

        # 2. Iluminação
        self.light_sys.limpar_luzes()
        if nicho == "luxo":
            self.light_sys.tres_pontos(alvo=self.target, intensidade=1.5)
        else:
            self.light_sys.neon_vibe(cor=paleta["destaque"])

        # 3. Câmera
        self.cam_sys.criar_camera(
            nome="Cam_Showcase",
            posicao=(0, -8, 2),
            alvo=self.target,
            foco_dist=50
        )

    def animate_spin(self, duracao=120):
        """Cria animação de rotação 360."""
        if not self.target: return
        
        self.target.rotation_mode = 'XYZ'
        self.target.rotation_euler.z = 0
        self.target.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        
        self.target.rotation_euler.z = math.radians(360)
        self.target.keyframe_insert(data_path="rotation_euler", index=2, frame=duracao)
        
        # Tornar linear
        for fc in self.target.animation_data.action.fcurves:
            if fc.data_path == "rotation_euler" and fc.array_index == 2:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
        
        bpy.context.scene.frame_end = duracao
        print(f"🎬 Rotação de {duracao} frames configurada.")

if __name__ == "__main__":
    showcase = ProductShowcase()
    showcase.build_scene(nicho="luxo")
    showcase.animate_spin(duracao=120)
