# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: ghost_material_handler.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Ghost Automations                 ║
║   Script: ghost_material_handler.py                         ║
║   Função: Aplicação Autônoma de Materiais PBR                ║
║           Decodifica tags de IA e aplica ao mesh ativo       ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path("D:/Blender/blenderscripts")
sys.path.append(str(BASE_DIR / "scripts" / "utils"))

try:
    from materials_library import MaterialLibrary
    from material_handler import MaterialHandler
except ImportError as e:
    print(f"❌ Erro ao importar utilitários: {e}")

class GhostMaterialHandler(MaterialHandler):
    """
    Extensão do MaterialHandler para operações autônomas (Ghost Mode).
    Capaz de interpretar 'estilos' complexos e aplicar a coleções inteiras.
    """
    
    def apply_style_to_collection(self, collection_name, style_tag):
        """
        Aplica um estilo completo a uma coleção.
        Ex: style_tag="cyberpunk" -> aplica neon e metais escuros.
        """
        col = bpy.data.collections.get(collection_name)
        if not col:
            print(f"⚠️ Coleção '{collection_name}' não encontrada.")
            return

        print(f"👻 Ghost Mode: Aplicando estilo '{style_tag}' na coleção '{collection_name}'")
        
        for obj in col.objects:
            if obj.type == 'MESH':
                self._auto_apply(obj, style_tag)

    def _auto_apply(self, obj, style):
        """Lógica interna de decisão de material baseada em estilo."""
        if style == "cyberpunk":
            # Tática #44: Contraste Cromático
            self.apply_to_object(obj, "neon", cor=(0, 1, 1, 1)) # Cyan
        elif style == "luxo":
            # Tática #91: Tangibilidade
            self.apply_to_object(obj, "metal_ouro")
        else:
            self.apply_to_object(obj, "plastico", cor=(0.1, 0.1, 0.1, 1))

if __name__ == "__main__":
    ghost = GhostMaterialHandler()
    # Exemplo de execução via CLI/Scripts
    if bpy.context.active_object:
        ghost._auto_apply(bpy.context.active_object, "luxo")
