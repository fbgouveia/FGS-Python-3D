# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: mocap_utils.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: mocap_utils.py                                     ║
║   Função: Gerenciamento e Retargeting de Motion Capture      ║
║           Importação BVH, Mixamo e aplicação em Rigify       ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from mocap_utils import MocapSystem
  
  mocap = MocapSystem()
  bvh_armature = mocap.import_bvh("D:/Animations/andar.bvh")
  mocap.retarget_animation(source_armature=bvh_armature, target_armature=meu_personagem)
"""

import bpy
import os
import math

class MocapSystem:
    """
    Sistema Universal de Motion Capture
    Permite importar animações de arquivos BVH (Mixamo, CMU, Rokoko)
    e repassar (retargeting) para o rig principal (ex: Rigify).
    """

    def __init__(self, fps=24):
        self.fps = fps
        self._ensure_bvh_addon()
        
    def _ensure_bvh_addon(self):
        """Garante que o addon de importação BVH do Blender está ativado."""
        import addon_utils
        is_enabled, is_loaded = addon_utils.check("io_anim_bvh")
        if not is_loaded:
            addon_utils.enable("io_anim_bvh")
            
    def _ativar(self, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
    def import_bvh(self, file_path: str, scale=1.0) -> bpy.types.Object:
        """
        Importa um arquivo BVH e retorna a armature gerada.
        """
        if not os.path.exists(file_path):
            print(f"❌ Erro: Arquivo BVH não encontrado: {file_path}")
            return None
            
        print(f"📥 Importando BVH: {os.path.basename(file_path)}")
        bpy.ops.import_anim.bvh(
            filepath=file_path,
            global_scale=scale,
            use_fps_scale=True,
            update_scene_fps=False,
            target='ARMATURE'
        )
        
        armature = bpy.context.active_object
        if armature and armature.type == 'ARMATURE':
            armature.name = f"Mocap_{os.path.basename(file_path).replace('.bvh', '')}"
            
            # Esconder armature do render
            armature.hide_render = True
            armature.hide_viewport = True
            
            # Colocá-lo em uma pose de descanso para evitar bugs (frame 0 geralmente é T-Pose no Mixamo)
            bpy.context.scene.frame_set(0)
            return armature
        
        print("❌ Erro: O arquivo BVH não carregou uma armature válida.")
        return None

    def retarget_animation(self, source_armature: bpy.types.Object, target_armature: bpy.types.Object, bone_map: dict = None):
        """
        Faz retargeting copiando rotação de ossos do BVH para o Target Armature.
        
        Se bone_map não for fornecido, tenta mapear usando nomes padrão Mixamo -> Rigify.
        
        bone_map ex: {"mixamorig:RightForeArm": "forearm.R", ...}
        """
        if not source_armature or not target_armature:
            print("❌ Erro: Armatures de source ou target inválidas.")
            return False
            
        print(f"🤖 Iniciando Retargeting de {source_armature.name} para {target_armature.name}...")
        
        # Mapeamento Padrão Mixamo -> Nomes Básicos Blender (Ajustar para Rigify real)
        if bone_map is None:
            bone_map = {
                "mixamorig:Hips": "hips",
                "mixamorig:Spine": "spine",
                "mixamorig:Spine1": "spine.001",
                "mixamorig:Spine2": "spine.002",
                "mixamorig:Neck": "neck",
                "mixamorig:Head": "head",
                
                "mixamorig:LeftShoulder": "shoulder.L",
                "mixamorig:LeftArm": "upper_arm.L",
                "mixamorig:LeftForeArm": "forearm.L",
                "mixamorig:LeftHand": "hand.L",
                
                "mixamorig:RightShoulder": "shoulder.R",
                "mixamorig:RightArm": "upper_arm.R",
                "mixamorig:RightForeArm": "forearm.R",
                "mixamorig:RightHand": "hand.R",
                
                "mixamorig:LeftUpLeg": "thigh.L",
                "mixamorig:LeftLeg": "shin.L",
                "mixamorig:LeftFoot": "foot.L",
                
                "mixamorig:RightUpLeg": "thigh.R",
                "mixamorig:RightLeg": "shin.R",
                "mixamorig:RightFoot": "foot.R"
            }
            
        self._ativar(target_armature)
        bpy.ops.object.mode_set(mode='POSE')
        
        sucessos = 0
        falhas = 0
        
        for src_bone_name, trg_bone_name in bone_map.items():
            if trg_bone_name in target_armature.pose.bones:
                trg_bone = target_armature.pose.bones[trg_bone_name]
                
                # Remover constraints antigas do bone se houver
                for con in trg_bone.constraints:
                    if con.name == "Mocap_Retarget":
                        trg_bone.constraints.remove(con)
                
                # Criar nova constraint Copy_Rotation
                crc = trg_bone.constraints.new(type='COPY_ROTATION')
                crc.name = "Mocap_Retarget"
                crc.target = source_armature
                crc.subtarget = src_bone_name
                
                # Para Mocap, normalmente é necessário usar LOCAL de ambos ou ajustar eixos.
                # Mixamo vs Blender standard geralmente precisa de LOCAL space.
                crc.target_space = 'LOCAL'
                crc.owner_space = 'LOCAL'
                
                # Se mixamo/Rigify tiver rest orientations diferentes, podemos tentar usar REPLACE vs ADD
                crc.mix_mode = 'REPLACE' 
                
                sucessos += 1
            else:
                falhas += 1
                
        # Oosso principal (Hips / Pelvis) precisa copiar LOCALIZAÇÃO além da rotação
        if "mixamorig:Hips" in bone_map:
            trg_hips_name = bone_map["mixamorig:Hips"]
            if trg_hips_name in target_armature.pose.bones:
                trg_hips = target_armature.pose.bones[trg_hips_name]
                
                # Copiar Loc
                clc = trg_hips.constraints.new(type='COPY_LOCATION')
                clc.name = "Mocap_Root_Loc"
                clc.target = source_armature
                clc.subtarget = "mixamorig:Hips"
                clc.target_space = 'LOCAL'
                clc.owner_space = 'LOCAL'
        
        bpy.ops.object.mode_set(mode='OBJECT')
        print(f"✅ Retarget Concluído! Copiados: {sucessos} ossos. Falhas: {falhas} ossos.")
        return True

    def bake_animation(self, target_armature: bpy.types.Object, start_frame: int, end_frame: int):
        """
        Bake (Assar) a animação baseada em constraints para keyframes reais.
        Isso permite apagar a rig de origem (BVH) e exportar/salvar sem dependências.
        """
        self._ativar(target_armature)
        bpy.ops.nla.bake(
            frame_start=start_frame,
            frame_end=end_frame,
            only_selected=False,
            visual_keying=True,
            clear_constraints=True,
            use_current_action=True,
            bake_types={'POSE'}
        )
        print(f"🔥 Bake concluído: {start_frame} até {end_frame}. Constraints removidas.")

if __name__ == "__main__":
    print("\\n=== Mocap Utilities Module Loaded ===")
