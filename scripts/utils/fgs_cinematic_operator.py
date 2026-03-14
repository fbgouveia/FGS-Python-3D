# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: fgs_cinematic_operator.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import json
import math

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            response = s.recv(16384) # Maior buffer para resposta de cena
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

cinematic_code = """
import bpy
import math

# 1. Limpeza Cinematográfica (Deleta Luzes e Câmeras extras)
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type in ['LIGHT', 'CAMERA']:
        bpy.data.objects.remove(obj, do_unlink=True)

# 2. Setup do Cubo Premium
cube = bpy.data.objects.get('Cube')
if cube:
    cube.location = (0, 0, 0)
    # Criar material se não existir
    mat_name = 'FGS_Premium_Metal'
    mat = bpy.data.materials.get(mat_name) or bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    mat.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
    
    node_principled.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
    node_principled.inputs['Metallic'].default_value = 1.0
    node_principled.inputs['Roughness'].default_value = 0.05
    
    if not cube.data.materials:
        cube.data.materials.append(mat)
    else:
        cube.data.materials[0] = mat

# 3. Iluminação Dramática (Rim & Key) - Estilo Comercial de Carro/Tênis
# Key Light
key_light = bpy.data.lights.new(name='Key_Light', type='AREA')
key_light.energy = 3000
key_light.size = 5
key_obj = bpy.data.objects.new(name='Key_Light', object_data=key_light)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (6, -6, 6)
key_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

# Rim Light (A luz que dá o contorno "pro")
rim_light = bpy.data.lights.new(name='Rim_Light', type='AREA')
rim_light.energy = 5000
rim_light.size = 3
rim_obj = bpy.data.objects.new(name='Rim_Light', object_data=rim_light)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-5, 5, 3)
rim_obj.rotation_euler = (math.radians(-45), 0, math.radians(225))

# 4. Câmera de Comercial (100mm para compressão de luxo)
cam_data = bpy.data.cameras.new(name='FGS_Cinematic_Cam')
cam_data.lens = 100
cam_obj = bpy.data.objects.new(name='FGS_Cinematic_Cam', object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (12, -12, 6)
cam_obj.rotation_euler = (math.radians(68), 0, math.radians(45))
bpy.context.scene.camera = cam_obj

# Ativar DOF (Depth of Field) para foco no cubo
cam_data.dof.use_dof = True
cam_data.dof.focus_object = cube
cam_data.dof.aperture_fstop = 1.2

# 5. Animação de Rotação Suave
cube.animation_data_clear()
cube.rotation_mode = 'XYZ'
cube.keyframe_insert(data_path='rotation_euler', frame=1)
cube.rotation_euler[2] = math.radians(360)
cube.keyframe_insert(data_path='rotation_euler', frame=250)

# Deixar a interpolação Linear para loop perfeito
if cube.animation_data and cube.animation_data.action:
    for fcurve in cube.animation_data.action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'

# 6. Configurar Viewport para Rendered Mode para o usuário ver
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": cinematic_code
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
