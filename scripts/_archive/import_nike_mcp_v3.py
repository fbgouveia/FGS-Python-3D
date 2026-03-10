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
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
        root = bpy.context.active_object
        root.name = "NIKE_CONTROL"
        for o in nike_objs:
            o.parent = root
            o.location = (0,0,0)
else:
    print("ERRO: Arquivo não encontrado no caminho especificado.")

# 3. Setup de Estúdio FGS (Blender 4.2+)
if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
else:
    bpy.context.scene.render.engine = 'CYCLES'

# World Setup robusto
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
nodes.clear()
node_output = nodes.new(type='ShaderNodeOutputWorld')
node_bg = nodes.new(type='ShaderNodeBackground')
node_bg.inputs['Color'].default_value = (0.005, 0.005, 0.005, 1) # Quase preto
world.node_tree.links.new(node_bg.outputs['Background'], node_output.inputs['Surface'])

# Luzes
light_data = bpy.data.lights.new(name="Key_Light", type='AREA')
light_data.energy = 5000
key_obj = bpy.data.objects.new(name="Key_Light", object_data=light_data)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (3, -3, 3)
key_obj.rotation_euler = (math.radians(45), 0, math.radians(45))

rim_data = bpy.data.lights.new(name="Rim_Light", type='AREA')
rim_data.energy = 10000
rim_obj = bpy.data.objects.new(name="Rim_Light", object_data=rim_data)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-3, 3, 2)
rim_obj.rotation_euler = (math.radians(-45), 0, math.radians(225))

# 4. Câmera
cam_data = bpy.data.cameras.new(name="PRO_CAM")
cam_data.lens = 85
cam_obj = bpy.data.objects.new(name="PRO_CAM", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (10, -10, 3)
track = cam_obj.constraints.new(type='TRACK_TO')
track.target = bpy.data.objects.get("NIKE_CONTROL")
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
