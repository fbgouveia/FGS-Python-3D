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
            response = s.recv(16384)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

nike_path = r"D:\Blender\blenderscripts\assets\props\nike.fbx"

import_nike_code = f"""
import bpy
import os
import math

# 1. Limpeza Cinematográfica
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Importar o Tênis Nike Real
path = r"{nike_path}"
if os.path.exists(path):
    bpy.ops.import_scene.fbx(filepath=path)
    
    # Centralizar e focar
    nike_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if nike_objs:
        # Criar um Empty para controlar o tênis
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
        root = bpy.context.active_object
        root.name = "NIKE_CONTROL"
        for o in nike_objs:
            o.parent = root
            o.location = (0,0,0)
else:
    print("ERRO: Arquivo não encontrado no caminho especificado.")

# 3. Setup de Estúdio FGS (Blender 4.2 Compatível)
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' 

# Sky/Environment
bpy.context.scene.world.use_nodes = True
nodes = bpy.context.scene.world.node_tree.nodes
nodes.clear()
node_background = nodes.new(type='ShaderNodeBackground')
node_output = nodes.new(type='ShaderNodeWorldOutput')
node_background.inputs['Color'].default_value = (0.01, 0.01, 0.01, 1) 
bpy.context.scene.world.node_tree.links.new(node_background.outputs['Background'], node_output.inputs['Surface'])

# Luzes
key_light = bpy.data.lights.new(name="Key_Softbox", type='AREA')
key_light.energy = 5000
key_obj = bpy.data.objects.new(name="Key_Softbox", object_data=key_light)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (4, -4, 4)
key_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

rim_light = bpy.data.lights.new(name="Rim_Light", type='AREA')
rim_light.energy = 8000
rim_obj = bpy.data.objects.new(name="Rim_Light", object_data=rim_light)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-4, 4, 3)
rim_obj.rotation_euler = (math.radians(-45), 0, math.radians(225))

# 4. Câmera
cam_data = bpy.data.cameras.new(name="NIKE_CAM")
cam_data.lens = 85
cam_obj = bpy.data.objects.new(name="NIKE_CAM", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (8, -8, 3)
cam_obj.rotation_euler = (math.radians(70), 0, math.radians(45))
bpy.context.scene.camera = cam_obj

# 5. Viewport
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
                space.overlay.show_overlays = False
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": import_nike_code
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
