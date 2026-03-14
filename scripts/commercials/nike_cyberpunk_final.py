# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: nike_cyberpunk_final.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import json
import os

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            response = s.recv(65536)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

cinematic_script = r'''
import bpy
import math

# 1. Limpeza de Cameras e Luzes anteriores
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type in ['LIGHT', 'CAMERA'] or 'Cyber' in obj.name or 'Target' in obj.name:
        if obj.name != 'Mesh_0': # Nao deletar o tenis
            bpy.data.objects.remove(obj, do_unlink=True)

# 2. Materiais Profissionais (Carbon Fiber + Neon Accents)
mesh = bpy.data.objects.get("Mesh_0")
if mesh:
    mat = bpy.data.materials.get("FGS_Cyber_Nike") or bpy.data.materials.new(name="FGS_Cyber_Nike")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Metal Negro com Roughness de Fibra de Carbono
    node_principled.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
    node_principled.inputs['Metallic'].default_value = 1.0
    node_principled.inputs['Roughness'].default_value = 0.2
    
    mat.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
    
    if not mesh.data.materials:
        mesh.data.materials.append(mat)
    else:
        mesh.data.materials[0] = mat

# 3. Atmosfera Cyberpunk (Haze + Lights)
# World
world = bpy.context.scene.world
world.use_nodes = True
w_nodes = world.node_tree.nodes
w_nodes.clear()
w_out = w_nodes.new(type='ShaderNodeOutputWorld')
w_bg = w_nodes.new(type='ShaderNodeBackground')
w_bg.inputs['Color'].default_value = (0.005, 0, 0.01, 1) # Dark purple
world.node_tree.links.new(w_bg.outputs['Background'], w_out.inputs['Surface'])

# Fog/Volume
bpy.ops.mesh.primitive_cube_add(size=40)
fog = bpy.context.active_object
fog.name = "Cyber_Fog_Volume"
f_mat = bpy.data.materials.new(name="FGS_Cyber_Fog")
f_mat.use_nodes = True
f_nodes = f_mat.node_tree.nodes
f_nodes.clear()
f_vol = f_nodes.new(type='ShaderNodeVolumePrincipled')
f_out = f_nodes.new(type='ShaderNodeOutputMaterial')
f_vol.inputs['Density'].default_value = 0.05
f_vol.inputs['Emission Color'].default_value = (0.2, 0, 0.4, 1)
f_vol.inputs['Emission Strength'].default_value = 0.01
f_mat.node_tree.links.new(f_vol.outputs['Volume'], f_out.inputs['Volume'])
fog.data.materials.append(f_mat)

# Luzes de Neon (Rim Lighting)
l1 = bpy.data.lights.new(name="Neon_Cyan", type='AREA')
l1.energy = 30000
l1.color = (0, 0.8, 1.0) # Ciano
o1 = bpy.data.objects.new(name="Neon_Cyan", object_data=l1)
bpy.context.collection.objects.link(o1)
o1.location = (6, -4, 4)
o1.rotation_euler = (math.radians(45), 0, math.radians(45))

l2 = bpy.data.lights.new(name="Neon_Magenta", type='AREA')
l2.energy = 35000
l2.color = (1.0, 0.0, 0.5) # Magenta
o2 = bpy.data.objects.new(name="Neon_Magenta", object_data=l2)
bpy.context.collection.objects.link(o2)
o2.location = (-6, 4, 3)
o2.rotation_euler = (math.radians(-45), 0, math.radians(225))

# 4. Animação 360 Orbital Master
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
target = bpy.context.active_object
target.name = "NIKE_CAM_TARGET"

cam_data = bpy.data.cameras.new(name="Master_Cinematic_Cam")
cam_data.lens = 100
cam_obj = bpy.data.objects.new(name="Master_Cinematic_Cam", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.parent = target
cam_obj.location = (0, -18, 5) # Distancia comercial
bpy.context.scene.camera = cam_obj

# DOF
cam_data.dof.use_dof = True
cam_data.dof.focus_object = mesh
cam_data.dof.aperture_fstop = 1.0

# Animacao Orbital (360 em 400 frames para ser "bem devagar")
target.animation_data_clear()
target.rotation_mode = 'XYZ'
target.keyframe_insert(data_path="rotation_euler", frame=1)
target.rotation_euler[2] = math.radians(360)
target.keyframe_insert(data_path="rotation_euler", frame=400)

for fcurve in target.animation_data.action.fcurves:
    for kp in fcurve.keyframe_points:
        kp.interpolation = 'LINEAR'

# 5. Forçar Refresh e Visual clean
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
                space.overlay.show_overlays = False
                with bpy.context.temp_override(area=area):
                    bpy.ops.view3d.view_all(center=True)

# 6. Screenshot de Auditoria
screenshot_dir = r"D:\Blender\blenderscripts\renders"
if not os.path.exists(screenshot_dir): os.makedirs(screenshot_dir)
screenshot_path = os.path.join(screenshot_dir, "final_cyberpunk_master.png")
# bpy.ops.screen.screenshot_area(filepath=screenshot_path) # Comentado para evitar bloqueio de thread
'''

cmd = {
    "type": "execute_code",
    "params": {
        "code": cinematic_script
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
