# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: material_preset_handler.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os
from pathlib import Path

# Adicionar o diretório de scripts ao path para importar a materials_library
scripts_path = "D:/Blender/blenderscripts/scripts/utils"
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

try:
    from materials_library import MaterialLibrary
except ImportError:
    # Caso o path absoluto não funcione por algum motivo (ex: drive diferente)
    # Tenta pegar relativo ao arquivo atual
    sys.path.append(os.path.dirname(__file__))
    from materials_library import MaterialLibrary

# Configurações do Painel
BL_ID_NAME = "FGS_PT_material_handler"

class FGS_OT_ApplyMaterial(bpy.types.Operator):
    """Aplica um material da biblioteca FGS ao objeto selecionado"""
    bl_idname = "fgs.apply_material"
    bl_label = "Aplicar Material"
    bl_options = {'REGISTER', 'UNDO'}
    
    mat_type: bpy.props.StringProperty()
    
    def execute(self, context):
        lib = MaterialLibrary()
        objs = context.selected_objects
        
        if not objs:
            self.report({'WARNING'}, "Nenhum objeto selecionado!")
            return {'CANCELLED'}
        
        # Mapeamento de métodos da MaterialLibrary
        methods = {
            "METAL": lib.metal,
            "OURO": lib.metal_ouro,
            "PRATA": lib.metal_prata,
            "ACO_ESCOVADO": lib.metal_aco_escovado,
            "PLASTICO": lib.plastico,
            "BORRACHA": lib.borracha,
            "MADEIRA": lib.madeira,
            "VIDRO": lib.vidro,
            "PELE": lib.pele_estilizada,
            "PELO": lib.pelo_animal,
            "FOLHA": lib.folha,
            "AGUA": lambda: lib.liquido(tipo="agua"),
            "MEL": lambda: lib.liquido(tipo="mel"),
            "LEITE": lambda: lib.liquido(tipo="leite"),
            "LAVA": lambda: lib.liquido(tipo="lava"),
            "NEON": lib.neon,
            "HOLOGRAMA": lib.holograma,
            "CRISTAL": lib.cristal,
            "CARTOON": lib.cartoon,
            "FUNDO_STUDIO": lib.fundo_studio,
            "TIJOLO": lib.tijolo,
            "GRADIENTE": lib.gradiente_degrade,
        }
        
        if self.mat_type in methods:
            # Criar o material
            mat = methods[self.mat_type]()
            
            for obj in objs:
                lib.aplicar(obj, mat)
            
            self.report({'INFO'}, f"Material {self.mat_type} aplicado a {len(objs)} objeto(s).")
            return {'FINISHED'}
        
        return {'CANCELLED'}

class FGS_PT_MaterialPanel(bpy.types.Panel):
    """Painel de Materiais FGS no Sidebar (N)"""
    bl_label = "FGS Material Library"
    bl_idname = BL_ID_NAME
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FGS Studio'

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Físicos & PBR", icon='MATERIAL')
        
        # Grid de botões para categorias
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Metal").mat_type = "METAL"
        row.operator("fgs.apply_material", text="Ouro").mat_type = "OURO"
        
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Prata").mat_type = "PRATA"
        row.operator("fgs.apply_material", text="Aço").mat_type = "ACO_ESCOVADO"
        
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Plástico").mat_type = "PLASTICO"
        row.operator("fgs.apply_material", text="Borracha").mat_type = "BORRACHA"
        
        col.separator()
        col.label(text="Orgânicos & Natureza", icon='OUTLINER_OB_LATTICE')
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Pele").mat_type = "PELE"
        row.operator("fgs.apply_material", text="Pelo").mat_type = "PELO"
        
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Folha").mat_type = "FOLHA"
        row.operator("fgs.apply_material", text="Madeira").mat_type = "MADEIRA"

        col.separator()
        col.label(text="Líquidos", icon='NODE_MATERIAL')
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Água").mat_type = "AGUA"
        row.operator("fgs.apply_material", text="Mel").mat_type = "MEL"
        
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Leite").mat_type = "LEITE"
        row.operator("fgs.apply_material", text="Lava").mat_type = "LAVA"

        col.separator()
        col.label(text="Especiais & VFX", icon='RESTRICT_RENDER_OFF')
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Neon").mat_type = "NEON"
        row.operator("fgs.apply_material", text="Vidro").mat_type = "VIDRO"
        
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Holograma").mat_type = "HOLOGRAMA"
        row.operator("fgs.apply_material", text="Cristal").mat_type = "CRISTAL"

        col.separator()
        col.label(text="Cenário & Estilizado", icon='SCENE_DATA')
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Cartoon").mat_type = "CARTOON"
        row.operator("fgs.apply_material", text="Fundo Std").mat_type = "FUNDO_STUDIO"
        
        row = col.row(align=True)
        row.operator("fgs.apply_material", text="Tijolo").mat_type = "TIJOLO"
        row.operator("fgs.apply_material", text="Gradiente").mat_type = "GRADIENTE"

def register():
    bpy.utils.register_class(FGS_OT_ApplyMaterial)
    bpy.utils.register_class(FGS_PT_MaterialPanel)

def unregister():
    bpy.utils.unregister_class(FGS_OT_ApplyMaterial)
    bpy.utils.unregister_class(FGS_PT_MaterialPanel)

if __name__ == "__main__":
    register()
    print("FGS Material Handler registrado com sucesso!")
