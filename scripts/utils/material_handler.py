# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: material_handler.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: material_handler.py                               ║
║   Função: Gestão de Materiais PBR e Paletas (Ghost Mode)     ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import pathlib
import json
import shutil
import bpy

# Garantir que estamos em D: e isolados
BASE_DIR = pathlib.Path(r"D:\Blender\blenderscripts")
sys.path.append(str(BASE_DIR / "scripts" / "utils"))

from materials_library import MaterialLibrary

class MaterialHandler:
    """
    Gerencia a aplicação e o cache de materiais de forma 'Ghost'.
    Operações exclusivas em D:\Blender\blenderscripts\assets\materials.
    """
    def __init__(self):
        self.assets_root = BASE_DIR / "assets" / "materials"
        self.assets_root.mkdir(parents=True, exist_ok=True)
        self.mat_lib = MaterialLibrary()

    def create_palette(self, name, materials_config):
        """
        Gera uma paleta (JSON) e prepara os assets necessários.
        Ex de config: {"corpo": "metal_ouro", "detalhes": "plastico_preto"}
        """
        palette_path = self.assets_root / f"palette_{name}.json"
        
        with open(palette_path, 'w') as f:
            json.dump(materials_config, f, indent=4)
            
        print(f"✅ Paleta '{name}' criada em: {palette_path}")
        return palette_path

    def apply_to_object(self, obj, material_type, **kwargs):
        """
        Aplica um material da biblioteca ao objeto respeitando o isolamento.
        """
        if not obj:
            return False
            
        # Mapeamento para funções da MaterialLibrary
        method_name = material_type.lower()
        if hasattr(self.mat_lib, method_name):
            mat_func = getattr(self.mat_lib, method_name)
            mat = mat_func(**kwargs)
            self.mat_lib.aplicar(obj, mat)
            return True
        else:
            print(f"⚠️ Material '{material_type}' não encontrado na biblioteca.")
            return False

    def cleanup_temp_assets(self):
        """
        Remove arquivos temporários de cache de materiais.
        """
        temp_dir = self.assets_root / "temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print("🧹 Cache temporário de materiais limpo.")

if __name__ == "__main__":
    # Teste rápido de sanidade
    handler = MaterialHandler()
    handler.create_palette("vibe_cyberpunk", {"hero": "neon", "floor": "metal"})
