# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: motion_handler.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os

# Adicionar o diretório de scripts ao path
scripts_path = "D:/Blender/blenderscripts/scripts/utils"
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

try:
    from mocap_utils import MocapSystem
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from mocap_utils import MocapSystem

# Configurações do Painel
BL_ID_NAME = "FGS_PT_motion_handler"

class FGS_OT_ApplyMotion(bpy.types.Operator):
    """Importa e aplica um arquivo BVH ao personagem selecionado"""
    bl_idname = "fgs.apply_motion"
    bl_label = "Aplicar Movimento"
    bl_options = {'REGISTER', 'UNDO'}
    
    bvh_name: bpy.props.StringProperty()
    
    def execute(self, context):
        target = context.active_object
        if not target or target.type != 'ARMATURE':
            self.report({'WARNING'}, "Selecione a AMATURE do personagem (Target)!")
            return {'CANCELLED'}
        
        # Caminho base para motions
        motions_dir = "D:/Blender/blenderscripts/motions/bvh"
        bvh_path = os.path.join(motions_dir, self.bvh_name)
        
        if not os.path.exists(bvh_path):
            self.report({'ERROR'}, f"Arquivo não encontrado: {self.bvh_name}. Coloque o arquivo em {motions_dir}")
            return {'CANCELLED'}
        
        mocap = MocapSystem()
        
        # 1. Importar BVH
        bvh_armature = mocap.import_bvh(bvh_path)
        
        if bvh_armature:
            # 2. Retarget
            mocap.retarget_animation(source_armature=bvh_armature, target_armature=target)
            
            # 3. Informar usuário sobre o Bake
            self.report({'INFO'}, f"Movimento {self.bvh_name} vinculado! Use 'Bake Animation' para fixar.")
            return {'FINISHED'}
        
        return {'CANCELLED'}

class FGS_OT_BakeMotion(bpy.types.Operator):
    """Assa as constraints em keyframes reais e limpa o BVH"""
    bl_idname = "fgs.bake_motion"
    bl_label = "Fixar Animação (Bake)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        target = context.active_object
        if not target or target.type != 'ARMATURE':
            return {'CANCELLED'}
        
        mocap = MocapSystem()
        
        # Detectar range de frames
        scene = context.scene
        mocap.bake_animation(target, scene.frame_start, scene.frame_end)
        
        # Limpar armatures de mocap (opcional, mas limpa a cena)
        for obj in bpy.data.objects:
            if obj.name.startswith("Mocap_"):
                bpy.data.objects.remove(obj, do_unlink=True)
                
        self.report({'INFO'}, "Animação fixada com sucesso!")
        return {'FINISHED'}

class FGS_PT_MotionPanel(bpy.types.Panel):
    """Painel de Movimentos FGS no Sidebar (N)"""
    bl_label = "FGS Motion Library"
    bl_idname = BL_ID_NAME
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FGS Studio'

    def draw(self, context):
        layout = self.layout
        motions_dir = "D:/Blender/blenderscripts/motions/bvh"
        
        if not os.path.exists(motions_dir):
            layout.label(text="Pasta 'motions/bvh' não encontrada!", icon='ERROR')
            return

        col = layout.column(align=True)
        col.label(text="Ficheiros BVH Disponíveis:", icon='ANIM')
        
        # Listar arquivos BVH na pasta
        files = [f for f in os.listdir(motions_dir) if f.endswith(".bvh")]
        
        if not files:
            layout.label(text="Nenhum .bvh encontrado em motions/bvh", icon='INFO')
            layout.operator("wm.url_open", text="Baixar do Mixamo").url = "https://www.mixamo.com"
        else:
            for f in files:
                row = col.row(align=True)
                row.operator("fgs.apply_motion", text=f.replace(".bvh", ""), icon='PLAY').bvh_name = f

        col.separator()
        col.operator("fgs.bake_motion", text="Assar (Bake) & Limpar", icon='REC')

def register():
    bpy.utils.register_class(FGS_OT_ApplyMotion)
    bpy.utils.register_class(FGS_OT_BakeMotion)
    bpy.utils.register_class(FGS_PT_MotionPanel)

def unregister():
    bpy.utils.unregister_class(FGS_OT_ApplyMotion)
    bpy.utils.unregister_class(FGS_OT_BakeMotion)
    bpy.utils.unregister_class(FGS_PT_MotionPanel)

if __name__ == "__main__":
    register()
    print("FGS Motion Handler registrado!")
